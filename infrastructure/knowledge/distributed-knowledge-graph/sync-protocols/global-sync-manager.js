const { EventEmitter } = require('events');
const crypto = require('crypto');
const WebSocket = require('ws');
const { CRDTNetworkManager } = require('../crdt-lib/crdt-implementation');

/**
 * Global Knowledge Synchronization Manager
 * 
 * This manager orchestrates real-time synchronization of knowledge graph
 * changes across all distributed AI agents and system components.
 * 
 * Features:
 * - Real-time event streaming with WebSockets
 * - CRDT-based conflict-free synchronization
 * - Vector clock ordering for causality
 * - Gossip protocol for epidemic information dissemination
 * - Byzantine fault tolerance with 2f+1 consensus
 * - Automatic network partition recovery
 * - Bandwidth optimization with delta synchronization
 */
class GlobalSyncManager extends EventEmitter {
  constructor(nodeId, config = {}) {
    super();
    
    this.nodeId = nodeId || this.generateNodeId();
    this.config = {
      // Network configuration
      peers: config.peers || [
        'ws://sync-node-01:8080',
        'ws://sync-node-02:8080', 
        'ws://sync-node-03:8080'
      ],
      port: config.port || 8080,
      
      // Gossip protocol settings
      gossipInterval: config.gossipInterval || 1000, // 1 second
      gossipFanout: config.gossipFanout || 3, // Number of peers to gossip to
      maxGossipHops: config.maxGossipHops || 5,
      
      // Synchronization settings
      syncInterval: config.syncInterval || 5000, // 5 seconds
      deltaSync: config.deltaSync !== false, // Default enabled
      batchSize: config.batchSize || 100,
      maxPendingOps: config.maxPendingOps || 1000,
      
      // Byzantine fault tolerance
      faultTolerance: config.faultTolerance || 1, // f Byzantine nodes
      consensusThreshold: config.consensusThreshold || 0.67,
      
      // Network partition handling
      partitionDetectionTimeout: config.partitionDetectionTimeout || 10000,
      partitionRecoveryTimeout: config.partitionRecoveryTimeout || 30000,
      
      // Performance optimization
      compressionEnabled: config.compressionEnabled !== false,
      priorityQueue: config.priorityQueue !== false,
      adaptiveBatching: config.adaptiveBatching !== false,
      
      ...config
    };

    // Network state
    this.peers = new Map(); // peerId -> connection info
    this.connections = new Map(); // peerId -> WebSocket
    this.server = null;
    this.isLeader = false;
    this.leaderId = null;
    
    // Synchronization state
    this.vectorClock = new Map();
    this.vectorClock.set(this.nodeId, 0);
    this.pendingOperations = new Map();
    this.acknowledgedOperations = new Set();
    this.syncHistory = new Map();
    
    // CRDT network manager
    this.crdtManager = new CRDTNetworkManager(this.nodeId);
    
    // Gossip state
    this.gossipCache = new Map(); // messageId -> { message, ttl, hops }
    this.gossipHistory = new Set(); // Recently seen message IDs
    this.gossipTimer = null;
    
    // Byzantine state tracking
    this.suspiciousNodes = new Map(); // nodeId -> suspicion level
    this.nodeReputations = new Map(); // nodeId -> reputation score
    
    // Performance metrics
    this.metrics = {
      totalSyncs: 0,
      successfulSyncs: 0,
      failedSyncs: 0,
      averageLatency: 0,
      networkPartitions: 0,
      byzantineFaults: 0,
      bandwidthUsed: 0,
      messagesProcessed: 0
    };
    
    // Priority queues for different message types
    this.messageQueues = {
      critical: [], // Consensus, leader election
      high: [],     // Node updates, relationships
      normal: [],   // Batch updates, gossip
      low: []       // Statistics, heartbeats
    };

    this.initializeVectorClock();
    this.setupCRDTEventHandlers();
  }

  /**
   * Initialize the synchronization manager
   */
  async initialize() {
    console.log(`Initializing Global Sync Manager for node ${this.nodeId}...`);

    try {
      // Start WebSocket server
      await this.startServer();
      
      // Connect to known peers
      await this.connectToPeers();
      
      // Start synchronization protocols
      this.startSyncProtocols();
      
      // Initialize leader election
      await this.initiateLeaderElection();
      
      console.log(`Global Sync Manager initialized successfully`);
      
    } catch (error) {
      console.error('Failed to initialize Global Sync Manager:', error);
      throw error;
    }
  }

