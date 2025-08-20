const Redis = require('ioredis');
const { EventEmitter } = require('events');

/**
 * Redis Cache Manager for Distributed Knowledge Graph
 * 
 * This manager provides high-performance distributed caching for:
 * - Knowledge graph query results
 * - Vector embeddings and similarity results
 * - Agent session data and working memory
 * - Consensus voting state
 * - Real-time synchronization events
 * 
 * Features:
 * - Automatic failover and clustering
 * - Intelligent cache warming and eviction
 * - Query result caching with TTL
 * - Real-time cache invalidation
 * - Performance monitoring and analytics
 */
class RedisCacheManager extends EventEmitter {
  constructor(config = {}) {
    super();
    
    this.config = {
      // Cluster configuration
      cluster: [
        { host: 'redis-cluster-01', port: 6379 },
        { host: 'redis-cluster-02', port: 6379 },
        { host: 'redis-cluster-03', port: 6379 },
        { host: 'redis-cluster-04', port: 6379 },
        { host: 'redis-cluster-05', port: 6379 },
        { host: 'redis-cluster-06', port: 6379 }
      ],
      
      // Connection options
      redisOptions: {
        password: process.env.REDIS_PASSWORD,
        retryDelayOnFailover: 100,
        enableReadyCheck: true,
        maxRetriesPerRequest: 3,
        lazyConnect: true,
        keepAlive: 30000
      },
      
      // Cache policies
      defaultTTL: 300, // 5 minutes
      queryResultTTL: 60, // 1 minute for query results
      embeddingTTL: 3600, // 1 hour for embeddings
      sessionTTL: 1800, // 30 minutes for sessions
      consensusTTL: 120, // 2 minutes for consensus state
      
      // Performance settings
      maxMemoryPolicy: 'allkeys-lru',
      compressionThreshold: 1024, // Compress values > 1KB
      batchSize: 100,
      pipelineTimeout: 1000,
      
      ...config
    };

    this.redis = null;
    this.subscriber = null;
    this.publisher = null;
    
    // Cache statistics
    this.stats = {
      hits: 0,
      misses: 0,
      sets: 0,
      deletes: 0,
      evictions: 0,
      compressions: 0,
      errors: 0,
      totalMemory: 0,
      keyCount: 0
    };
    
    // Performance metrics
    this.metrics = {
      averageLatency: 0,
      peakLatency: 0,
      throughput: 0,
      errorRate: 0
    };
    
    // Key prefixes for different data types
    this.prefixes = {
      query: 'kg:query:',
      node: 'kg:node:',
      relationship: 'kg:rel:',
      embedding: 'kg:emb:',
      similarity: 'kg:sim:',
      session: 'kg:session:',
      consensus: 'kg:consensus:',
      sync: 'kg:sync:',
      agent: 'kg:agent:',
      metadata: 'kg:meta:'
    };
    
    this.invalidationPatterns = new Map();
    this.warmupQueues = new Set();
  }

  /**
   * Initialize Redis cluster connection
   */
  async initialize() {
    console.log('Initializing Redis Cache Manager...');

    try {
      // Create main cluster connection
      this.redis = new Redis.Cluster(this.config.cluster, {
        redisOptions: this.config.redisOptions,
        enableOfflineQueue: false,
        retryDelayOnFailover: 100,
        maxRetriesPerRequest: 3
      });

      // Create subscriber for cache invalidation
      this.subscriber = new Redis.Cluster(this.config.cluster, {
        redisOptions: this.config.redisOptions,
        enableOfflineQueue: false
      });

      // Create publisher for cache events
      this.publisher = new Redis.Cluster(this.config.cluster, {
        redisOptions: this.config.redisOptions,
        enableOfflineQueue: false
      });

      // Event handlers
      this.redis.on('connect', () => {
        console.log('Connected to Redis cluster');
        this.emit('connected');
      });

      this.redis.on('ready', () => {
        console.log('Redis cluster is ready');
        this.emit('ready');
        this.startBackgroundTasks();
      });

      this.redis.on('error', (error) => {
        console.error('Redis cluster error:', error);
        this.stats.errors++;
        this.emit('error', error);
      });

      this.redis.on('node error', (error, node) => {
        console.error(`Redis node error (${node.options.host}:${node.options.port}):`, error);
      });

      // Set up cache invalidation subscription
      await this.setupCacheInvalidation();
      
      // Connect to cluster
      await this.redis.connect();
      await this.subscriber.connect();
      await this.publisher.connect();
      
      console.log('Redis Cache Manager initialized successfully');

    } catch (error) {
      console.error('Failed to initialize Redis Cache Manager:', error);
      throw error;
    }
  }

