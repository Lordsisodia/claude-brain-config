const { EventEmitter } = require('events');
const crypto = require('crypto');
const Neo4jShardManager = require('../neo4j-cluster/shard-manager');
const IPFSClient = require('../ipfs-storage/ipfs-client');
const ConsensusClient = require('../consensus-layer/consensus-client');
const RedisCacheManager = require('../redis-cluster/redis-cache-manager');
const VectorDatabaseClient = require('../vector-db/vector-client');
const GlobalSyncManager = require('../sync-protocols/global-sync-manager');
const { KnowledgeGraphCRDT, CRDTNetworkManager } = require('../crdt-lib/crdt-implementation');

/**
 * AI Agent Interface for Distributed Knowledge Graph
 * 
 * This interface provides a high-level API for AI agents to interact
 * with the distributed knowledge graph system. It abstracts away the
 * complexity of the underlying infrastructure while providing:
 * 
 * - Simple CRUD operations on knowledge nodes and relationships
 * - Semantic search and graph traversal
 * - Real-time collaboration with other agents
 * - Automatic conflict resolution and consensus
 * - Memory management (working, episodic, semantic, procedural)
 * - Learning and adaptation capabilities
 */
class KnowledgeGraphAgent extends EventEmitter {
  constructor(agentId, config = {}) {
    super();
    
    this.agentId = agentId || this.generateAgentId();
    this.sessionId = this.generateSessionId();
    
    this.config = {
      // Agent configuration
      agentType: config.agentType || 'GeneralPurposeAgent',
      capabilities: config.capabilities || [
        'knowledge_creation',
        'knowledge_retrieval', 
        'semantic_search',
        'graph_traversal',
        'collaboration',
        'learning'
      ],
      
      // Memory configuration
      workingMemorySize: config.workingMemorySize || 1000,
      episodicMemoryLimit: config.episodicMemoryLimit || 10000,
      semanticMemoryThreshold: config.semanticMemoryThreshold || 0.8,
      proceduralMemoryDecay: config.proceduralMemoryDecay || 0.95,
      
      // Learning parameters
      learningRate: config.learningRate || 0.01,
      adaptationThreshold: config.adaptationThreshold || 0.1,
      explorationRate: config.explorationRate || 0.1,
      
      // Collaboration settings
      trustThreshold: config.trustThreshold || 0.7,
      consensusParticipation: config.consensusParticipation !== false,
      shareKnowledge: config.shareKnowledge !== false,
      
      // Performance settings
      cacheEnabled: config.cacheEnabled !== false,
      batchOperations: config.batchOperations !== false,
      maxConcurrentOperations: config.maxConcurrentOperations || 10,
      
      ...config
    };

    // System components
    this.neo4j = null;
    this.ipfs = null;
    this.consensus = null;
    this.cache = null;
    this.vectorDb = null;
    this.syncManager = null;
    this.crdtManager = null;
    
    // Agent state
    this.workingMemory = new Map();
    this.episodicMemory = [];
    this.semanticMemory = new Map();
    this.proceduralMemory = new Map();
    this.reputation = 1.0;
    this.trustScores = new Map(); // agentId -> trust score
    
    // Operation tracking
    this.operationQueue = [];
    this.activeOperations = new Set();
    this.operationHistory = [];
    
    // Learning state
    this.experienceBuffer = [];
    this.knowledgeGraph = null; // Local CRDT instance
    this.collaborations = new Map(); // agentId -> collaboration context
    
    // Metrics
    this.metrics = {
      operationsPerformed: 0,
      knowledgeNodesCreated: 0,
      relationshipsEstablished: 0,
      collaborationsInitiated: 0,
      consensusParticipations: 0,
      learningEvents: 0,
      averageResponseTime: 0,
      successRate: 1.0
    };
  }

