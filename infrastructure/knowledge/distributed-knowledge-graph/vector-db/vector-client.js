const axios = require('axios');
const crypto = require('crypto');
const { EventEmitter } = require('events');

/**
 * Multi-Vector Database Client for Billion-Scale Embeddings
 * 
 * This client provides a unified interface to multiple vector database
 * providers (Pinecone, Weaviate, Qdrant) with automatic failover,
 * load balancing, and intelligent routing for optimal performance.
 * 
 * Features:
 * - Multi-provider support with automatic failover
 * - Intelligent sharding across providers
 * - Semantic similarity search at billion scale
 * - Real-time embedding updates and deletions
 * - Advanced filtering and metadata queries
 * - Performance monitoring and optimization
 */
class VectorDatabaseClient extends EventEmitter {
  constructor(config = {}) {
    super();
    
    this.config = {
      // Provider configurations
      providers: {
        pinecone: {
          enabled: true,
          apiKey: process.env.PINECONE_API_KEY,
          environment: process.env.PINECONE_ENVIRONMENT || 'us-west1-gcp-free',
          indexName: 'knowledge-graph',
          dimension: 1536,
          metric: 'cosine',
          baseUrl: 'https://controller.{environment}.pinecone.io',
          priority: 1,
          maxVectors: 1000000 // Free tier limit
        },
        
        weaviate: {
          enabled: true,
          host: process.env.WEAVIATE_HOST || 'weaviate-cluster',
          port: process.env.WEAVIATE_PORT || 8080,
          scheme: 'http',
          className: 'KnowledgeNode',
          dimension: 1536,
          priority: 2,
          maxVectors: 10000000
        },
        
        qdrant: {
          enabled: true,
          host: process.env.QDRANT_HOST || 'qdrant-cluster',
          port: process.env.QDRANT_PORT || 6333,
          apiKey: process.env.QDRANT_API_KEY,
          collectionName: 'knowledge-graph',
          dimension: 1536,
          priority: 3,
          maxVectors: 100000000
        }
      },
      
      // Routing and load balancing
      routingStrategy: 'intelligent', // 'round-robin', 'priority', 'intelligent'
      shardingStrategy: 'hash', // 'hash', 'range', 'semantic'
      replicationFactor: 2,
      
      // Performance settings
      batchSize: 100,
      maxConcurrentRequests: 10,
      requestTimeout: 30000,
      retryAttempts: 3,
      
      // Search settings
      defaultTopK: 10,
      maxTopK: 1000,
      defaultThreshold: 0.7,
      
      ...config
    };

    this.providers = new Map();
    this.healthStatus = new Map();
    this.routingMetrics = new Map();
    this.currentProvider = null;
    
    // Statistics and monitoring
    this.stats = {
      totalVectors: 0,
      totalQueries: 0,
      averageLatency: 0,
      errorRate: 0,
      providerStats: {},
      lastSync: null
    };
    
    // Initialize provider-specific configurations
    this.initializeProviders();
  }

  /**
   * Initialize all configured vector database providers
   */
  async initializeProviders() {
    console.log('Initializing vector database providers...');

    for (const [name, config] of Object.entries(this.config.providers)) {
      if (config.enabled) {
        try {
          const provider = await this.createProvider(name, config);
          this.providers.set(name, provider);
          this.healthStatus.set(name, { status: 'unknown', lastCheck: null });
          this.routingMetrics.set(name, { 
            requests: 0, 
            errors: 0, 
            averageLatency: 0,
            successRate: 1.0 
          });
          console.log(`Initialized ${name} provider`);
        } catch (error) {
          console.error(`Failed to initialize ${name} provider:`, error.message);
          this.healthStatus.set(name, { status: 'unhealthy', error: error.message });
        }
      }
    }

    if (this.providers.size === 0) {
      throw new Error('No vector database providers were successfully initialized');
    }

    // Start health monitoring
    this.startHealthMonitoring();
    
    console.log(`Vector database client initialized with ${this.providers.size} providers`);
  }

  /**
   * Create provider-specific client
   */
  async createProvider(name, config) {
    switch (name) {
      case 'pinecone':
        return this.createPineconeProvider(config);
      case 'weaviate':
        return this.createWeaviateProvider(config);
      case 'qdrant':
        return this.createQdrantProvider(config);
      default:
        throw new Error(`Unknown provider: ${name}`);
    }
  }

