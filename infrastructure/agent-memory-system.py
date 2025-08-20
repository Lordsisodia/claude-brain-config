#!/usr/bin/env python3
"""
Agent Memory Storage System - Phase 2 Implementation
Persistent learning and memory capabilities for multi-agent architecture
Based on SuperAGI and AutoGen patterns for agent learning
"""

import asyncio
import json
import pickle
import time
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import hashlib
from collections import defaultdict, deque
import numpy as np
from pathlib import Path
import sqlite3
import redis

# Memory Types and Classifications

class MemoryType(Enum):
    """Types of agent memory"""
    EPISODIC = "episodic"          # Specific experiences and events
    SEMANTIC = "semantic"          # Facts and general knowledge
    PROCEDURAL = "procedural"      # How to perform tasks
    WORKING = "working"            # Current context and active tasks
    SENSORY = "sensory"            # Raw input/output data
    PROSPECTIVE = "prospective"    # Future tasks and reminders
    COLLECTIVE = "collective"      # Shared knowledge across agents

class MemoryImportance(Enum):
    """Importance levels for memory items"""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    TRIVIAL = 1

class LearningStrategy(Enum):
    """Learning strategies for agents"""
    REINFORCEMENT = "reinforcement"
    SUPERVISED = "supervised"
    UNSUPERVISED = "unsupervised"
    TRANSFER = "transfer"
    META = "meta"
    CONTINUAL = "continual"
    FEDERATED = "federated"

@dataclass
class MemoryItem:
    """Individual memory item"""
    id: str
    agent_id: str
    memory_type: MemoryType
    content: Any
    embedding: Optional[np.ndarray] = None
    importance: MemoryImportance = MemoryImportance.MEDIUM
    timestamp: datetime = field(default_factory=datetime.utcnow)
    last_accessed: datetime = field(default_factory=datetime.utcnow)
    access_count: int = 0
    decay_rate: float = 0.01
    associations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    source_context: Optional[Dict[str, Any]] = None

@dataclass
class LearningExperience:
    """Learning experience from agent execution"""
    experience_id: str
    agent_id: str
    task: str
    action_taken: str
    outcome: str
    reward: float
    state_before: Dict[str, Any]
    state_after: Dict[str, Any]
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SkillPattern:
    """Learned skill pattern"""
    pattern_id: str
    name: str
    description: str
    trigger_conditions: List[Dict[str, Any]]
    action_sequence: List[str]
    success_rate: float
    usage_count: int
    learned_from: List[str]  # Experience IDs
    applicable_agents: List[str]

@dataclass
class AgentProfile:
    """Agent learning profile"""
    agent_id: str
    specialization: str
    total_experiences: int
    success_rate: float
    learned_skills: List[str]
    knowledge_domains: Dict[str, float]  # Domain -> expertise level
    performance_history: List[float]
    learning_rate: float
    adaptation_speed: float