  /**
   * Initialize the agent and connect to the knowledge graph system
   */
  async initialize() {
    console.log(`Initializing Knowledge Graph Agent ${this.agentId}...`);
    
    try {
      // Initialize system components
      this.neo4j = new Neo4jShardManager();
      this.ipfs = new IPFSClient();
      this.consensus = new ConsensusClient({ nodeId: this.agentId });
      this.cache = new RedisCacheManager();
      this.vectorDb = new VectorDatabaseClient();
      this.syncManager = new GlobalSyncManager(this.agentId);
      this.crdtManager = new CRDTNetworkManager(this.agentId);
      
      // Initialize local knowledge graph CRDT
      this.knowledgeGraph = new KnowledgeGraphCRDT(this.agentId);
      this.crdtManager.register('agent-knowledge', this.knowledgeGraph);
      
      // Set up event handlers
      this.setupEventHandlers();
      
      // Initialize components that don't require external services
      await this.crdtManager.startPeriodicSync();
      
      // Load agent's existing memory and state
      await this.loadAgentState();
      
      console.log(`Agent ${this.agentId} initialized successfully`);
      this.emit('initialized');
      
    } catch (error) {
      console.error(`Failed to initialize agent ${this.agentId}:`, error);
      throw error;
    }
  }

  /**
   * Create a new knowledge node
   */
  async createKnowledgeNode(nodeData) {
    const startTime = Date.now();
    
    try {
      const nodeId = nodeData.id || this.generateNodeId();
      const node = {
        id: nodeId,
        type: nodeData.type || 'KnowledgeNode',
        properties: {
          ...nodeData.properties,
          createdBy: this.agentId,
          sessionId: this.sessionId,
          createdAt: new Date().toISOString(),
          version: 1
        },
        embeddings: nodeData.embeddings || await this.generateEmbeddings(nodeData)
      };

      // Add to local CRDT
      this.knowledgeGraph.addNode(nodeId, node.properties);
      
      // Store embeddings if available
      if (node.embeddings && this.vectorDb) {
        await this.vectorDb.storeEmbeddings([{
          id: nodeId,
          vector: node.embeddings,
          metadata: {
            agentId: this.agentId,
            type: node.type,
            createdAt: node.properties.createdAt
          }
        }]);
      }

      // Cache the node
      if (this.cache) {
        await this.cache.cacheNode(nodeId, node);
      }

      // Add to working memory
      this.addToWorkingMemory(`node:${nodeId}`, node);
      
      // Record experience
      this.recordExperience({
        type: 'knowledge_creation',
        action: 'create_node',
        nodeId,
        success: true,
        latency: Date.now() - startTime
      });

      this.metrics.knowledgeNodesCreated++;
      this.metrics.operationsPerformed++;
      this.updateAverageResponseTime(Date.now() - startTime);
      
      console.log(`Agent ${this.agentId} created knowledge node: ${nodeId}`);
      this.emit('nodeCreated', { nodeId, node });
      
      return { nodeId, node, executionTime: Date.now() - startTime };
      
    } catch (error) {
      this.recordExperience({
        type: 'knowledge_creation',
        action: 'create_node',
        success: false,
        error: error.message,
        latency: Date.now() - startTime
      });
      
      console.error(`Failed to create node:`, error);
      throw error;
    }
  }

  /**
   * Retrieve a knowledge node by ID
   */
  async getKnowledgeNode(nodeId) {
    const startTime = Date.now();
    
    try {
      // Check working memory first
      const fromMemory = this.workingMemory.get(`node:${nodeId}`);
      if (fromMemory) {
        this.updateAverageResponseTime(Date.now() - startTime);
        return { node: fromMemory, source: 'working_memory' };
      }

      // Check cache
      let node = null;
      if (this.cache) {
        node = await this.cache.getCachedNode(nodeId);
        if (node) {
          this.addToWorkingMemory(`node:${nodeId}`, node);
          this.updateAverageResponseTime(Date.now() - startTime);
          return { node, source: 'cache' };
        }
      }

      // Check local CRDT
      node = this.knowledgeGraph.getNode(nodeId);
      if (node) {
        // Cache it for future use
        if (this.cache) {
          await this.cache.cacheNode(nodeId, node);
        }
        this.addToWorkingMemory(`node:${nodeId}`, node);
        this.updateAverageResponseTime(Date.now() - startTime);
        return { node, source: 'local_crdt' };
      }

      // Query distributed graph (mock implementation)
      if (this.neo4j) {
        const result = await Promise.resolve({
          node: {
            id: nodeId,
            type: 'KnowledgeNode',
            properties: { name: 'Mock Node' }
          }
        });
        
        if (result.node) {
          // Add to local CRDT
          this.knowledgeGraph.addNode(nodeId, result.node.properties);
          
          // Cache it
          if (this.cache) {
            await this.cache.cacheNode(nodeId, result.node);
          }
          
          this.addToWorkingMemory(`node:${nodeId}`, result.node);
          this.updateAverageResponseTime(Date.now() - startTime);
          return { node: result.node, source: 'distributed_graph' };
        }
      }

      this.updateAverageResponseTime(Date.now() - startTime);
      return { node: null, source: 'not_found' };
      
    } catch (error) {
      console.error(`Failed to get node ${nodeId}:`, error);
      throw error;
    }
  }