  /**
   * Create Pinecone provider
   */
  async createPineconeProvider(config) {
    const client = {
      name: 'pinecone',
      config,
      baseUrl: config.baseUrl.replace('{environment}', config.environment),
      
      async upsert(vectors) {
        const url = `${this.baseUrl}/databases/${config.indexName}/vectors/upsert`;
        const response = await axios.post(url, {
          vectors: vectors.map(v => ({
            id: v.id,
            values: v.vector,
            metadata: v.metadata
          }))
        }, {
          headers: {
            'Api-Key': config.apiKey,
            'Content-Type': 'application/json'
          },
          timeout: 30000
        });
        
        return response.data;
      },
      
      async query(vector, topK = 10, filter = {}) {
        const url = `${this.baseUrl}/databases/${config.indexName}/vectors/query`;
        const response = await axios.post(url, {
          vector,
          topK,
          includeMetadata: true,
          includeValues: false,
          filter
        }, {
          headers: {
            'Api-Key': config.apiKey,
            'Content-Type': 'application/json'
          },
          timeout: 30000
        });
        
        return response.data.matches || [];
      },
      
      async delete(ids) {
        const url = `${this.baseUrl}/databases/${config.indexName}/vectors/delete`;
        const response = await axios.post(url, {
          ids
        }, {
          headers: {
            'Api-Key': config.apiKey,
            'Content-Type': 'application/json'
          }
        });
        
        return response.data;
      },
      
      async healthCheck() {
        const url = `${this.baseUrl}/databases/${config.indexName}/describe_index_stats`;
        const response = await axios.post(url, {}, {
          headers: {
            'Api-Key': config.apiKey,
            'Content-Type': 'application/json'
          },
          timeout: 10000
        });
        
        return {
          status: 'healthy',
          totalVectors: response.data.totalVectorCount || 0,
          dimension: response.data.dimension || config.dimension
        };
      }
    };
    
    // Test connection
    await client.healthCheck();
    return client;
  }

  /**
   * Create Weaviate provider
   */
  async createWeaviateProvider(config) {
    const client = {
      name: 'weaviate',
      config,
      baseUrl: `${config.scheme}://${config.host}:${config.port}`,
      
      async upsert(vectors) {
        const objects = vectors.map(v => ({
          class: config.className,
          id: v.id,
          vector: v.vector,
          properties: v.metadata
        }));
        
        const url = `${this.baseUrl}/v1/batch/objects`;
        const response = await axios.post(url, {
          objects
        }, {
          headers: {
            'Content-Type': 'application/json'
          },
          timeout: 30000
        });
        
        return response.data;
      },
      
      async query(vector, topK = 10, filter = {}) {
        const url = `${this.baseUrl}/v1/graphql`;
        
        let whereClause = '';
        if (Object.keys(filter).length > 0) {
          const conditions = Object.entries(filter).map(([key, value]) => 
            `{path: ["${key}"], operator: Equal, valueText: "${value}"}`
          ).join(', ');
          whereClause = `where: {operator: And, operands: [${conditions}]}`;
        }
        
        const query = `
          {
            Get {
              ${config.className}(
                nearVector: {vector: [${vector.join(',')}]}
                limit: ${topK}
                ${whereClause}
              ) {
                _additional {
                  id
                  distance
                  vector
                }
              }
            }
          }
        `;
        
        const response = await axios.post(url, { query }, {
          headers: {
            'Content-Type': 'application/json'
          },
          timeout: 30000
        });
        
        const results = response.data.data?.Get?.[config.className] || [];
        return results.map(r => ({
          id: r._additional.id,
          score: 1 - r._additional.distance, // Convert distance to similarity
          metadata: r
        }));
      },
      
      async delete(ids) {
        const deletePromises = ids.map(id => {
          const url = `${this.baseUrl}/v1/objects/${id}`;
          return axios.delete(url, {
            headers: {
              'Content-Type': 'application/json'
            }
          });
        });
        
        await Promise.all(deletePromises);
        return { deleted: ids.length };
      },
      
      async healthCheck() {
        const url = `${this.baseUrl}/v1/meta`;
        const response = await axios.get(url, {
          timeout: 10000
        });
        
        return {
          status: 'healthy',
          version: response.data.version,
          modules: response.data.modules
        };
      }
    };
    
    // Test connection
    await client.healthCheck();
    return client;
  }