class AgentMemorySystem:
    """
    Comprehensive memory and learning system for multi-agent architecture
    Enables persistent learning, skill transfer, and collective intelligence
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._default_config()
        self.memory_stores = self._initialize_memory_stores()
        self.learning_engine = LearningEngine(self.config)
        self.skill_library = SkillLibrary()
        self.knowledge_graph = KnowledgeGraph()
        self.consolidation_engine = MemoryConsolidation()
        self.agent_profiles = {}
        self._initialize_persistence()
        
    def _default_config(self) -> Dict[str, Any]:
        """Default memory system configuration"""
        return {
            "storage_backend": "hybrid",  # sqlite + redis + vector
            "max_memory_items": 1000000,
            "consolidation_interval_hours": 24,
            "decay_enabled": True,
            "decay_rate": 0.01,
            "importance_threshold": MemoryImportance.LOW.value,
            "learning_enabled": True,
            "transfer_learning_enabled": True,
            "collective_learning_enabled": True,
            "persistence_path": "./agent_memory",
            "redis_config": {
                "host": "localhost",
                "port": 6379,
                "db": 0
            }
        }
    
    def _initialize_memory_stores(self) -> Dict[str, Any]:
        """Initialize different memory stores"""
        stores = {}
        
        # Episodic memory - experiences and events
        stores["episodic"] = EpisodicMemoryStore(
            max_items=100000,
            consolidation_threshold=0.7
        )
        
        # Semantic memory - facts and knowledge
        stores["semantic"] = SemanticMemoryStore(
            max_items=500000,
            use_knowledge_graph=True
        )
        
        # Procedural memory - skills and procedures
        stores["procedural"] = ProceduralMemoryStore(
            max_patterns=10000
        )
        
        # Working memory - current context
        stores["working"] = WorkingMemoryStore(
            capacity=100,
            duration_minutes=30
        )
        
        # Collective memory - shared across agents
        stores["collective"] = CollectiveMemoryStore(
            consensus_threshold=0.8
        )
        
        return stores
    
    def _initialize_persistence(self):
        """Initialize persistent storage"""
        
        # Create storage directory
        Path(self.config["persistence_path"]).mkdir(parents=True, exist_ok=True)
        
        # Initialize SQLite for structured data
        self.db_path = Path(self.config["persistence_path"]) / "agent_memory.db"
        self._init_database()
        
        # Initialize Redis for fast access (if available)
        try:
            self.redis_client = redis.Redis(
                **self.config["redis_config"],
                decode_responses=True
            )
            self.redis_client.ping()
            self.redis_available = True
        except:
            self.redis_available = False
            print("Redis not available, using SQLite only")
    
    def _init_database(self):
        """Initialize SQLite database schema"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Memory items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory_items (
                id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                memory_type TEXT NOT NULL,
                content TEXT NOT NULL,
                importance INTEGER NOT NULL,
                timestamp REAL NOT NULL,
                last_accessed REAL NOT NULL,
                access_count INTEGER DEFAULT 0,
                decay_rate REAL DEFAULT 0.01,
                metadata TEXT,
                embedding BLOB,
                INDEX idx_agent_id (agent_id),
                INDEX idx_memory_type (memory_type),
                INDEX idx_importance (importance),
                INDEX idx_timestamp (timestamp)
            )
        """)
        
        # Learning experiences table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_experiences (
                experience_id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                task TEXT NOT NULL,
                action_taken TEXT NOT NULL,
                outcome TEXT NOT NULL,
                reward REAL NOT NULL,
                state_before TEXT NOT NULL,
                state_after TEXT NOT NULL,
                timestamp REAL NOT NULL,
                metadata TEXT,
                INDEX idx_agent_id (agent_id),
                INDEX idx_reward (reward),
                INDEX idx_timestamp (timestamp)
            )
        """)
        
        # Skill patterns table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skill_patterns (
                pattern_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                trigger_conditions TEXT NOT NULL,
                action_sequence TEXT NOT NULL,
                success_rate REAL DEFAULT 0.0,
                usage_count INTEGER DEFAULT 0,
                learned_from TEXT,
                applicable_agents TEXT,
                INDEX idx_success_rate (success_rate),
                INDEX idx_usage_count (usage_count)
            )
        """)
        
        # Agent profiles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_profiles (
                agent_id TEXT PRIMARY KEY,
                specialization TEXT,
                total_experiences INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0,
                learned_skills TEXT,
                knowledge_domains TEXT,
                performance_history TEXT,
                learning_rate REAL DEFAULT 0.1,
                adaptation_speed REAL DEFAULT 0.5,
                last_updated REAL NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
    
    async def store_memory(self, agent_id: str, memory_item: MemoryItem) -> bool:
        """Store a memory item for an agent"""
        
        # Determine memory type and route to appropriate store
        store = self.memory_stores.get(memory_item.memory_type.value)
        if not store:
            return False
        
        # Store in appropriate memory store
        success = await store.store(memory_item)
        
        # Persist to database
        if success:
            self._persist_memory_item(memory_item)
            
            # Cache in Redis if available
            if self.redis_available:
                self._cache_memory_item(memory_item)
        
        # Update agent profile
        self._update_agent_profile(agent_id, "memory_stored")
        
        # Trigger consolidation if needed
        if self._should_consolidate(agent_id):
            asyncio.create_task(self._consolidate_memories(agent_id))
        
        return success
    
    async def recall_memory(self, agent_id: str, query: str, 
                          memory_types: List[MemoryType] = None,
                          k: int = 5) -> List[MemoryItem]:
        """Recall relevant memories for an agent"""
        
        recalled_memories = []
        
        # Search in specified memory types or all
        types_to_search = memory_types or list(MemoryType)
        
        for mem_type in types_to_search:
            store = self.memory_stores.get(mem_type.value)
            if store:
                memories = await store.search(query, agent_id, k)
                recalled_memories.extend(memories)
        
        # Sort by relevance and importance
        recalled_memories.sort(
            key=lambda m: (m.importance.value, -m.decay_rate),
            reverse=True
        )
        
        # Update access patterns
        for memory in recalled_memories[:k]:
            self._update_memory_access(memory)
        
        return recalled_memories[:k]
    
    async def learn_from_experience(self, experience: LearningExperience) -> Dict[str, Any]:
        """Learn from an agent's experience"""
        
        # Store the experience
        self._persist_experience(experience)
        
        # Extract patterns and insights
        insights = await self.learning_engine.process_experience(experience)
        
        # Update skill library if new pattern discovered
        if insights.get("new_pattern"):
            skill = self._create_skill_from_pattern(insights["new_pattern"])
            self.skill_library.add_skill(skill)
        
        # Update agent profile with learning
        self._update_agent_learning_profile(
            experience.agent_id,
            experience.reward,
            insights
        )
        
        # Share learning with other agents if enabled
        if self.config["collective_learning_enabled"]:
            await self._share_learning(experience, insights)
        
        return {
            "experience_stored": True,
            "insights_gained": insights,
            "skills_learned": insights.get("new_skills", []),
            "performance_delta": insights.get("performance_improvement", 0.0)
        }
    
    async def transfer_knowledge(self, from_agent: str, to_agent: str,
                                domain: str = None) -> Dict[str, Any]:
        """Transfer knowledge from one agent to another"""
        
        if not self.config["transfer_learning_enabled"]:
            return {"transferred": False, "reason": "Transfer learning disabled"}
        
        # Get source agent's knowledge
        source_knowledge = await self._get_agent_knowledge(from_agent, domain)
        
        # Adapt knowledge for target agent
        adapted_knowledge = await self._adapt_knowledge(
            source_knowledge,
            from_agent,
            to_agent
        )
        
        # Transfer to target agent
        transfer_results = []
        for knowledge_item in adapted_knowledge:
            result = await self.store_memory(to_agent, knowledge_item)
            transfer_results.append(result)
        
        # Update both agents' profiles
        self._record_knowledge_transfer(from_agent, to_agent, len(adapted_knowledge))
        
        return {
            "transferred": True,
            "items_transferred": len(adapted_knowledge),
            "success_rate": sum(transfer_results) / max(len(transfer_results), 1),
            "domains": list(set(k.metadata.get("domain") for k in adapted_knowledge))
        }
    
    async def get_agent_skills(self, agent_id: str) -> List[SkillPattern]:
        """Get all skills learned by an agent"""
        
        profile = self._get_agent_profile(agent_id)
        if not profile:
            return []
        
        skills = []
        for skill_id in profile.learned_skills:
            skill = self.skill_library.get_skill(skill_id)
            if skill:
                skills.append(skill)
        
        return skills
    
    async def apply_skill(self, agent_id: str, skill_id: str,
                         context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply a learned skill in a given context"""
        
        skill = self.skill_library.get_skill(skill_id)
        if not skill:
            return {"success": False, "reason": "Skill not found"}
        
        # Check if skill is applicable
        if not self._is_skill_applicable(skill, context):
            return {"success": False, "reason": "Skill not applicable in context"}
        
        # Execute skill action sequence
        results = []
        for action in skill.action_sequence:
            result = await self._execute_skill_action(action, context)
            results.append(result)
            
            if not result["success"]:
                break
        
        # Update skill statistics
        success = all(r["success"] for r in results)
        self.skill_library.update_skill_stats(skill_id, success)
        
        return {
            "success": success,
            "skill_applied": skill.name,
            "actions_executed": len([r for r in results if r["success"]]),
            "total_actions": len(skill.action_sequence),
            "results": results
        }
    
    async def consolidate_memories(self, agent_id: str = None):
        """Consolidate and optimize memories"""
        
        agents_to_consolidate = [agent_id] if agent_id else self.agent_profiles.keys()
        
        consolidation_results = {}
        for agent in agents_to_consolidate:
            result = await self._consolidate_memories(agent)
            consolidation_results[agent] = result
        
        return consolidation_results
    
    async def _consolidate_memories(self, agent_id: str) -> Dict[str, Any]:
        """Consolidate memories for a specific agent"""
        
        start_time = time.time()
        
        # Get all memories for agent
        memories = self._get_agent_memories(agent_id)
        
        # Apply decay
        if self.config["decay_enabled"]:
            memories = self._apply_memory_decay(memories)
        
        # Compress similar memories
        compressed = self.consolidation_engine.compress_memories(memories)
        
        # Extract semantic patterns
        patterns = self.consolidation_engine.extract_patterns(compressed)
        
        # Update semantic memory with patterns
        for pattern in patterns:
            semantic_memory = MemoryItem(
                id=self._generate_id(),
                agent_id=agent_id,
                memory_type=MemoryType.SEMANTIC,
                content=pattern["content"],
                importance=MemoryImportance.HIGH,
                metadata={"pattern_type": pattern["type"], "frequency": pattern["frequency"]}
            )
            await self.store_memory(agent_id, semantic_memory)
        
        # Remove consolidated episodic memories
        removed_count = self._cleanup_consolidated_memories(agent_id, compressed)
        
        execution_time = time.time() - start_time
        
        return {
            "memories_processed": len(memories),
            "memories_compressed": len(compressed),
            "patterns_extracted": len(patterns),
            "memories_removed": removed_count,
            "execution_time": execution_time
        }
    
    def _persist_memory_item(self, memory_item: MemoryItem):
        """Persist memory item to database"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO memory_items
            (id, agent_id, memory_type, content, importance, timestamp,
             last_accessed, access_count, decay_rate, metadata, embedding)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            memory_item.id,
            memory_item.agent_id,
            memory_item.memory_type.value,
            json.dumps(memory_item.content),
            memory_item.importance.value,
            memory_item.timestamp.timestamp(),
            memory_item.last_accessed.timestamp(),
            memory_item.access_count,
            memory_item.decay_rate,
            json.dumps(memory_item.metadata),
            pickle.dumps(memory_item.embedding) if memory_item.embedding is not None else None
        ))
        
        conn.commit()
        conn.close()
    
    def _persist_experience(self, experience: LearningExperience):
        """Persist learning experience to database"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO learning_experiences
            (experience_id, agent_id, task, action_taken, outcome,
             reward, state_before, state_after, timestamp, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            experience.experience_id,
            experience.agent_id,
            experience.task,
            experience.action_taken,
            experience.outcome,
            experience.reward,
            json.dumps(experience.state_before),
            json.dumps(experience.state_after),
            experience.timestamp.timestamp(),
            json.dumps(experience.metadata)
        ))
        
        conn.commit()
        conn.close()
    
    def _cache_memory_item(self, memory_item: MemoryItem):
        """Cache memory item in Redis for fast access"""
        
        if not self.redis_available:
            return
        
        key = f"memory:{memory_item.agent_id}:{memory_item.id}"
        value = json.dumps({
            "content": memory_item.content,
            "type": memory_item.memory_type.value,
            "importance": memory_item.importance.value,
            "timestamp": memory_item.timestamp.isoformat()
        })
        
        # Set with expiration based on importance
        ttl = 3600 * memory_item.importance.value  # Hours based on importance
        self.redis_client.setex(key, ttl, value)
    
    def _get_agent_profile(self, agent_id: str) -> Optional[AgentProfile]:
        """Get agent profile from database"""
        
        if agent_id in self.agent_profiles:
            return self.agent_profiles[agent_id]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM agent_profiles WHERE agent_id = ?
        """, (agent_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            profile = AgentProfile(
                agent_id=row[0],
                specialization=row[1],
                total_experiences=row[2],
                success_rate=row[3],
                learned_skills=json.loads(row[4]) if row[4] else [],
                knowledge_domains=json.loads(row[5]) if row[5] else {},
                performance_history=json.loads(row[6]) if row[6] else [],
                learning_rate=row[7],
                adaptation_speed=row[8]
            )
            self.agent_profiles[agent_id] = profile
            return profile
        
        return None
    
    def _update_agent_profile(self, agent_id: str, event_type: str):
        """Update agent profile based on events"""
        
        profile = self._get_agent_profile(agent_id)
        if not profile:
            profile = AgentProfile(
                agent_id=agent_id,
                specialization="general",
                total_experiences=0,
                success_rate=0.0,
                learned_skills=[],
                knowledge_domains={},
                performance_history=[],
                learning_rate=0.1,
                adaptation_speed=0.5
            )
        
        if event_type == "memory_stored":
            profile.total_experiences += 1
        
        # Save updated profile
        self._save_agent_profile(profile)
    
    def _save_agent_profile(self, profile: AgentProfile):
        """Save agent profile to database"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO agent_profiles
            (agent_id, specialization, total_experiences, success_rate,
             learned_skills, knowledge_domains, performance_history,
             learning_rate, adaptation_speed, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            profile.agent_id,
            profile.specialization,
            profile.total_experiences,
            profile.success_rate,
            json.dumps(profile.learned_skills),
            json.dumps(profile.knowledge_domains),
            json.dumps(profile.performance_history),
            profile.learning_rate,
            profile.adaptation_speed,
            datetime.utcnow().timestamp()
        ))
        
        conn.commit()
        conn.close()
        
        self.agent_profiles[profile.agent_id] = profile
    
    def _generate_id(self) -> str:
        """Generate unique ID"""
        return hashlib.md5(
            f"{datetime.utcnow().isoformat()}{np.random.rand()}".encode()
        ).hexdigest()

class LearningEngine:
    """Engine for processing experiences and extracting learning"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.pattern_detector = PatternDetector()
        self.reward_calculator = RewardCalculator()
    
    async def process_experience(self, experience: LearningExperience) -> Dict[str, Any]:
        """Process experience and extract insights"""
        
        insights = {
            "patterns_detected": [],
            "performance_improvement": 0.0,
            "new_skills": [],
            "recommendations": []
        }
        
        # Detect patterns in state transitions
        patterns = self.pattern_detector.detect(
            experience.state_before,
            experience.state_after,
            experience.action_taken
        )
        insights["patterns_detected"] = patterns
        
        # Calculate performance improvement
        improvement = self.reward_calculator.calculate_improvement(
            experience.reward,
            experience.agent_id
        )
        insights["performance_improvement"] = improvement
        
        # Identify potential new skills
        if experience.reward > 0.8:  # High reward threshold
            potential_skill = self._extract_skill_from_success(experience)
            if potential_skill:
                insights["new_skills"].append(potential_skill)
                insights["new_pattern"] = potential_skill
        
        # Generate recommendations
        recommendations = self._generate_recommendations(experience, patterns)
        insights["recommendations"] = recommendations
        
        return insights
    
    def _extract_skill_from_success(self, experience: LearningExperience) -> Optional[Dict[str, Any]]:
        """Extract reusable skill from successful experience"""
        
        if experience.reward < 0.8:
            return None
        
        return {
            "name": f"skill_{experience.task}_{experience.agent_id}",
            "trigger_conditions": [experience.state_before],
            "action_sequence": [experience.action_taken],
            "expected_outcome": experience.outcome,
            "confidence": experience.reward
        }
    
    def _generate_recommendations(self, experience: LearningExperience,
                                 patterns: List[Dict[str, Any]]) -> List[str]:
        """Generate learning recommendations"""
        
        recommendations = []
        
        if experience.reward < 0.5:
            recommendations.append(f"Consider alternative approach for task: {experience.task}")
        
        if patterns:
            recommendations.append(f"Detected {len(patterns)} patterns that could be optimized")
        
        return recommendations

class SkillLibrary:
    """Library of learned skills and procedures"""
    
    def __init__(self):
        self.skills = {}
        self.skill_index = defaultdict(list)  # Task type -> skill IDs
    
    def add_skill(self, skill: SkillPattern):
        """Add a new skill to the library"""
        self.skills[skill.pattern_id] = skill
        
        # Index by trigger conditions
        for condition in skill.trigger_conditions:
            task_type = condition.get("task_type", "general")
            self.skill_index[task_type].append(skill.pattern_id)
    
    def get_skill(self, skill_id: str) -> Optional[SkillPattern]:
        """Retrieve a skill by ID"""
        return self.skills.get(skill_id)
    
    def find_applicable_skills(self, context: Dict[str, Any]) -> List[SkillPattern]:
        """Find skills applicable to a given context"""
        
        applicable = []
        task_type = context.get("task_type", "general")
        
        for skill_id in self.skill_index[task_type]:
            skill = self.skills[skill_id]
            if self._matches_conditions(skill.trigger_conditions, context):
                applicable.append(skill)
        
        # Sort by success rate
        applicable.sort(key=lambda s: s.success_rate, reverse=True)
        
        return applicable
    
    def _matches_conditions(self, conditions: List[Dict[str, Any]],
                          context: Dict[str, Any]) -> bool:
        """Check if context matches skill trigger conditions"""
        
        for condition in conditions:
            for key, value in condition.items():
                if context.get(key) != value:
                    return False
        return True
    
    def update_skill_stats(self, skill_id: str, success: bool):
        """Update skill usage statistics"""
        
        if skill_id in self.skills:
            skill = self.skills[skill_id]
            skill.usage_count += 1
            
            # Update success rate with exponential moving average
            alpha = 0.1  # Learning rate
            skill.success_rate = (1 - alpha) * skill.success_rate + alpha * (1.0 if success else 0.0)

class KnowledgeGraph:
    """Knowledge graph for semantic relationships"""
    
    def __init__(self):
        self.nodes = {}  # concept -> node data
        self.edges = defaultdict(list)  # concept -> [(related_concept, relationship_type, weight)]
    
    def add_concept(self, concept: str, data: Dict[str, Any]):
        """Add a concept node to the graph"""
        self.nodes[concept] = data
    
    def add_relationship(self, concept1: str, concept2: str,
                        relationship: str, weight: float = 1.0):
        """Add a relationship between concepts"""
        self.edges[concept1].append((concept2, relationship, weight))
        self.edges[concept2].append((concept1, f"inverse_{relationship}", weight))
    
    def find_related(self, concept: str, relationship: str = None,
                     max_depth: int = 2) -> List[Tuple[str, float]]:
        """Find related concepts"""
        
        if concept not in self.nodes:
            return []
        
        visited = set()
        related = []
        queue = [(concept, 0, 1.0)]  # (concept, depth, weight)
        
        while queue:
            current, depth, weight = queue.pop(0)
            
            if current in visited or depth > max_depth:
                continue
            
            visited.add(current)
            
            if current != concept:
                related.append((current, weight))
            
            # Add neighbors to queue
            for neighbor, rel, edge_weight in self.edges[current]:
                if relationship and rel != relationship:
                    continue
                
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1, weight * edge_weight))
        
        # Sort by weight
        related.sort(key=lambda x: x[1], reverse=True)
        
        return related

