const neo4j = require('neo4j-driver');
const crypto = require('crypto');

/**
 * Neo4j Shard Manager for Billion-Scale Knowledge Graph
 * 
 * This class manages automatic sharding of knowledge graph data across
 * multiple Neo4j instances using consistent hashing and Fabric queries.
 */
class Neo4jShardManager {
  constructor(config = {}) {
    this.config = {
      coreNodes: [
        'bolt://neo4j-core-01:7687',
        'bolt://neo4j-core-02:7687', 
        'bolt://neo4j-core-03:7687'
      ],
      readReplicas: [
        'bolt://neo4j-replica-01:7690',
        'bolt://neo4j-replica-02:7691'
      ],
      auth: { username: 'neo4j', password: 'password' },
      fabricUri: 'bolt://neo4j-core-01:7687',
      ...config
    };

    this.drivers = new Map();
    this.fabricDriver = null;
    this.shardRing = [];
    this.replicationFactor = 2;
    
    this.initializeDrivers();
    this.buildConsistentHashRing();
  }

  /**
   * Initialize Neo4j drivers for all cluster nodes
   */
  initializeDrivers() {
    // Core cluster drivers
    this.config.coreNodes.forEach((uri, index) => {
      const driver = neo4j.driver(uri, neo4j.auth.basic(
        this.config.auth.username, 
        this.config.auth.password
      ), {
        maxConnectionPoolSize: 100,
        connectionAcquisitionTimeout: 60000,
        disableLosslessIntegers: true
      });
      
      this.drivers.set(`core-${index}`, driver);
    });

    // Read replica drivers  
    this.config.readReplicas.forEach((uri, index) => {
      const driver = neo4j.driver(uri, neo4j.auth.basic(
        this.config.auth.username,
        this.config.auth.password
      ), {
        maxConnectionPoolSize: 50,
        disableLosslessIntegers: true
      });
      
      this.drivers.set(`replica-${index}`, driver);
    });

    // Fabric driver for distributed queries
    this.fabricDriver = neo4j.driver(this.config.fabricUri, neo4j.auth.basic(
      this.config.auth.username,
      this.config.auth.password
    ), {
      database: 'fabric',
      maxConnectionPoolSize: 200,
      disableLosslessIntegers: true
    });
  }

  /**
   * Build consistent hash ring for data distribution
   */
  buildConsistentHashRing() {
    const virtualNodes = 150; // Virtual nodes per physical node
    
    this.config.coreNodes.forEach((uri, nodeIndex) => {
      for (let i = 0; i < virtualNodes; i++) {
        const hash = this.hash(`${uri}-${i}`);
        this.shardRing.push({
          hash,
          nodeId: `core-${nodeIndex}`,
          uri,
          database: `knowledge_shard_${nodeIndex + 1}`
        });
      }
    });

    // Sort ring by hash value
    this.shardRing.sort((a, b) => a.hash.localeCompare(b.hash));
    console.log(`Consistent hash ring built with ${this.shardRing.length} virtual nodes`);
  }

  /**
   * Hash function for consistent hashing
   */
  hash(key) {
    return crypto.createHash('sha256').update(key).digest('hex');
  }

  /**
   * Determine which shard(s) a node should be stored on
   */
  getShardForNode(nodeId) {
    const nodeHash = this.hash(nodeId);
    const shards = [];
    
    // Find the first shard in the ring
    let startIndex = 0;
    for (let i = 0; i < this.shardRing.length; i++) {
      if (this.shardRing[i].hash >= nodeHash) {
        startIndex = i;
        break;
      }
    }
    
    // Add primary shard and replicas
    const uniqueNodes = new Set();
    let currentIndex = startIndex;
    
    while (uniqueNodes.size < this.replicationFactor) {
      const shard = this.shardRing[currentIndex];
      if (!uniqueNodes.has(shard.nodeId)) {
        shards.push(shard);
        uniqueNodes.add(shard.nodeId);
      }
      currentIndex = (currentIndex + 1) % this.shardRing.length;
    }
    
    return shards;
  }