  /**
   * Update a knowledge node
   */
  async updateKnowledgeNode(nodeId, updates) {
    const startTime = Date.now();
    
    try {
      // Get current node
      const current = await this.getKnowledgeNode(nodeId);
      if (!current.node) {
        throw new Error(`Node ${nodeId} not found`);
      }

      // Prepare updates
      const updatedProperties = {
        ...current.node.properties,
        ...updates,
        updatedBy: this.agentId,
        sessionId: this.sessionId,
        updatedAt: new Date().toISOString(),
        version: (current.node.properties.version || 1) + 1
      };

      // Check if consensus is required for this update
      if (this.requiresConsensus(updates) && this.consensus) {
        const consensusResult = await this.consensus.proposeChange(
          nodeId, 
          updates, 
          this.agentId,
          { 
            updateType: 'node_properties',
            importance: this.calculateUpdateImportance(updates)
          }
        );
        
        // Wait for consensus (simplified)
        console.log(`Consensus initiated for node ${nodeId}: ${consensusResult.proposalId}`);
      }

      // Update local CRDT
      for (const [key, value] of Object.entries(updates)) {
        this.knowledgeGraph.updateNodeProperty(nodeId, key, value);
      }

      // Update cache
      if (this.cache) {
        await this.cache.cacheNode(nodeId, {
          ...current.node,
          properties: updatedProperties
        });
      }

      // Update working memory
      this.addToWorkingMemory(`node:${nodeId}`, {
        ...current.node,
        properties: updatedProperties
      });

      this.metrics.operationsPerformed++;
      this.updateAverageResponseTime(Date.now() - startTime);
      
      console.log(`Agent ${this.agentId} updated node: ${nodeId}`);
      this.emit('nodeUpdated', { nodeId, updates });
      
      return { 
        nodeId, 
        updates, 
        newVersion: updatedProperties.version,
        executionTime: Date.now() - startTime 
      };
      
    } catch (error) {
      console.error(`Failed to update node ${nodeId}:`, error);
      throw error;
    }
  }

  /**
   * Create a relationship between nodes
   */
  async createRelationship(fromNodeId, toNodeId, relationshipType, properties = {}) {
    const startTime = Date.now();
    
    try {
      const relationshipId = `${fromNodeId}-${relationshipType}-${toNodeId}`;
      
      const relationship = {
        id: relationshipId,
        fromNodeId,
        toNodeId,
        type: relationshipType,
        properties: {
          ...properties,
          createdBy: this.agentId,
          sessionId: this.sessionId,
          createdAt: new Date().toISOString(),
          weight: properties.weight || 1.0
        }
      };

      // Add to local CRDT
      this.knowledgeGraph.addRelationship(
        relationshipId,
        fromNodeId,
        toNodeId,
        relationshipType,
        relationship.properties
      );

      // Cache the relationship
      if (this.cache) {
        await this.cache.cacheNode(`rel:${relationshipId}`, relationship);
      }

      // Add to working memory
      this.addToWorkingMemory(`rel:${relationshipId}`, relationship);

      this.metrics.relationshipsEstablished++;
      this.metrics.operationsPerformed++;
      this.updateAverageResponseTime(Date.now() - startTime);
      
      console.log(`Agent ${this.agentId} created relationship: ${relationshipId}`);
      this.emit('relationshipCreated', { relationshipId, relationship });
      
      return { relationshipId, relationship, executionTime: Date.now() - startTime };
      
    } catch (error) {
      console.error(`Failed to create relationship:`, error);
      throw error;
    }
  }