class MemoryConsolidation:
    """Engine for memory consolidation and compression"""
    
    def compress_memories(self, memories: List[MemoryItem]) -> List[MemoryItem]:
        """Compress similar memories"""
        
        compressed = []
        clusters = self._cluster_memories(memories)
        
        for cluster in clusters:
            if len(cluster) == 1:
                compressed.append(cluster[0])
            else:
                # Create consolidated memory
                consolidated = self._consolidate_cluster(cluster)
                compressed.append(consolidated)
        
        return compressed
    
    def extract_patterns(self, memories: List[MemoryItem]) -> List[Dict[str, Any]]:
        """Extract patterns from memories"""
        
        patterns = []
        
        # Group by content similarity
        content_groups = defaultdict(list)
        for memory in memories:
            content_hash = self._hash_content(memory.content)
            content_groups[content_hash].append(memory)
        
        # Extract patterns from groups
        for group_hash, group_memories in content_groups.items():
            if len(group_memories) >= 3:  # Minimum frequency for pattern
                pattern = {
                    "type": "recurring",
                    "content": group_memories[0].content,
                    "frequency": len(group_memories),
                    "agents": list(set(m.agent_id for m in group_memories))
                }
                patterns.append(pattern)
        
        return patterns
    
    def _cluster_memories(self, memories: List[MemoryItem]) -> List[List[MemoryItem]]:
        """Cluster similar memories"""
        
        # Simple clustering based on content similarity
        clusters = []
        used = set()
        
        for i, memory in enumerate(memories):
            if i in used:
                continue
            
            cluster = [memory]
            used.add(i)
            
            for j, other in enumerate(memories[i+1:], i+1):
                if j not in used and self._are_similar(memory, other):
                    cluster.append(other)
                    used.add(j)
            
            clusters.append(cluster)
        
        return clusters
    
    def _are_similar(self, mem1: MemoryItem, mem2: MemoryItem,
                    threshold: float = 0.8) -> bool:
        """Check if two memories are similar"""
        
        # Simple similarity check based on content
        if isinstance(mem1.content, str) and isinstance(mem2.content, str):
            # Calculate Jaccard similarity
            words1 = set(mem1.content.lower().split())
            words2 = set(mem2.content.lower().split())
            
            if not words1 or not words2:
                return False
            
            intersection = len(words1.intersection(words2))
            union = len(words1.union(words2))
            
            return intersection / union >= threshold
        
        return False
    
    def _consolidate_cluster(self, cluster: List[MemoryItem]) -> MemoryItem:
        """Consolidate a cluster of memories into one"""
        
        # Use the most important memory as base
        base = max(cluster, key=lambda m: m.importance.value)
        
        # Aggregate metadata
        aggregated_metadata = {}
        for memory in cluster:
            aggregated_metadata.update(memory.metadata)
        
        # Create consolidated memory
        consolidated = MemoryItem(
            id=base.id + "_consolidated",
            agent_id=base.agent_id,
            memory_type=MemoryType.SEMANTIC,
            content=base.content,
            importance=MemoryImportance(
                min(5, max(m.importance.value for m in cluster) + 1)
            ),
            metadata={
                **aggregated_metadata,
                "consolidated_from": len(cluster),
                "original_ids": [m.id for m in cluster]
            }
        )
        
        return consolidated
    
    def _hash_content(self, content: Any) -> str:
        """Generate hash for content"""
        
        if isinstance(content, str):
            # Normalize and hash
            normalized = " ".join(sorted(content.lower().split()))
            return hashlib.md5(normalized.encode()).hexdigest()[:8]
        else:
            return hashlib.md5(str(content).encode()).hexdigest()[:8]

