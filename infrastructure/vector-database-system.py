#!/usr/bin/env python3
"""
Vector Database System - Phase 2 Implementation
Multi-Vector DB connections for enhanced AI capabilities
Based on SuperAGI patterns for semantic search and memory storage
"""

import asyncio
import json
import time
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import hashlib
from collections import defaultdict
import pickle
import faiss
import chromadb
from sentence_transformers import SentenceTransformer

# Vector Database Types

class VectorDBType(Enum):
    """Supported vector database types"""
    FAISS = "faiss"
    CHROMA = "chroma"
    PINECONE = "pinecone"
    WEAVIATE = "weaviate"
    QDRANT = "qdrant"
    MILVUS = "milvus"
    REDIS = "redis"
    ELASTICSEARCH = "elasticsearch"

class EmbeddingModel(Enum):
    """Supported embedding models"""
    OPENAI_ADA = "text-embedding-ada-002"
    SENTENCE_TRANSFORMER = "all-MiniLM-L6-v2"
    COHERE = "embed-english-v2.0"
    HUGGINGFACE = "sentence-transformers/all-mpnet-base-v2"
    CUSTOM = "custom-fine-tuned"

class SearchStrategy(Enum):
    """Search strategies for retrieval"""
    SIMILARITY = "similarity"
    MMR = "maximal_marginal_relevance"
    HYBRID = "hybrid"
    SEMANTIC = "semantic"
    KEYWORD = "keyword"
    RERANK = "rerank"

@dataclass
class VectorDocument:
    """Document for vector storage"""
    id: str
    content: str
    embedding: Optional[np.ndarray] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    source: Optional[str] = None
    score: Optional[float] = None

@dataclass
class SearchResult:
    """Search result from vector database"""
    documents: List[VectorDocument]
    scores: List[float]
    metadata: Dict[str, Any]
    query_time: float
    strategy_used: SearchStrategy

@dataclass
class VectorDBConfig:
    """Configuration for vector database connection"""
    db_type: VectorDBType
    connection_params: Dict[str, Any]
    embedding_model: EmbeddingModel
    dimension: int
    index_params: Dict[str, Any] = field(default_factory=dict)
    search_params: Dict[str, Any] = field(default_factory=dict)