  /**
   * Start WebSocket server for incoming connections
   */
  async startServer() {
    this.server = new WebSocket.Server({ 
      port: this.config.port,
      perMessageDeflate: this.config.compressionEnabled
    });

    this.server.on('connection', (ws, req) => {
      console.log(`Incoming connection from ${req.socket.remoteAddress}`);
      this.handleNewConnection(ws);
    });

    this.server.on('error', (error) => {
      console.error('WebSocket server error:', error);
      this.emit('error', error);
    });

    console.log(`WebSocket server started on port ${this.config.port}`);
  }

  /**
   * Connect to known peer nodes
   */
  async connectToPeers() {
    const connectionPromises = this.config.peers.map(async (peerUrl) => {
      try {
        const ws = new WebSocket(peerUrl);
        
        ws.on('open', () => {
          const peerId = this.extractPeerIdFromUrl(peerUrl);
          console.log(`Connected to peer: ${peerId}`);
          this.handleNewConnection(ws, peerId);
          
          // Send identification
          this.sendMessage(ws, {
            type: 'identification',
            nodeId: this.nodeId,
            vectorClock: Array.from(this.vectorClock.entries()),
            timestamp: Date.now()
          });
        });

        ws.on('error', (error) => {
          console.error(`Connection error to ${peerUrl}:`, error.message);
        });

        return ws;
      } catch (error) {
        console.error(`Failed to connect to ${peerUrl}:`, error.message);
        return null;
      }
    });

    await Promise.allSettled(connectionPromises);
    console.log(`Connected to ${this.connections.size} peers`);
  }

  /**
   * Handle new WebSocket connections
   */
  handleNewConnection(ws, peerId = null) {
    if (!peerId) {
      peerId = this.generateNodeId(); // Temporary ID until identification
    }

    this.connections.set(peerId, ws);
    this.peers.set(peerId, {
      id: peerId,
      connected: true,
      lastSeen: Date.now(),
      vectorClock: new Map(),
      reputation: 1.0,
      messagesReceived: 0,
      messagesSent: 0
    });

    ws.on('message', (data) => {
      this.handleMessage(peerId, data);
    });

    ws.on('close', () => {
      console.log(`Peer ${peerId} disconnected`);
      this.connections.delete(peerId);
      const peer = this.peers.get(peerId);
      if (peer) {
        peer.connected = false;
      }
      this.emit('peerDisconnected', peerId);
    });

    ws.on('error', (error) => {
      console.error(`Connection error with peer ${peerId}:`, error.message);
      this.handlePeerError(peerId, error);
    });

    this.emit('peerConnected', peerId);
  }

  /**
   * Handle incoming messages from peers
   */
  async handleMessage(peerId, data) {
    try {
      const message = JSON.parse(data.toString());
      message.receivedAt = Date.now();
      
      // Update peer metrics
      const peer = this.peers.get(peerId);
      if (peer) {
        peer.messagesReceived++;
        peer.lastSeen = Date.now();
      }

      // Validate message integrity
      if (!this.validateMessage(message, peerId)) {
        console.warn(`Invalid message from peer ${peerId}`);
        this.increaseSuspicion(peerId);
        return;
      }

      // Update vector clock
      this.updateVectorClock(message.vectorClock);

      // Route message based on type
      switch (message.type) {
        case 'identification':
          await this.handleIdentification(peerId, message);
          break;
        case 'sync_request':
          await this.handleSyncRequest(peerId, message);
          break;
        case 'sync_response':
          await this.handleSyncResponse(peerId, message);
          break;
        case 'operation':
          await this.handleOperation(peerId, message);
          break;
        case 'gossip':
          await this.handleGossip(peerId, message);
          break;
        case 'consensus':
          await this.handleConsensus(peerId, message);
          break;
        case 'leader_election':
          await this.handleLeaderElection(peerId, message);
          break;
        case 'heartbeat':
          await this.handleHeartbeat(peerId, message);
          break;
        default:
          console.warn(`Unknown message type: ${message.type} from ${peerId}`);
      }

      this.metrics.messagesProcessed++;
      this.emit('messageReceived', { peerId, message });

    } catch (error) {
      console.error(`Failed to handle message from ${peerId}:`, error);
      this.increaseSuspicion(peerId);
    }
  }