# Specialized Memory Stores

class EpisodicMemoryStore:
    """Store for episodic memories"""
    
    def __init__(self, max_items: int, consolidation_threshold: float):
        self.max_items = max_items
        self.consolidation_threshold = consolidation_threshold
        self.memories = deque(maxlen=max_items)
        self.index = {}  # ID -> memory
    
    async def store(self, memory: MemoryItem) -> bool:
        """Store episodic memory"""
        self.memories.append(memory)
        self.index[memory.id] = memory
        return True
    
    async def search(self, query: str, agent_id: str, k: int) -> List[MemoryItem]:
        """Search episodic memories"""
        
        agent_memories = [m for m in self.memories if m.agent_id == agent_id]
        
        # Simple relevance scoring
        scored = []
        for memory in agent_memories:
            score = self._calculate_relevance(query, memory)
            scored.append((memory, score))
        
        # Sort by score
        scored.sort(key=lambda x: x[1], reverse=True)
        
        return [m for m, _ in scored[:k]]
    
    def _calculate_relevance(self, query: str, memory: MemoryItem) -> float:
        """Calculate relevance score"""
        
        # Simple keyword matching
        query_words = set(query.lower().split())
        
        if isinstance(memory.content, str):
            content_words = set(memory.content.lower().split())
            overlap = len(query_words.intersection(content_words))
            return overlap / max(len(query_words), 1)
        
        return 0.0