  /**
   * Create a knowledge node with automatic sharding
   */
  async createKnowledgeNode(nodeData) {
    const { id, type, properties, embeddings } = nodeData;
    const shards = this.getShardForNode(id);
    
    const promises = shards.map(async (shard) => {
      const driver = this.drivers.get(shard.nodeId);
      const session = driver.session({ database: shard.database });
      
      try {
        const query = `
          MERGE (n:KnowledgeNode {id: $id})
          SET n.type = $type,
              n.properties = $properties,
              n.embeddings = $embeddings,
              n.shard_id = $shardId,
              n.created_at = datetime(),
              n.updated_at = datetime()
          RETURN n
        `;
        
        const result = await session.run(query, {
          id,
          type,
          properties,
          embeddings,
          shardId: shard.nodeId
        });
        
        return {
          shard: shard.nodeId,
          success: true,
          node: result.records[0]?.get('n')
        };
      } catch (error) {
        console.error(`Error creating node on shard ${shard.nodeId}:`, error);
        return {
          shard: shard.nodeId,
          success: false,
          error: error.message
        };
      } finally {
        await session.close();
      }
    });
    
    const results = await Promise.all(promises);
    return {
      nodeId: id,
      shards: results,
      primaryShard: shards[0].nodeId
    };
  }

  /**
   * Create relationship between knowledge nodes (may span shards)
   */
  async createRelationship(fromId, toId, relationshipType, properties = {}) {
    const fromShards = this.getShardForNode(fromId);
    const toShards = this.getShardForNode(toId);
    
    // If nodes are on same shard, create local relationship
    const commonShard = fromShards.find(f => 
      toShards.some(t => t.nodeId === f.nodeId)
    );
    
    if (commonShard) {
      return this.createLocalRelationship(
        fromId, toId, relationshipType, properties, commonShard
      );
    } else {
      // Cross-shard relationship - use Fabric
      return this.createCrossShardRelationship(
        fromId, toId, relationshipType, properties
      );
    }
  }

  /**
   * Create relationship within same shard
   */
  async createLocalRelationship(fromId, toId, type, properties, shard) {
    const driver = this.drivers.get(shard.nodeId);
    const session = driver.session({ database: shard.database });
    
    try {
      const query = `
        MATCH (from:KnowledgeNode {id: $fromId})
        MATCH (to:KnowledgeNode {id: $toId})
        MERGE (from)-[r:${type}]->(to)
        SET r += $properties,
            r.created_at = datetime(),
            r.shard_id = $shardId
        RETURN r
      `;
      
      const result = await session.run(query, {
        fromId,
        toId,
        properties,
        shardId: shard.nodeId
      });
      
      return {
        type: 'local',
        shard: shard.nodeId,
        relationship: result.records[0]?.get('r')
      };
    } finally {
      await session.close();
    }
  }

  /**
   * Create cross-shard relationship using Fabric
   */
  async createCrossShardRelationship(fromId, toId, type, properties) {
    const session = this.fabricDriver.session();
    
    try {
      const query = `
        USE fabric.knowledge_shard_1, fabric.knowledge_shard_2, fabric.knowledge_shard_3
        MATCH (from:KnowledgeNode {id: $fromId})
        MATCH (to:KnowledgeNode {id: $toId})
        CREATE (from)-[r:${type} {
          properties: $properties,
          created_at: datetime(),
          cross_shard: true,
          from_shard: from.shard_id,
          to_shard: to.shard_id
        }]->(to)
        RETURN r
      `;
      
      const result = await session.run(query, {
        fromId,
        toId,
        properties
      });
      
      return {
        type: 'cross-shard',
        relationship: result.records[0]?.get('r')
      };
    } finally {
      await session.close();
    }
  }

  /**
   * Query knowledge graph across all shards
   */
  async queryKnowledgeGraph(query, parameters = {}) {
    const session = this.fabricDriver.session();
    
    try {
      // Use all shards in Fabric query
      const fabricQuery = `
        USE fabric.knowledge_shard_1, fabric.knowledge_shard_2, fabric.knowledge_shard_3
        ${query}
      `;
      
      const result = await session.run(fabricQuery, parameters);
      
      return {
        records: result.records,
        summary: result.summary,
        shards: ['knowledge_shard_1', 'knowledge_shard_2', 'knowledge_shard_3']
      };
    } finally {
      await session.close();
    }
  }

