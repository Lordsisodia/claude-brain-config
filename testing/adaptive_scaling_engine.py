#!/usr/bin/env python3
"""
ADAPTIVE AUTO-SCALING ENGINE
Revolutionary intelligent scaling for multi-agent AI coordination platform
"""

import asyncio
import time
import json
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, asdict, field
from collections import defaultdict, deque
from enum import Enum
import threading
import statistics
import logging

class ScalingAction(Enum):
    """Types of scaling actions"""
    SCALE_UP = "scale_up"
    SCALE_DOWN = "scale_down"
    LOAD_BALANCE = "load_balance"
    CIRCUIT_BREAK = "circuit_break"
    FAILOVER = "failover"
    OPTIMIZE = "optimize"
    NO_ACTION = "no_action"

class ScalingTrigger(Enum):
    """What triggered the scaling action"""
    CPU_THRESHOLD = "cpu_threshold"
    MEMORY_THRESHOLD = "memory_threshold"
    QUEUE_LENGTH = "queue_length"
    LATENCY_THRESHOLD = "latency_threshold"
    ERROR_RATE = "error_rate"
    QUALITY_DEGRADATION = "quality_degradation"
    COST_OPTIMIZATION = "cost_optimization"
    PREDICTIVE = "predictive"
    MANUAL = "manual"