class SemanticMemoryStore:
    """Store for semantic memories"""
    
    def __init__(self, max_items: int, use_knowledge_graph: bool):
        self.max_items = max_items
        self.use_knowledge_graph = use_knowledge_graph
        self.memories = {}
        self.knowledge_graph = KnowledgeGraph() if use_knowledge_graph else None
    
    async def store(self, memory: MemoryItem) -> bool:
        """Store semantic memory"""
        
        self.memories[memory.id] = memory
        
        # Add to knowledge graph
        if self.knowledge_graph and isinstance(memory.content, str):
            concepts = self._extract_concepts(memory.content)
            for concept in concepts:
                self.knowledge_graph.add_concept(concept, {
                    "memory_id": memory.id,
                    "agent_id": memory.agent_id
                })
        
        return True
    
    async def search(self, query: str, agent_id: str, k: int) -> List[MemoryItem]:
        """Search semantic memories"""
        
        if self.knowledge_graph:
            # Use knowledge graph for search
            concepts = self._extract_concepts(query)
            related_memories = set()
            
            for concept in concepts:
                related = self.knowledge_graph.find_related(concept)
                for related_concept, _ in related[:k]:
                    node_data = self.knowledge_graph.nodes.get(related_concept, {})
                    memory_id = node_data.get("memory_id")
                    if memory_id and memory_id in self.memories:
                        related_memories.add(self.memories[memory_id])
            
            return list(related_memories)[:k]
        else:
            # Simple search
            return list(self.memories.values())[:k]
    
    def _extract_concepts(self, text: str) -> List[str]:
        """Extract concepts from text"""
        
        # Simple concept extraction (would use NLP in production)
        words = text.lower().split()
        # Filter common words
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'in', 'on', 'at'}
        concepts = [w for w in words if w not in stopwords and len(w) > 3]
        return concepts[:5]  # Top 5 concepts