  /**
   * Search for similar knowledge nodes using semantic embeddings
   */
  async searchSimilar(query, options = {}) {
    const startTime = Date.now();
    
    try {
      let queryVector = options.queryVector;
      
      // Generate embedding for text query if not provided
      if (!queryVector && typeof query === 'string') {
        queryVector = await this.generateEmbeddings({ text: query });
      }

      if (!queryVector) {
        throw new Error('Query vector is required for similarity search');
      }

      // Perform vector search
      let results = [];
      if (this.vectorDb) {
        const searchResult = await this.vectorDb.searchSimilar(queryVector, {
          topK: options.limit || 10,
          threshold: options.threshold || 0.7,
          filter: options.filter || {}
        });
        
        results = searchResult.results;
      } else {
        // Mock results for testing
        results = Array(Math.min(options.limit || 10, 5)).fill(0).map((_, i) => ({
          id: `similar-node-${i}`,
          score: 0.9 - (i * 0.1),
          metadata: { type: 'MockNode', name: `Similar Node ${i}` }
        }));
      }

      // Enrich results with additional node data
      const enrichedResults = await Promise.all(
        results.map(async (result) => {
          const nodeData = await this.getKnowledgeNode(result.id);
          return {
            ...result,
            node: nodeData.node,
            source: nodeData.source
          };
        })
      );

      // Add to episodic memory
      this.addToEpisodicMemory({
        type: 'semantic_search',
        query,
        results: enrichedResults.length,
        timestamp: new Date().toISOString()
      });

      this.metrics.operationsPerformed++;
      this.updateAverageResponseTime(Date.now() - startTime);
      
      console.log(`Agent ${this.agentId} found ${enrichedResults.length} similar nodes`);
      this.emit('similaritySearchCompleted', { query, results: enrichedResults });
      
      return {
        query,
        results: enrichedResults,
        totalFound: results.length,
        executionTime: Date.now() - startTime
      };
      
    } catch (error) {
      console.error(`Failed to search similar nodes:`, error);
      throw error;
    }
  }

  /**
   * Traverse the knowledge graph from a starting node
   */
  async traverseGraph(startNodeId, options = {}) {
    const startTime = Date.now();
    
    try {
      const {
        direction = 'BOTH',
        relationshipTypes = [],
        maxDepth = 3,
        limit = 100,
        filter = {}
      } = options;

      // Mock traversal results (replace with actual Neo4j traversal)
      const mockResults = {
        nodes: Array(Math.min(limit, 25)).fill(0).map((_, i) => ({
          id: `traversed-node-${i}`,
          type: 'TraversedNode',
          properties: { name: `Node ${i}`, depth: Math.floor(i / 5) },
          distance: Math.floor(i / 5)
        })),
        relationships: Array(Math.min(limit - 1, 24)).fill(0).map((_, i) => ({
          id: `traversed-rel-${i}`,
          type: relationshipTypes[i % relationshipTypes.length] || 'CONNECTED_TO',
          fromNodeId: `traversed-node-${i}`,
          toNodeId: `traversed-node-${i + 1}`
        })),
        paths: []
      };

      // Build paths from results
      const paths = this.constructPaths(mockResults.nodes, mockResults.relationships);
      mockResults.paths = paths.slice(0, 10); // Limit paths

      // Add to working memory
      this.addToWorkingMemory(`traversal:${startNodeId}`, {
        startNode: startNodeId,
        results: mockResults,
        options,
        timestamp: new Date().toISOString()
      });

      this.metrics.operationsPerformed++;
      this.updateAverageResponseTime(Date.now() - startTime);
      
      console.log(`Agent ${this.agentId} traversed from ${startNodeId}: ${mockResults.nodes.length} nodes, ${mockResults.relationships.length} relationships`);
      this.emit('graphTraversalCompleted', { startNodeId, results: mockResults });
      
      return {
        startNodeId,
        ...mockResults,
        executionTime: Date.now() - startTime,
        shardsQueried: ['core-0', 'core-1'], // Mock shard info
        options
      };
      
    } catch (error) {
      console.error(`Failed to traverse graph from ${startNodeId}:`, error);
      throw error;
    }
  }