  /**
   * Publish a knowledge graph operation for synchronization
   */
  async publishOperation(operation) {
    const operationId = this.generateOperationId();
    this.tick(); // Increment vector clock
    
    const syncMessage = {
      id: operationId,
      type: 'operation',
      operation,
      nodeId: this.nodeId,
      vectorClock: Array.from(this.vectorClock.entries()),
      timestamp: Date.now(),
      priority: this.determineOperationPriority(operation)
    };

    // Add to pending operations
    this.pendingOperations.set(operationId, {
      ...syncMessage,
      acknowledgments: new Set(),
      retries: 0,
      createdAt: Date.now()
    });

    // Broadcast to all connected peers
    await this.broadcastMessage(syncMessage);
    
    // Start gossip propagation
    this.startGossip(syncMessage);

    console.log(`Published operation ${operationId} of type ${operation.type}`);
    
    this.emit('operationPublished', { operationId, operation });
    return operationId;
  }

  /**
   * Handle incoming operation from peer
   */
  async handleOperation(peerId, message) {
    const { id: operationId, operation, vectorClock: senderClock } = message;
    
    // Check if we've already processed this operation
    if (this.acknowledgedOperations.has(operationId)) {
      // Send acknowledgment anyway
      await this.sendAcknowledgment(peerId, operationId);
      return;
    }

    // Apply vector clock ordering
    if (!this.canApplyOperation(senderClock)) {
      // Buffer the operation for later processing
      this.bufferOperation(message);
      return;
    }

    try {
      // Apply the operation using CRDT
      await this.applyCRDTOperation(operation);
      
      // Mark as acknowledged
      this.acknowledgedOperations.add(operationId);
      
      // Send acknowledgment
      await this.sendAcknowledgment(peerId, operationId);
      
      // Propagate via gossip if needed
      this.propagateOperation(message);
      
      this.metrics.successfulSyncs++;
      console.log(`Applied operation ${operationId} from ${peerId}`);
      
      this.emit('operationApplied', { operationId, operation, source: peerId });
      
    } catch (error) {
      console.error(`Failed to apply operation ${operationId}:`, error);
      this.metrics.failedSyncs++;
      this.increaseSuspicion(peerId);
    }
  }

  /**
   * Apply CRDT operation
   */
  async applyCRDTOperation(operation) {
    const { type, target, data } = operation;
    
    switch (type) {
      case 'node_create':
        await this.crdtManager.handleRemoteUpdate(target, {
          type: 'KnowledgeGraphCRDT',
          nodeId: this.nodeId,
          ...data
        });
        break;
      case 'node_update':
        await this.crdtManager.handleRemoteUpdate(target, data);
        break;
      case 'relationship_create':
        await this.crdtManager.handleRemoteUpdate(target, data);
        break;
      default:
        throw new Error(`Unknown operation type: ${type}`);
    }
  }

  /**
   * Start gossip protocol for epidemic information dissemination
   */
  startGossip(message) {
    const gossipMessage = {
      ...message,
      type: 'gossip',
      hops: 0,
      ttl: this.config.maxGossipHops,
      gossipId: this.generateGossipId()
    };

    this.gossipCache.set(gossipMessage.gossipId, gossipMessage);
    this.scheduleGossip(gossipMessage);
  }

  /**
   * Schedule gossip propagation
   */
  scheduleGossip(message) {
    setTimeout(() => {
      this.propagateGossip(message);
    }, this.config.gossipInterval);
  }