class ProceduralMemoryStore:
    """Store for procedural memories and skills"""
    
    def __init__(self, max_patterns: int):
        self.max_patterns = max_patterns
        self.procedures = {}
        self.skill_tree = {}  # Hierarchical skill organization
    
    async def store(self, memory: MemoryItem) -> bool:
        """Store procedural memory"""
        
        self.procedures[memory.id] = memory
        
        # Organize in skill tree if it's a skill
        if memory.metadata.get("is_skill"):
            skill_type = memory.metadata.get("skill_type", "general")
            if skill_type not in self.skill_tree:
                self.skill_tree[skill_type] = []
            self.skill_tree[skill_type].append(memory.id)
        
        return True
    
    async def search(self, query: str, agent_id: str, k: int) -> List[MemoryItem]:
        """Search procedural memories"""
        
        # Look for applicable procedures
        applicable = []
        
        for memory in self.procedures.values():
            if memory.agent_id == agent_id:
                if self._is_applicable(query, memory):
                    applicable.append(memory)
        
        return applicable[:k]
    
    def _is_applicable(self, query: str, memory: MemoryItem) -> bool:
        """Check if procedure is applicable to query"""
        
        # Check trigger conditions in metadata
        triggers = memory.metadata.get("triggers", [])
        
        for trigger in triggers:
            if trigger.lower() in query.lower():
                return True
        
        return False

