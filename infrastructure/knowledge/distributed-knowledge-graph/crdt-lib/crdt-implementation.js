const crypto = require('crypto');
const EventEmitter = require('events');

/**
 * CRDT (Conflict-free Replicated Data Types) Implementation
 * 
 * This library provides conflict-free data structures for distributed
 * knowledge graph synchronization across multiple AI agents.
 * 
 * Supported CRDTs:
 * - G-Counter (Grow-only Counter)
 * - PN-Counter (Increment/Decrement Counter)
 * - G-Set (Grow-only Set)
 * - 2P-Set (Two-Phase Set)
 * - OR-Set (Observed-Remove Set)
 * - LWW-Register (Last-Write-Wins Register)
 * - Multi-Value Register (MV-Register)
 * - OR-Map (Observed-Remove Map)
 * - RGA (Replicated Growable Array/List)
 */

/**
 * Base CRDT class with common functionality
 */
class BaseCRDT extends EventEmitter {
  constructor(nodeId) {
    super();
    this.nodeId = nodeId || this.generateNodeId();
    this.vectorClock = new Map();
    this.vectorClock.set(this.nodeId, 0);
  }

  generateNodeId() {
    return crypto.randomBytes(8).toString('hex');
  }

  tick() {
    const current = this.vectorClock.get(this.nodeId) || 0;
    this.vectorClock.set(this.nodeId, current + 1);
    return current + 1;
  }

  updateVectorClock(otherClock) {
    for (const [nodeId, timestamp] of otherClock.entries()) {
      const currentTimestamp = this.vectorClock.get(nodeId) || 0;
      this.vectorClock.set(nodeId, Math.max(currentTimestamp, timestamp));
    }
  }

  compareVectorClocks(clock1, clock2) {
    const allNodes = new Set([...clock1.keys(), ...clock2.keys()]);
    let isEqual = true;
    let isLess = true;
    let isGreater = true;

    for (const nodeId of allNodes) {
      const ts1 = clock1.get(nodeId) || 0;
      const ts2 = clock2.get(nodeId) || 0;

      if (ts1 !== ts2) isEqual = false;
      if (ts1 > ts2) isLess = false;
      if (ts1 < ts2) isGreater = false;
    }

    if (isEqual) return 0;
    if (isLess && !isGreater) return -1;
    if (isGreater && !isLess) return 1;
    return null; // Concurrent
  }

  serialize() {
    return {
      nodeId: this.nodeId,
      vectorClock: Array.from(this.vectorClock.entries())
    };
  }

  deserialize(data) {
    this.nodeId = data.nodeId;
    this.vectorClock = new Map(data.vectorClock);
  }
}

/**
 * Grow-only Counter (G-Counter)
 * Supports increment operations only
 */
class GCounter extends BaseCRDT {
  constructor(nodeId) {
    super(nodeId);
    this.counters = new Map();
    this.counters.set(this.nodeId, 0);
  }

  increment(amount = 1) {
    if (amount < 0) {
      throw new Error('G-Counter only supports positive increments');
    }
    
    this.tick();
    const current = this.counters.get(this.nodeId) || 0;
    this.counters.set(this.nodeId, current + amount);
    
    this.emit('increment', { nodeId: this.nodeId, amount, total: this.value() });
    return this;
  }

  value() {
    let sum = 0;
    for (const count of this.counters.values()) {
      sum += count;
    }
    return sum;
  }

  merge(other) {
    if (!(other instanceof GCounter)) {
      throw new Error('Can only merge with another G-Counter');
    }

    this.updateVectorClock(other.vectorClock);

    for (const [nodeId, count] of other.counters.entries()) {
      const currentCount = this.counters.get(nodeId) || 0;
      this.counters.set(nodeId, Math.max(currentCount, count));
    }

    this.emit('merge', { other: other.nodeId, newValue: this.value() });
    return this;
  }

  serialize() {
    return {
      ...super.serialize(),
      type: 'GCounter',
      counters: Array.from(this.counters.entries())
    };
  }

  deserialize(data) {
    super.deserialize(data);
    this.counters = new Map(data.counters);
  }
}

/**
 * Increment/Decrement Counter (PN-Counter)
 * Supports both increment and decrement operations
 */
class PNCounter extends BaseCRDT {
  constructor(nodeId) {
    super(nodeId);
    this.positive = new GCounter(nodeId);
    this.negative = new GCounter(nodeId);
  }

  increment(amount = 1) {
    this.tick();
    this.positive.increment(Math.abs(amount));
    this.emit('increment', { amount, total: this.value() });
    return this;
  }

