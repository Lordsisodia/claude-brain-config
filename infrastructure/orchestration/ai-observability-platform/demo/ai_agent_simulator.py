#!/usr/bin/env python3
"""
AI Agent Simulator for Demonstrating Billion-Scale Monitoring

This script simulates 10,000+ AI agents with realistic behaviors,
metrics, and interactions to demonstrate the observability platform.
"""

import asyncio
import aiohttp
import json
import random
import time
import logging
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
import argparse
from concurrent.futures import ThreadPoolExecutor
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIAgentSimulator:
    def __init__(self, num_agents: int = 10000, base_url: str = "http://localhost"):
        self.num_agents = num_agents
        self.base_url = base_url
        self.agents = {}
        self.agent_behaviors = {}
        self.running = False
        
        # Service endpoints
        self.endpoints = {
            'health_monitor': f"{base_url}:8080",
            'anomaly_detector': f"{base_url}:8081", 
            'emergence_detector': f"{base_url}:8082",
            'autoscaler': f"{base_url}:8083"
        }
        
        # Agent behavior patterns
        self.behavior_templates = {
            'high_performer': {
                'base_intelligence': 0.85,
                'response_time_base': 0.5,
                'error_rate_base': 0.01,
                'resource_efficiency': 0.9
            },
            'average_performer': {
                'base_intelligence': 0.65,
                'response_time_base': 1.5,
                'error_rate_base': 0.03,
                'resource_efficiency': 0.7
            },
            'struggling_agent': {
                'base_intelligence': 0.45,
                'response_time_base': 3.0,
                'error_rate_base': 0.08,
                'resource_efficiency': 0.5
            },
            'anomalous_agent': {
                'base_intelligence': 0.3,
                'response_time_base': 8.0,
                'error_rate_base': 0.15,
                'resource_efficiency': 0.3
            }
        }
        
        # Model types for diversity
        self.model_types = [
            'gpt-4o', 'claude-3.5-sonnet', 'gemini-pro', 'llama-3.1-70b',
            'mixtral-8x7b', 'command-r-plus', 'phi-3-medium', 'qwen-72b'
        ]
        
        # Agent types for different use cases
        self.agent_types = [
            'general', 'coding', 'research', 'creative', 'analytical', 
            'customer-service', 'data-processing', 'content-generation'
        ]

    async def initialize_agents(self):
        """Initialize all AI agents with diverse characteristics"""
        logger.info(f"Initializing {self.num_agents} AI agents...")
        
        for i in range(self.num_agents):
            agent_id = f"agent_{i:06d}"
            
            # Assign behavior pattern (80% normal, 15% struggling, 5% anomalous)
            behavior_weights = [0.4, 0.4, 0.15, 0.05]  # high, average, struggling, anomalous
            behavior_type = np.random.choice(
                list(self.behavior_templates.keys()), 
                p=behavior_weights
            )
            
            # Assign model and agent type
            model_name = random.choice(self.model_types)
            agent_type = random.choice(self.agent_types)
            
            # Create agent profile
            agent_profile = {
                'agent_id': agent_id,
                'model_name': model_name,
                'agent_type': agent_type,
                'behavior_type': behavior_type,
                'created_at': datetime.now(),
                'region': random.choice(['us-west', 'us-east', 'eu-west', 'asia-pacific']),
                'cluster_id': f"cluster_{i // 100}",  # 100 agents per cluster
                'version': f"v{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}"
            }
            
            self.agents[agent_id] = agent_profile
            self.agent_behaviors[agent_id] = self.behavior_templates[behavior_type].copy()
            
            # Add some randomness to base values
            for key in self.agent_behaviors[agent_id]:
                if isinstance(self.agent_behaviors[agent_id][key], float):
                    noise = random.uniform(-0.1, 0.1)
                    self.agent_behaviors[agent_id][key] += noise
                    self.agent_behaviors[agent_id][key] = max(0, min(1, self.agent_behaviors[agent_id][key]))
        
        logger.info(f"Initialized {len(self.agents)} agents")
        
        # Register agents with health monitor
        await self.register_all_agents()

    async def register_all_agents(self):
        """Register all agents with the health monitoring service"""
        logger.info("Registering agents with health monitor...")
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for agent_id, profile in self.agents.items():
                metadata = {
                    'model_name': profile['model_name'],
                    'type': profile['agent_type'],
                    'cluster_id': profile['cluster_id'],
                    'region': profile['region'],
                    'version': profile['version']
                }
                
                task = self.register_agent(session, agent_id, metadata)
                tasks.append(task)
                
                # Batch registration to avoid overwhelming the service
                if len(tasks) >= 100:
                    await asyncio.gather(*tasks, return_exceptions=True)
                    tasks = []
            
            # Register remaining agents
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
        
        logger.info("Agent registration completed")

    async def register_agent(self, session: aiohttp.ClientSession, agent_id: str, metadata: Dict[str, Any]):
        """Register a single agent"""
        try:
            url = f"{self.endpoints['health_monitor']}/agents/{agent_id}/register"
            async with session.post(url, json=metadata) as response:
                if response.status == 200:
                    logger.debug(f"Registered agent {agent_id}")
                else:
                    logger.warning(f"Failed to register agent {agent_id}: {response.status}")
        except Exception as e:
            logger.error(f"Error registering agent {agent_id}: {e}")

    async def simulate_agent_activity(self):
        """Main simulation loop for agent activity"""
        logger.info("Starting agent activity simulation...")
        self.running = True
        
        async with aiohttp.ClientSession() as session:
            while self.running:
                # Generate metrics for all agents
                tasks = []
                
                for agent_id in self.agents.keys():
                    task = self.simulate_single_agent(session, agent_id)
                    tasks.append(task)
                    
                    # Process in batches to control load
                    if len(tasks) >= 500:
                        await asyncio.gather(*tasks, return_exceptions=True)
                        tasks = []
                        await asyncio.sleep(0.1)  # Small delay between batches
                
                # Process remaining tasks
                if tasks:
                    await asyncio.gather(*tasks, return_exceptions=True)
                
                # Generate agent interactions
                await self.simulate_agent_interactions(session)
                
                # Simulate some system events
                await self.simulate_system_events(session)
                
                # Wait before next cycle
                await asyncio.sleep(15)  # Update every 15 seconds

    async def simulate_single_agent(self, session: aiohttp.ClientSession, agent_id: str):
        """Simulate activity for a single agent"""
        try:
            behavior = self.agent_behaviors[agent_id]
            profile = self.agents[agent_id]
            
            # Generate realistic metrics with temporal patterns and noise
            current_time = datetime.now()
            time_factor = self.get_time_factor(current_time)
            
            # Base metrics with circadian rhythm and random noise
            base_load = 0.7 + 0.3 * time_factor + random.gauss(0, 0.1)
            base_load = max(0.1, min(1.0, base_load))
            
            metrics = {
                'response_time': max(0.1, behavior['response_time_base'] * base_load + random.gauss(0, 0.2)),
                'cpu_usage': max(5, min(95, 30 + 40 * base_load + random.gauss(0, 5))),
                'memory_usage': int(max(100*1024*1024, min(2*1024*1024*1024, 
                    (200 + 300 * base_load) * 1024 * 1024 + random.gauss(0, 50*1024*1024)))),
                'error_count': max(0, int(behavior['error_rate_base'] * 100 * base_load + random.gauss(0, 2))),
                'success_count': int(100 * base_load + random.gauss(0, 10)),
                'queue_length': max(0, int(20 * base_load + random.gauss(0, 5))),
                'intelligence_metrics': {
                    'accuracy': max(0, min(1, behavior['base_intelligence'] + random.gauss(0, 0.05))),
                    'coherence': max(0, min(1, behavior['base_intelligence'] * 0.9 + random.gauss(0, 0.03))),
                    'efficiency': max(0, min(1, behavior['resource_efficiency'] + random.gauss(0, 0.04))),
                    'adaptability': max(0, min(1, 0.7 + random.gauss(0, 0.1)))
                },
                'input_tokens': int(500 + 1000 * base_load + random.gauss(0, 200)),
                'output_tokens': int(200 + 400 * base_load + random.gauss(0, 100)),
                'inference_time': max(0.05, behavior['response_time_base'] * 0.8 + random.gauss(0, 0.1)),
                'model_load_time': random.uniform(0.1, 0.5),
                'context_length': int(2000 + 1000 * base_load + random.gauss(0, 500))
            }
            
            # Add some behavioral patterns based on agent type
            if profile['agent_type'] == 'coding':
                metrics['intelligence_metrics']['accuracy'] += 0.1
                metrics['context_length'] *= 1.5
            elif profile['agent_type'] == 'creative':
                metrics['output_tokens'] *= 1.3
                metrics['intelligence_metrics']['coherence'] += 0.05
            elif profile['agent_type'] == 'analytical':
                metrics['input_tokens'] *= 1.2
                metrics['inference_time'] *= 1.1
            
            # Simulate occasional anomalies
            if random.random() < 0.001:  # 0.1% chance
                self.inject_anomaly(metrics, behavior)
            
            # Update health monitor
            await self.update_agent_metrics(session, agent_id, metrics)
            
            # Send to anomaly detector
            await self.send_to_anomaly_detector(session, agent_id, metrics)
            
        except Exception as e:
            logger.error(f"Error simulating agent {agent_id}: {e}")

    def get_time_factor(self, current_time: datetime) -> float:
        """Generate circadian rhythm pattern (higher activity during business hours)"""
        hour = current_time.hour
        # Peak activity around 10 AM and 2 PM, lower at night
        if 8 <= hour <= 18:
            return 0.8 + 0.2 * np.sin((hour - 8) * np.pi / 10)
        else:
            return 0.3 + 0.2 * np.sin((hour + 16) % 24 * np.pi / 12)

    def inject_anomaly(self, metrics: Dict[str, Any], behavior: Dict[str, float]):
        """Inject various types of anomalies"""
        anomaly_type = random.choice(['performance', 'memory_leak', 'error_spike', 'intelligence_drop'])
        
        if anomaly_type == 'performance':
            metrics['response_time'] *= random.uniform(5, 20)
            metrics['cpu_usage'] = min(95, metrics['cpu_usage'] * 2)
            
        elif anomaly_type == 'memory_leak':
            metrics['memory_usage'] *= random.uniform(3, 8)
            
        elif anomaly_type == 'error_spike':
            metrics['error_count'] *= random.randint(10, 50)
            metrics['success_count'] = max(0, metrics['success_count'] // 2)
            
        elif anomaly_type == 'intelligence_drop':
            for key in metrics['intelligence_metrics']:
                metrics['intelligence_metrics'][key] *= random.uniform(0.2, 0.5)

    async def update_agent_metrics(self, session: aiohttp.ClientSession, agent_id: str, metrics: Dict[str, Any]):
        """Update agent metrics in the health monitor"""
        try:
            url = f"{self.endpoints['health_monitor']}/agents/{agent_id}/metrics"
            async with session.post(url, json=metrics, timeout=aiohttp.ClientTimeout(total=5)) as response:
                if response.status != 200:
                    logger.debug(f"Failed to update metrics for {agent_id}: {response.status}")
        except Exception as e:
            logger.debug(f"Error updating metrics for {agent_id}: {e}")

    async def send_to_anomaly_detector(self, session: aiohttp.ClientSession, agent_id: str, metrics: Dict[str, Any]):
        """Send metrics to anomaly detector"""
        try:
            url = f"{self.endpoints['anomaly_detector']}/detect/{agent_id}"
            async with session.post(url, json=metrics, timeout=aiohttp.ClientTimeout(total=5)) as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get('count', 0) > 0:
                        logger.info(f"Anomalies detected for {agent_id}: {result['count']}")
        except Exception as e:
            logger.debug(f"Error sending to anomaly detector for {agent_id}: {e}")

    async def simulate_agent_interactions(self, session: aiohttp.ClientSession):
        """Simulate interactions between agents"""
        try:
            # Generate random interactions
            num_interactions = random.randint(50, 200)
            interactions = []
            
            agent_ids = list(self.agents.keys())
            
            for _ in range(num_interactions):
                source_agent = random.choice(agent_ids)
                target_agent = random.choice(agent_ids)
                
                if source_agent != target_agent:
                    interaction = {
                        'source_agent': source_agent,
                        'target_agent': target_agent,
                        'interaction_type': random.choice([
                            'collaboration', 'data_sharing', 'model_sharing', 
                            'knowledge_transfer', 'task_delegation', 'peer_review'
                        ]),
                        'strength': random.uniform(0.1, 1.0),
                        'timestamp': datetime.now().isoformat(),
                        'metadata': {
                            'context': random.choice(['research', 'problem_solving', 'optimization', 'learning']),
                            'duration': random.uniform(0.5, 30.0),
                            'success': random.choice([True, True, True, False])  # 75% success rate
                        }
                    }
                    interactions.append(interaction)
            
            # Send to emergence detector for analysis
            if interactions:
                agents_data = [
                    {
                        'agent_id': agent_id,
                        'model_name': profile['model_name'],
                        'agent_type': profile['agent_type'],
                        'intelligence_metrics': {
                            'accuracy': self.agent_behaviors[agent_id]['base_intelligence'],
                            'coherence': self.agent_behaviors[agent_id]['base_intelligence'] * 0.9,
                            'efficiency': self.agent_behaviors[agent_id]['resource_efficiency'],
                            'adaptability': 0.7
                        },
                        'response_time': self.agent_behaviors[agent_id]['response_time_base'],
                        'cpu_usage': random.uniform(20, 80),
                        'memory_usage': random.randint(100*1024*1024, 1024*1024*1024),
                        'queue_length': random.randint(0, 50)
                    }
                    for agent_id, profile in random.sample(list(self.agents.items()), min(100, len(self.agents)))
                ]
                
                url = f"{self.endpoints['emergence_detector']}/analyze"
                payload = {
                    'agents_data': agents_data,
                    'interactions': interactions
                }
                
                async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('count', 0) > 0:
                            logger.info(f"Emergence events detected: {result['count']}")
                            for event in result.get('emergence_events', []):
                                logger.info(f"  - {event['emergence_type']}: {event['description']}")
                    
        except Exception as e:
            logger.error(f"Error simulating agent interactions: {e}")

    async def simulate_system_events(self, session: aiohttp.ClientSession):
        """Simulate system-level events like scaling decisions"""
        try:
            # Randomly trigger autoscaler analysis
            if random.random() < 0.3:  # 30% chance per cycle
                url = f"{self.endpoints['autoscaler']}/analyze"
                async with session.post(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('count', 0) > 0:
                            logger.info(f"Scaling decisions made: {result['count']}")
                            for decision in result.get('decisions', []):
                                logger.info(f"  - {decision['action_type']}: {decision['target_resource']} "
                                          f"({decision['current_instances']} -> {decision['target_instances']})")
        except Exception as e:
            logger.debug(f"Error in system events simulation: {e}")

    async def generate_load_test(self, duration_minutes: int = 10, ramp_up_minutes: int = 2):
        """Generate a load test scenario"""
        logger.info(f"Starting load test for {duration_minutes} minutes with {ramp_up_minutes} minute ramp-up")
        
        start_time = time.time()
        ramp_up_duration = ramp_up_minutes * 60
        total_duration = duration_minutes * 60
        
        async with aiohttp.ClientSession() as session:
            while time.time() - start_time < total_duration:
                elapsed = time.time() - start_time
                
                # Calculate load factor (ramp up, then steady, then ramp down)
                if elapsed < ramp_up_duration:
                    load_factor = elapsed / ramp_up_duration
                elif elapsed < total_duration - ramp_up_duration:
                    load_factor = 1.0
                else:
                    remaining = total_duration - elapsed
                    load_factor = remaining / ramp_up_duration
                
                load_factor = max(0.1, min(1.0, load_factor))
                
                # Simulate higher activity
                num_agents_to_update = int(self.num_agents * load_factor)
                agent_subset = random.sample(list(self.agents.keys()), num_agents_to_update)
                
                tasks = []
                for agent_id in agent_subset:
                    # Amplify metrics during load test
                    original_behavior = self.agent_behaviors[agent_id].copy()
                    self.agent_behaviors[agent_id]['response_time_base'] *= (1 + load_factor)
                    self.agent_behaviors[agent_id]['error_rate_base'] *= (1 + load_factor * 2)
                    
                    task = self.simulate_single_agent(session, agent_id)
                    tasks.append(task)
                    
                    # Restore original behavior
                    self.agent_behaviors[agent_id] = original_behavior
                
                # Process in smaller batches during load test
                batch_size = 100
                for i in range(0, len(tasks), batch_size):
                    batch = tasks[i:i + batch_size]
                    await asyncio.gather(*batch, return_exceptions=True)
                    await asyncio.sleep(0.05)  # Very short delay
                
                logger.info(f"Load test progress: {elapsed/60:.1f}/{duration_minutes} minutes, "
                          f"load factor: {load_factor:.2f}")
                
                await asyncio.sleep(2)  # Faster updates during load test
        
        logger.info("Load test completed")

    def stop_simulation(self):
        """Stop the simulation"""
        logger.info("Stopping simulation...")
        self.running = False

async def main():
    parser = argparse.ArgumentParser(description='AI Agent Simulator for Billion-Scale Monitoring')
    parser.add_argument('--agents', type=int, default=10000, help='Number of agents to simulate')
    parser.add_argument('--base-url', default='http://localhost', help='Base URL for services')
    parser.add_argument('--load-test', action='store_true', help='Run a load test scenario')
    parser.add_argument('--duration', type=int, default=60, help='Simulation duration in minutes')
    
    args = parser.parse_args()
    
    # Create simulator
    simulator = AIAgentSimulator(num_agents=args.agents, base_url=args.base_url)
    
    try:
        # Initialize agents
        await simulator.initialize_agents()
        
        if args.load_test:
            # Run load test
            await simulator.generate_load_test(duration_minutes=args.duration)
        else:
            # Run normal simulation
            task = asyncio.create_task(simulator.simulate_agent_activity())
            
            # Run for specified duration
            await asyncio.sleep(args.duration * 60)
            simulator.stop_simulation()
            
            # Wait for task to complete
            await task
            
    except KeyboardInterrupt:
        logger.info("Simulation interrupted by user")
        simulator.stop_simulation()
    except Exception as e:
        logger.error(f"Simulation error: {e}")
    finally:
        logger.info("Simulation finished")

if __name__ == "__main__":
    asyncio.run(main())