class WorkingMemoryStore:
    """Short-term working memory store"""
    
    def __init__(self, capacity: int, duration_minutes: int):
        self.capacity = capacity
        self.duration = timedelta(minutes=duration_minutes)
        self.memories = deque(maxlen=capacity)
        self.timestamps = {}
    
    async def store(self, memory: MemoryItem) -> bool:
        """Store in working memory"""
        
        self.memories.append(memory)
        self.timestamps[memory.id] = datetime.utcnow()
        
        # Clean expired memories
        self._cleanup_expired()
        
        return True
    
    async def search(self, query: str, agent_id: str, k: int) -> List[MemoryItem]:
        """Search working memory"""
        
        # Return most recent relevant memories
        agent_memories = [m for m in self.memories 
                         if m.agent_id == agent_id and not self._is_expired(m)]
        
        return agent_memories[-k:]  # Most recent k
    
    def _is_expired(self, memory: MemoryItem) -> bool:
        """Check if memory has expired"""
        
        if memory.id not in self.timestamps:
            return True
        
        age = datetime.utcnow() - self.timestamps[memory.id]
        return age > self.duration
    
    def _cleanup_expired(self):
        """Remove expired memories"""
        
        current_memories = list(self.memories)
        self.memories.clear()
        
        for memory in current_memories:
            if not self._is_expired(memory):
                self.memories.append(memory)
            else:
                del self.timestamps[memory.id]

class CollectiveMemoryStore:
    """Shared memory store across all agents"""
    
    def __init__(self, consensus_threshold: float):
        self.consensus_threshold = consensus_threshold
        self.shared_memories = {}
        self.agent_votes = defaultdict(lambda: defaultdict(int))  # memory_id -> agent_id -> vote
    
    async def store(self, memory: MemoryItem) -> bool:
        """Store in collective memory with voting"""
        
        # Add agent's vote for this memory
        self.agent_votes[memory.id][memory.agent_id] = 1
        
        # Check if consensus reached
        unique_agents = len(self.agent_votes[memory.id])
        if unique_agents >= 3:  # Minimum agents for consensus
            total_votes = sum(self.agent_votes[memory.id].values())
            consensus_score = total_votes / unique_agents
            
            if consensus_score >= self.consensus_threshold:
                # Add to shared memories
                memory.metadata["consensus_score"] = consensus_score
                memory.metadata["endorsing_agents"] = list(self.agent_votes[memory.id].keys())
                self.shared_memories[memory.id] = memory
                return True
        
        return False
    
    async def search(self, query: str, agent_id: str, k: int) -> List[MemoryItem]:
        """Search collective memories"""
        
        # Return highest consensus memories
        memories = list(self.shared_memories.values())
        
        # Sort by consensus score
        memories.sort(
            key=lambda m: m.metadata.get("consensus_score", 0),
            reverse=True
        )
        
        return memories[:k]