  decrement(amount = 1) {
    this.tick();
    this.negative.increment(Math.abs(amount));
    this.emit('decrement', { amount, total: this.value() });
    return this;
  }

  value() {
    return this.positive.value() - this.negative.value();
  }

  merge(other) {
    if (!(other instanceof PNCounter)) {
      throw new Error('Can only merge with another PN-Counter');
    }

    this.updateVectorClock(other.vectorClock);
    this.positive.merge(other.positive);
    this.negative.merge(other.negative);

    this.emit('merge', { other: other.nodeId, newValue: this.value() });
    return this;
  }

  serialize() {
    return {
      ...super.serialize(),
      type: 'PNCounter',
      positive: this.positive.serialize(),
      negative: this.negative.serialize()
    };
  }

  deserialize(data) {
    super.deserialize(data);
    this.positive = new GCounter();
    this.positive.deserialize(data.positive);
    this.negative = new GCounter();
    this.negative.deserialize(data.negative);
  }
}

/**
 * Observed-Remove Set (OR-Set)
 * Supports add and remove operations with unique tags
 */
class ORSet extends BaseCRDT {
  constructor(nodeId) {
    super(nodeId);
    this.elements = new Map(); // element -> Set of unique tags
    this.removed = new Set(); // removed unique tags
  }

  add(element) {
    this.tick();
    const tag = `${this.nodeId}-${this.vectorClock.get(this.nodeId)}-${crypto.randomBytes(4).toString('hex')}`;
    
    if (!this.elements.has(element)) {
      this.elements.set(element, new Set());
    }
    this.elements.get(element).add(tag);

    this.emit('add', { element, tag });
    return this;
  }

  remove(element) {
    if (!this.elements.has(element)) {
      return this; // Element not present
    }

    this.tick();
    const tags = this.elements.get(element);
    for (const tag of tags) {
      this.removed.add(tag);
    }

    this.emit('remove', { element, tags: Array.from(tags) });
    return this;
  }

  has(element) {
    if (!this.elements.has(element)) {
      return false;
    }

    const tags = this.elements.get(element);
    for (const tag of tags) {
      if (!this.removed.has(tag)) {
        return true;
      }
    }

    return false;
  }

  values() {
    const result = new Set();
    for (const [element, tags] of this.elements.entries()) {
      for (const tag of tags) {
        if (!this.removed.has(tag)) {
          result.add(element);
          break;
        }
      }
    }
    return Array.from(result);
  }

  size() {
    return this.values().length;
  }

  merge(other) {
    if (!(other instanceof ORSet)) {
      throw new Error('Can only merge with another OR-Set');
    }

    this.updateVectorClock(other.vectorClock);

    // Merge elements
    for (const [element, tags] of other.elements.entries()) {
      if (!this.elements.has(element)) {
        this.elements.set(element, new Set());
      }
      for (const tag of tags) {
        this.elements.get(element).add(tag);
      }
    }

    // Merge removed tags
    for (const tag of other.removed) {
      this.removed.add(tag);
    }

    this.emit('merge', { other: other.nodeId, size: this.size() });
    return this;
  }

  serialize() {
    const elementsArray = [];
    for (const [element, tags] of this.elements.entries()) {
      elementsArray.push([element, Array.from(tags)]);
    }

    return {
      ...super.serialize(),
      type: 'ORSet',
      elements: elementsArray,
      removed: Array.from(this.removed)
    };
  }

  deserialize(data) {
    super.deserialize(data);
    this.elements = new Map();
    for (const [element, tags] of data.elements) {
      this.elements.set(element, new Set(tags));
    }
    this.removed = new Set(data.removed);
  }
}

/**
 * Last-Write-Wins Register (LWW-Register)
 * Stores a single value with timestamp-based conflict resolution
 */
class LWWRegister extends BaseCRDT {
  constructor(nodeId, initialValue = null) {
    super(nodeId);
    this.value = initialValue;
    this.timestamp = 0;
    this.writerNodeId = nodeId;
  }

  assign(value) {
    this.tick();
    this.value = value;
    this.timestamp = this.vectorClock.get(this.nodeId);
    this.writerNodeId = this.nodeId;

    this.emit('assign', { value, timestamp: this.timestamp });
    return this;
  }

  get() {
    return this.value;
  }

  merge(other) {
    if (!(other instanceof LWWRegister)) {
      throw new Error('Can only merge with another LWW-Register');
    }

    this.updateVectorClock(other.vectorClock);

    // Use timestamp to resolve conflicts
    if (other.timestamp > this.timestamp || 
        (other.timestamp === this.timestamp && other.writerNodeId > this.writerNodeId)) {
      const oldValue = this.value;
      this.value = other.value;
      this.timestamp = other.timestamp;
      this.writerNodeId = other.writerNodeId;

      this.emit('merge', { 
        other: other.nodeId, 
        oldValue, 
        newValue: this.value,
        timestamp: this.timestamp
      });
    }

    return this;
  }