  /**
   * Collaborate with another agent on knowledge building
   */
  async collaborateWith(otherAgentId, collaborationType = 'knowledge_sharing') {
    const startTime = Date.now();
    
    try {
      // Check trust level with the other agent
      const trustScore = this.trustScores.get(otherAgentId) || 0.5;
      if (trustScore < this.config.trustThreshold) {
        console.warn(`Trust score too low for collaboration with ${otherAgentId}: ${trustScore}`);
        return null;
      }

      // Initialize collaboration context
      const collaborationId = this.generateCollaborationId();
      const collaboration = {
        id: collaborationId,
        participants: [this.agentId, otherAgentId],
        type: collaborationType,
        startedAt: new Date().toISOString(),
        sharedKnowledge: [],
        status: 'active'
      };

      this.collaborations.set(collaborationId, collaboration);

      // Share relevant knowledge based on working memory
      if (this.config.shareKnowledge) {
        const knowledgeToShare = this.selectKnowledgeForSharing(collaborationType);
        collaboration.sharedKnowledge = knowledgeToShare;
        
        console.log(`Agent ${this.agentId} sharing ${knowledgeToShare.length} knowledge items with ${otherAgentId}`);
      }

      this.metrics.collaborationsInitiated++;
      this.metrics.operationsPerformed++;
      this.updateAverageResponseTime(Date.now() - startTime);
      
      this.emit('collaborationStarted', { collaborationId, otherAgentId, collaboration });
      
      return {
        collaborationId,
        otherAgentId,
        type: collaborationType,
        sharedKnowledgeCount: collaboration.sharedKnowledge.length,
        executionTime: Date.now() - startTime
      };
      
    } catch (error) {
      console.error(`Failed to collaborate with ${otherAgentId}:`, error);
      throw error;
    }
  }

  /**
   * Learn from experience and adapt behavior
   */
  async learn() {
    const startTime = Date.now();
    
    try {
      if (this.experienceBuffer.length === 0) {
        return { message: 'No experiences to learn from' };
      }

      // Analyze experiences
      const experiences = [...this.experienceBuffer];
      this.experienceBuffer.length = 0; // Clear buffer
      
      const successfulOperations = experiences.filter(exp => exp.success);
      const failedOperations = experiences.filter(exp => !exp.success);
      
      // Update success rate
      const successRate = successfulOperations.length / experiences.length;
      this.metrics.successRate = (this.metrics.successRate * 0.9) + (successRate * 0.1);
      
      // Learn from failed operations
      const learningInsights = [];
      for (const failure of failedOperations) {
        const insight = this.analyzeFailure(failure);
        if (insight) {
          learningInsights.push(insight);
          this.addToProceduralMemory(`failure_pattern:${failure.type}`, insight);
        }
      }
      
      // Learn from successful patterns
      const successPatterns = this.identifySuccessPatterns(successfulOperations);
      for (const pattern of successPatterns) {
        this.addToProceduralMemory(`success_pattern:${pattern.type}`, pattern);
      }
      
      // Update reputation based on learning
      if (successRate > 0.8) {
        this.reputation = Math.min(1.0, this.reputation + 0.01);
      } else if (successRate < 0.6) {
        this.reputation = Math.max(0.1, this.reputation - 0.01);
      }

      this.metrics.learningEvents++;
      this.updateAverageResponseTime(Date.now() - startTime);
      
      console.log(`Agent ${this.agentId} learned from ${experiences.length} experiences. Success rate: ${(successRate * 100).toFixed(1)}%`);
      this.emit('learningCompleted', { 
        experiencesProcessed: experiences.length,
        successRate,
        insights: learningInsights.length,
        newReputation: this.reputation
      });
      
      return {
        experiencesProcessed: experiences.length,
        successRate,
        insights: learningInsights,
        reputation: this.reputation,
        executionTime: Date.now() - startTime
      };
      
    } catch (error) {
      console.error(`Learning process failed:`, error);
      throw error;
    }
  }