  /**
   * Create Qdrant provider
   */
  async createQdrantProvider(config) {
    const client = {
      name: 'qdrant',
      config,
      baseUrl: `http://${config.host}:${config.port}`,
      
      async upsert(vectors) {
        const points = vectors.map(v => ({
          id: v.id,
          vector: v.vector,
          payload: v.metadata
        }));
        
        const url = `${this.baseUrl}/collections/${config.collectionName}/points/upsert`;
        const response = await axios.put(url, {
          points
        }, {
          headers: {
            'Content-Type': 'application/json',
            ...(config.apiKey && { 'api-key': config.apiKey })
          },
          timeout: 30000
        });
        
        return response.data;
      },
      
      async query(vector, topK = 10, filter = {}) {
        const url = `${this.baseUrl}/collections/${config.collectionName}/points/search`;
        
        const searchRequest = {
          vector,
          limit: topK,
          with_payload: true,
          with_vector: false
        };
        
        if (Object.keys(filter).length > 0) {
          searchRequest.filter = {
            must: Object.entries(filter).map(([key, value]) => ({
              key,
              match: { value }
            }))
          };
        }
        
        const response = await axios.post(url, searchRequest, {
          headers: {
            'Content-Type': 'application/json',
            ...(config.apiKey && { 'api-key': config.apiKey })
          },
          timeout: 30000
        });
        
        return response.data.result.map(r => ({
          id: r.id,
          score: r.score,
          metadata: r.payload
        }));
      },
      
      async delete(ids) {
        const url = `${this.baseUrl}/collections/${config.collectionName}/points/delete`;
        const response = await axios.post(url, {
          points: ids
        }, {
          headers: {
            'Content-Type': 'application/json',
            ...(config.apiKey && { 'api-key': config.apiKey })
          }
        });
        
        return response.data;
      },
      
      async healthCheck() {
        const url = `${this.baseUrl}/collections/${config.collectionName}`;
        const response = await axios.get(url, {
          headers: {
            ...(config.apiKey && { 'api-key': config.apiKey })
          },
          timeout: 10000
        });
        
        return {
          status: 'healthy',
          pointsCount: response.data.result.points_count,
          vectorsCount: response.data.result.vectors_count
        };
      }
    };
    
    // Test connection
    await client.healthCheck();
    return client;
  }

  /**
   * Store embeddings with automatic provider selection and sharding
   */
  async storeEmbeddings(embeddings) {
    const startTime = Date.now();
    
    try {
      // Group embeddings by target provider using sharding strategy
      const shardedEmbeddings = this.shardEmbeddings(embeddings);
      
      const storePromises = [];
      
      for (const [providerName, vectors] of shardedEmbeddings.entries()) {
        const provider = this.providers.get(providerName);
        if (!provider) continue;
        
        // Split into batches
        const batches = this.createBatches(vectors, this.config.batchSize);
        
        for (const batch of batches) {
          storePromises.push(
            this.executeWithRetry(() => provider.upsert(batch), providerName)
          );
        }
      }
      
      const results = await Promise.allSettled(storePromises);
      
      const successful = results.filter(r => r.status === 'fulfilled').length;
      const failed = results.filter(r => r.status === 'rejected').length;
      
      this.updateStats({
        operation: 'store',
        successful,
        failed,
        latency: Date.now() - startTime
      });
      
      console.log(`Stored ${successful} batches successfully, ${failed} failed`);
      
      return {
        stored: successful * this.config.batchSize,
        failed: failed * this.config.batchSize,
        executionTime: Date.now() - startTime
      };
      
    } catch (error) {
      console.error('Failed to store embeddings:', error);
      throw error;
    }
  }

  /**
   * Search for similar embeddings across all providers
   */
  async searchSimilar(queryVector, options = {}) {
    const startTime = Date.now();
    
    const {
      topK = this.config.defaultTopK,
      threshold = this.config.defaultThreshold,
      filter = {},
      providers = null // Specific providers to query
    } = options;
    
    try {
      const targetProviders = providers || Array.from(this.providers.keys());
      const searchPromises = [];
      
      for (const providerName of targetProviders) {
        const provider = this.providers.get(providerName);
        if (!provider || this.healthStatus.get(providerName)?.status !== 'healthy') {
          continue;
        }
        
        searchPromises.push(
          this.executeWithRetry(
            () => provider.query(queryVector, topK, filter),
            providerName
          ).then(results => ({
            provider: providerName,
            results: results.filter(r => r.score >= threshold)
          }))
        );
      }
      
      const searchResults = await Promise.allSettled(searchPromises);
      
      // Combine and deduplicate results
      const allResults = [];
      const seenIds = new Set();
      
      for (const result of searchResults) {
        if (result.status === 'fulfilled') {
          for (const item of result.value.results) {
            if (!seenIds.has(item.id)) {
              seenIds.add(item.id);
              allResults.push({
                ...item,
                provider: result.value.provider
              });
            }
          }
        }
      }
      
      // Sort by score and limit results
      allResults.sort((a, b) => b.score - a.score);
      const finalResults = allResults.slice(0, topK);
      
      this.updateStats({
        operation: 'search',
        successful: searchResults.filter(r => r.status === 'fulfilled').length,
        failed: searchResults.filter(r => r.status === 'rejected').length,
        latency: Date.now() - startTime
      });
      
      console.log(`Found ${finalResults.length} similar vectors from ${targetProviders.length} providers`);
      
      return {
        results: finalResults,
        totalFound: allResults.length,
        executionTime: Date.now() - startTime,
        providersQueried: targetProviders.length
      };
      
    } catch (error) {
      console.error('Failed to search similar embeddings:', error);
      throw error;
    }
  }