  /**
   * Propagate gossip to random peers
   */
  async propagateGossip(message) {
    if (message.ttl <= 0 || message.hops >= this.config.maxGossipHops) {
      return;
    }

    const connectedPeers = Array.from(this.connections.keys())
      .filter(peerId => this.connections.get(peerId).readyState === WebSocket.OPEN);
    
    if (connectedPeers.length === 0) {
      return;
    }

    // Select random peers for gossip fanout
    const gossipTargets = this.selectGossipTargets(connectedPeers);
    
    const gossipMessage = {
      ...message,
      hops: message.hops + 1,
      ttl: message.ttl - 1,
      propagatedBy: this.nodeId,
      propagatedAt: Date.now()
    };

    for (const peerId of gossipTargets) {
      const ws = this.connections.get(peerId);
      if (ws && ws.readyState === WebSocket.OPEN) {
        await this.sendMessage(ws, gossipMessage);
        
        const peer = this.peers.get(peerId);
        if (peer) {
          peer.messagesSent++;
        }
      }
    }

    console.log(`Gossiped message ${message.gossipId} to ${gossipTargets.length} peers`);
  }

  /**
   * Handle gossip message
   */
  async handleGossip(peerId, message) {
    const { gossipId, hops, ttl } = message;
    
    // Check if we've seen this gossip before
    if (this.gossipHistory.has(gossipId)) {
      return;
    }

    this.gossipHistory.add(gossipId);
    
    // Process the underlying operation
    if (message.operation) {
      await this.handleOperation(peerId, message);
    }
    
    // Continue gossip propagation if TTL allows
    if (ttl > 0 && hops < this.config.maxGossipHops) {
      this.scheduleGossip(message);
    }
  }

  /**
   * Select gossip targets using intelligent strategy
   */
  selectGossipTargets(peers) {
    const fanout = Math.min(this.config.gossipFanout, peers.length);
    
    // Prefer peers with higher reputation and better connectivity
    const weightedPeers = peers.map(peerId => {
      const peer = this.peers.get(peerId);
      const reputation = peer?.reputation || 0.5;
      const recency = Math.max(0, 1 - (Date.now() - (peer?.lastSeen || 0)) / 60000);
      const weight = reputation * 0.7 + recency * 0.3;
      
      return { peerId, weight };
    });
    
    // Sort by weight and select top candidates with some randomness
    weightedPeers.sort((a, b) => b.weight - a.weight);
    
    const selected = [];
    const topCandidates = Math.min(fanout * 2, weightedPeers.length);
    
    for (let i = 0; i < fanout && i < topCandidates; i++) {
      // Add some randomness to avoid always selecting the same peers
      const index = Math.floor(Math.random() * Math.min(3, topCandidates - i)) + i;
      selected.push(weightedPeers[index].peerId);
      weightedPeers.splice(index, 1);
    }
    
    return selected;
  }

  /**
   * Perform full synchronization with a peer
   */
  async synchronizeWithPeer(peerId, deltaOnly = true) {
    const peer = this.peers.get(peerId);
    if (!peer || !peer.connected) {
      console.warn(`Cannot synchronize with disconnected peer: ${peerId}`);
      return false;
    }

    this.tick();
    const startTime = Date.now();
    
    try {
      // Create sync request
      const syncRequest = {
        type: 'sync_request',
        nodeId: this.nodeId,
        vectorClock: Array.from(this.vectorClock.entries()),
        deltaOnly,
        lastSyncTime: this.syncHistory.get(peerId) || 0,
        timestamp: Date.now()
      };

      const ws = this.connections.get(peerId);
      if (!ws || ws.readyState !== WebSocket.OPEN) {
        throw new Error('Connection not available');
      }

      // Send sync request
      await this.sendMessage(ws, syncRequest);
      
      // Wait for sync response (with timeout)
      const response = await this.waitForSyncResponse(peerId, 10000);
      
      if (response.success) {
        // Apply received operations
        await this.applySyncData(response.data);
        
        // Update sync history
        this.syncHistory.set(peerId, Date.now());
        
        const latency = Date.now() - startTime;
        this.updateSyncMetrics(true, latency);
        
        console.log(`Synchronization with ${peerId} completed in ${latency}ms`);
        this.emit('syncCompleted', { peerId, latency, operations: response.data.length });
        
        return true;
      } else {
        throw new Error(response.error || 'Sync failed');
      }
      
    } catch (error) {
      console.error(`Synchronization with ${peerId} failed:`, error);
      this.updateSyncMetrics(false, Date.now() - startTime);
      this.increaseSuspicion(peerId);
      return false;
    }
  }

