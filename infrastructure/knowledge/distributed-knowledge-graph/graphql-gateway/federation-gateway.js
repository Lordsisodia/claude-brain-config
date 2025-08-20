const { ApolloServer } = require('@apollo/server');
const { startStandaloneServer } = require('@apollo/server/standalone');
const { buildSubgraphSchema } = require('@apollo/subgraph');
const { ApolloGateway, IntrospectAndCompose, RemoteGraphQLDataSource } = require('@apollo/gateway');
const { readFileSync } = require('fs');
const { GraphQLScalarType } = require('graphql');
const { Kind } = require('graphql/language');
const Redis = require('ioredis');
const Neo4jShardManager = require('../neo4j-cluster/shard-manager');
const IPFSClient = require('../ipfs-storage/ipfs-client');
const VectorDatabase = require('../vector-db/vector-client');
const ConsensusClient = require('../consensus-layer/consensus-client');

/**
 * GraphQL Federation Gateway for Distributed Knowledge Graph
 * 
 * This gateway orchestrates queries across multiple subgraphs:
 * - Knowledge Graph Service (Neo4j cluster)
 * - Vector Search Service (Pinecone/Weaviate/Qdrant)
 * - IPFS Storage Service
 * - Consensus Service (Blockchain)
 * - Agent Memory Service (Redis)
 */
class FederationGateway {
  constructor(config = {}) {
    this.config = {
      port: process.env.GRAPHQL_PORT || 4000,
      redis: {
        host: process.env.REDIS_HOST || 'redis-cluster-01',
        port: process.env.REDIS_PORT || 6379,
        password: process.env.REDIS_PASSWORD
      },
      subgraphs: [
        {
          name: 'knowledge-graph',
          url: 'http://knowledge-graph-service:4001/graphql'
        },
        {
          name: 'vector-search',
          url: 'http://vector-search-service:4002/graphql'
        },
        {
          name: 'ipfs-storage',
          url: 'http://ipfs-storage-service:4003/graphql'
        },
        {
          name: 'consensus',
          url: 'http://consensus-service:4004/graphql'
        },
        {
          name: 'agent-memory',
          url: 'http://agent-memory-service:4005/graphql'
        }
      ],
      ...config
    };

    this.redis = null;
    this.neo4jManager = null;
    this.ipfsClient = null;
    this.vectorDb = null;
    this.consensusClient = null;
    this.gateway = null;
    this.server = null;
  }

  /**
   * Initialize all services and connections
   */
  async initialize() {
    console.log('Initializing Federation Gateway...');

    // Initialize Redis cluster for caching
    this.redis = new Redis.Cluster([
      { host: 'redis-cluster-01', port: 6379 },
      { host: 'redis-cluster-02', port: 6379 },
      { host: 'redis-cluster-03', port: 6379 }
    ], {
      redisOptions: {
        password: this.config.redis.password
      },
      enableReadyCheck: true,
      maxRetriesPerRequest: 3
    });

    // Initialize Neo4j shard manager
    this.neo4jManager = new Neo4jShardManager();

    // Initialize IPFS client
    this.ipfsClient = new IPFSClient();
    await this.ipfsClient.initialize();

    // Initialize vector database
    this.vectorDb = new VectorDatabase();
    await this.vectorDb.initialize();

    // Initialize consensus client
    this.consensusClient = new ConsensusClient();
    await this.consensusClient.initialize();

    console.log('All services initialized successfully');
  }

  /**
   * Create Apollo Gateway with subgraph federation
   */
  createGateway() {
    this.gateway = new ApolloGateway({
      supergraphSdl: new IntrospectAndCompose({
        subgraphs: this.config.subgraphs.map(subgraph => ({
          name: subgraph.name,
          url: subgraph.url
        }))
      }),
      buildService({ url }) {
        return new RemoteGraphQLDataSource({
          url,
          willSendRequest({ request, context }) {
            // Add authentication and tracing headers
            if (context.agentId) {
              request.http.headers.set('x-agent-id', context.agentId);
            }
            if (context.sessionId) {
              request.http.headers.set('x-session-id', context.sessionId);
            }
            request.http.headers.set('x-trace-id', context.traceId || generateTraceId());
          },
          didReceiveResponse({ response, request, context }) {
            // Log performance metrics
            const executionTime = Date.now() - context.startTime;
            console.log(`Subgraph ${request.url} responded in ${executionTime}ms`);
            return response;
          },
          didEncounterError(error, request, context) {
            console.error(`Subgraph error from ${request.url}:`, error);
            // Implement circuit breaker logic here
            return error;
          }
        });
      }
    });

    return this.gateway;
  }