  /**
   * Cache a knowledge graph query result
   */
  async cacheQueryResult(queryHash, result, ttl = this.config.queryResultTTL) {
    const startTime = Date.now();
    
    try {
      const key = `${this.prefixes.query}${queryHash}`;
      const serializedResult = this.serialize(result);
      
      await this.redis.setex(key, ttl, serializedResult);
      
      // Add to invalidation tracking
      this.trackInvalidationPattern(key, result.shardsQueried || []);
      
      this.stats.sets++;
      this.updateLatencyMetrics(Date.now() - startTime);
      
      console.log(`Cached query result: ${queryHash} (TTL: ${ttl}s)`);
      return true;
    } catch (error) {
      console.error('Failed to cache query result:', error);
      this.stats.errors++;
      return false;
    }
  }

  /**
   * Retrieve cached query result
   */
  async getCachedQueryResult(queryHash) {
    const startTime = Date.now();
    
    try {
      const key = `${this.prefixes.query}${queryHash}`;
      const cachedResult = await this.redis.get(key);
      
      this.updateLatencyMetrics(Date.now() - startTime);
      
      if (cachedResult) {
        this.stats.hits++;
        const result = this.deserialize(cachedResult);
        console.log(`Cache hit for query: ${queryHash}`);
        return result;
      } else {
        this.stats.misses++;
        console.log(`Cache miss for query: ${queryHash}`);
        return null;
      }
    } catch (error) {
      console.error('Failed to get cached query result:', error);
      this.stats.errors++;
      this.stats.misses++;
      return null;
    }
  }

  /**
   * Cache a knowledge node
   */
  async cacheNode(nodeId, nodeData, ttl = this.config.defaultTTL) {
    const startTime = Date.now();
    
    try {
      const key = `${this.prefixes.node}${nodeId}`;
      const serializedData = this.serialize(nodeData);
      
      await this.redis.setex(key, ttl, serializedData);
      
      this.stats.sets++;
      this.updateLatencyMetrics(Date.now() - startTime);
      
      return true;
    } catch (error) {
      console.error('Failed to cache node:', error);
      this.stats.errors++;
      return false;
    }
  }

  /**
   * Get cached knowledge node
   */
  async getCachedNode(nodeId) {
    const startTime = Date.now();
    
    try {
      const key = `${this.prefixes.node}${nodeId}`;
      const cachedData = await this.redis.get(key);
      
      this.updateLatencyMetrics(Date.now() - startTime);
      
      if (cachedData) {
        this.stats.hits++;
        return this.deserialize(cachedData);
      } else {
        this.stats.misses++;
        return null;
      }
    } catch (error) {
      console.error('Failed to get cached node:', error);
      this.stats.errors++;
      this.stats.misses++;
      return null;
    }
  }

  /**
   * Cache embeddings for a node
   */
  async cacheEmbeddings(nodeId, embeddings, ttl = this.config.embeddingTTL) {
    const startTime = Date.now();
    
    try {
      const key = `${this.prefixes.embedding}${nodeId}`;
      const serializedEmbeddings = this.serialize(embeddings);
      
      await this.redis.setex(key, ttl, serializedEmbeddings);
      
      this.stats.sets++;
      this.updateLatencyMetrics(Date.now() - startTime);
      
      return true;
    } catch (error) {
      console.error('Failed to cache embeddings:', error);
      this.stats.errors++;
      return false;
    }
  }

  /**
   * Get cached embeddings
   */
  async getCachedEmbeddings(nodeId) {
    const startTime = Date.now();
    
    try {
      const key = `${this.prefixes.embedding}${nodeId}`;
      const cachedData = await this.redis.get(key);
      
      this.updateLatencyMetrics(Date.now() - startTime);
      
      if (cachedData) {
        this.stats.hits++;
        return this.deserialize(cachedData);
      } else {
        this.stats.misses++;
        return null;
      }
    } catch (error) {
      console.error('Failed to get cached embeddings:', error);
      this.stats.errors++;
      this.stats.misses++;
      return null;
    }
  }