  serialize() {
    return {
      ...super.serialize(),
      type: 'LWWRegister',
      value: this.value,
      timestamp: this.timestamp,
      writerNodeId: this.writerNodeId
    };
  }

  deserialize(data) {
    super.deserialize(data);
    this.value = data.value;
    this.timestamp = data.timestamp;
    this.writerNodeId = data.writerNodeId;
  }
}

/**
 * Multi-Value Register (MV-Register)
 * Stores multiple concurrent values
 */
class MVRegister extends BaseCRDT {
  constructor(nodeId) {
    super(nodeId);
    this.values = new Map(); // timestamp -> { value, nodeId }
  }

  assign(value) {
    this.tick();
    const timestamp = this.vectorClock.get(this.nodeId);
    
    // Clear all existing values (this is a new assignment)
    this.values.clear();
    this.values.set(timestamp, { value, nodeId: this.nodeId });

    this.emit('assign', { value, timestamp });
    return this;
  }

  values() {
    return Array.from(this.values.values()).map(entry => entry.value);
  }

  merge(other) {
    if (!(other instanceof MVRegister)) {
      throw new Error('Can only merge with another MV-Register');
    }

    this.updateVectorClock(other.vectorClock);

    // Merge values, keeping only concurrent ones
    const allValues = new Map([...this.values, ...other.values]);
    const concurrentValues = new Map();

    for (const [timestamp, entry] of allValues.entries()) {
      let isConcurrent = true;
      
      for (const [otherTimestamp] of allValues.entries()) {
        if (timestamp !== otherTimestamp) {
          const clock1 = new Map([[entry.nodeId, timestamp]]);
          const clock2 = new Map([[allValues.get(otherTimestamp).nodeId, otherTimestamp]]);
          
          if (this.compareVectorClocks(clock1, clock2) === -1) {
            isConcurrent = false;
            break;
          }
        }
      }

      if (isConcurrent) {
        concurrentValues.set(timestamp, entry);
      }
    }

    this.values = concurrentValues;
    this.emit('merge', { other: other.nodeId, valueCount: this.values.size });
    return this;
  }

  serialize() {
    return {
      ...super.serialize(),
      type: 'MVRegister',
      values: Array.from(this.values.entries())
    };
  }

  deserialize(data) {
    super.deserialize(data);
    this.values = new Map(data.values);
  }
}

/**
 * Observed-Remove Map (OR-Map)
 * CRDT map with add/remove operations on keys
 */
class ORMap extends BaseCRDT {
  constructor(nodeId) {
    super(nodeId);
    this.keys = new ORSet(nodeId);
    this.values = new Map(); // key -> CRDT value
  }

  set(key, crdtValue) {
    this.tick();
    this.keys.add(key);
    this.values.set(key, crdtValue);

    this.emit('set', { key, value: crdtValue });
    return this;
  }

  get(key) {
    if (!this.keys.has(key)) {
      return undefined;
    }
    return this.values.get(key);
  }

  delete(key) {
    this.tick();
    this.keys.remove(key);
    this.values.delete(key);

    this.emit('delete', { key });
    return this;
  }

  has(key) {
    return this.keys.has(key);
  }

  entries() {
    const result = [];
    for (const key of this.keys.values()) {
      const value = this.values.get(key);
      if (value) {
        result.push([key, value]);
      }
    }
    return result;
  }

  size() {
    return this.keys.size();
  }

  merge(other) {
    if (!(other instanceof ORMap)) {
      throw new Error('Can only merge with another OR-Map');
    }

    this.updateVectorClock(other.vectorClock);
    this.keys.merge(other.keys);

    // Merge values for common keys
    for (const [key, otherValue] of other.values.entries()) {
      if (this.keys.has(key)) {
        const myValue = this.values.get(key);
        if (myValue && typeof myValue.merge === 'function') {
          myValue.merge(otherValue);
        } else {
          this.values.set(key, otherValue);
        }
      }
    }

    this.emit('merge', { other: other.nodeId, size: this.size() });
    return this;
  }

  serialize() {
    const valuesArray = [];
    for (const [key, value] of this.values.entries()) {
      valuesArray.push([
        key, 
        typeof value.serialize === 'function' ? value.serialize() : value
      ]);
    }

    return {
      ...super.serialize(),
      type: 'ORMap',
      keys: this.keys.serialize(),
      values: valuesArray
    };
  }