  /**
   * Get node by ID (searches across shards)
   */
  async getKnowledgeNode(nodeId) {
    const shards = this.getShardForNode(nodeId);
    
    // Try primary shard first
    const primaryDriver = this.drivers.get(shards[0].nodeId);
    const session = primaryDriver.session({ database: shards[0].database });
    
    try {
      const query = `
        MATCH (n:KnowledgeNode {id: $nodeId})
        RETURN n, labels(n) as labels
      `;
      
      const result = await session.run(query, { nodeId });
      
      if (result.records.length > 0) {
        return {
          node: result.records[0].get('n'),
          labels: result.records[0].get('labels'),
          shard: shards[0].nodeId
        };
      }
      
      return null;
    } finally {
      await session.close();
    }
  }

  /**
   * Bulk load nodes with automatic sharding
   */
  async bulkLoadNodes(nodes) {
    const shardBatches = new Map();
    
    // Group nodes by their target shards
    nodes.forEach(node => {
      const shards = this.getShardForNode(node.id);
      shards.forEach(shard => {
        if (!shardBatches.has(shard.nodeId)) {
          shardBatches.set(shard.nodeId, { shard, nodes: [] });
        }
        shardBatches.get(shard.nodeId).nodes.push(node);
      });
    });

    // Execute batch loads in parallel
    const promises = Array.from(shardBatches.values()).map(async (batch) => {
      const driver = this.drivers.get(batch.shard.nodeId);
      const session = driver.session({ database: batch.shard.database });
      
      try {
        const query = `
          UNWIND $nodes as nodeData
          MERGE (n:KnowledgeNode {id: nodeData.id})
          SET n.type = nodeData.type,
              n.properties = nodeData.properties,
              n.embeddings = nodeData.embeddings,
              n.shard_id = $shardId,
              n.created_at = datetime(),
              n.updated_at = datetime()
          RETURN count(n) as created
        `;
        
        const result = await session.run(query, {
          nodes: batch.nodes,
          shardId: batch.shard.nodeId
        });
        
        return {
          shard: batch.shard.nodeId,
          created: result.records[0].get('created').toNumber(),
          success: true
        };
      } catch (error) {
        console.error(`Bulk load error on shard ${batch.shard.nodeId}:`, error);
        return {
          shard: batch.shard.nodeId,
          success: false,
          error: error.message
        };
      } finally {
        await session.close();
      }
    });
    
    return Promise.all(promises);
  }

  /**
   * Get cluster health status
   */
  async getClusterHealth() {
    const healthChecks = [];
    
    // Check core nodes
    for (const [nodeId, driver] of this.drivers.entries()) {
      if (nodeId.startsWith('core-')) {
        try {
          const session = driver.session();
          await session.run('RETURN 1');
          await session.close();
          
          healthChecks.push({
            nodeId,
            type: 'core',
            status: 'healthy',
            timestamp: new Date()
          });
        } catch (error) {
          healthChecks.push({
            nodeId,
            type: 'core', 
            status: 'unhealthy',
            error: error.message,
            timestamp: new Date()
          });
        }
      }
    }
    
    // Check fabric connectivity
    try {
      const session = this.fabricDriver.session();
      await session.run('SHOW DATABASES');
      await session.close();
      
      healthChecks.push({
        nodeId: 'fabric',
        type: 'fabric',
        status: 'healthy',
        timestamp: new Date()
      });
    } catch (error) {
      healthChecks.push({
        nodeId: 'fabric',
        type: 'fabric',
        status: 'unhealthy',
        error: error.message,
        timestamp: new Date()
      });
    }
    
    return healthChecks;
  }

  /**
   * Close all connections
   */
  async close() {
    const closePromises = [];
    
    for (const driver of this.drivers.values()) {
      closePromises.push(driver.close());
    }
    
    if (this.fabricDriver) {
      closePromises.push(this.fabricDriver.close());
    }
    
    await Promise.all(closePromises);
    console.log('All Neo4j connections closed');
  }
}

module.exports = Neo4jShardManager;