  /**
   * Generate embeddings for text or data (mock implementation)
   */
  async generateEmbeddings(data) {
    // Mock embedding generation - replace with actual embedding model
    return Array(1536).fill(0).map(() => Math.random() * 2 - 1);
  }

  /**
   * Memory management methods
   */
  
  addToWorkingMemory(key, value) {
    // Implement LRU eviction if memory is full
    if (this.workingMemory.size >= this.config.workingMemorySize) {
      const firstKey = this.workingMemory.keys().next().value;
      this.workingMemory.delete(firstKey);
    }
    
    this.workingMemory.set(key, {
      ...value,
      accessedAt: Date.now(),
      accessCount: (this.workingMemory.get(key)?.accessCount || 0) + 1
    });
  }

  addToEpisodicMemory(event) {
    this.episodicMemory.push({
      ...event,
      id: crypto.randomBytes(8).toString('hex'),
      timestamp: new Date().toISOString(),
      agentId: this.agentId
    });
    
    // Limit episodic memory size
    if (this.episodicMemory.length > this.config.episodicMemoryLimit) {
      this.episodicMemory.shift(); // Remove oldest
    }
  }

  addToProceduralMemory(key, procedure) {
    this.proceduralMemory.set(key, {
      ...procedure,
      learnedAt: Date.now(),
      usageCount: (this.proceduralMemory.get(key)?.usageCount || 0) + 1,
      successRate: procedure.successRate || 1.0
    });
  }

  /**
   * Utility and helper methods
   */
  
  generateAgentId() {
    return 'agent-' + crypto.randomBytes(8).toString('hex');
  }

  generateSessionId() {
    return 'session-' + crypto.randomBytes(8).toString('hex');
  }

  generateNodeId() {
    return 'node-' + crypto.randomBytes(8).toString('hex');
  }

  generateCollaborationId() {
    return 'collab-' + crypto.randomBytes(8).toString('hex');
  }

  requiresConsensus(updates) {
    // Simple heuristic - require consensus for critical properties
    const criticalProperties = ['type', 'category', 'importance', 'verified'];
    return Object.keys(updates).some(key => criticalProperties.includes(key));
  }

  calculateUpdateImportance(updates) {
    // Simple importance calculation
    const importantKeys = ['type', 'category', 'verified'];
    const score = Object.keys(updates).reduce((acc, key) => {
      return acc + (importantKeys.includes(key) ? 1 : 0.1);
    }, 0);
    return Math.min(score, 1.0);
  }

  selectKnowledgeForSharing(collaborationType) {
    // Select recent and relevant knowledge from working memory
    const recentItems = Array.from(this.workingMemory.entries())
      .filter(([key]) => key.startsWith('node:'))
      .slice(-10) // Last 10 items
      .map(([key, value]) => ({ key, ...value }));
    
    return recentItems;
  }

  analyzeFailure(failure) {
    // Simple failure analysis
    if (failure.error && failure.error.includes('timeout')) {
      return {
        type: 'timeout_handling',
        recommendation: 'increase_timeout',
        confidence: 0.8
      };
    }
    return null;
  }

  identifySuccessPatterns(successes) {
    // Simple pattern identification
    const patterns = [];
    const fastOperations = successes.filter(op => op.latency < 100);
    
    if (fastOperations.length > successes.length * 0.7) {
      patterns.push({
        type: 'fast_operations',
        threshold: 100,
        successRate: fastOperations.length / successes.length
      });
    }
    
    return patterns;
  }

  constructPaths(nodes, relationships) {
    // Simple path construction
    const paths = [];
    const nodeMap = new Map(nodes.map(n => [n.id, n]));
    
    for (let i = 0; i < Math.min(relationships.length, 5); i++) {
      const rel = relationships[i];
      const fromNode = nodeMap.get(rel.fromNodeId);
      const toNode = nodeMap.get(rel.toNodeId);
      
      if (fromNode && toNode) {
        paths.push({
          nodes: [fromNode, toNode],
          relationships: [rel],
          length: 1,
          weight: rel.properties?.weight || 1.0
        });
      }
    }
    
    return paths;
  }

