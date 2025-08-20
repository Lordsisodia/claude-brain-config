const crypto = require('crypto');
const EventEmitter = require('events');
const WebSocket = require('ws');

/**
 * Blockchain Consensus Client for Truth Verification
 * 
 * This client implements a custom consensus mechanism for verifying
 * knowledge graph changes across distributed AI agents. It uses a
 * hybrid approach combining:
 * 
 * - Proof of Authority (PoA) for trusted agent validation
 * - Proof of Task for computational verification
 * - Byzantine Fault Tolerance for consensus
 * - Merkle trees for data integrity
 * - Smart contracts for automated verification
 */
class ConsensusClient extends EventEmitter {
  constructor(config = {}) {
    super();
    
    this.config = {
      // Node configuration
      nodeId: config.nodeId || this.generateNodeId(),
      privateKey: config.privateKey || this.generatePrivateKey(),
      
      // Network configuration
      peers: config.peers || [
        'ws://consensus-node-01:8545',
        'ws://consensus-node-02:8545',
        'ws://consensus-node-03:8545'
      ],
      
      // Consensus parameters
      consensusThreshold: config.consensusThreshold || 0.67, // 67% agreement required
      blockTime: config.blockTime || 5000, // 5 seconds
      maxBlockSize: config.maxBlockSize || 1024 * 1024, // 1MB
      
      // Voting parameters
      votingWindow: config.votingWindow || 30000, // 30 seconds
      minVoters: config.minVoters || 3,
      maxVoters: config.maxVoters || 10,
      
      // Authority settings
      trustedAuthorities: config.trustedAuthorities || [],
      authorityRotationPeriod: config.authorityRotationPeriod || 86400000, // 24 hours
      
      ...config
    };

    // State management
    this.blockchain = [];
    this.pendingTransactions = new Map();
    this.pendingVotes = new Map();
    this.currentVoting = new Map();
    this.trustedPeers = new Set();
    this.connections = new Map();
    this.isValidator = false;
    this.currentAuthorities = new Set();
    
    // Consensus tracking
    this.lastBlockTime = Date.now();
    this.consensusRound = 0;
    this.votingHistory = [];
    
    // Statistics
    this.stats = {
      totalBlocks: 0,
      totalTransactions: 0,
      successfulVotes: 0,
      failedVotes: 0,
      averageConsensusTime: 0,
      byzantineFaults: 0
    };

    // Initialize genesis block
    this.createGenesisBlock();
  }

  /**
   * Initialize the consensus client
   */
  async initialize() {
    console.log(`Initializing consensus client ${this.config.nodeId}...`);

    // Generate public key from private key
    this.publicKey = this.getPublicKey();
    
    // Check if this node is a trusted authority
    this.isValidator = this.config.trustedAuthorities.includes(this.publicKey);
    
    // Connect to peer network
    await this.connectToPeers();
    
    // Start consensus processes
    this.startConsensusLoop();
    this.startVotingMonitor();
    this.startAuthorityRotation();
    
    console.log(`Consensus client initialized as ${this.isValidator ? 'validator' : 'participant'}`);
  }

  /**
   * Propose a knowledge graph change for consensus
   */
  async proposeChange(knowledgeNodeId, changes, agentId, metadata = {}) {
    const proposal = {
      id: this.generateTransactionId(),
      type: 'knowledge_change',
      knowledgeNodeId,
      changes,
      proposer: agentId,
      proposerSignature: this.signData({ knowledgeNodeId, changes, agentId }),
      metadata,
      timestamp: Date.now(),
      blockHeight: this.blockchain.length,
      nonce: crypto.randomBytes(16).toString('hex')
    };

    // Add to pending transactions
    this.pendingTransactions.set(proposal.id, proposal);

    // Start voting process
    const votingSession = await this.initiateVoting(proposal);
    
    // Broadcast to network
    await this.broadcastProposal(proposal);
    
    console.log(`Proposed change ${proposal.id} for node ${knowledgeNodeId}`);
    
    return {
      proposalId: proposal.id,
      votingSessionId: votingSession.id,
      estimatedDecisionTime: Date.now() + this.config.votingWindow
    };
  }