  /**
   * Create Apollo Server with custom resolvers and context
   */
  async createServer() {
    const gateway = this.createGateway();

    this.server = new ApolloServer({
      gateway,
      context: async ({ req }) => {
        const startTime = Date.now();
        const traceId = req.headers['x-trace-id'] || generateTraceId();
        const agentId = req.headers['x-agent-id'];
        const sessionId = req.headers['x-session-id'];

        return {
          startTime,
          traceId,
          agentId,
          sessionId,
          redis: this.redis,
          neo4jManager: this.neo4jManager,
          ipfsClient: this.ipfsClient,
          vectorDb: this.vectorDb,
          consensusClient: this.consensusClient,
          
          // Add data loaders for efficient batching
          dataloaders: this.createDataLoaders()
        };
      },
      plugins: [
        // Custom plugin for performance monitoring
        {
          requestDidStart() {
            return {
              didResolveOperation(requestContext) {
                console.log(`Operation: ${requestContext.request.operationName}`);
              },
              willSendResponse(requestContext) {
                const executionTime = Date.now() - requestContext.context.startTime;
                console.log(`Total execution time: ${executionTime}ms`);
                
                // Cache successful queries
                if (requestContext.response.http.status === 200) {
                  this.cacheResponse(requestContext);
                }
              }
            };
          }
        },
        
        // Circuit breaker plugin
        {
          requestDidStart() {
            return {
              didEncounterErrors(requestContext) {
                // Implement circuit breaker logic
                const errors = requestContext.errors;
                this.handleCircuitBreaker(errors, requestContext.context);
              }
            };
          }
        }
      ],
      
      // Custom scalar resolvers
      resolvers: {
        DateTime: new GraphQLScalarType({
          name: 'DateTime',
          description: 'A valid date time value.',
          serialize: value => value instanceof Date ? value.toISOString() : value,
          parseValue: value => new Date(value),
          parseLiteral: ast => ast.kind === Kind.STRING ? new Date(ast.value) : null
        }),
        
        JSON: new GraphQLScalarType({
          name: 'JSON',
          description: 'A JSON object.',
          serialize: value => value,
          parseValue: value => value,
          parseLiteral: ast => ast.kind === Kind.STRING ? JSON.parse(ast.value) : ast.value
        })
      },
      
      // Enhanced error handling
      formatError: (error) => {
        console.error('GraphQL Error:', error);
        
        // Don't expose internal errors in production
        if (process.env.NODE_ENV === 'production') {
          return new Error('Internal server error');
        }
        
        return error;
      }
    });

    return this.server;
  }

  /**
   * Create data loaders for efficient batching
   */
  createDataLoaders() {
    const DataLoader = require('dataloader');
    
    return {
      knowledgeNodes: new DataLoader(async (ids) => {
        const cacheKeys = ids.map(id => `node:${id}`);
        const cachedResults = await this.redis.mget(cacheKeys);
        
        const uncachedIds = [];
        const results = [];
        
        cachedResults.forEach((cached, index) => {
          if (cached) {
            results[index] = JSON.parse(cached);
          } else {
            uncachedIds.push({ id: ids[index], index });
          }
        });
        
        // Fetch uncached nodes from Neo4j
        if (uncachedIds.length > 0) {
          const nodes = await Promise.all(
            uncachedIds.map(async ({ id }) => {
              return this.neo4jManager.getKnowledgeNode(id);
            })
          );
          
          // Cache the results
          const cacheOperations = [];
          uncachedIds.forEach(({ index }, i) => {
            results[index] = nodes[i];
            if (nodes[i]) {
              cacheOperations.push(
                this.redis.setex(`node:${ids[index]}`, 300, JSON.stringify(nodes[i]))
              );
            }
          });
          
          await Promise.all(cacheOperations);
        }
        
        return results;
      }),
      
      vectorSimilarity: new DataLoader(async (queries) => {
        return Promise.all(queries.map(query => 
          this.vectorDb.findSimilar(query.embedding, query.threshold, query.limit)
        ));
      }),
      
      consensusRecords: new DataLoader(async (nodeIds) => {
        return Promise.all(nodeIds.map(nodeId => 
          this.consensusClient.getConsensusRecords(nodeId)
        ));
      })
    };
  }

