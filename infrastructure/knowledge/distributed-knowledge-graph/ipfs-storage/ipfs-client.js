const { create } = require('ipfs-http-client');
const { CID } = require('multiformats/cid');
const { sha256 } = require('multiformats/hashes/sha2');
const { base58btc } = require('multiformats/bases/base58');
const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');

/**
 * IPFS Client for Distributed Knowledge Graph Storage
 * 
 * This client manages decentralized storage of large knowledge artifacts,
 * embeddings, and metadata using the InterPlanetary File System.
 * 
 * Features:
 * - Content-addressed storage with cryptographic hashing
 * - Automatic pinning and replication
 * - Chunked uploads for large files
 * - Metadata management and indexing  
 * - Content verification and integrity checking
 */
class IPFSClient {
  constructor(config = {}) {
    this.config = {
      // IPFS node configurations
      nodes: [
        { url: 'http://ipfs-node-01:5001' },
        { url: 'http://ipfs-node-02:5001' },
        { url: 'http://ipfs-node-03:5001' }
      ],
      gateway: 'http://ipfs-gateway:8080',
      
      // Storage settings
      chunkSize: 256 * 1024, // 256KB chunks
      replicationFactor: 3,
      pinningTimeout: 60000,
      
      // Local cache settings
      cacheDir: '/tmp/ipfs-cache',
      maxCacheSize: 10 * 1024 * 1024 * 1024, // 10GB
      
      ...config
    };

    this.clients = [];
    this.primaryClient = null;
    this.contentIndex = new Map(); // Local content index
    this.pinnedContent = new Set();
    
    this.stats = {
      uploads: 0,
      downloads: 0,
      pins: 0,
      cacheHits: 0,
      totalStorage: 0
    };
  }

  /**
   * Initialize IPFS clients and verify connectivity
   */
  async initialize() {
    console.log('Initializing IPFS client...');

    // Create client connections to all IPFS nodes
    for (const nodeConfig of this.config.nodes) {
      try {
        const client = create({ 
          url: nodeConfig.url,
          timeout: 10000
        });
        
        // Test connectivity
        const id = await client.id();
        console.log(`Connected to IPFS node: ${id.id} at ${nodeConfig.url}`);
        
        this.clients.push({
          client,
          url: nodeConfig.url,
          peerId: id.id,
          healthy: true
        });
        
        // Set first healthy client as primary
        if (!this.primaryClient) {
          this.primaryClient = client;
        }
      } catch (error) {
        console.error(`Failed to connect to IPFS node ${nodeConfig.url}:`, error.message);
      }
    }

    if (this.clients.length === 0) {
      throw new Error('Failed to connect to any IPFS nodes');
    }

    // Create cache directory
    try {
      await fs.mkdir(this.config.cacheDir, { recursive: true });
    } catch (error) {
      console.warn('Failed to create cache directory:', error.message);
    }

    // Start background tasks
    this.startBackgroundTasks();

    console.log(`IPFS client initialized with ${this.clients.length} nodes`);
  }

  /**
   * Store knowledge artifact on IPFS with metadata
   */
  async storeKnowledgeArtifact(data, metadata = {}) {
    const startTime = Date.now();
    
    try {
      // Prepare artifact with metadata
      const artifact = {
        content: data,
        metadata: {
          ...metadata,
          timestamp: new Date().toISOString(),
          nodeId: metadata.nodeId || this.generateNodeId(),
          version: metadata.version || '1.0.0',
          contentType: metadata.contentType || 'application/json'
        },
        checksum: this.calculateChecksum(data)
      };

      const artifactBuffer = Buffer.from(JSON.stringify(artifact));
      
      // Upload to IPFS
      const uploadResult = await this.uploadWithReplication(artifactBuffer);
      
      // Pin content for persistence
      await this.pinContent(uploadResult.cid);
      
      // Update local index
      this.updateContentIndex(uploadResult.cid, artifact.metadata);
      
      // Update statistics
      this.stats.uploads++;
      this.stats.totalStorage += artifactBuffer.length;
      
      const executionTime = Date.now() - startTime;
      console.log(`Stored knowledge artifact ${uploadResult.cid} in ${executionTime}ms`);
      
      return {
        cid: uploadResult.cid,
        size: artifactBuffer.length,
        metadata: artifact.metadata,
        replicationNodes: uploadResult.replicationNodes,
        executionTime
      };
    } catch (error) {
      console.error('Failed to store knowledge artifact:', error);
      throw error;
    }
  }