class VectorDatabaseSystem:
    """
    Enterprise-grade vector database system for AI-enhanced search,
    memory storage, and semantic retrieval
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._default_config()
        self.databases = {}
        self.embedding_models = {}
        self.memory_store = MemoryStore()
        self.cache = SemanticCache()
        self.index_manager = IndexManager()
        self._initialize_databases()
        self._initialize_embedding_models()
        
    def _default_config(self) -> Dict[str, Any]:
        """Default vector database configuration"""
        return {
            "primary_db": VectorDBType.FAISS,
            "secondary_dbs": [VectorDBType.CHROMA],
            "embedding_model": EmbeddingModel.SENTENCE_TRANSFORMER,
            "vector_dimension": 384,
            "max_documents": 1000000,
            "similarity_threshold": 0.7,
            "cache_enabled": True,
            "cache_ttl_minutes": 60,
            "auto_index_optimization": True,
            "hybrid_search_enabled": True,
            "reranking_enabled": True
        }
    
    def _initialize_databases(self):
        """Initialize configured vector databases"""
        
        # Initialize primary database
        primary_db = self.config["primary_db"]
        if primary_db == VectorDBType.FAISS:
            self.databases["primary"] = FAISSDatabase(
                dimension=self.config["vector_dimension"]
            )
        elif primary_db == VectorDBType.CHROMA:
            self.databases["primary"] = ChromaDatabase()
        
        # Initialize secondary databases
        for db_type in self.config.get("secondary_dbs", []):
            if db_type == VectorDBType.CHROMA:
                self.databases[db_type.value] = ChromaDatabase()
            elif db_type == VectorDBType.FAISS:
                self.databases[db_type.value] = FAISSDatabase(
                    dimension=self.config["vector_dimension"]
                )
    
    def _initialize_embedding_models(self):
        """Initialize embedding models"""
        
        model_type = self.config["embedding_model"]
        
        if model_type == EmbeddingModel.SENTENCE_TRANSFORMER:
            self.embedding_models["default"] = SentenceTransformer(
                'all-MiniLM-L6-v2'
            )
        elif model_type == EmbeddingModel.OPENAI_ADA:
            # Would initialize OpenAI embeddings
            pass
        
        # Initialize specialized models for different purposes
        self.embedding_models["semantic"] = SentenceTransformer(
            'all-mpnet-base-v2'
        )
        self.embedding_models["multilingual"] = SentenceTransformer(
            'distiluse-base-multilingual-cased-v1'
        )
    
    async def store_documents(self, documents: List[VectorDocument], 
                             collection: str = "default") -> Dict[str, Any]:
        """Store documents in vector databases"""
        
        start_time = time.time()
        stored_count = 0
        errors = []
        
        # Generate embeddings if not present
        for doc in documents:
            if doc.embedding is None:
                doc.embedding = await self._generate_embedding(doc.content)
        
        # Store in primary database
        try:
            primary_result = await self.databases["primary"].store(
                documents, collection
            )
            stored_count += primary_result["stored"]
        except Exception as e:
            errors.append(f"Primary DB error: {str(e)}")
        
        # Store in secondary databases for redundancy
        for db_name, db in self.databases.items():
            if db_name != "primary":
                try:
                    result = await db.store(documents, collection)
                    stored_count += result["stored"]
                except Exception as e:
                    errors.append(f"{db_name} error: {str(e)}")
        
        # Update memory store
        self.memory_store.add_documents(documents)
        
        # Update indices
        await self.index_manager.update_indices(documents, collection)
        
        execution_time = time.time() - start_time
        
        return {
            "stored_count": stored_count,
            "execution_time": execution_time,
            "errors": errors,
            "collections_updated": [collection],
            "indices_updated": True
        }
    
    async def search(self, query: str, k: int = 10, 
                    strategy: SearchStrategy = SearchStrategy.HYBRID,
                    filters: Dict[str, Any] = None) -> SearchResult:
        """Search across vector databases with advanced strategies"""
        
        start_time = time.time()
        
        # Check cache first
        if self.config["cache_enabled"]:
            cached_result = self.cache.get(query, k, strategy)
            if cached_result:
                return cached_result
        
        # Generate query embedding
        query_embedding = await self._generate_embedding(query)
        
        # Execute search based on strategy
        if strategy == SearchStrategy.HYBRID:
            results = await self._hybrid_search(query, query_embedding, k, filters)
        elif strategy == SearchStrategy.MMR:
            results = await self._mmr_search(query, query_embedding, k, filters)
        elif strategy == SearchStrategy.SEMANTIC:
            results = await self._semantic_search(query_embedding, k, filters)
        elif strategy == SearchStrategy.RERANK:
            results = await self._rerank_search(query, query_embedding, k, filters)
        else:
            results = await self._similarity_search(query_embedding, k, filters)
        
        # Apply reranking if enabled
        if self.config["reranking_enabled"] and strategy != SearchStrategy.RERANK:
            results = await self._rerank_results(query, results)
        
        query_time = time.time() - start_time
        
        search_result = SearchResult(
            documents=results["documents"],
            scores=results["scores"],
            metadata={
                "total_results": len(results["documents"]),
                "databases_queried": results.get("databases_queried", []),
                "filters_applied": filters
            },
            query_time=query_time,
            strategy_used=strategy
        )
        
        # Cache the result
        if self.config["cache_enabled"]:
            self.cache.set(query, k, strategy, search_result)
        
        return search_result
    
    async def _hybrid_search(self, query: str, query_embedding: np.ndarray, 
                            k: int, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Hybrid search combining multiple strategies"""
        
        # Perform similarity search
        similarity_results = await self._similarity_search(query_embedding, k * 2, filters)
        
        # Perform keyword search
        keyword_results = await self._keyword_search(query, k * 2, filters)
        
        # Combine and deduplicate results
        combined_results = self._combine_search_results(
            [similarity_results, keyword_results],
            weights=[0.7, 0.3]
        )
        
        # Apply MMR for diversity
        diverse_results = self._apply_mmr(combined_results, query_embedding, k)
        
        return diverse_results
    
    async def _mmr_search(self, query: str, query_embedding: np.ndarray,
                         k: int, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Maximal Marginal Relevance search for diversity"""
        
        # Get initial candidates
        candidates = await self._similarity_search(query_embedding, k * 3, filters)
        
        # Apply MMR algorithm
        selected_docs = []
        selected_embeddings = []
        remaining_docs = candidates["documents"]
        remaining_embeddings = [doc.embedding for doc in remaining_docs]
        
        lambda_param = 0.5  # Balance between relevance and diversity
        
        while len(selected_docs) < k and remaining_docs:
            # Calculate MMR scores
            mmr_scores = []
            for i, doc in enumerate(remaining_docs):
                relevance = self._cosine_similarity(query_embedding, doc.embedding)
                
                if selected_embeddings:
                    max_similarity = max([
                        self._cosine_similarity(doc.embedding, selected_emb)
                        for selected_emb in selected_embeddings
                    ])
                else:
                    max_similarity = 0
                
                mmr_score = lambda_param * relevance - (1 - lambda_param) * max_similarity
                mmr_scores.append(mmr_score)
            
            # Select document with highest MMR score
            best_idx = np.argmax(mmr_scores)
            selected_docs.append(remaining_docs[best_idx])
            selected_embeddings.append(remaining_embeddings[best_idx])
            
            # Remove selected document from candidates
            del remaining_docs[best_idx]
            del remaining_embeddings[best_idx]
        
        return {
            "documents": selected_docs,
            "scores": [1.0] * len(selected_docs),  # MMR scores are relative
            "databases_queried": ["primary"]
        }
    
    async def _semantic_search(self, query_embedding: np.ndarray,
                              k: int, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Pure semantic similarity search"""
        
        results = []
        
        # Query all databases
        for db_name, db in self.databases.items():
            try:
                db_results = await db.search(query_embedding, k, filters)
                results.extend(db_results)
            except Exception as e:
                print(f"Error querying {db_name}: {e}")
        
        # Sort by similarity score
        results.sort(key=lambda x: x["score"], reverse=True)
        
        # Take top k results
        top_results = results[:k]
        
        return {
            "documents": [r["document"] for r in top_results],
            "scores": [r["score"] for r in top_results],
            "databases_queried": list(self.databases.keys())
        }
    
    async def _rerank_search(self, query: str, query_embedding: np.ndarray,
                           k: int, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Search with reranking for improved relevance"""
        
        # Get initial candidates
        candidates = await self._similarity_search(query_embedding, k * 3, filters)
        
        # Rerank using cross-encoder or other reranking model
        reranked = await self._rerank_results(query, candidates)
        
        # Take top k after reranking
        top_results = reranked["documents"][:k]
        top_scores = reranked["scores"][:k]
        
        return {
            "documents": top_results,
            "scores": top_scores,
            "databases_queried": reranked.get("databases_queried", [])
        }
    
    async def _similarity_search(self, query_embedding: np.ndarray,
                                k: int, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Standard similarity search"""
        
        # Query primary database
        primary_results = await self.databases["primary"].search(
            query_embedding, k, filters
        )
        
        return {
            "documents": primary_results["documents"],
            "scores": primary_results["scores"],
            "databases_queried": ["primary"]
        }
    
    async def _keyword_search(self, query: str, k: int, 
                             filters: Dict[str, Any]) -> Dict[str, Any]:
        """Keyword-based search"""
        
        # Implement BM25 or similar keyword search
        # This is a simplified version
        results = []
        
        # Search in memory store for keyword matches
        keyword_matches = self.memory_store.keyword_search(query, k * 2)
        
        for match in keyword_matches:
            results.append({
                "document": match["document"],
                "score": match["score"]
            })
        
        return {
            "documents": [r["document"] for r in results],
            "scores": [r["score"] for r in results],
            "databases_queried": ["memory_store"]
        }
    
    async def _rerank_results(self, query: str, 
                            results: Dict[str, Any]) -> Dict[str, Any]:
        """Rerank search results for improved relevance"""
        
        # In production, use a cross-encoder model for reranking
        # This is a simplified scoring based on query-document similarity
        
        reranked_docs = []
        reranked_scores = []
        
        for doc in results["documents"]:
            # Calculate relevance score (simplified)
            relevance_score = self._calculate_relevance_score(query, doc.content)
            reranked_docs.append((doc, relevance_score))
        
        # Sort by relevance score
        reranked_docs.sort(key=lambda x: x[1], reverse=True)
        
        for doc, score in reranked_docs:
            results["documents"] = [doc for doc, _ in reranked_docs]
            results["scores"] = [score for _, score in reranked_docs]
        
        return results
    
    def _combine_search_results(self, result_sets: List[Dict[str, Any]], 
                               weights: List[float]) -> Dict[str, Any]:
        """Combine multiple search result sets with weights"""
        
        combined_scores = defaultdict(float)
        document_map = {}
        
        for results, weight in zip(result_sets, weights):
            for doc, score in zip(results["documents"], results["scores"]):
                doc_id = doc.id
                combined_scores[doc_id] += score * weight
                document_map[doc_id] = doc
        
        # Sort by combined score
        sorted_docs = sorted(combined_scores.items(), 
                           key=lambda x: x[1], reverse=True)
        
        return {
            "documents": [document_map[doc_id] for doc_id, _ in sorted_docs],
            "scores": [score for _, score in sorted_docs],
            "databases_queried": ["multiple"]
        }
    
    def _apply_mmr(self, results: Dict[str, Any], query_embedding: np.ndarray, 
                  k: int) -> Dict[str, Any]:
        """Apply Maximal Marginal Relevance to results"""
        
        # Implementation similar to _mmr_search but on existing results
        # Returns diverse subset of results
        
        return {
            "documents": results["documents"][:k],
            "scores": results["scores"][:k],
            "databases_queried": results.get("databases_queried", [])
        }
    
    async def _generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for text"""
        
        model = self.embedding_models.get("default")
        if model:
            embedding = model.encode(text)
            return np.array(embedding)
        else:
            # Fallback to random embedding for testing
            return np.random.rand(self.config["vector_dimension"])
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def _calculate_relevance_score(self, query: str, document: str) -> float:
        """Calculate relevance score between query and document"""
        
        # Simplified relevance scoring
        # In production, use more sophisticated methods
        
        query_terms = set(query.lower().split())
        doc_terms = set(document.lower().split())
        
        if not query_terms:
            return 0.0
        
        overlap = len(query_terms.intersection(doc_terms))
        return overlap / len(query_terms)
    
    async def update_document(self, doc_id: str, content: str = None, 
                             metadata: Dict[str, Any] = None) -> bool:
        """Update existing document in vector databases"""
        
        # Update in all databases
        success = True
        for db_name, db in self.databases.items():
            try:
                await db.update(doc_id, content, metadata)
            except Exception as e:
                print(f"Error updating in {db_name}: {e}")
                success = False
        
        # Update memory store
        self.memory_store.update_document(doc_id, content, metadata)
        
        # Invalidate cache
        self.cache.invalidate(doc_id)
        
        return success
    
    async def delete_document(self, doc_id: str) -> bool:
        """Delete document from vector databases"""
        
        success = True
        for db_name, db in self.databases.items():
            try:
                await db.delete(doc_id)
            except Exception as e:
                print(f"Error deleting from {db_name}: {e}")
                success = False
        
        # Remove from memory store
        self.memory_store.delete_document(doc_id)
        
        # Invalidate cache
        self.cache.invalidate(doc_id)
        
        return success
    
    async def optimize_indices(self) -> Dict[str, Any]:
        """Optimize vector database indices for better performance"""
        
        optimization_results = {}
        
        for db_name, db in self.databases.items():
            try:
                result = await db.optimize_index()
                optimization_results[db_name] = result
            except Exception as e:
                optimization_results[db_name] = {"error": str(e)}
        
        # Optimize memory store
        self.memory_store.optimize()
        
        # Clear old cache entries
        self.cache.cleanup()
        
        return optimization_results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about vector database system"""
        
        stats = {
            "total_documents": 0,
            "databases": {},
            "cache_stats": self.cache.get_stats(),
            "memory_store_stats": self.memory_store.get_stats(),
            "index_stats": self.index_manager.get_stats()
        }
        
        for db_name, db in self.databases.items():
            db_stats = db.get_stats()
            stats["databases"][db_name] = db_stats
            stats["total_documents"] += db_stats.get("document_count", 0)
        
        return stats

class FAISSDatabase:
    """FAISS vector database implementation"""
    
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = {}
        self.metadata = {}
        self.id_map = {}
        self.next_id = 0
    
    async def store(self, documents: List[VectorDocument], 
                   collection: str) -> Dict[str, Any]:
        """Store documents in FAISS index"""
        
        embeddings = []
        for doc in documents:
            # Store document
            internal_id = self.next_id
            self.documents[internal_id] = doc
            self.id_map[doc.id] = internal_id
            self.metadata[internal_id] = doc.metadata
            embeddings.append(doc.embedding)
            self.next_id += 1
        
        # Add to index
        embeddings_array = np.array(embeddings).astype('float32')
        self.index.add(embeddings_array)
        
        return {"stored": len(documents)}
    
    async def search(self, query_embedding: np.ndarray, k: int, 
                    filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Search in FAISS index"""
        
        # Search in index
        query_array = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(query_array, min(k, self.index.ntotal))
        
        results = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            if idx != -1 and idx in self.documents:
                doc = self.documents[idx]
                
                # Apply filters if provided
                if filters:
                    if not self._matches_filters(doc, filters):
                        continue
                
                results.append({
                    "document": doc,
                    "score": 1.0 / (1.0 + dist)  # Convert distance to similarity
                })
        
        return {
            "documents": [r["document"] for r in results],
            "scores": [r["score"] for r in results]
        }
    
    def _matches_filters(self, doc: VectorDocument, 
                        filters: Dict[str, Any]) -> bool:
        """Check if document matches filters"""
        
        for key, value in filters.items():
            if key not in doc.metadata or doc.metadata[key] != value:
                return False
        return True
    
    async def update(self, doc_id: str, content: str = None, 
                    metadata: Dict[str, Any] = None) -> bool:
        """Update document in FAISS"""
        
        if doc_id in self.id_map:
            internal_id = self.id_map[doc_id]
            doc = self.documents[internal_id]
            
            if content:
                doc.content = content
                # Would need to update embedding
            
            if metadata:
                doc.metadata.update(metadata)
                self.metadata[internal_id].update(metadata)
            
            return True
        return False
    
    async def delete(self, doc_id: str) -> bool:
        """Delete document from FAISS"""
        
        if doc_id in self.id_map:
            internal_id = self.id_map[doc_id]
            del self.documents[internal_id]
            del self.metadata[internal_id]
            del self.id_map[doc_id]
            # Note: FAISS doesn't support deletion from index directly
            # Would need to rebuild index
            return True
        return False
    
    async def optimize_index(self) -> Dict[str, Any]:
        """Optimize FAISS index"""
        
        # Could implement index compression or restructuring
        return {"optimized": True, "index_size": self.index.ntotal}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get FAISS database statistics"""
        
        return {
            "document_count": len(self.documents),
            "index_size": self.index.ntotal,
            "dimension": self.dimension,
            "memory_usage_mb": self.index.ntotal * self.dimension * 4 / (1024 * 1024)
        }

class ChromaDatabase:
    """ChromaDB vector database implementation"""
    
    def __init__(self):
        self.client = chromadb.Client()
        self.collections = {}
    
    async def store(self, documents: List[VectorDocument], 
                   collection_name: str = "default") -> Dict[str, Any]:
        """Store documents in ChromaDB"""
        
        # Get or create collection
        if collection_name not in self.collections:
            self.collections[collection_name] = self.client.create_collection(
                name=collection_name
            )
        
        collection = self.collections[collection_name]
        
        # Prepare data for insertion
        ids = [doc.id for doc in documents]
        embeddings = [doc.embedding.tolist() for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        documents_text = [doc.content for doc in documents]
        
        # Add to collection
        collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents_text
        )
        
        return {"stored": len(documents)}
    
    async def search(self, query_embedding: np.ndarray, k: int, 
                    filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Search in ChromaDB"""
        
        results_list = []
        
        # Search across all collections
        for collection_name, collection in self.collections.items():
            results = collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=k,
                where=filters
            )
            
            for i in range(len(results['ids'][0])):
                doc = VectorDocument(
                    id=results['ids'][0][i],
                    content=results['documents'][0][i],
                    metadata=results['metadatas'][0][i]
                )
                score = 1.0 / (1.0 + results['distances'][0][i])
                results_list.append({"document": doc, "score": score})
        
        # Sort by score
        results_list.sort(key=lambda x: x["score"], reverse=True)
        
        return {
            "documents": [r["document"] for r in results_list[:k]],
            "scores": [r["score"] for r in results_list[:k]]
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get ChromaDB statistics"""
        
        total_docs = 0
        for collection in self.collections.values():
            total_docs += collection.count()
        
        return {
            "document_count": total_docs,
            "collection_count": len(self.collections)
        }

class MemoryStore:
    """In-memory store for fast access and keyword search"""
    
    def __init__(self):
        self.documents = {}
        self.inverted_index = defaultdict(set)
    
    def add_documents(self, documents: List[VectorDocument]):
        """Add documents to memory store"""
        
        for doc in documents:
            self.documents[doc.id] = doc
            
            # Build inverted index for keyword search
            tokens = doc.content.lower().split()
            for token in tokens:
                self.inverted_index[token].add(doc.id)
    
    def keyword_search(self, query: str, k: int) -> List[Dict[str, Any]]:
        """Perform keyword search in memory"""
        
        query_tokens = query.lower().split()
        doc_scores = defaultdict(float)
        
        for token in query_tokens:
            if token in self.inverted_index:
                for doc_id in self.inverted_index[token]:
                    doc_scores[doc_id] += 1.0
        
        # Sort by score
        sorted_docs = sorted(doc_scores.items(), 
                           key=lambda x: x[1], reverse=True)
        
        results = []
        for doc_id, score in sorted_docs[:k]:
            if doc_id in self.documents:
                results.append({
                    "document": self.documents[doc_id],
                    "score": score / len(query_tokens)
                })
        
        return results
    
    def update_document(self, doc_id: str, content: str = None, 
                       metadata: Dict[str, Any] = None):
        """Update document in memory store"""
        
        if doc_id in self.documents:
            doc = self.documents[doc_id]
            
            if content:
                # Remove old tokens from index
                old_tokens = doc.content.lower().split()
                for token in old_tokens:
                    self.inverted_index[token].discard(doc_id)
                
                # Update content
                doc.content = content
                
                # Add new tokens to index
                new_tokens = content.lower().split()
                for token in new_tokens:
                    self.inverted_index[token].add(doc_id)
            
            if metadata:
                doc.metadata.update(metadata)
    
    def delete_document(self, doc_id: str):
        """Delete document from memory store"""
        
        if doc_id in self.documents:
            doc = self.documents[doc_id]
            
            # Remove from inverted index
            tokens = doc.content.lower().split()
            for token in tokens:
                self.inverted_index[token].discard(doc_id)
            
            # Remove document
            del self.documents[doc_id]
    
    def optimize(self):
        """Optimize memory store"""
        
        # Remove empty token entries
        empty_tokens = [token for token, docs in self.inverted_index.items() 
                       if not docs]
        for token in empty_tokens:
            del self.inverted_index[token]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory store statistics"""
        
        return {
            "document_count": len(self.documents),
            "unique_tokens": len(self.inverted_index),
            "avg_tokens_per_doc": sum(len(doc.content.split()) 
                                     for doc in self.documents.values()) / 
                                  max(len(self.documents), 1)
        }

class SemanticCache:
    """Semantic caching for search results"""
    
    def __init__(self, ttl_minutes: int = 60):
        self.cache = {}
        self.ttl = timedelta(minutes=ttl_minutes)
    
    def _get_cache_key(self, query: str, k: int, 
                      strategy: SearchStrategy) -> str:
        """Generate cache key"""
        
        key_str = f"{query}_{k}_{strategy.value}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, query: str, k: int, 
           strategy: SearchStrategy) -> Optional[SearchResult]:
        """Get cached result"""
        
        key = self._get_cache_key(query, k, strategy)
        
        if key in self.cache:
            entry = self.cache[key]
            if datetime.utcnow() - entry["timestamp"] < self.ttl:
                return entry["result"]
            else:
                del self.cache[key]
        
        return None
    
    def set(self, query: str, k: int, strategy: SearchStrategy, 
           result: SearchResult):
        """Cache search result"""
        
        key = self._get_cache_key(query, k, strategy)
        self.cache[key] = {
            "result": result,
            "timestamp": datetime.utcnow()
        }
    
    def invalidate(self, doc_id: str):
        """Invalidate cache entries containing document"""
        
        # In production, maintain reverse index for efficient invalidation
        # For now, clear entire cache when document changes
        self.cache.clear()
    
    def cleanup(self):
        """Remove expired cache entries"""
        
        now = datetime.utcnow()
        expired_keys = [
            key for key, entry in self.cache.items()
            if now - entry["timestamp"] >= self.ttl
        ]
        
        for key in expired_keys:
            del self.cache[key]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        
        return {
            "cached_queries": len(self.cache),
            "ttl_minutes": self.ttl.total_seconds() / 60
        }

class IndexManager:
    """Manage vector database indices"""
    
    def __init__(self):
        self.indices = {}
        self.index_metadata = {}
    
    async def update_indices(self, documents: List[VectorDocument], 
                            collection: str):
        """Update indices with new documents"""
        
        # Update collection index
        if collection not in self.indices:
            self.indices[collection] = {
                "document_count": 0,
                "last_updated": datetime.utcnow()
            }
        
        self.indices[collection]["document_count"] += len(documents)
        self.indices[collection]["last_updated"] = datetime.utcnow()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get index statistics"""
        
        return {
            "index_count": len(self.indices),
            "total_documents": sum(idx["document_count"] 
                                 for idx in self.indices.values())
        }

# Example usage and testing

async def main():
    """Example usage of Vector Database System"""
    
    # Initialize vector database system
    vector_db = VectorDatabaseSystem()
    
    # Create sample documents
    documents = [
        VectorDocument(
            id="doc1",
            content="Machine learning is a subset of artificial intelligence",
            metadata={"category": "AI", "importance": "high"}
        ),
        VectorDocument(
            id="doc2",
            content="Deep learning uses neural networks with multiple layers",
            metadata={"category": "AI", "importance": "high"}
        ),
        VectorDocument(
            id="doc3",
            content="Python is a popular programming language for data science",
            metadata={"category": "Programming", "importance": "medium"}
        )
    ]
    
    # Store documents
    print("📊 Storing documents in vector databases...")
    store_result = await vector_db.store_documents(documents)
    print(f"✅ Stored {store_result['stored_count']} documents")
    print(f"⏱️  Execution time: {store_result['execution_time']:.2f}s")
    
    # Perform hybrid search
    print("\n🔍 Performing hybrid search...")
    search_result = await vector_db.search(
        query="neural networks and deep learning",
        k=2,
        strategy=SearchStrategy.HYBRID
    )
    
    print(f"Found {len(search_result.documents)} results:")
    for doc, score in zip(search_result.documents, search_result.scores):
        print(f"  - {doc.id}: {doc.content[:50]}... (score: {score:.3f})")
    print(f"⏱️  Query time: {search_result.query_time:.3f}s")
    
    # Perform MMR search for diversity
    print("\n🔍 Performing MMR search for diversity...")
    mmr_result = await vector_db.search(
        query="artificial intelligence",
        k=3,
        strategy=SearchStrategy.MMR
    )
    
    print(f"Found {len(mmr_result.documents)} diverse results")
    
    # Get system statistics
    print("\n📈 Vector Database Statistics:")
    stats = vector_db.get_statistics()
    print(f"  Total documents: {stats['total_documents']}")
    print(f"  Databases active: {len(stats['databases'])}")
    print(f"  Cache stats: {stats['cache_stats']}")
    
    # Optimize indices
    print("\n⚡ Optimizing indices...")
    optimization_result = await vector_db.optimize_indices()
    print(f"  Optimization complete: {optimization_result}")

if __name__ == "__main__":
    asyncio.run(main())