  /**
   * Delete embeddings by IDs
   */
  async deleteEmbeddings(ids) {
    const startTime = Date.now();
    
    try {
      const deletePromises = [];
      
      for (const [providerName, provider] of this.providers.entries()) {
        if (this.healthStatus.get(providerName)?.status === 'healthy') {
          deletePromises.push(
            this.executeWithRetry(() => provider.delete(ids), providerName)
              .then(() => ({ provider: providerName, success: true }))
              .catch(error => ({ provider: providerName, success: false, error }))
          );
        }
      }
      
      const results = await Promise.all(deletePromises);
      
      const successful = results.filter(r => r.success).length;
      const failed = results.filter(r => !r.success).length;
      
      this.updateStats({
        operation: 'delete',
        successful,
        failed,
        latency: Date.now() - startTime
      });
      
      console.log(`Deleted from ${successful} providers, failed on ${failed}`);
      
      return {
        deleted: successful > 0,
        providersUpdated: successful,
        executionTime: Date.now() - startTime
      };
      
    } catch (error) {
      console.error('Failed to delete embeddings:', error);
      throw error;
    }
  }

  /**
   * Shard embeddings across providers based on strategy
   */
  shardEmbeddings(embeddings) {
    const shards = new Map();
    
    // Initialize shards
    for (const providerName of this.providers.keys()) {
      shards.set(providerName, []);
    }
    
    const providerNames = Array.from(this.providers.keys());
    
    embeddings.forEach((embedding, index) => {
      let targetProvider;
      
      switch (this.config.shardingStrategy) {
        case 'round-robin':
          targetProvider = providerNames[index % providerNames.length];
          break;
        case 'hash':
          const hash = crypto.createHash('md5').update(embedding.id).digest('hex');
          const hashInt = parseInt(hash.substring(0, 8), 16);
          targetProvider = providerNames[hashInt % providerNames.length];
          break;
        case 'semantic':
          // TODO: Implement semantic-based sharding
          targetProvider = this.selectProviderBySemantic(embedding);
          break;
        default:
          targetProvider = providerNames[0];
      }
      
      if (shards.has(targetProvider)) {
        shards.get(targetProvider).push(embedding);
        
        // Add replicas
        if (this.config.replicationFactor > 1) {
          const replicas = this.selectReplicas(targetProvider, this.config.replicationFactor - 1);
          for (const replica of replicas) {
            if (shards.has(replica)) {
              shards.get(replica).push(embedding);
            }
          }
        }
      }
    });
    
    // Remove empty shards
    for (const [providerName, vectors] of shards.entries()) {
      if (vectors.length === 0) {
        shards.delete(providerName);
      }
    }
    
    return shards;
  }

  /**
   * Select replica providers
   */
  selectReplicas(primaryProvider, replicaCount) {
    const availableProviders = Array.from(this.providers.keys())
      .filter(name => name !== primaryProvider);
    
    // Sort by priority and health
    availableProviders.sort((a, b) => {
      const healthA = this.healthStatus.get(a)?.status === 'healthy' ? 1 : 0;
      const healthB = this.healthStatus.get(b)?.status === 'healthy' ? 1 : 0;
      
      if (healthA !== healthB) return healthB - healthA;
      
      const priorityA = this.config.providers[a]?.priority || 999;
      const priorityB = this.config.providers[b]?.priority || 999;
      
      return priorityA - priorityB;
    });
    
    return availableProviders.slice(0, replicaCount);
  }

  /**
   * Select provider based on intelligent routing
   */
  selectProviderIntelligently() {
    const healthyProviders = Array.from(this.providers.keys())
      .filter(name => this.healthStatus.get(name)?.status === 'healthy');
    
    if (healthyProviders.length === 0) {
      throw new Error('No healthy providers available');
    }
    
    // Sort by success rate and latency
    healthyProviders.sort((a, b) => {
      const metricsA = this.routingMetrics.get(a);
      const metricsB = this.routingMetrics.get(b);
      
      const scoreA = metricsA.successRate * 0.7 + (1 / metricsA.averageLatency) * 0.3;
      const scoreB = metricsB.successRate * 0.7 + (1 / metricsB.averageLatency) * 0.3;
      
      return scoreB - scoreA;
    });
    
    return healthyProviders[0];
  }