  /**
   * Retrieve knowledge artifact by CID
   */
  async retrieveKnowledgeArtifact(cid, options = {}) {
    const startTime = Date.now();
    
    try {
      // Check local cache first
      const cached = await this.getCachedContent(cid);
      if (cached) {
        this.stats.cacheHits++;
        return {
          ...cached,
          fromCache: true,
          executionTime: Date.now() - startTime
        };
      }

      // Retrieve from IPFS network
      const content = await this.downloadContent(cid);
      
      // Parse and validate artifact
      const artifact = JSON.parse(content.toString());
      
      // Verify checksum
      if (!this.verifyChecksum(artifact.content, artifact.checksum)) {
        throw new Error('Content integrity check failed');
      }
      
      // Cache the content locally
      await this.cacheContent(cid, artifact);
      
      this.stats.downloads++;
      const executionTime = Date.now() - startTime;
      
      console.log(`Retrieved knowledge artifact ${cid} in ${executionTime}ms`);
      
      return {
        content: artifact.content,
        metadata: artifact.metadata,
        fromCache: false,
        executionTime
      };
    } catch (error) {
      console.error(`Failed to retrieve knowledge artifact ${cid}:`, error);
      throw error;
    }
  }

  /**
   * Store large embedding vectors efficiently
   */
  async storeEmbeddings(embeddings, metadata = {}) {
    const chunkSize = 1000; // Embeddings per chunk
    const chunks = [];
    
    // Split embeddings into chunks
    for (let i = 0; i < embeddings.length; i += chunkSize) {
      const chunk = embeddings.slice(i, i + chunkSize);
      const chunkData = {
        vectors: chunk,
        chunkIndex: Math.floor(i / chunkSize),
        totalChunks: Math.ceil(embeddings.length / chunkSize),
        metadata: {
          ...metadata,
          chunkStart: i,
          chunkEnd: Math.min(i + chunkSize, embeddings.length)
        }
      };
      
      const result = await this.storeKnowledgeArtifact(chunkData, {
        ...metadata,
        contentType: 'application/x-embeddings',
        isChunk: true
      });
      
      chunks.push(result.cid);
    }
    
    // Store chunk index
    const indexData = {
      chunks,
      totalVectors: embeddings.length,
      chunkSize,
      metadata
    };
    
    const indexResult = await this.storeKnowledgeArtifact(indexData, {
      ...metadata,
      contentType: 'application/x-embedding-index',
      isIndex: true
    });
    
    return {
      indexCid: indexResult.cid,
      chunks,
      totalVectors: embeddings.length,
      chunkCount: chunks.length
    };
  }

  /**
   * Retrieve embeddings by index CID
   */
  async retrieveEmbeddings(indexCid) {
    const index = await this.retrieveKnowledgeArtifact(indexCid);
    const embeddings = [];
    
    // Retrieve all chunks in parallel
    const chunkPromises = index.content.chunks.map(chunkCid => 
      this.retrieveKnowledgeArtifact(chunkCid)
    );
    
    const chunks = await Promise.all(chunkPromises);
    
    // Reassemble embeddings
    chunks
      .sort((a, b) => a.metadata.chunkStart - b.metadata.chunkStart)
      .forEach(chunk => {
        embeddings.push(...chunk.content.vectors);
      });
    
    return {
      embeddings,
      metadata: index.metadata,
      totalVectors: embeddings.length,
      retrievedChunks: chunks.length
    };
  }

  /**
   * Upload content with automatic replication
   */
  async uploadWithReplication(buffer) {
    const replicationPromises = [];
    const replicationNodes = [];
    
    // Upload to multiple nodes for redundancy
    for (let i = 0; i < Math.min(this.clients.length, this.config.replicationFactor); i++) {
      const clientInfo = this.clients[i];
      if (clientInfo.healthy) {
        replicationPromises.push(
          this.uploadToNode(buffer, clientInfo)
            .then(result => {
              replicationNodes.push(clientInfo.peerId);
              return result;
            })
            .catch(error => {
              console.error(`Upload failed to node ${clientInfo.peerId}:`, error.message);
              clientInfo.healthy = false;
              return null;
            })
        );
      }
    }
    
    const results = await Promise.allSettled(replicationPromises);
    const successfulResults = results
      .filter(r => r.status === 'fulfilled' && r.value)
      .map(r => r.value);
    
    if (successfulResults.length === 0) {
      throw new Error('Failed to upload to any IPFS nodes');
    }
    
    return {
      cid: successfulResults[0].path, // All should have the same CID
      replicationNodes,
      successfulReplications: successfulResults.length
    };
  }