  /**
   * Cache similarity search results
   */
  async cacheSimilarityResults(embeddingHash, results, ttl = this.config.queryResultTTL) {
    const startTime = Date.now();
    
    try {
      const key = `${this.prefixes.similarity}${embeddingHash}`;
      const serializedResults = this.serialize(results);
      
      await this.redis.setex(key, ttl, serializedResults);
      
      this.stats.sets++;
      this.updateLatencyMetrics(Date.now() - startTime);
      
      return true;
    } catch (error) {
      console.error('Failed to cache similarity results:', error);
      this.stats.errors++;
      return false;
    }
  }

  /**
   * Get cached similarity results
   */
  async getCachedSimilarityResults(embeddingHash) {
    const startTime = Date.now();
    
    try {
      const key = `${this.prefixes.similarity}${embeddingHash}`;
      const cachedData = await this.redis.get(key);
      
      this.updateLatencyMetrics(Date.now() - startTime);
      
      if (cachedData) {
        this.stats.hits++;
        return this.deserialize(cachedData);
      } else {
        this.stats.misses++;
        return null;
      }
    } catch (error) {
      console.error('Failed to get cached similarity results:', error);
      this.stats.errors++;
      this.stats.misses++;
      return null;
    }
  }

  /**
   * Cache agent session data
   */
  async cacheAgentSession(agentId, sessionId, sessionData, ttl = this.config.sessionTTL) {
    const startTime = Date.now();
    
    try {
      const key = `${this.prefixes.session}${agentId}:${sessionId}`;
      const serializedData = this.serialize(sessionData);
      
      await this.redis.setex(key, ttl, serializedData);
      
      this.stats.sets++;
      this.updateLatencyMetrics(Date.now() - startTime);
      
      return true;
    } catch (error) {
      console.error('Failed to cache agent session:', error);
      this.stats.errors++;
      return false;
    }
  }

  /**
   * Get cached agent session
   */
  async getCachedAgentSession(agentId, sessionId) {
    const startTime = Date.now();
    
    try {
      const key = `${this.prefixes.session}${agentId}:${sessionId}`;
      const cachedData = await this.redis.get(key);
      
      this.updateLatencyMetrics(Date.now() - startTime);
      
      if (cachedData) {
        this.stats.hits++;
        return this.deserialize(cachedData);
      } else {
        this.stats.misses++;
        return null;
      }
    } catch (error) {
      console.error('Failed to get cached agent session:', error);
      this.stats.errors++;
      this.stats.misses++;
      return null;
    }
  }

  /**
   * Cache consensus state
   */
  async cacheConsensusState(proposalId, consensusData, ttl = this.config.consensusTTL) {
    const startTime = Date.now();
    
    try {
      const key = `${this.prefixes.consensus}${proposalId}`;
      const serializedData = this.serialize(consensusData);
      
      await this.redis.setex(key, ttl, serializedData);
      
      this.stats.sets++;
      this.updateLatencyMetrics(Date.now() - startTime);
      
      return true;
    } catch (error) {
      console.error('Failed to cache consensus state:', error);
      this.stats.errors++;
      return false;
    }
  }

  /**
   * Batch cache operations for better performance
   */
  async batchSet(operations) {
    const startTime = Date.now();
    
    try {
      const pipeline = this.redis.pipeline();
      
      for (const op of operations) {
        const { key, value, ttl = this.config.defaultTTL } = op;
        const serializedValue = this.serialize(value);
        pipeline.setex(key, ttl, serializedValue);
      }
      
      const results = await pipeline.exec();
      
      this.stats.sets += operations.length;
      this.updateLatencyMetrics(Date.now() - startTime);
      
      const errors = results.filter(result => result[0] !== null);
      if (errors.length > 0) {
        console.error('Batch set errors:', errors);
        this.stats.errors += errors.length;
      }
      
      return results.length - errors.length; // Number of successful operations
    } catch (error) {
      console.error('Batch set operation failed:', error);
      this.stats.errors++;
      return 0;
    }
  }