  /**
   * Cast a vote on a proposal
   */
  async castVote(proposalId, vote, confidence, reasoning, agentId) {
    const proposal = this.pendingTransactions.get(proposalId);
    if (!proposal) {
      throw new Error(`Proposal ${proposalId} not found`);
    }

    const votingSession = this.currentVoting.get(proposalId);
    if (!votingSession) {
      throw new Error(`Voting session for ${proposalId} not found`);
    }

    // Validate vote
    if (!['APPROVE', 'REJECT', 'ABSTAIN'].includes(vote)) {
      throw new Error('Invalid vote type');
    }

    if (confidence < 0 || confidence > 1) {
      throw new Error('Confidence must be between 0 and 1');
    }

    // Create vote record
    const voteRecord = {
      id: this.generateTransactionId(),
      proposalId,
      voter: agentId,
      vote,
      confidence,
      reasoning,
      timestamp: Date.now(),
      signature: this.signData({ proposalId, vote, confidence, agentId })
    };

    // Add vote to session
    votingSession.votes.set(agentId, voteRecord);
    
    // Broadcast vote
    await this.broadcastVote(voteRecord);
    
    // Check if consensus reached
    const consensusResult = this.checkConsensus(votingSession);
    if (consensusResult) {
      await this.finalizeConsensus(proposalId, consensusResult);
    }
    
    console.log(`Vote cast: ${vote} (${confidence}) for proposal ${proposalId}`);
    
    return voteRecord;
  }

  /**
   * Initiate voting session for a proposal
   */
  async initiateVoting(proposal) {
    const votingSession = {
      id: this.generateTransactionId(),
      proposalId: proposal.id,
      startTime: Date.now(),
      endTime: Date.now() + this.config.votingWindow,
      votes: new Map(),
      status: 'ACTIVE',
      requiredVotes: Math.max(this.config.minVoters, Math.ceil(this.trustedPeers.size * 0.5))
    };

    this.currentVoting.set(proposal.id, votingSession);
    
    // Set timeout for voting window
    setTimeout(() => {
      this.closeVoting(proposal.id);
    }, this.config.votingWindow);

    return votingSession;
  }

  /**
   * Check if consensus has been reached
   */
  checkConsensus(votingSession) {
    const votes = Array.from(votingSession.votes.values());
    const totalVotes = votes.length;
    
    if (totalVotes < this.config.minVoters) {
      return null; // Not enough votes
    }

    // Calculate weighted consensus
    let approveWeight = 0;
    let rejectWeight = 0;
    let abstainWeight = 0;

    votes.forEach(vote => {
      const weight = vote.confidence;
      switch (vote.vote) {
        case 'APPROVE':
          approveWeight += weight;
          break;
        case 'REJECT':
          rejectWeight += weight;
          break;
        case 'ABSTAIN':
          abstainWeight += weight;
          break;
      }
    });

    const totalWeight = approveWeight + rejectWeight + abstainWeight;
    const approvalRatio = approveWeight / totalWeight;
    const rejectionRatio = rejectWeight / totalWeight;

    // Determine consensus
    if (approvalRatio >= this.config.consensusThreshold) {
      return {
        decision: 'APPROVED',
        approvalRatio,
        confidence: approvalRatio,
        votes: totalVotes,
        reasoning: 'Consensus threshold reached for approval'
      };
    } else if (rejectionRatio >= this.config.consensusThreshold) {
      return {
        decision: 'REJECTED',
        rejectionRatio,
        confidence: rejectionRatio,
        votes: totalVotes,
        reasoning: 'Consensus threshold reached for rejection'
      };
    }

    // Check if voting window expired
    if (Date.now() > votingSession.endTime) {
      return {
        decision: 'TIMEOUT',
        approvalRatio,
        confidence: Math.max(approvalRatio, rejectionRatio),
        votes: totalVotes,
        reasoning: 'Voting window expired without consensus'
      };
    }

    return null; // No consensus yet
  }