  /**
   * Upload to a specific IPFS node
   */
  async uploadToNode(buffer, clientInfo) {
    const { client } = clientInfo;
    
    const result = await client.add(buffer, {
      pin: false, // We'll pin separately
      cidVersion: 1,
      hashAlg: 'sha2-256'
    });
    
    return result;
  }

  /**
   * Download content from IPFS network
   */
  async downloadContent(cid) {
    let lastError;
    
    // Try each healthy client
    for (const clientInfo of this.clients) {
      if (clientInfo.healthy) {
        try {
          const chunks = [];
          for await (const chunk of clientInfo.client.cat(cid, { timeout: 30000 })) {
            chunks.push(chunk);
          }
          return Buffer.concat(chunks);
        } catch (error) {
          lastError = error;
          console.warn(`Download failed from node ${clientInfo.peerId}:`, error.message);
        }
      }
    }
    
    throw lastError || new Error('All IPFS nodes are unhealthy');
  }

  /**
   * Pin content for persistence
   */
  async pinContent(cid) {
    const pinPromises = this.clients
      .filter(c => c.healthy)
      .slice(0, this.config.replicationFactor)
      .map(async (clientInfo) => {
        try {
          await clientInfo.client.pin.add(cid, { timeout: this.config.pinningTimeout });
          return { node: clientInfo.peerId, success: true };
        } catch (error) {
          console.error(`Pin failed on node ${clientInfo.peerId}:`, error.message);
          return { node: clientInfo.peerId, success: false, error: error.message };
        }
      });
    
    const pinResults = await Promise.all(pinPromises);
    const successfulPins = pinResults.filter(r => r.success);
    
    if (successfulPins.length > 0) {
      this.pinnedContent.add(cid);
      this.stats.pins++;
    }
    
    console.log(`Pinned ${cid} to ${successfulPins.length} nodes`);
    return pinResults;
  }

  /**
   * Unpin content
   */
  async unpinContent(cid) {
    const unpinPromises = this.clients
      .filter(c => c.healthy)
      .map(async (clientInfo) => {
        try {
          await clientInfo.client.pin.rm(cid);
          return { node: clientInfo.peerId, success: true };
        } catch (error) {
          return { node: clientInfo.peerId, success: false, error: error.message };
        }
      });
    
    const unpinResults = await Promise.all(unpinPromises);
    this.pinnedContent.delete(cid);
    
    return unpinResults;
  }

  /**
   * Search content by metadata
   */
  async searchContent(query) {
    const results = [];
    
    for (const [cid, metadata] of this.contentIndex.entries()) {
      if (this.matchesQuery(metadata, query)) {
        results.push({
          cid,
          metadata,
          score: this.calculateRelevanceScore(metadata, query)
        });
      }
    }
    
    // Sort by relevance score
    results.sort((a, b) => b.score - a.score);
    
    return results;
  }

  /**
   * Get cached content
   */
  async getCachedContent(cid) {
    try {
      const cacheFile = path.join(this.config.cacheDir, `${cid}.json`);
      const content = await fs.readFile(cacheFile, 'utf8');
      return JSON.parse(content);
    } catch (error) {
      return null; // Cache miss
    }
  }

  /**
   * Cache content locally
   */
  async cacheContent(cid, content) {
    try {
      const cacheFile = path.join(this.config.cacheDir, `${cid}.json`);
      await fs.writeFile(cacheFile, JSON.stringify(content));
    } catch (error) {
      console.warn('Failed to cache content:', error.message);
    }
  }

  /**
   * Update content index
   */
  updateContentIndex(cid, metadata) {
    this.contentIndex.set(cid, metadata);
  }

  /**
   * Calculate content checksum
   */
  calculateChecksum(content) {
    return crypto.createHash('sha256')
      .update(typeof content === 'string' ? content : JSON.stringify(content))
      .digest('hex');
  }