  /**
   * Batch get operations
   */
  async batchGet(keys) {
    const startTime = Date.now();
    
    try {
      const pipeline = this.redis.pipeline();
      
      for (const key of keys) {
        pipeline.get(key);
      }
      
      const results = await pipeline.exec();
      
      this.updateLatencyMetrics(Date.now() - startTime);
      
      const values = results.map(result => {
        if (result[0] === null && result[1] !== null) {
          this.stats.hits++;
          return this.deserialize(result[1]);
        } else {
          this.stats.misses++;
          return null;
        }
      });
      
      return values;
    } catch (error) {
      console.error('Batch get operation failed:', error);
      this.stats.errors++;
      this.stats.misses += keys.length;
      return new Array(keys.length).fill(null);
    }
  }

  /**
   * Invalidate cache entries by pattern
   */
  async invalidateByPattern(pattern) {
    try {
      const keys = await this.redis.keys(pattern);
      
      if (keys.length > 0) {
        const pipeline = this.redis.pipeline();
        
        for (const key of keys) {
          pipeline.del(key);
        }
        
        await pipeline.exec();
        this.stats.deletes += keys.length;
        
        // Notify other instances
        await this.publisher.publish('cache:invalidation', JSON.stringify({
          pattern,
          keys,
          timestamp: Date.now()
        }));
        
        console.log(`Invalidated ${keys.length} keys matching pattern: ${pattern}`);
      }
      
      return keys.length;
    } catch (error) {
      console.error('Failed to invalidate cache by pattern:', error);
      this.stats.errors++;
      return 0;
    }
  }

  /**
   * Invalidate specific cache key
   */
  async invalidate(key) {
    try {
      const deleted = await this.redis.del(key);
      
      if (deleted > 0) {
        this.stats.deletes += deleted;
        
        // Notify other instances
        await this.publisher.publish('cache:invalidation', JSON.stringify({
          keys: [key],
          timestamp: Date.now()
        }));
        
        console.log(`Invalidated cache key: ${key}`);
      }
      
      return deleted > 0;
    } catch (error) {
      console.error('Failed to invalidate cache key:', error);
      this.stats.errors++;
      return false;
    }
  }

  /**
   * Warm up cache with frequently accessed data
   */
  async warmupCache(warmupData) {
    console.log('Starting cache warmup...');
    
    const batchOperations = [];
    
    for (const item of warmupData) {
      batchOperations.push({
        key: item.key,
        value: item.value,
        ttl: item.ttl || this.config.defaultTTL
      });
      
      if (batchOperations.length >= this.config.batchSize) {
        await this.batchSet(batchOperations);
        batchOperations.length = 0;
      }
    }
    
    if (batchOperations.length > 0) {
      await this.batchSet(batchOperations);
    }
    
    console.log(`Cache warmup completed for ${warmupData.length} items`);
  }

  /**
   * Setup cache invalidation subscription
   */
  async setupCacheInvalidation() {
    await this.subscriber.subscribe('cache:invalidation');
    
    this.subscriber.on('message', (channel, message) => {
      if (channel === 'cache:invalidation') {
        try {
          const invalidationData = JSON.parse(message);
          console.log('Received cache invalidation:', invalidationData);
          this.emit('invalidation', invalidationData);
        } catch (error) {
          console.error('Failed to parse invalidation message:', error);
        }
      }
    });
  }

  /**
   * Track patterns for intelligent cache invalidation
   */
  trackInvalidationPattern(key, affectedShards) {
    for (const shard of affectedShards) {
      if (!this.invalidationPatterns.has(shard)) {
        this.invalidationPatterns.set(shard, new Set());
      }
      this.invalidationPatterns.get(shard).add(key);
    }
  }

  /**
   * Serialize data for caching
   */
  serialize(data) {
    try {
      const serialized = JSON.stringify(data);
      
      // Compress if data is large
      if (serialized.length > this.config.compressionThreshold) {
        this.stats.compressions++;
        // Note: In production, you might want to use actual compression library
        return `compressed:${serialized}`;
      }
      
      return serialized;
    } catch (error) {
      console.error('Failed to serialize data:', error);
      throw error;
    }
  }

  /**
   * Deserialize cached data
   */
  deserialize(data) {
    try {
      if (data.startsWith('compressed:')) {
        // Decompress data
        return JSON.parse(data.substring(11));
      }
      
      return JSON.parse(data);
    } catch (error) {
      console.error('Failed to deserialize data:', error);
      throw error;
    }
  }

  /**
   * Update latency metrics
   */
  updateLatencyMetrics(latency) {
    this.metrics.averageLatency = (this.metrics.averageLatency * 0.9) + (latency * 0.1);
    this.metrics.peakLatency = Math.max(this.metrics.peakLatency, latency);
  }