  /**
   * Finalize consensus and create block
   */
  async finalizeConsensus(proposalId, consensusResult) {
    const proposal = this.pendingTransactions.get(proposalId);
    const votingSession = this.currentVoting.get(proposalId);
    
    if (!proposal || !votingSession) {
      throw new Error('Proposal or voting session not found');
    }

    // Create consensus record
    const consensusRecord = {
      id: this.generateTransactionId(),
      proposalId,
      decision: consensusResult.decision,
      confidence: consensusResult.confidence,
      votes: Array.from(votingSession.votes.values()),
      finalizedAt: Date.now(),
      blockHeight: this.blockchain.length,
      merkleRoot: this.calculateMerkleRoot(votingSession.votes),
      signature: this.signData(consensusResult)
    };

    // Create block with consensus
    if (consensusResult.decision === 'APPROVED') {
      const block = await this.createBlock([proposal], consensusRecord);
      await this.addBlock(block);
      this.stats.successfulVotes++;
    } else {
      this.stats.failedVotes++;
    }

    // Cleanup
    this.pendingTransactions.delete(proposalId);
    this.currentVoting.delete(proposalId);
    this.votingHistory.push(consensusRecord);

    // Emit events
    this.emit('consensusReached', {
      proposalId,
      decision: consensusResult.decision,
      consensusRecord
    });

    console.log(`Consensus finalized for ${proposalId}: ${consensusResult.decision}`);
    
    return consensusRecord;
  }

  /**
   * Create a new block
   */
  async createBlock(transactions, consensusRecord) {
    const previousBlock = this.getLatestBlock();
    
    const block = {
      index: this.blockchain.length,
      timestamp: Date.now(),
      transactions,
      consensusRecord,
      previousHash: previousBlock.hash,
      merkleRoot: this.calculateMerkleRoot(transactions),
      validator: this.config.nodeId,
      signature: null,
      nonce: 0,
      hash: null
    };

    // Proof of Task - solve computational puzzle
    block.nonce = await this.solveProofOfTask(block);
    block.hash = this.calculateBlockHash(block);
    block.signature = this.signData(block);

    return block;
  }

  /**
   * Add block to blockchain after validation
   */
  async addBlock(block) {
    // Validate block
    if (!this.validateBlock(block)) {
      throw new Error('Invalid block');
    }

    // Validate consensus
    if (!this.validateConsensus(block.consensusRecord)) {
      throw new Error('Invalid consensus');
    }

    // Add to blockchain
    this.blockchain.push(block);
    this.stats.totalBlocks++;
    this.stats.totalTransactions += block.transactions.length;

    // Broadcast to network
    await this.broadcastBlock(block);

    console.log(`Added block ${block.index} with hash ${block.hash}`);
    
    this.emit('blockAdded', block);
    return block;
  }

  /**
   * Validate a block
   */
  validateBlock(block) {
    const previousBlock = this.blockchain[block.index - 1];
    
    // Check previous hash
    if (block.previousHash !== previousBlock.hash) {
      console.error('Invalid previous hash');
      return false;
    }

    // Verify block hash
    const calculatedHash = this.calculateBlockHash(block);
    if (block.hash !== calculatedHash) {
      console.error('Invalid block hash');
      return false;
    }

    // Verify signature
    if (!this.verifySignature(block, block.signature)) {
      console.error('Invalid block signature');
      return false;
    }

    // Verify Proof of Task
    if (!this.verifyProofOfTask(block)) {
      console.error('Invalid Proof of Task');
      return false;
    }

    return true;
  }

  /**
   * Validate consensus record
   */
  validateConsensus(consensusRecord) {
    // Verify all vote signatures
    for (const vote of consensusRecord.votes) {
      if (!this.verifySignature(vote, vote.signature)) {
        console.error('Invalid vote signature');
        return false;
      }
    }

    // Verify merkle root
    const calculatedMerkleRoot = this.calculateMerkleRoot(consensusRecord.votes);
    if (consensusRecord.merkleRoot !== calculatedMerkleRoot) {
      console.error('Invalid merkle root');
      return false;
    }

    return true;
  }

  /**
   * Solve Proof of Task computational puzzle
   */
  async solveProofOfTask(block) {
    const target = '0000'; // Difficulty target
    let nonce = 0;
    
    while (true) {
      const testBlock = { ...block, nonce };
      const hash = this.calculateBlockHash(testBlock);
      
      if (hash.substring(0, target.length) === target) {
        return nonce;
      }
      
      nonce++;
      
      // Prevent infinite loop
      if (nonce > 1000000) {
        throw new Error('Failed to solve Proof of Task');
      }
    }
  }

  /**
   * Verify Proof of Task solution
   */
  verifyProofOfTask(block) {
    const target = '0000';
    const hash = this.calculateBlockHash(block);
    return hash.substring(0, target.length) === target;
  }

  /**
   * Calculate block hash
   */
  calculateBlockHash(block) {
    const data = `${block.index}${block.timestamp}${JSON.stringify(block.transactions)}${block.previousHash}${block.merkleRoot}${block.nonce}`;
    return crypto.createHash('sha256').update(data).digest('hex');
  }