# Helper Classes

class PatternDetector:
    """Detect patterns in experiences"""
    
    def detect(self, state_before: Dict[str, Any], state_after: Dict[str, Any],
              action: str) -> List[Dict[str, Any]]:
        """Detect patterns in state transitions"""
        
        patterns = []
        
        # Detect state changes
        changes = self._detect_changes(state_before, state_after)
        if changes:
            patterns.append({
                "type": "state_transition",
                "action": action,
                "changes": changes
            })
        
        # Detect repeated actions
        if action in state_before.get("recent_actions", []):
            patterns.append({
                "type": "repeated_action",
                "action": action,
                "frequency": state_before.get("recent_actions", []).count(action)
            })
        
        return patterns
    
    def _detect_changes(self, before: Dict[str, Any], 
                       after: Dict[str, Any]) -> Dict[str, Any]:
        """Detect what changed between states"""
        
        changes = {}
        
        for key in set(before.keys()) | set(after.keys()):
            before_val = before.get(key)
            after_val = after.get(key)
            
            if before_val != after_val:
                changes[key] = {
                    "before": before_val,
                    "after": after_val
                }
        
        return changes

class RewardCalculator:
    """Calculate and track rewards"""
    
    def __init__(self):
        self.agent_rewards = defaultdict(list)
    
    def calculate_improvement(self, reward: float, agent_id: str) -> float:
        """Calculate performance improvement"""
        
        self.agent_rewards[agent_id].append(reward)
        
        if len(self.agent_rewards[agent_id]) < 2:
            return 0.0
        
        # Calculate improvement over moving average
        recent = self.agent_rewards[agent_id][-10:]
        if len(recent) < 2:
            return 0.0
        
        old_avg = sum(recent[:-1]) / len(recent[:-1])
        new_avg = sum(recent) / len(recent)
        
        return new_avg - old_avg

# Example usage

async def main():
    """Example usage of Agent Memory System"""
    
    # Initialize memory system
    memory_system = AgentMemorySystem()
    
    # Create sample memory for an agent
    memory1 = MemoryItem(
        id="mem_001",
        agent_id="product_manager",
        memory_type=MemoryType.EPISODIC,
        content="Successfully analyzed user requirements for authentication system",
        importance=MemoryImportance.HIGH,
        metadata={"task": "requirement_analysis", "project": "auth_system"}
    )
    
    # Store memory
    print("📝 Storing agent memory...")
    await memory_system.store_memory("product_manager", memory1)
    
    # Create learning experience
    experience = LearningExperience(
        experience_id="exp_001",
        agent_id="developer",
        task="implement_authentication",
        action_taken="created_jwt_based_auth",
        outcome="successful_implementation",
        reward=0.95,
        state_before={"code_complete": False, "tests_passing": False},
        state_after={"code_complete": True, "tests_passing": True},
        timestamp=datetime.utcnow()
    )
    
    # Learn from experience
    print("\n🧠 Learning from experience...")
    learning_result = await memory_system.learn_from_experience(experience)
    print(f"  Insights gained: {learning_result['insights_gained']}")
    print(f"  Performance improvement: {learning_result['performance_delta']:.2%}")
    
    # Recall memories
    print("\n🔍 Recalling relevant memories...")
    memories = await memory_system.recall_memory(
        "product_manager",
        "authentication requirements",
        memory_types=[MemoryType.EPISODIC]
    )
    
    for memory in memories:
        print(f"  - {memory.content[:50]}... (importance: {memory.importance.value})")
    
    # Transfer knowledge between agents
    print("\n🔄 Transferring knowledge between agents...")
    transfer_result = await memory_system.transfer_knowledge(
        from_agent="developer",
        to_agent="qa_engineer",
        domain="authentication"
    )
    print(f"  Items transferred: {transfer_result['items_transferred']}")
    print(f"  Success rate: {transfer_result['success_rate']:.1%}")
    
    # Consolidate memories
    print("\n♻️ Consolidating memories...")
    consolidation_result = await memory_system.consolidate_memories("product_manager")
    print(f"  Memories processed: {consolidation_result.get('product_manager', {}).get('memories_processed', 0)}")
    print(f"  Patterns extracted: {consolidation_result.get('product_manager', {}).get('patterns_extracted', 0)}")

if __name__ == "__main__":
    asyncio.run(main())