  updateAverageResponseTime(latency) {
    this.metrics.averageResponseTime = 
      (this.metrics.averageResponseTime * 0.9) + (latency * 0.1);
  }

  recordExperience(experience) {
    this.experienceBuffer.push({
      ...experience,
      timestamp: Date.now(),
      agentId: this.agentId
    });
    
    // Limit buffer size
    if (this.experienceBuffer.length > 1000) {
      this.experienceBuffer.shift();
    }
  }

  setupEventHandlers() {
    // Handle CRDT updates
    this.crdtManager.on('updated', (data) => {
      this.emit('knowledgeUpdated', data);
    });

    // Handle sync events
    this.crdtManager.on('sync', (data) => {
      this.emit('knowledgeSynced', data);
    });
  }

  async loadAgentState() {
    // Load agent's persistent state from storage
    // This would typically load from IPFS or database
    console.log(`Loading state for agent ${this.agentId}...`);
    
    // Mock loading
    const mockState = {
      reputation: 0.85,
      learningHistory: [],
      trustedAgents: []
    };
    
    if (mockState.reputation) {
      this.reputation = mockState.reputation;
    }
  }

  async saveAgentState() {
    // Save agent's state to persistent storage
    const state = {
      agentId: this.agentId,
      reputation: this.reputation,
      metrics: this.metrics,
      proceduralMemory: Array.from(this.proceduralMemory.entries()),
      trustScores: Array.from(this.trustScores.entries()),
      timestamp: new Date().toISOString()
    };
    
    // Would save to IPFS or database
    console.log(`Saving state for agent ${this.agentId}...`);
    return state;
  }

  /**
   * Get comprehensive agent statistics
   */
  getStats() {
    return {
      agentId: this.agentId,
      sessionId: this.sessionId,
      reputation: this.reputation,
      memory: {
        working: this.workingMemory.size,
        episodic: this.episodicMemory.length,
        semantic: this.semanticMemory.size,
        procedural: this.proceduralMemory.size
      },
      collaborations: {
        active: Array.from(this.collaborations.values()).filter(c => c.status === 'active').length,
        total: this.collaborations.size
      },
      operations: {
        queue: this.operationQueue.length,
        active: this.activeOperations.size,
        history: this.operationHistory.length
      },
      trust: {
        trustedAgents: this.trustScores.size,
        averageTrust: Array.from(this.trustScores.values()).reduce((a, b) => a + b, 0) / this.trustScores.size || 0
      },
      metrics: this.metrics
    };
  }

  /**
   * Health check for monitoring
   */
  async healthCheck() {
    return {
      status: 'healthy',
      agentId: this.agentId,
      uptime: Date.now() - (this.startTime || Date.now()),
      operationsPerformed: this.metrics.operationsPerformed,
      averageResponseTime: this.metrics.averageResponseTime,
      successRate: this.metrics.successRate,
      reputation: this.reputation,
      memoryUtilization: {
        working: this.workingMemory.size / this.config.workingMemorySize,
        episodic: this.episodicMemory.length / this.config.episodicMemoryLimit
      },
      lastCheck: new Date().toISOString()
    };
  }

  /**
   * Graceful shutdown
   */
  async shutdown() {
    console.log(`Shutting down agent ${this.agentId}...`);
    
    // Save current state
    await this.saveAgentState();
    
    // Stop CRDT sync
    if (this.crdtManager) {
      this.crdtManager.stopPeriodicSync();
    }
    
    // Close system connections
    if (this.syncManager) await this.syncManager.shutdown();
    if (this.consensus) await this.consensus.close();
    if (this.cache) await this.cache.close();
    if (this.vectorDb) await this.vectorDb.close();
    if (this.ipfs) await this.ipfs.close();
    if (this.neo4j) await this.neo4j.close();
    
    console.log(`Agent ${this.agentId} shut down gracefully`);
    this.emit('shutdown');
  }
}

module.exports = KnowledgeGraphAgent;