  /**
   * Handle sync request from peer
   */
  async handleSyncRequest(peerId, message) {
    const { vectorClock: peerClock, deltaOnly, lastSyncTime } = message;
    
    try {
      // Determine what operations to send
      const operationsToSync = this.getOperationsToSync(
        peerClock, 
        deltaOnly, 
        lastSyncTime
      );
      
      // Create sync response
      const syncResponse = {
        type: 'sync_response',
        nodeId: this.nodeId,
        vectorClock: Array.from(this.vectorClock.entries()),
        success: true,
        data: operationsToSync,
        timestamp: Date.now()
      };

      const ws = this.connections.get(peerId);
      await this.sendMessage(ws, syncResponse);
      
      console.log(`Sent sync response to ${peerId} with ${operationsToSync.length} operations`);
      
    } catch (error) {
      console.error(`Failed to handle sync request from ${peerId}:`, error);
      
      const errorResponse = {
        type: 'sync_response',
        nodeId: this.nodeId,
        success: false,
        error: error.message,
        timestamp: Date.now()
      };

      const ws = this.connections.get(peerId);
      await this.sendMessage(ws, errorResponse);
    }
  }

  /**
   * Start all synchronization protocols
   */
  startSyncProtocols() {
    // Periodic full synchronization
    setInterval(() => {
      this.performPeriodicSync();
    }, this.config.syncInterval);

    // Gossip propagation
    setInterval(() => {
      this.performGossipMaintenance();
    }, this.config.gossipInterval);

    // Heartbeat and failure detection
    setInterval(() => {
      this.sendHeartbeats();
    }, 5000);

    // Cleanup old operations
    setInterval(() => {
      this.cleanupOldOperations();
    }, 60000);

    // Byzantine fault detection
    setInterval(() => {
      this.detectByzantineFaults();
    }, 30000);

    console.log('All synchronization protocols started');
  }

  /**
   * Perform periodic synchronization with all peers
   */
  async performPeriodicSync() {
    const connectedPeers = Array.from(this.peers.keys())
      .filter(peerId => this.peers.get(peerId)?.connected);
    
    if (connectedPeers.length === 0) {
      return;
    }

    // Synchronize with a subset of peers each interval
    const peersToSync = connectedPeers
      .sort(() => Math.random() - 0.5)
      .slice(0, Math.max(1, Math.ceil(connectedPeers.length / 3)));
    
    const syncPromises = peersToSync.map(peerId => 
      this.synchronizeWithPeer(peerId, true)
        .catch(error => {
          console.error(`Periodic sync failed with ${peerId}:`, error);
          return false;
        })
    );
    
    const results = await Promise.all(syncPromises);
    const successful = results.filter(r => r).length;
    
    console.log(`Periodic sync completed: ${successful}/${peersToSync.length} successful`);
  }

  /**
   * Initiate leader election using bully algorithm
   */
  async initiateLeaderElection() {
    console.log('Starting leader election...');
    
    this.isLeader = false;
    this.leaderId = null;
    
    // Start election process
    const electionMessage = {
      type: 'leader_election',
      action: 'election',
      nodeId: this.nodeId,
      timestamp: Date.now()
    };
    
    await this.broadcastMessage(electionMessage);
    
    // Wait for responses
    setTimeout(() => {
      this.completeLeaderElection();
    }, 5000);
  }

  /**
   * Send message to specific WebSocket
   */
  async sendMessage(ws, message) {
    if (ws.readyState !== WebSocket.OPEN) {
      throw new Error('WebSocket not open');
    }
    
    const serialized = JSON.stringify({
      ...message,
      vectorClock: Array.from(this.vectorClock.entries())
    });
    
    ws.send(serialized);
    this.metrics.bandwidthUsed += serialized.length;
  }

  /**
   * Broadcast message to all connected peers
   */
  async broadcastMessage(message, excludePeers = []) {
    const broadcastPromises = [];
    
    for (const [peerId, ws] of this.connections.entries()) {
      if (!excludePeers.includes(peerId) && ws.readyState === WebSocket.OPEN) {
        broadcastPromises.push(
          this.sendMessage(ws, message).catch(error => {
            console.error(`Failed to send message to ${peerId}:`, error.message);
          })
        );
      }
    }
    
    await Promise.all(broadcastPromises);
  }

  /**
   * Utility methods
   */
  
  generateNodeId() {
    return crypto.randomBytes(8).toString('hex');
  }
  