  deserialize(data) {
    super.deserialize(data);
    this.keys = new ORSet();
    this.keys.deserialize(data.keys);
    
    this.values = new Map();
    for (const [key, value] of data.values) {
      if (typeof value === 'object' && value.type) {
        const crdt = CRDTFactory.create(value.type, value.nodeId);
        crdt.deserialize(value);
        this.values.set(key, crdt);
      } else {
        this.values.set(key, value);
      }
    }
  }
}

/**
 * Knowledge Graph CRDT
 * Specialized CRDT for knowledge graph nodes and relationships
 */
class KnowledgeGraphCRDT extends BaseCRDT {
  constructor(nodeId) {
    super(nodeId);
    this.nodes = new ORMap(nodeId);
    this.relationships = new ORMap(nodeId);
    this.metadata = new LWWRegister(nodeId);
  }

  addNode(nodeId, properties) {
    this.tick();
    const nodeData = new ORMap(this.nodeId);
    
    for (const [key, value] of Object.entries(properties)) {
      nodeData.set(key, new LWWRegister(this.nodeId, value));
    }
    
    this.nodes.set(nodeId, nodeData);
    this.emit('nodeAdded', { nodeId, properties });
    return this;
  }

  updateNodeProperty(nodeId, property, value) {
    const node = this.nodes.get(nodeId);
    if (!node) {
      throw new Error(`Node ${nodeId} not found`);
    }

    this.tick();
    let propertyRegister = node.get(property);
    if (!propertyRegister) {
      propertyRegister = new LWWRegister(this.nodeId);
      node.set(property, propertyRegister);
    }
    
    propertyRegister.assign(value);
    this.emit('nodePropertyUpdated', { nodeId, property, value });
    return this;
  }

  removeNode(nodeId) {
    this.tick();
    this.nodes.delete(nodeId);
    
    // Remove all relationships involving this node
    for (const [relId, relationship] of this.relationships.entries()) {
      const fromNode = relationship.get('fromNode');
      const toNode = relationship.get('toNode');
      
      if ((fromNode && fromNode.get() === nodeId) || 
          (toNode && toNode.get() === nodeId)) {
        this.relationships.delete(relId);
      }
    }

    this.emit('nodeRemoved', { nodeId });
    return this;
  }

  addRelationship(relationshipId, fromNodeId, toNodeId, type, properties = {}) {
    this.tick();
    const relationshipData = new ORMap(this.nodeId);
    
    relationshipData.set('fromNode', new LWWRegister(this.nodeId, fromNodeId));
    relationshipData.set('toNode', new LWWRegister(this.nodeId, toNodeId));
    relationshipData.set('type', new LWWRegister(this.nodeId, type));
    
    for (const [key, value] of Object.entries(properties)) {
      relationshipData.set(key, new LWWRegister(this.nodeId, value));
    }
    
    this.relationships.set(relationshipId, relationshipData);
    this.emit('relationshipAdded', { relationshipId, fromNodeId, toNodeId, type, properties });
    return this;
  }

  removeRelationship(relationshipId) {
    this.tick();
    this.relationships.delete(relationshipId);
    this.emit('relationshipRemoved', { relationshipId });
    return this;
  }

  getNode(nodeId) {
    const nodeData = this.nodes.get(nodeId);
    if (!nodeData) return null;

    const result = {};
    for (const [property, register] of nodeData.entries()) {
      result[property] = register.get();
    }
    return result;
  }

  getRelationship(relationshipId) {
    const relationshipData = this.relationships.get(relationshipId);
    if (!relationshipData) return null;

    const result = {};
    for (const [property, register] of relationshipData.entries()) {
      result[property] = register.get();
    }
    return result;
  }

  getAllNodes() {
    const nodes = {};
    for (const [nodeId, nodeData] of this.nodes.entries()) {
      nodes[nodeId] = this.getNode(nodeId);
    }
    return nodes;
  }

  getAllRelationships() {
    const relationships = {};
    for (const [relId, relData] of this.relationships.entries()) {
      relationships[relId] = this.getRelationship(relId);
    }
    return relationships;
  }

  merge(other) {
    if (!(other instanceof KnowledgeGraphCRDT)) {
      throw new Error('Can only merge with another KnowledgeGraphCRDT');
    }

    this.updateVectorClock(other.vectorClock);
    this.nodes.merge(other.nodes);
    this.relationships.merge(other.relationships);
    this.metadata.merge(other.metadata);

    this.emit('merge', { 
      other: other.nodeId,
      nodeCount: this.nodes.size(),
      relationshipCount: this.relationships.size()
    });
    return this;
  }