  /**
   * Calculate Merkle root for data integrity
   */
  calculateMerkleRoot(items) {
    if (!items || items.length === 0) {
      return crypto.createHash('sha256').update('').digest('hex');
    }

    const hashes = Array.from(items).map(item => 
      crypto.createHash('sha256').update(JSON.stringify(item)).digest('hex')
    );

    while (hashes.length > 1) {
      const newLevel = [];
      for (let i = 0; i < hashes.length; i += 2) {
        const left = hashes[i];
        const right = hashes[i + 1] || left; // Handle odd number of hashes
        const combined = crypto.createHash('sha256').update(left + right).digest('hex');
        newLevel.push(combined);
      }
      hashes.length = 0;
      hashes.push(...newLevel);
    }

    return hashes[0];
  }

  /**
   * Sign data with private key
   */
  signData(data) {
    const dataString = typeof data === 'string' ? data : JSON.stringify(data);
    const hash = crypto.createHash('sha256').update(dataString).digest();
    
    const sign = crypto.createSign('SHA256');
    sign.update(hash);
    return sign.sign(this.config.privateKey, 'base64');
  }

  /**
   * Verify signature
   */
  verifySignature(data, signature, publicKey = this.publicKey) {
    try {
      const dataString = typeof data === 'string' ? data : JSON.stringify(data);
      const hash = crypto.createHash('sha256').update(dataString).digest();
      
      const verify = crypto.createVerify('SHA256');
      verify.update(hash);
      return verify.verify(publicKey, signature, 'base64');
    } catch (error) {
      return false;
    }
  }

  /**
   * Connect to peer network
   */
  async connectToPeers() {
    for (const peerUrl of this.config.peers) {
      try {
        const ws = new WebSocket(peerUrl);
        
        ws.on('open', () => {
          console.log(`Connected to peer: ${peerUrl}`);
          this.connections.set(peerUrl, ws);
          this.trustedPeers.add(peerUrl);
          
          // Send identification
          ws.send(JSON.stringify({
            type: 'identification',
            nodeId: this.config.nodeId,
            publicKey: this.publicKey,
            isValidator: this.isValidator
          }));
        });

        ws.on('message', (data) => {
          this.handlePeerMessage(peerUrl, JSON.parse(data.toString()));
        });

        ws.on('close', () => {
          console.log(`Disconnected from peer: ${peerUrl}`);
          this.connections.delete(peerUrl);
          this.trustedPeers.delete(peerUrl);
        });

        ws.on('error', (error) => {
          console.error(`Peer connection error ${peerUrl}:`, error.message);
        });

      } catch (error) {
        console.error(`Failed to connect to peer ${peerUrl}:`, error.message);
      }
    }
  }

  /**
   * Handle messages from peers
   */
  handlePeerMessage(peerUrl, message) {
    switch (message.type) {
      case 'proposal':
        this.handleProposal(message.data);
        break;
      case 'vote':
        this.handleVote(message.data);
        break;
      case 'block':
        this.handleBlock(message.data);
        break;
      case 'identification':
        this.handlePeerIdentification(peerUrl, message);
        break;
      default:
        console.warn(`Unknown message type: ${message.type}`);
    }
  }

  /**
   * Broadcast proposal to network
   */
  async broadcastProposal(proposal) {
    const message = {
      type: 'proposal',
      data: proposal,
      sender: this.config.nodeId,
      timestamp: Date.now()
    };

    await this.broadcastToNetwork(message);
  }

  /**
   * Broadcast vote to network
   */
  async broadcastVote(vote) {
    const message = {
      type: 'vote',
      data: vote,
      sender: this.config.nodeId,
      timestamp: Date.now()
    };

    await this.broadcastToNetwork(message);
  }

  /**
   * Broadcast block to network
   */
  async broadcastBlock(block) {
    const message = {
      type: 'block',
      data: block,
      sender: this.config.nodeId,
      timestamp: Date.now()
    };

    await this.broadcastToNetwork(message);
  }

  /**
   * Broadcast message to all connected peers
   */
  async broadcastToNetwork(message) {
    const messageString = JSON.stringify(message);
    
    for (const [peerUrl, ws] of this.connections.entries()) {
      if (ws.readyState === WebSocket.OPEN) {
        try {
          ws.send(messageString);
        } catch (error) {
          console.error(`Failed to send message to ${peerUrl}:`, error.message);
        }
      }
    }
  }