  /**
   * Start background maintenance tasks
   */
  startBackgroundTasks() {
    // Statistics collection
    setInterval(() => {
      this.collectStatistics();
    }, 30000); // Every 30 seconds
    
    // Memory monitoring
    setInterval(() => {
      this.monitorMemoryUsage();
    }, 60000); // Every minute
    
    // Performance metrics
    setInterval(() => {
      this.calculatePerformanceMetrics();
    }, 10000); // Every 10 seconds
  }

  /**
   * Collect cache statistics
   */
  async collectStatistics() {
    try {
      const info = await this.redis.info('memory');
      const keyspaceInfo = await this.redis.info('keyspace');
      
      // Parse memory info
      const memoryMatch = info.match(/used_memory:(\d+)/);
      if (memoryMatch) {
        this.stats.totalMemory = parseInt(memoryMatch[1]);
      }
      
      // Parse keyspace info to get key count
      const keyspaceMatch = keyspaceInfo.match(/keys=(\d+)/);
      if (keyspaceMatch) {
        this.stats.keyCount = parseInt(keyspaceMatch[1]);
      }
      
      this.emit('statistics', this.stats);
    } catch (error) {
      console.error('Failed to collect statistics:', error);
    }
  }

  /**
   * Monitor memory usage and trigger eviction if needed
   */
  async monitorMemoryUsage() {
    try {
      const info = await this.redis.info('memory');
      const memoryMatch = info.match(/used_memory:(\d+)/);
      const maxMemoryMatch = info.match(/maxmemory:(\d+)/);
      
      if (memoryMatch && maxMemoryMatch) {
        const usedMemory = parseInt(memoryMatch[1]);
        const maxMemory = parseInt(maxMemoryMatch[1]);
        const memoryRatio = usedMemory / maxMemory;
        
        if (memoryRatio > 0.9) {
          console.warn(`High memory usage: ${(memoryRatio * 100).toFixed(1)}%`);
          this.emit('highMemoryUsage', { usedMemory, maxMemory, ratio: memoryRatio });
        }
      }
    } catch (error) {
      console.error('Failed to monitor memory usage:', error);
    }
  }

  /**
   * Calculate performance metrics
   */
  calculatePerformanceMetrics() {
    const totalOperations = this.stats.hits + this.stats.misses + this.stats.sets;
    
    if (totalOperations > 0) {
      this.metrics.throughput = totalOperations / 10; // Operations per second over last 10 seconds
      this.metrics.errorRate = this.stats.errors / totalOperations;
    }
    
    // Reset counters for next interval
    this.stats.hits = 0;
    this.stats.misses = 0;
    this.stats.sets = 0;
    this.stats.deletes = 0;
    this.stats.errors = 0;
  }

  /**
   * Get comprehensive cache statistics
   */
  getStats() {
    const hitRate = this.stats.hits + this.stats.misses > 0 
      ? (this.stats.hits / (this.stats.hits + this.stats.misses)) * 100 
      : 0;
    
    return {
      ...this.stats,
      hitRate: hitRate.toFixed(2) + '%',
      metrics: this.metrics,
      memoryUsageMB: (this.stats.totalMemory / (1024 * 1024)).toFixed(2)
    };
  }

  /**
   * Health check
   */
  async healthCheck() {
    try {
      const pong = await this.redis.ping();
      const info = await this.redis.info('server');
      
      return {
        status: pong === 'PONG' ? 'healthy' : 'unhealthy',
        clusterStatus: 'connected',
        uptime: info.match(/uptime_in_seconds:(\d+)/)?.[1] || 'unknown',
        connectedClients: info.match(/connected_clients:(\d+)/)?.[1] || 'unknown',
        lastCheck: new Date().toISOString()
      };
    } catch (error) {
      return {
        status: 'unhealthy',
        error: error.message,
        lastCheck: new Date().toISOString()
      };
    }
  }

  /**
   * Close all connections
   */
  async close() {
    console.log('Closing Redis Cache Manager...');
    
    if (this.redis) {
      await this.redis.disconnect();
    }
    
    if (this.subscriber) {
      await this.subscriber.disconnect();
    }
    
    if (this.publisher) {
      await this.publisher.disconnect();
    }
    
    console.log('Redis Cache Manager closed');
  }
}

module.exports = RedisCacheManager;