  /**
   * Cache response based on query characteristics
   */
  async cacheResponse(requestContext) {
    const { query, variables } = requestContext.request;
    const operation = requestContext.request.operationName;
    
    // Only cache read operations
    if (operation && operation.toLowerCase().includes('query')) {
      const cacheKey = `query:${createHash(query + JSON.stringify(variables))}`;
      const ttl = this.determineCacheTTL(operation);
      
      await this.redis.setex(
        cacheKey, 
        ttl, 
        JSON.stringify(requestContext.response.data)
      );
    }
  }

  /**
   * Determine cache TTL based on query type
   */
  determineCacheTTL(operation) {
    const operationLower = operation.toLowerCase();
    
    if (operationLower.includes('statistics') || operationLower.includes('analytics')) {
      return 300; // 5 minutes
    } else if (operationLower.includes('search') || operationLower.includes('similar')) {
      return 60; // 1 minute
    } else if (operationLower.includes('node') || operationLower.includes('relationship')) {
      return 30; // 30 seconds
    }
    
    return 60; // Default 1 minute
  }

  /**
   * Handle circuit breaker logic
   */
  handleCircuitBreaker(errors, context) {
    errors.forEach(error => {
      if (error.extensions && error.extensions.serviceName) {
        const serviceName = error.extensions.serviceName;
        const errorKey = `circuit:${serviceName}:errors`;
        
        // Increment error counter
        this.redis.incr(errorKey);
        this.redis.expire(errorKey, 60); // 1 minute window
        
        // Check if circuit should be opened
        this.redis.get(errorKey).then(errorCount => {
          if (parseInt(errorCount) > 10) { // Threshold of 10 errors per minute
            console.warn(`Opening circuit breaker for service: ${serviceName}`);
            this.redis.setex(`circuit:${serviceName}:open`, 300, '1'); // 5 minute cooldown
          }
        });
      }
    });
  }

  /**
   * Start the federation gateway
   */
  async start() {
    await this.initialize();
    const server = await this.createServer();
    
    const { url } = await startStandaloneServer(server, {
      listen: { port: this.config.port },
      context: async ({ req }) => {
        // Context creation is handled in createServer
        return {};
      }
    });

    console.log(`🚀 Federation Gateway ready at ${url}`);
    console.log(`🔍 GraphQL Playground available at ${url}`);
    
    return { server, url };
  }

  /**
   * Stop the gateway and close all connections
   */
  async stop() {
    console.log('Stopping Federation Gateway...');
    
    if (this.server) {
      await this.server.stop();
    }
    
    if (this.gateway) {
      await this.gateway.stop();
    }
    
    if (this.redis) {
      this.redis.disconnect();
    }
    
    if (this.neo4jManager) {
      await this.neo4jManager.close();
    }
    
    if (this.ipfsClient) {
      await this.ipfsClient.close();
    }
    
    if (this.vectorDb) {
      await this.vectorDb.close();
    }
    
    if (this.consensusClient) {
      await this.consensusClient.close();
    }
    
    console.log('Federation Gateway stopped');
  }

  /**
   * Health check endpoint
   */
  async healthCheck() {
    const health = {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      services: {}
    };

    try {
      // Check Redis
      await this.redis.ping();
      health.services.redis = 'healthy';
    } catch (error) {
      health.services.redis = 'unhealthy';
      health.status = 'degraded';
    }

    try {
      // Check Neo4j
      const neo4jHealth = await this.neo4jManager.getClusterHealth();
      health.services.neo4j = neo4jHealth.every(node => node.status === 'healthy') ? 'healthy' : 'degraded';
    } catch (error) {
      health.services.neo4j = 'unhealthy';
      health.status = 'degraded';
    }

    try {
      // Check IPFS
      const ipfsHealth = await this.ipfsClient.healthCheck();
      health.services.ipfs = ipfsHealth.status;
    } catch (error) {
      health.services.ipfs = 'unhealthy';
      health.status = 'degraded';
    }

    try {
      // Check Vector Database
      const vectorHealth = await this.vectorDb.healthCheck();
      health.services.vectorDb = vectorHealth.status;
    } catch (error) {
      health.services.vectorDb = 'unhealthy';
      health.status = 'degraded';
    }

    try {
      // Check Consensus
      const consensusHealth = await this.consensusClient.healthCheck();
      health.services.consensus = consensusHealth.status;
    } catch (error) {
      health.services.consensus = 'unhealthy';
      health.status = 'degraded';
    }

    return health;
  }
}

/**
 * Utility functions
 */
function generateTraceId() {
  return Math.random().toString(36).substring(2, 15) + 
         Math.random().toString(36).substring(2, 15);
}

function createHash(input) {
  const crypto = require('crypto');
  return crypto.createHash('md5').update(input).digest('hex');
}

module.exports = FederationGateway;