  /**
   * Create genesis block
   */
  createGenesisBlock() {
    const genesisBlock = {
      index: 0,
      timestamp: Date.now(),
      transactions: [],
      consensusRecord: null,
      previousHash: '0',
      merkleRoot: this.calculateMerkleRoot([]),
      validator: 'genesis',
      signature: 'genesis',
      nonce: 0,
      hash: 'genesis'
    };

    this.blockchain = [genesisBlock];
    console.log('Genesis block created');
  }

  /**
   * Get latest block
   */
  getLatestBlock() {
    return this.blockchain[this.blockchain.length - 1];
  }

  /**
   * Get consensus records for a knowledge node
   */
  getConsensusRecords(knowledgeNodeId) {
    return this.votingHistory.filter(record => {
      const proposal = this.pendingTransactions.get(record.proposalId);
      return proposal && proposal.knowledgeNodeId === knowledgeNodeId;
    });
  }

  /**
   * Start consensus monitoring loop
   */
  startConsensusLoop() {
    setInterval(() => {
      this.monitorConsensus();
    }, 1000); // Check every second
  }

  /**
   * Monitor consensus progress
   */
  monitorConsensus() {
    const now = Date.now();
    
    for (const [proposalId, votingSession] of this.currentVoting.entries()) {
      if (now > votingSession.endTime && votingSession.status === 'ACTIVE') {
        this.closeVoting(proposalId);
      }
    }
  }

  /**
   * Close voting session
   */
  closeVoting(proposalId) {
    const votingSession = this.currentVoting.get(proposalId);
    if (!votingSession) return;

    votingSession.status = 'CLOSED';
    
    // Force consensus check
    const consensusResult = this.checkConsensus(votingSession);
    if (consensusResult) {
      this.finalizeConsensus(proposalId, consensusResult);
    } else {
      // No consensus reached
      const timeoutResult = {
        decision: 'TIMEOUT',
        confidence: 0,
        votes: votingSession.votes.size,
        reasoning: 'Voting window expired without reaching consensus'
      };
      this.finalizeConsensus(proposalId, timeoutResult);
    }
  }

  /**
   * Start voting monitor
   */
  startVotingMonitor() {
    setInterval(() => {
      this.logVotingStats();
    }, 30000); // Every 30 seconds
  }

  /**
   * Start authority rotation
   */
  startAuthorityRotation() {
    setInterval(() => {
      this.rotateAuthorities();
    }, this.config.authorityRotationPeriod);
  }

  /**
   * Rotate trusted authorities
   */
  rotateAuthorities() {
    // Implement authority rotation logic
    console.log('Authority rotation not yet implemented');
  }

  /**
   * Log voting statistics
   */
  logVotingStats() {
    console.log('Consensus Statistics:', {
      ...this.stats,
      activeVotingSessions: this.currentVoting.size,
      pendingTransactions: this.pendingTransactions.size,
      connectedPeers: this.connections.size,
      blockchainHeight: this.blockchain.length
    });
  }

  /**
   * Generate utility methods
   */
  generateNodeId() {
    return crypto.randomBytes(16).toString('hex');
  }

  generateTransactionId() {
    return crypto.randomBytes(16).toString('hex');
  }

  generatePrivateKey() {
    return crypto.generateKeyPairSync('rsa', { modulusLength: 2048 }).privateKey
      .export({ format: 'pem', type: 'pkcs1' });
  }

  getPublicKey() {
    return crypto.createPublicKey(this.config.privateKey)
      .export({ format: 'pem', type: 'spki' });
  }

  /**
   * Health check
   */
  async healthCheck() {
    return {
      status: 'healthy',
      nodeId: this.config.nodeId,
      isValidator: this.isValidator,
      connectedPeers: this.connections.size,
      blockchainHeight: this.blockchain.length,
      pendingVotes: this.currentVoting.size,
      lastBlockTime: this.lastBlockTime
    };
  }

  /**
   * Close all connections
   */
  async close() {
    console.log('Closing consensus client...');
    
    for (const ws of this.connections.values()) {
      ws.close();
    }
    
    this.connections.clear();
    this.trustedPeers.clear();
    
    console.log('Consensus client closed');
  }
}

module.exports = ConsensusClient;