class AgentPoolState(Enum):
    """Agent pool states"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    OVERLOADED = "overloaded"
    FAILING = "failing"
    CIRCUIT_BROKEN = "circuit_broken"
    SCALING = "scaling"

@dataclass
class ScalingRule:
    """Intelligent scaling rule"""
    name: str
    trigger: ScalingTrigger
    condition: str  # e.g., "latency > 5000 AND queue_length > 100"
    action: ScalingAction
    cooldown_minutes: int = 5
    max_instances: int = 10
    min_instances: int = 1
    priority: int = 1  # 1-10, higher is more important
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ScalingEvent:
    """Record of a scaling event"""
    timestamp: datetime
    rule_name: str
    trigger: ScalingTrigger
    action: ScalingAction
    agent_type: str
    from_count: int
    to_count: int
    reason: str
    success: bool
    execution_time_ms: float
    impact_metrics: Dict[str, float] = field(default_factory=dict)

@dataclass
class AgentPool:
    """Intelligent agent pool with auto-scaling"""
    agent_type: str
    current_instances: int
    target_instances: int
    max_instances: int
    min_instances: int
    state: AgentPoolState
    last_scaled: datetime
    scaling_cooldown: int  # minutes
    
    # Performance metrics
    average_load: float = 0.0
    average_latency: float = 0.0
    error_rate: float = 0.0
    success_rate: float = 1.0
    queue_length: int = 0
    
    # Health metrics
    healthy_instances: int = 0
    unhealthy_instances: int = 0
    circuit_broken_instances: int = 0
    
    # Cost metrics
    cost_per_instance: float = 0.001
    total_cost_hour: float = 0.0

@dataclass
class LoadBalancerConfig:
    """Load balancer configuration"""
    algorithm: str = "weighted_round_robin"  # round_robin, weighted_round_robin, least_connections, quality_weighted
    health_check_interval: int = 30  # seconds
    failure_threshold: int = 3  # consecutive failures before marking unhealthy
    recovery_threshold: int = 2   # consecutive successes before marking healthy
    timeout_seconds: int = 30
    max_retries: int = 2
    circuit_breaker_enabled: bool = True
    circuit_breaker_failure_threshold: int = 5
    circuit_breaker_recovery_time: int = 60  # seconds

@dataclass
class QueueManager:
    """Intelligent queue management"""
    max_queue_size: int = 1000
    priority_levels: int = 3
    queue_timeout_seconds: int = 300
    batch_processing_enabled: bool = True
    batch_size: int = 10
    adaptive_batching: bool = True

class CircuitBreaker:
    """Circuit breaker pattern implementation"""
    
    def __init__(self, failure_threshold: int = 5, recovery_time: int = 60, timeout: int = 30):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.timeout = timeout
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.lock = threading.RLock()
    
    async def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        
        with self.lock:
            if self.state == "OPEN":
                if self._should_attempt_reset():
                    self.state = "HALF_OPEN"
                else:
                    raise Exception(f"Circuit breaker OPEN - failing fast")
        
        try:
            # Execute with timeout
            result = await asyncio.wait_for(func(*args, **kwargs), timeout=self.timeout)
            
            with self.lock:
                if self.state == "HALF_OPEN":
                    self.state = "CLOSED"
                    self.failure_count = 0
                    self.last_failure_time = None
                    logging.info("Circuit breaker reset to CLOSED")
            
            return result
            
        except Exception as e:
            with self.lock:
                self.failure_count += 1
                self.last_failure_time = datetime.now()
                
                if self.failure_count >= self.failure_threshold:
                    self.state = "OPEN"
                    logging.warning(f"Circuit breaker OPENED after {self.failure_count} failures")
            
            raise e
    
    def _should_attempt_reset(self) -> bool:
        """Check if we should attempt to reset the circuit breaker"""
        if self.last_failure_time is None:
            return True
        
        time_since_failure = (datetime.now() - self.last_failure_time).total_seconds()
        return time_since_failure >= self.recovery_time
    
    def get_state(self) -> Dict[str, Any]:
        """Get current circuit breaker state"""
        return {
            'state': self.state,
            'failure_count': self.failure_count,
            'last_failure_time': self.last_failure_time.isoformat() if self.last_failure_time else None,
            'time_until_retry': max(0, self.recovery_time - (
                datetime.now() - self.last_failure_time).total_seconds()) if self.last_failure_time else 0
        }

class IntelligentLoadBalancer:
    """Advanced load balancer with multiple algorithms and health checking"""
    
    def __init__(self, config: LoadBalancerConfig):
        self.config = config
        self.agent_health = {}
        self.agent_metrics = {}
        self.circuit_breakers = {}
        self.request_counts = defaultdict(int)
        self.response_times = defaultdict(list)
        
        # Health check task
        self.health_check_task = None
        self.running = False
    
    async def start(self):
        """Start the load balancer"""
        self.running = True
        self.health_check_task = asyncio.create_task(self._health_check_loop())
        logging.info("Intelligent load balancer started")
    
    async def stop(self):
        """Stop the load balancer"""
        self.running = False
        if self.health_check_task:
            self.health_check_task.cancel()
            await self.health_check_task
        logging.info("Intelligent load balancer stopped")
    
    def register_agent(self, agent_id: str, agent_config: Dict[str, Any]):
        """Register an agent with the load balancer"""
        
        self.agent_health[agent_id] = {
            'healthy': True,
            'consecutive_failures': 0,
            'consecutive_successes': 0,
            'last_check': datetime.now(),
            'last_success': datetime.now(),
            'last_failure': None
        }
        
        self.agent_metrics[agent_id] = {
            'current_connections': 0,
            'total_requests': 0,
            'total_failures': 0,
            'average_response_time': 0.0,
            'load_score': 0.0,
            'quality_score': 1.0,
            'weight': agent_config.get('weight', 1.0)
        }
        
        if self.config.circuit_breaker_enabled:
            self.circuit_breakers[agent_id] = CircuitBreaker(
                failure_threshold=self.config.circuit_breaker_failure_threshold,
                recovery_time=self.config.circuit_breaker_recovery_time,
                timeout=self.config.timeout_seconds
            )
        
        logging.info(f"Agent {agent_id} registered with load balancer")
    
    def unregister_agent(self, agent_id: str):
        """Unregister an agent from the load balancer"""
        
        self.agent_health.pop(agent_id, None)
        self.agent_metrics.pop(agent_id, None)
        self.circuit_breakers.pop(agent_id, None)
        self.request_counts.pop(agent_id, None)
        self.response_times.pop(agent_id, None)
        
        logging.info(f"Agent {agent_id} unregistered from load balancer")
    
    async def select_agent(self, task_requirements: Dict[str, Any] = None) -> Optional[str]:
        """Select the best agent based on the configured algorithm"""
        
        healthy_agents = self._get_healthy_agents()
        
        if not healthy_agents:
            logging.warning("No healthy agents available")
            return None
        
        if self.config.algorithm == "round_robin":
            return self._round_robin_selection(healthy_agents)
        elif self.config.algorithm == "weighted_round_robin":
            return self._weighted_round_robin_selection(healthy_agents)
        elif self.config.algorithm == "least_connections":
            return self._least_connections_selection(healthy_agents)
        elif self.config.algorithm == "quality_weighted":
            return self._quality_weighted_selection(healthy_agents, task_requirements)
        else:
            return healthy_agents[0]  # Default to first healthy agent
    
    def _get_healthy_agents(self) -> List[str]:
        """Get list of healthy agents"""
        
        healthy = []
        for agent_id, health_info in self.agent_health.items():
            if health_info['healthy']:
                # Additional check for circuit breaker
                if (self.config.circuit_breaker_enabled and 
                    agent_id in self.circuit_breakers and 
                    self.circuit_breakers[agent_id].state == "OPEN"):
                    continue
                healthy.append(agent_id)
        
        return healthy
    
    def _round_robin_selection(self, agents: List[str]) -> str:
        """Simple round-robin selection"""
        
        # Use total request count to determine next agent
        total_requests = sum(self.request_counts.values())
        return agents[total_requests % len(agents)]
    
    def _weighted_round_robin_selection(self, agents: List[str]) -> str:
        """Weighted round-robin based on agent weights and performance"""
        
        # Calculate effective weights based on current performance
        weights = []
        for agent_id in agents:
            base_weight = self.agent_metrics[agent_id]['weight']
            performance_modifier = (
                (2.0 - self.agent_metrics[agent_id]['load_score']) *
                self.agent_metrics[agent_id]['quality_score']
            )
            effective_weight = base_weight * performance_modifier
            weights.append(max(0.1, effective_weight))  # Minimum weight of 0.1
        
        # Weighted random selection
        total_weight = sum(weights)
        if total_weight == 0:
            return agents[0]
        
        import random
        rand_val = random.uniform(0, total_weight)
        cumulative_weight = 0
        
        for i, weight in enumerate(weights):
            cumulative_weight += weight
            if rand_val <= cumulative_weight:
                return agents[i]
        
        return agents[-1]  # Fallback to last agent
    
    def _least_connections_selection(self, agents: List[str]) -> str:
        """Select agent with least current connections"""
        
        min_connections = float('inf')
        selected_agent = agents[0]
        
        for agent_id in agents:
            connections = self.agent_metrics[agent_id]['current_connections']
            if connections < min_connections:
                min_connections = connections
                selected_agent = agent_id
        
        return selected_agent
    
    def _quality_weighted_selection(self, agents: List[str], 
                                   task_requirements: Dict[str, Any] = None) -> str:
        """Select agent based on quality score and task requirements"""
        
        scores = {}
        
        for agent_id in agents:
            metrics = self.agent_metrics[agent_id]
            
            # Base score from quality and performance
            base_score = (
                metrics['quality_score'] * 0.4 +
                (1.0 - metrics['load_score']) * 0.3 +
                (1.0 / max(1.0, metrics['average_response_time'])) * 0.2 +
                (1.0 - metrics['total_failures'] / max(1, metrics['total_requests'])) * 0.1
            )
            
            # Adjust score based on task requirements
            if task_requirements:
                if task_requirements.get('priority') == 'high':
                    # Prefer less loaded agents for high priority
                    base_score *= (2.0 - metrics['load_score'])
                
                if task_requirements.get('quality_critical', False):
                    # Heavily weight quality for quality-critical tasks
                    base_score *= (metrics['quality_score'] ** 2)
                
                if task_requirements.get('cost_sensitive', False):
                    # Consider cost efficiency (not implemented in this simplified version)
                    pass
            
            scores[agent_id] = base_score
        
        # Select agent with highest score
        return max(scores.items(), key=lambda x: x[1])[0]
    
    async def execute_request(self, agent_id: str, request_func: Callable, 
                            *args, **kwargs) -> Any:
        """Execute request through load balancer with health tracking"""
        
        start_time = time.time()
        
        try:
            # Update connection count
            self.agent_metrics[agent_id]['current_connections'] += 1
            
            # Execute through circuit breaker if enabled
            if self.config.circuit_breaker_enabled and agent_id in self.circuit_breakers:
                result = await self.circuit_breakers[agent_id].call(request_func, *args, **kwargs)
            else:
                result = await request_func(*args, **kwargs)
            
            # Record success
            execution_time = (time.time() - start_time) * 1000  # ms
            self._record_success(agent_id, execution_time)
            
            return result
            
        except Exception as e:
            # Record failure
            execution_time = (time.time() - start_time) * 1000  # ms
            self._record_failure(agent_id, execution_time, str(e))
            raise e
            
        finally:
            # Update connection count
            self.agent_metrics[agent_id]['current_connections'] -= 1
    
    def _record_success(self, agent_id: str, execution_time_ms: float):
        """Record successful request"""
        
        # Update health tracking
        health_info = self.agent_health[agent_id]
        health_info['consecutive_failures'] = 0
        health_info['consecutive_successes'] += 1
        health_info['last_success'] = datetime.now()
        
        # Ensure agent is marked healthy if it was unhealthy
        if (not health_info['healthy'] and 
            health_info['consecutive_successes'] >= self.config.recovery_threshold):
            health_info['healthy'] = True
            logging.info(f"Agent {agent_id} recovered and marked healthy")
        
        # Update metrics
        metrics = self.agent_metrics[agent_id]
        metrics['total_requests'] += 1
        
        # Update response time (rolling average)
        self.response_times[agent_id].append(execution_time_ms)
        if len(self.response_times[agent_id]) > 100:  # Keep last 100 response times
            self.response_times[agent_id].pop(0)
        
        metrics['average_response_time'] = statistics.mean(self.response_times[agent_id])
        
        # Update request count
        self.request_counts[agent_id] += 1
    
    def _record_failure(self, agent_id: str, execution_time_ms: float, error: str):
        """Record failed request"""
        
        # Update health tracking
        health_info = self.agent_health[agent_id]
        health_info['consecutive_successes'] = 0
        health_info['consecutive_failures'] += 1
        health_info['last_failure'] = datetime.now()
        
        # Mark unhealthy if failure threshold reached
        if (health_info['healthy'] and 
            health_info['consecutive_failures'] >= self.config.failure_threshold):
            health_info['healthy'] = False
            logging.warning(f"Agent {agent_id} marked unhealthy after {health_info['consecutive_failures']} consecutive failures")
        
        # Update metrics
        metrics = self.agent_metrics[agent_id]
        metrics['total_requests'] += 1
        metrics['total_failures'] += 1
        
        logging.warning(f"Request to agent {agent_id} failed: {error}")
    
    async def _health_check_loop(self):
        """Periodic health check loop"""
        
        while self.running:
            try:
                await self._perform_health_checks()
                await asyncio.sleep(self.config.health_check_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(f"Health check error: {e}")
                await asyncio.sleep(5)  # Brief pause before retrying
    
    async def _perform_health_checks(self):
        """Perform health checks on all agents"""
        
        # This would typically ping each agent or check their status
        # For now, we'll update load scores based on current metrics
        
        for agent_id in self.agent_metrics:
            metrics = self.agent_metrics[agent_id]
            
            # Calculate load score (0.0 = no load, 1.0 = fully loaded)
            connection_load = min(1.0, metrics['current_connections'] / 10.0)
            response_time_load = min(1.0, metrics['average_response_time'] / 5000.0)  # 5s max
            
            metrics['load_score'] = (connection_load + response_time_load) / 2.0
            
            # Update quality score based on recent performance
            if metrics['total_requests'] > 0:
                success_rate = 1.0 - (metrics['total_failures'] / metrics['total_requests'])
                metrics['quality_score'] = success_rate
    
    def get_load_balancer_stats(self) -> Dict[str, Any]:
        """Get comprehensive load balancer statistics"""
        
        total_requests = sum(metrics['total_requests'] for metrics in self.agent_metrics.values())
        total_failures = sum(metrics['total_failures'] for metrics in self.agent_metrics.values())
        
        healthy_agents = self._get_healthy_agents()
        
        agent_stats = {}
        for agent_id, metrics in self.agent_metrics.items():
            agent_stats[agent_id] = {
                **metrics,
                'health_status': self.agent_health[agent_id],
                'circuit_breaker_state': (
                    self.circuit_breakers[agent_id].get_state() 
                    if agent_id in self.circuit_breakers else None
                )
            }
        
        return {
            'total_requests': total_requests,
            'total_failures': total_failures,
            'overall_success_rate': 1.0 - (total_failures / max(1, total_requests)),
            'healthy_agents': len(healthy_agents),
            'total_agents': len(self.agent_metrics),
            'algorithm': self.config.algorithm,
            'agent_stats': agent_stats,
            'average_response_time': statistics.mean([
                metrics['average_response_time'] 
                for metrics in self.agent_metrics.values() 
                if metrics['average_response_time'] > 0
            ]) if self.agent_metrics else 0.0
        }

# Continue with the main AdaptiveScalingEngine class...