  serialize() {
    return {
      ...super.serialize(),
      type: 'KnowledgeGraphCRDT',
      nodes: this.nodes.serialize(),
      relationships: this.relationships.serialize(),
      metadata: this.metadata.serialize()
    };
  }

  deserialize(data) {
    super.deserialize(data);
    this.nodes = new ORMap();
    this.nodes.deserialize(data.nodes);
    this.relationships = new ORMap();
    this.relationships.deserialize(data.relationships);
    this.metadata = new LWWRegister();
    this.metadata.deserialize(data.metadata);
  }
}

/**
 * CRDT Factory for creating and deserializing CRDTs
 */
class CRDTFactory {
  static create(type, nodeId, ...args) {
    switch (type) {
      case 'GCounter':
        return new GCounter(nodeId);
      case 'PNCounter':
        return new PNCounter(nodeId);
      case 'ORSet':
        return new ORSet(nodeId);
      case 'LWWRegister':
        return new LWWRegister(nodeId, ...args);
      case 'MVRegister':
        return new MVRegister(nodeId);
      case 'ORMap':
        return new ORMap(nodeId);
      case 'KnowledgeGraphCRDT':
        return new KnowledgeGraphCRDT(nodeId);
      default:
        throw new Error(`Unknown CRDT type: ${type}`);
    }
  }

  static deserialize(data) {
    const crdt = this.create(data.type, data.nodeId);
    crdt.deserialize(data);
    return crdt;
  }
}

/**
 * CRDT Network Manager
 * Manages synchronization of CRDTs across the network
 */
class CRDTNetworkManager extends EventEmitter {
  constructor(nodeId) {
    super();
    this.nodeId = nodeId;
    this.crdts = new Map();
    this.peers = new Set();
    this.syncInterval = 5000; // 5 seconds
    this.syncTimer = null;
  }

  register(name, crdt) {
    this.crdts.set(name, crdt);
    
    crdt.on('increment', () => this.scheduleSync(name));
    crdt.on('decrement', () => this.scheduleSync(name));
    crdt.on('add', () => this.scheduleSync(name));
    crdt.on('remove', () => this.scheduleSync(name));
    crdt.on('assign', () => this.scheduleSync(name));
    crdt.on('set', () => this.scheduleSync(name));
    crdt.on('delete', () => this.scheduleSync(name));
    
    return this;
  }

  scheduleSync(crdtName) {
    if (this.syncTimer) {
      clearTimeout(this.syncTimer);
    }
    
    this.syncTimer = setTimeout(() => {
      this.syncWithPeers(crdtName);
    }, 100); // Debounce for 100ms
  }

  async syncWithPeers(crdtName) {
    const crdt = this.crdts.get(crdtName);
    if (!crdt) return;

    const serialized = crdt.serialize();
    
    this.emit('sync', {
      crdtName,
      nodeId: this.nodeId,
      data: serialized
    });
  }

  handleRemoteUpdate(crdtName, remoteData) {
    let crdt = this.crdts.get(crdtName);
    
    if (!crdt) {
      // Create new CRDT from remote data
      crdt = CRDTFactory.deserialize(remoteData);
      this.crdts.set(crdtName, crdt);
    } else {
      // Merge with existing CRDT
      const remoteCRDT = CRDTFactory.deserialize(remoteData);
      crdt.merge(remoteCRDT);
    }

    this.emit('updated', { crdtName, crdt });
  }

  startPeriodicSync() {
    this.stopPeriodicSync();
    
    this.syncTimer = setInterval(() => {
      for (const crdtName of this.crdts.keys()) {
        this.syncWithPeers(crdtName);
      }
    }, this.syncInterval);
  }

  stopPeriodicSync() {
    if (this.syncTimer) {
      clearInterval(this.syncTimer);
      this.syncTimer = null;
    }
  }

  getCRDT(name) {
    return this.crdts.get(name);
  }

  getAllCRDTs() {
    return new Map(this.crdts);
  }

  getStats() {
    const stats = {};
    for (const [name, crdt] of this.crdts.entries()) {
      stats[name] = {
        type: crdt.constructor.name,
        nodeId: crdt.nodeId,
        vectorClock: Array.from(crdt.vectorClock.entries())
      };
    }
    return stats;
  }
}

module.exports = {
  BaseCRDT,
  GCounter,
  PNCounter,
  ORSet,
  LWWRegister,
  MVRegister,
  ORMap,
  KnowledgeGraphCRDT,
  CRDTFactory,
  CRDTNetworkManager
};