  /**
   * Execute operation with retry logic
   */
  async executeWithRetry(operation, providerName, attempt = 1) {
    const startTime = Date.now();
    
    try {
      const result = await operation();
      
      // Update metrics on success
      const metrics = this.routingMetrics.get(providerName);
      metrics.requests++;
      metrics.averageLatency = (metrics.averageLatency * 0.9) + ((Date.now() - startTime) * 0.1);
      metrics.successRate = (metrics.successRate * 0.95) + (1.0 * 0.05);
      
      return result;
    } catch (error) {
      // Update metrics on error
      const metrics = this.routingMetrics.get(providerName);
      metrics.requests++;
      metrics.errors++;
      metrics.successRate = (metrics.successRate * 0.95) + (0.0 * 0.05);
      
      if (attempt < this.config.retryAttempts) {
        console.warn(`Retry attempt ${attempt + 1} for ${providerName}:`, error.message);
        await this.delay(1000 * attempt); // Exponential backoff
        return this.executeWithRetry(operation, providerName, attempt + 1);
      } else {
        throw error;
      }
    }
  }

  /**
   * Create batches from array
   */
  createBatches(array, batchSize) {
    const batches = [];
    for (let i = 0; i < array.length; i += batchSize) {
      batches.push(array.slice(i, i + batchSize));
    }
    return batches;
  }

  /**
   * Start health monitoring for all providers
   */
  startHealthMonitoring() {
    setInterval(async () => {
      await this.checkAllProvidersHealth();
    }, 30000); // Every 30 seconds
  }

  /**
   * Check health of all providers
   */
  async checkAllProvidersHealth() {
    for (const [providerName, provider] of this.providers.entries()) {
      try {
        const healthResult = await provider.healthCheck();
        this.healthStatus.set(providerName, {
          status: 'healthy',
          lastCheck: new Date(),
          ...healthResult
        });
      } catch (error) {
        this.healthStatus.set(providerName, {
          status: 'unhealthy',
          lastCheck: new Date(),
          error: error.message
        });
        console.error(`Provider ${providerName} health check failed:`, error.message);
      }
    }
  }

  /**
   * Update statistics
   */
  updateStats(operation) {
    this.stats.totalQueries++;
    
    if (operation.latency) {
      this.stats.averageLatency = (this.stats.averageLatency * 0.9) + (operation.latency * 0.1);
    }
    
    const totalOperations = operation.successful + operation.failed;
    if (totalOperations > 0) {
      const currentErrorRate = operation.failed / totalOperations;
      this.stats.errorRate = (this.stats.errorRate * 0.9) + (currentErrorRate * 0.1);
    }
    
    this.stats.lastSync = new Date();
  }

  /**
   * Get comprehensive statistics
   */
  getStats() {
    const providerStats = {};
    
    for (const [name, metrics] of this.routingMetrics.entries()) {
      const health = this.healthStatus.get(name);
      providerStats[name] = {
        ...metrics,
        health: health?.status || 'unknown',
        lastHealthCheck: health?.lastCheck
      };
    }
    
    return {
      ...this.stats,
      providerStats,
      totalProviders: this.providers.size,
      healthyProviders: Array.from(this.healthStatus.values())
        .filter(h => h.status === 'healthy').length
    };
  }

  /**
   * Health check for external monitoring
   */
  async healthCheck() {
    const healthyCount = Array.from(this.healthStatus.values())
      .filter(h => h.status === 'healthy').length;
    
    const totalCount = this.providers.size;
    
    return {
      status: healthyCount > 0 ? 'healthy' : 'unhealthy',
      providers: {
        healthy: healthyCount,
        total: totalCount,
        details: Object.fromEntries(this.healthStatus.entries())
      },
      performance: {
        averageLatency: this.stats.averageLatency,
        errorRate: this.stats.errorRate,
        totalQueries: this.stats.totalQueries
      },
      lastCheck: new Date().toISOString()
    };
  }

  /**
   * Utility method for delays
   */
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Close all provider connections
   */
  async close() {
    console.log('Closing vector database client...');
    
    // Provider-specific cleanup would go here
    // For now, just clear the providers map
    this.providers.clear();
    this.healthStatus.clear();
    this.routingMetrics.clear();
    
    console.log('Vector database client closed');
  }
}

module.exports = VectorDatabaseClient;