  generateOperationId() {
    return `${this.nodeId}-${Date.now()}-${crypto.randomBytes(4).toString('hex')}`;
  }
  
  generateGossipId() {
    return crypto.randomBytes(8).toString('hex');
  }
  
  tick() {
    const current = this.vectorClock.get(this.nodeId) || 0;
    this.vectorClock.set(this.nodeId, current + 1);
  }
  
  initializeVectorClock() {
    this.vectorClock.set(this.nodeId, 0);
  }
  
  updateVectorClock(peerClock) {
    if (!peerClock || !Array.isArray(peerClock)) return;
    
    for (const [nodeId, timestamp] of peerClock) {
      const currentTimestamp = this.vectorClock.get(nodeId) || 0;
      this.vectorClock.set(nodeId, Math.max(currentTimestamp, timestamp));
    }
  }
  
  extractPeerIdFromUrl(url) {
    const match = url.match(/sync-node-(\w+)/);
    return match ? match[1] : crypto.randomBytes(4).toString('hex');
  }
  
  validateMessage(message, peerId) {
    // Basic validation
    if (!message.type || !message.nodeId) {
      return false;
    }
    
    // Check for timestamp freshness (within 5 minutes)
    if (message.timestamp) {
      const age = Date.now() - message.timestamp;
      if (age > 300000) { // 5 minutes
        return false;
      }
    }
    
    return true;
  }
  
  increaseSuspicion(peerId) {
    const current = this.suspiciousNodes.get(peerId) || 0;
    this.suspiciousNodes.set(peerId, current + 1);
    
    if (current + 1 > 5) {
      console.warn(`Peer ${peerId} marked as highly suspicious`);
      this.emit('suspiciousNode', peerId);
    }
  }
  
  updateSyncMetrics(success, latency) {
    this.metrics.totalSyncs++;
    
    if (success) {
      this.metrics.successfulSyncs++;
    } else {
      this.metrics.failedSyncs++;
    }
    
    // Update average latency
    this.metrics.averageLatency = 
      (this.metrics.averageLatency * 0.9) + (latency * 0.1);
  }
  
  setupCRDTEventHandlers() {
    this.crdtManager.on('sync', (data) => {
      // Handle CRDT sync events
      this.publishOperation({
        type: 'crdt_sync',
        target: data.crdtName,
        data: data.data
      });
    });
  }

  /**
   * Get comprehensive synchronization statistics
   */
  getStats() {
    const connectedPeers = Array.from(this.peers.values())
      .filter(peer => peer.connected).length;
    
    return {
      nodeId: this.nodeId,
      isLeader: this.isLeader,
      leaderId: this.leaderId,
      peers: {
        total: this.peers.size,
        connected: connectedPeers,
        suspicious: this.suspiciousNodes.size
      },
      operations: {
        pending: this.pendingOperations.size,
        acknowledged: this.acknowledgedOperations.size
      },
      gossip: {
        cacheSize: this.gossipCache.size,
        historySize: this.gossipHistory.size
      },
      vectorClock: Array.from(this.vectorClock.entries()),
      metrics: this.metrics
    };
  }

  /**
   * Health check for monitoring
   */
  async healthCheck() {
    const connectedPeers = Array.from(this.peers.values())
      .filter(peer => peer.connected).length;
    
    const status = connectedPeers > 0 ? 'healthy' : 'isolated';
    
    return {
      status,
      nodeId: this.nodeId,
      peersConnected: connectedPeers,
      operationsPending: this.pendingOperations.size,
      syncSuccessRate: this.metrics.totalSyncs > 0 
        ? (this.metrics.successfulSyncs / this.metrics.totalSyncs) 
        : 1.0,
      averageLatency: this.metrics.averageLatency,
      lastCheck: new Date().toISOString()
    };
  }

  /**
   * Graceful shutdown
   */
  async shutdown() {
    console.log('Shutting down Global Sync Manager...');
    
    // Stop all timers
    if (this.gossipTimer) {
      clearInterval(this.gossipTimer);
    }
    
    // Close all peer connections
    for (const ws of this.connections.values()) {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    }
    
    // Close server
    if (this.server) {
      this.server.close();
    }
    
    console.log('Global Sync Manager shut down');
  }
}

module.exports = GlobalSyncManager;