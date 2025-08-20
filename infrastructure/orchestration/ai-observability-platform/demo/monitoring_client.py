#!/usr/bin/env python3
"""
Monitoring Client Library for AI Observability Platform

Provides easy-to-use client libraries for integrating AI agents with the
billion-scale observability platform.
"""

import asyncio
import aiohttp
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
import uuid
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AgentMetrics:
    """Data class for agent metrics"""
    response_time: float
    cpu_usage: float
    memory_usage: int
    error_count: int = 0
    success_count: int = 1
    queue_length: int = 0
    intelligence_metrics: Dict[str, float] = None
    input_tokens: int = 0
    output_tokens: int = 0
    inference_time: float = 0.0
    model_load_time: float = 0.0
    context_length: int = 0

    def __post_init__(self):
        if self.intelligence_metrics is None:
            self.intelligence_metrics = {
                'accuracy': 0.0,
                'coherence': 0.0,
                'efficiency': 0.0,
                'adaptability': 0.0
            }

@dataclass
class AgentInteraction:
    """Data class for agent interactions"""
    source_agent: str
    target_agent: str
    interaction_type: str
    strength: float
    timestamp: datetime
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class ObservabilityClient:
    """Client for interacting with the AI observability platform"""
    
    def __init__(self, base_url: str = "http://localhost", timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = None
        
        # Service endpoints
        self.endpoints = {
            'health_monitor': f"{base_url}:8080",
            'anomaly_detector': f"{base_url}:8081",
            'emergence_detector': f"{base_url}:8082",
            'autoscaler': f"{base_url}:8083"
        }
        
        # Agent registry
        self.registered_agents = set()
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    async def register_agent(self, agent_id: str, model_name: str, agent_type: str, **metadata) -> bool:
        """Register an AI agent with the monitoring system"""
        try:
            agent_metadata = {
                'model_name': model_name,
                'type': agent_type,
                **metadata
            }
            
            url = f"{self.endpoints['health_monitor']}/agents/{agent_id}/register"
            async with self.session.post(url, json=agent_metadata) as response:
                if response.status == 200:
                    self.registered_agents.add(agent_id)
                    logger.info(f"Successfully registered agent {agent_id}")
                    return True
                else:
                    logger.error(f"Failed to register agent {agent_id}: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error registering agent {agent_id}: {e}")
            return False

    async def update_agent_metrics(self, agent_id: str, metrics: AgentMetrics) -> bool:
        """Update metrics for an AI agent"""
        try:
            if agent_id not in self.registered_agents:
                logger.warning(f"Agent {agent_id} not registered, registering now...")
                await self.register_agent(agent_id, "unknown", "general")
            
            metrics_dict = asdict(metrics)
            url = f"{self.endpoints['health_monitor']}/agents/{agent_id}/metrics"
            
            async with self.session.post(url, json=metrics_dict) as response:
                if response.status == 200:
                    return True
                else:
                    logger.error(f"Failed to update metrics for {agent_id}: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error updating metrics for {agent_id}: {e}")
            return False

    async def detect_anomalies(self, agent_id: str, metrics: AgentMetrics) -> List[Dict[str, Any]]:
        """Detect anomalies for an agent"""
        try:
            metrics_dict = asdict(metrics)
            url = f"{self.endpoints['anomaly_detector']}/detect/{agent_id}"
            
            async with self.session.post(url, json=metrics_dict) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get('alerts', [])
                else:
                    logger.error(f"Failed to detect anomalies for {agent_id}: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error detecting anomalies for {agent_id}: {e}")
            return []

    async def report_interaction(self, interaction: AgentInteraction) -> bool:
        """Report an interaction between agents"""
        try:
            interaction_dict = asdict(interaction)
            interaction_dict['timestamp'] = interaction.timestamp.isoformat()
            
            # Store interaction for emergence analysis
            # Note: In a real implementation, you might want to batch these
            logger.debug(f"Recorded interaction: {interaction.source_agent} -> {interaction.target_agent}")
            return True
            
        except Exception as e:
            logger.error(f"Error reporting interaction: {e}")
            return False

    async def get_agent_health(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get health information for an agent"""
        try:
            url = f"{self.endpoints['health_monitor']}/agents/{agent_id}"
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to get health for {agent_id}: {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error getting agent health for {agent_id}: {e}")
            return None

    async def get_all_agents(self) -> List[Dict[str, Any]]:
        """Get information about all registered agents"""
        try:
            url = f"{self.endpoints['health_monitor']}/agents"
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to get all agents: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error getting all agents: {e}")
            return []

    async def get_emergence_events(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get recent emergence events"""
        try:
            url = f"{self.endpoints['emergence_detector']}/events?hours={hours}"
            async with self.session.get(url) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get('events', [])
                else:
                    logger.error(f"Failed to get emergence events: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error getting emergence events: {e}")
            return []

    async def get_scaling_decisions(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get recent scaling decisions"""
        try:
            url = f"{self.endpoints['autoscaler']}/decisions?hours={hours}"
            async with self.session.get(url) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get('decisions', [])
                else:
                    logger.error(f"Failed to get scaling decisions: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error getting scaling decisions: {e}")
            return []

    async def get_system_efficiency(self) -> Dict[str, Any]:
        """Get system efficiency metrics"""
        try:
            url = f"{self.endpoints['autoscaler']}/efficiency"
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to get system efficiency: {response.status}")
                    return {}
                    
        except Exception as e:
            logger.error(f"Error getting system efficiency: {e}")
            return {}

class AIAgentMonitor:
    """High-level monitoring wrapper for AI agents"""
    
    def __init__(self, agent_id: str, model_name: str, agent_type: str, 
                 base_url: str = "http://localhost", auto_register: bool = True):
        self.agent_id = agent_id
        self.model_name = model_name
        self.agent_type = agent_type
        self.base_url = base_url
        self.client = None
        self.auto_register = auto_register
        
        # Metrics tracking
        self.current_metrics = AgentMetrics(
            response_time=0.0,
            cpu_usage=0.0,
            memory_usage=0
        )
        
        # Performance tracking
        self.request_start_time = None
        self.total_requests = 0
        self.successful_requests = 0
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.client = ObservabilityClient(self.base_url)
        await self.client.__aenter__()
        
        if self.auto_register:
            await self.client.register_agent(
                self.agent_id, 
                self.model_name, 
                self.agent_type
            )
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.client:
            await self.client.__aexit__(exc_type, exc_val, exc_tb)

    @asynccontextmanager
    async def track_request(self, input_tokens: int = 0, context_length: int = 0):
        """Context manager for tracking request performance"""
        self.request_start_time = time.time()
        self.total_requests += 1
        
        try:
            yield
            # Request successful
            self.successful_requests += 1
            
        except Exception as e:
            # Request failed
            logger.error(f"Request failed for agent {self.agent_id}: {e}")
            self.current_metrics.error_count += 1
            raise
            
        finally:
            # Calculate metrics
            if self.request_start_time:
                response_time = time.time() - self.request_start_time
                self.current_metrics.response_time = response_time
                self.current_metrics.success_count = self.successful_requests
                
                # Update tokens if provided
                if input_tokens > 0:
                    self.current_metrics.input_tokens = input_tokens
                if context_length > 0:
                    self.current_metrics.context_length = context_length
                
                # Send metrics to monitoring system
                await self.update_metrics()

    async def update_metrics(self, **additional_metrics):
        """Update agent metrics"""
        # Apply additional metrics
        for key, value in additional_metrics.items():
            if hasattr(self.current_metrics, key):
                setattr(self.current_metrics, key, value)
        
        # Send to monitoring system
        if self.client:
            await self.client.update_agent_metrics(self.agent_id, self.current_metrics)
            
            # Check for anomalies
            anomalies = await self.client.detect_anomalies(self.agent_id, self.current_metrics)
            if anomalies:
                logger.warning(f"Anomalies detected for agent {self.agent_id}: {len(anomalies)}")
                for anomaly in anomalies:
                    logger.warning(f"  - {anomaly.get('anomaly_type', 'unknown')}: {anomaly.get('description', 'no description')}")

    async def report_intelligence_metrics(self, accuracy: float, coherence: float, 
                                        efficiency: float, adaptability: float):
        """Report intelligence metrics"""
        self.current_metrics.intelligence_metrics = {
            'accuracy': accuracy,
            'coherence': coherence,
            'efficiency': efficiency,
            'adaptability': adaptability
        }
        await self.update_metrics()

    async def interact_with_agent(self, target_agent_id: str, interaction_type: str, 
                                strength: float = 1.0, **metadata):
        """Report interaction with another agent"""
        interaction = AgentInteraction(
            source_agent=self.agent_id,
            target_agent=target_agent_id,
            interaction_type=interaction_type,
            strength=strength,
            timestamp=datetime.now(),
            metadata=metadata
        )
        
        if self.client:
            await self.client.report_interaction(interaction)

# Convenience functions for quick integration
async def quick_register_agent(agent_id: str, model_name: str, agent_type: str, 
                             base_url: str = "http://localhost") -> bool:
    """Quick agent registration"""
    async with ObservabilityClient(base_url) as client:
        return await client.register_agent(agent_id, model_name, agent_type)

async def quick_update_metrics(agent_id: str, metrics: AgentMetrics, 
                             base_url: str = "http://localhost") -> bool:
    """Quick metrics update"""
    async with ObservabilityClient(base_url) as client:
        return await client.update_agent_metrics(agent_id, metrics)

async def quick_health_check(agent_id: str, base_url: str = "http://localhost") -> Optional[Dict[str, Any]]:
    """Quick health check"""
    async with ObservabilityClient(base_url) as client:
        return await client.get_agent_health(agent_id)

# Example usage
async def example_usage():
    """Example of how to use the monitoring client"""
    
    # Method 1: Using the high-level AIAgentMonitor
    async with AIAgentMonitor("example_agent", "gpt-4o", "general") as monitor:
        # Track a request
        async with monitor.track_request(input_tokens=500, context_length=2000):
            # Simulate some work
            await asyncio.sleep(0.1)
            
            # Simulate generating output
            output_tokens = 200
            await monitor.update_metrics(output_tokens=output_tokens)
        
        # Report intelligence metrics
        await monitor.report_intelligence_metrics(
            accuracy=0.95,
            coherence=0.88,
            efficiency=0.92,
            adaptability=0.85
        )
        
        # Report interaction with another agent
        await monitor.interact_with_agent(
            "other_agent",
            "collaboration",
            strength=0.8,
            context="problem_solving"
        )
    
    # Method 2: Using the low-level ObservabilityClient
    async with ObservabilityClient() as client:
        # Register agent
        await client.register_agent("low_level_agent", "claude-3.5-sonnet", "research")
        
        # Create metrics
        metrics = AgentMetrics(
            response_time=0.5,
            cpu_usage=45.0,
            memory_usage=512 * 1024 * 1024,  # 512MB
            intelligence_metrics={
                'accuracy': 0.92,
                'coherence': 0.89,
                'efficiency': 0.87,
                'adaptability': 0.91
            }
        )
        
        # Update metrics
        await client.update_agent_metrics("low_level_agent", metrics)
        
        # Check for anomalies
        anomalies = await client.detect_anomalies("low_level_agent", metrics)
        print(f"Detected {len(anomalies)} anomalies")
        
        # Get system overview
        all_agents = await client.get_all_agents()
        print(f"Total agents: {len(all_agents)}")
        
        emergence_events = await client.get_emergence_events(hours=1)
        print(f"Emergence events in last hour: {len(emergence_events)}")

if __name__ == "__main__":
    # Run example
    asyncio.run(example_usage())