  /**
   * Verify content checksum
   */
  verifyChecksum(content, expectedChecksum) {
    const actualChecksum = this.calculateChecksum(content);
    return actualChecksum === expectedChecksum;
  }

  /**
   * Generate unique node ID
   */
  generateNodeId() {
    return crypto.randomBytes(16).toString('hex');
  }

  /**
   * Check if metadata matches query
   */
  matchesQuery(metadata, query) {
    if (!query || typeof query !== 'object') return false;
    
    for (const [key, value] of Object.entries(query)) {
      if (metadata[key] !== value) {
        return false;
      }
    }
    
    return true;
  }

  /**
   * Calculate relevance score for search results
   */
  calculateRelevanceScore(metadata, query) {
    let score = 0;
    
    for (const [key, value] of Object.entries(query)) {
      if (metadata[key] === value) {
        score += 1;
      }
    }
    
    // Add recency bonus
    if (metadata.timestamp) {
      const age = Date.now() - new Date(metadata.timestamp).getTime();
      const daysSinceCreation = age / (1000 * 60 * 60 * 24);
      score += Math.max(0, 1 - daysSinceCreation / 365); // Decay over a year
    }
    
    return score;
  }

  /**
   * Start background maintenance tasks
   */
  startBackgroundTasks() {
    // Health check interval
    setInterval(() => {
      this.performHealthChecks();
    }, 60000); // Every minute
    
    // Garbage collection
    setInterval(() => {
      this.performGarbageCollection();
    }, 300000); // Every 5 minutes
    
    // Statistics logging
    setInterval(() => {
      console.log('IPFS Client Statistics:', this.stats);
    }, 600000); // Every 10 minutes
  }

  /**
   * Perform health checks on all nodes
   */
  async performHealthChecks() {
    for (const clientInfo of this.clients) {
      try {
        await clientInfo.client.id();
        clientInfo.healthy = true;
      } catch (error) {
        clientInfo.healthy = false;
        console.warn(`Node ${clientInfo.peerId} is unhealthy:`, error.message);
      }
    }
  }

  /**
   * Perform garbage collection on cache
   */
  async performGarbageCollection() {
    try {
      const files = await fs.readdir(this.config.cacheDir);
      let totalSize = 0;
      const fileStats = [];
      
      for (const file of files) {
        const filePath = path.join(this.config.cacheDir, file);
        const stats = await fs.stat(filePath);
        totalSize += stats.size;
        fileStats.push({
          path: filePath,
          size: stats.size,
          mtime: stats.mtime
        });
      }
      
      // Clean up if cache is too large
      if (totalSize > this.config.maxCacheSize) {
        fileStats.sort((a, b) => a.mtime - b.mtime); // Oldest first
        
        let deletedSize = 0;
        for (const file of fileStats) {
          if (totalSize - deletedSize <= this.config.maxCacheSize * 0.8) break;
          
          await fs.unlink(file.path);
          deletedSize += file.size;
        }
        
        console.log(`Garbage collected ${deletedSize} bytes from IPFS cache`);
      }
    } catch (error) {
      console.warn('Garbage collection failed:', error.message);
    }
  }

  /**
   * Get client statistics and health
   */
  async getStats() {
    const healthyNodes = this.clients.filter(c => c.healthy).length;
    
    return {
      ...this.stats,
      nodes: {
        total: this.clients.length,
        healthy: healthyNodes,
        unhealthy: this.clients.length - healthyNodes
      },
      pinnedContent: this.pinnedContent.size,
      indexedContent: this.contentIndex.size
    };
  }

  /**
   * Health check for external monitoring
   */
  async healthCheck() {
    const healthyNodes = this.clients.filter(c => c.healthy).length;
    
    return {
      status: healthyNodes > 0 ? 'healthy' : 'unhealthy',
      nodes: {
        healthy: healthyNodes,
        total: this.clients.length
      },
      primaryNode: this.primaryClient ? 'connected' : 'disconnected',
      lastCheck: new Date().toISOString()
    };
  }

  /**
   * Close all connections and cleanup
   */
  async close() {
    console.log('Closing IPFS client...');
    
    // No explicit close needed for IPFS HTTP clients
    this.clients.length = 0;
    this.primaryClient = null;
    this.contentIndex.clear();
    this.pinnedContent.clear();
    
    console.log('IPFS client closed');
  }
}

module.exports = IPFSClient;