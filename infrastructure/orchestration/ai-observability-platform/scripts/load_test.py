#!/usr/bin/env python3
"""
Load Testing Script for AI Observability Platform

This script generates various load testing scenarios to validate
the platform's ability to handle billion-scale monitoring.
"""

import asyncio
import aiohttp
import json
import time
import random
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
import argparse
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import sys
import os

# Add the demo directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../demo'))
from monitoring_client import ObservabilityClient, AgentMetrics

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LoadTestScenario:
    """Base class for load test scenarios"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.metrics = {
            'requests_sent': 0,
            'requests_successful': 0,
            'requests_failed': 0,
            'avg_response_time': 0.0,
            'errors': []
        }
        
    async def run(self, duration_minutes: int, **kwargs):
        """Run the load test scenario"""
        raise NotImplementedError
        
    def get_results(self) -> Dict[str, Any]:
        """Get test results"""
        if self.metrics['requests_sent'] > 0:
            success_rate = self.metrics['requests_successful'] / self.metrics['requests_sent'] * 100
        else:
            success_rate = 0
            
        return {
            'scenario': self.name,
            'description': self.description,
            'total_requests': self.metrics['requests_sent'],
            'successful_requests': self.metrics['requests_successful'],
            'failed_requests': self.metrics['requests_failed'],
            'success_rate': success_rate,
            'avg_response_time': self.metrics['avg_response_time'],
            'error_count': len(self.metrics['errors']),
            'unique_errors': len(set(self.metrics['errors']))
        }

class BurstLoadScenario(LoadTestScenario):
    """Scenario that generates burst traffic patterns"""
    
    def __init__(self):
        super().__init__(
            "Burst Load",
            "Simulates sudden traffic spikes to test auto-scaling responsiveness"
        )
    
    async def run(self, duration_minutes: int = 10, max_agents: int = 5000, base_url: str = "http://localhost"):
        logger.info(f"Starting Burst Load scenario for {duration_minutes} minutes with {max_agents} max agents")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        async with ObservabilityClient(base_url) as client:
            # Register agents
            logger.info("Registering agents...")
            agents = []
            for i in range(max_agents):
                agent_id = f"burst_agent_{i:05d}"
                model_name = random.choice(['gpt-4o', 'claude-3.5-sonnet', 'gemini-pro'])
                agent_type = random.choice(['general', 'coding', 'research'])
                
                success = await client.register_agent(agent_id, model_name, agent_type)
                if success:
                    agents.append(agent_id)
                    self.metrics['requests_successful'] += 1
                else:
                    self.metrics['requests_failed'] += 1
                self.metrics['requests_sent'] += 1
            
            logger.info(f"Registered {len(agents)} agents")
            
            # Generate burst patterns
            while time.time() < end_time:
                current_time = time.time()
                elapsed = current_time - start_time
                
                # Create burst pattern: high activity for 30 seconds, then low for 90 seconds
                cycle_position = elapsed % 120  # 2-minute cycles
                
                if cycle_position < 30:
                    # High activity period
                    load_factor = 1.0
                    active_agents_ratio = 0.8
                    update_interval = 0.1
                else:
                    # Low activity period
                    load_factor = 0.2
                    active_agents_ratio = 0.3
                    update_interval = 1.0
                
                # Select active agents
                num_active = int(len(agents) * active_agents_ratio)
                active_agents = random.sample(agents, num_active)
                
                # Generate metrics with burst characteristics
                tasks = []
                for agent_id in active_agents:
                    metrics = self._generate_burst_metrics(load_factor)
                    task = self._update_agent_metrics(client, agent_id, metrics)
                    tasks.append(task)
                
                # Execute in batches
                batch_size = 200
                for i in range(0, len(tasks), batch_size):
                    batch = tasks[i:i + batch_size]
                    results = await asyncio.gather(*batch, return_exceptions=True)
                    
                    for result in results:
                        if isinstance(result, Exception):
                            self.metrics['requests_failed'] += 1
                            self.metrics['errors'].append(str(result))
                        else:
                            self.metrics['requests_successful'] += 1
                        self.metrics['requests_sent'] += 1
                
                await asyncio.sleep(update_interval)
                
                # Log progress
                progress = (elapsed / (duration_minutes * 60)) * 100
                logger.info(f"Burst Load progress: {progress:.1f}%, load_factor: {load_factor:.1f}")
    
    def _generate_burst_metrics(self, load_factor: float) -> AgentMetrics:
        """Generate metrics with burst characteristics"""
        # Base metrics amplified by load factor
        response_time = 0.5 * (1 + load_factor * 3) + random.gauss(0, 0.2)
        cpu_usage = 30 + (40 * load_factor) + random.gauss(0, 10)
        memory_usage = int((200 + 300 * load_factor) * 1024 * 1024 + random.gauss(0, 50*1024*1024))
        
        # Higher error rates during bursts
        error_count = int(load_factor * 5 + random.gauss(0, 2))
        success_count = int(50 * load_factor + random.gauss(0, 10))
        
        return AgentMetrics(
            response_time=max(0.1, response_time),
            cpu_usage=max(5, min(95, cpu_usage)),
            memory_usage=max(100*1024*1024, memory_usage),
            error_count=max(0, error_count),
            success_count=max(1, success_count),
            queue_length=int(load_factor * 20 + random.gauss(0, 5)),
            intelligence_metrics={
                'accuracy': max(0.1, 0.8 - load_factor * 0.2 + random.gauss(0, 0.05)),
                'coherence': max(0.1, 0.75 - load_factor * 0.15 + random.gauss(0, 0.03)),
                'efficiency': max(0.1, 0.7 - load_factor * 0.1 + random.gauss(0, 0.04)),
                'adaptability': max(0.1, 0.65 + random.gauss(0, 0.1))
            },
            input_tokens=int(500 + 1000 * load_factor + random.gauss(0, 200)),
            output_tokens=int(200 + 400 * load_factor + random.gauss(0, 100))
        )
    
    async def _update_agent_metrics(self, client: ObservabilityClient, agent_id: str, metrics: AgentMetrics):
        """Update agent metrics with timing"""
        start_time = time.time()
        try:
            success = await client.update_agent_metrics(agent_id, metrics)
            response_time = time.time() - start_time
            self.metrics['avg_response_time'] = (
                (self.metrics['avg_response_time'] * (self.metrics['requests_sent'] - 1) + response_time) 
                / self.metrics['requests_sent']
            ) if self.metrics['requests_sent'] > 0 else response_time
            return success
        except Exception as e:
            raise e

class SustainedLoadScenario(LoadTestScenario):
    """Scenario that generates sustained high load"""
    
    def __init__(self):
        super().__init__(
            "Sustained Load",
            "Tests system stability under continuous high load"
        )
    
    async def run(self, duration_minutes: int = 15, max_agents: int = 8000, base_url: str = "http://localhost"):
        logger.info(f"Starting Sustained Load scenario for {duration_minutes} minutes with {max_agents} agents")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        async with ObservabilityClient(base_url) as client:
            # Register all agents
            logger.info("Registering agents...")
            agents = []
            batch_size = 500
            
            for i in range(0, max_agents, batch_size):
                batch_agents = []
                batch_end = min(i + batch_size, max_agents)
                
                for j in range(i, batch_end):
                    agent_id = f"sustained_agent_{j:05d}"
                    model_name = random.choice(['gpt-4o', 'claude-3.5-sonnet', 'gemini-pro', 'llama-3.1-70b'])
                    agent_type = random.choice(['general', 'coding', 'research', 'creative', 'analytical'])
                    
                    try:
                        success = await client.register_agent(agent_id, model_name, agent_type)
                        if success:
                            batch_agents.append(agent_id)
                            self.metrics['requests_successful'] += 1
                        else:
                            self.metrics['requests_failed'] += 1
                    except Exception as e:
                        self.metrics['requests_failed'] += 1
                        self.metrics['errors'].append(str(e))
                    
                    self.metrics['requests_sent'] += 1
                
                agents.extend(batch_agents)
                logger.info(f"Registered batch {i//batch_size + 1}/{(max_agents-1)//batch_size + 1}, "
                          f"total agents: {len(agents)}")
                
                await asyncio.sleep(1)  # Brief pause between batches
            
            logger.info(f"Successfully registered {len(agents)} agents, starting sustained load...")
            
            # Sustained load loop
            update_cycle = 0
            while time.time() < end_time:
                update_cycle += 1
                cycle_start = time.time()
                
                # Update all agents every cycle
                tasks = []
                for agent_id in agents:
                    metrics = self._generate_sustained_metrics()
                    task = self._update_agent_metrics(client, agent_id, metrics)
                    tasks.append(task)
                
                # Process in batches to control load
                batch_size = 300
                successful_updates = 0
                failed_updates = 0
                
                for i in range(0, len(tasks), batch_size):
                    batch = tasks[i:i + batch_size]
                    results = await asyncio.gather(*batch, return_exceptions=True)
                    
                    for result in results:
                        if isinstance(result, Exception):
                            failed_updates += 1
                            self.metrics['errors'].append(str(result))
                        else:
                            successful_updates += 1
                        self.metrics['requests_sent'] += 1
                
                self.metrics['requests_successful'] += successful_updates
                self.metrics['requests_failed'] += failed_updates
                
                cycle_time = time.time() - cycle_start
                elapsed = time.time() - start_time
                progress = (elapsed / (duration_minutes * 60)) * 100
                
                logger.info(f"Sustained Load cycle {update_cycle}: {progress:.1f}% complete, "
                          f"cycle time: {cycle_time:.2f}s, success rate: {successful_updates/(successful_updates+failed_updates)*100:.1f}%")
                
                # Aim for consistent update intervals
                target_interval = 10  # 10 seconds between full updates
                if cycle_time < target_interval:
                    await asyncio.sleep(target_interval - cycle_time)
    
    def _generate_sustained_metrics(self) -> AgentMetrics:
        """Generate realistic metrics for sustained load"""
        return AgentMetrics(
            response_time=random.lognormal(0.5, 0.5),  # Log-normal distribution for response times
            cpu_usage=random.normal(60, 15),  # Higher CPU usage under sustained load
            memory_usage=int(random.normal(400 * 1024 * 1024, 100 * 1024 * 1024)),  # ~400MB average
            error_count=int(max(0, random.poisson(2))),  # Poisson distribution for errors
            success_count=int(random.normal(100, 20)),
            queue_length=int(max(0, random.normal(15, 8))),
            intelligence_metrics={
                'accuracy': random.beta(8, 2),  # Skewed towards higher accuracy
                'coherence': random.beta(7, 3),
                'efficiency': random.beta(6, 4),
                'adaptability': random.beta(5, 5)
            },
            input_tokens=int(random.normal(800, 300)),
            output_tokens=int(random.normal(300, 100))
        )
    
    async def _update_agent_metrics(self, client: ObservabilityClient, agent_id: str, metrics: AgentMetrics):
        """Update agent metrics with error handling"""
        start_time = time.time()
        try:
            success = await client.update_agent_metrics(agent_id, metrics)
            response_time = time.time() - start_time
            self.metrics['avg_response_time'] = (
                (self.metrics['avg_response_time'] * (self.metrics['requests_sent'] - 1) + response_time) 
                / self.metrics['requests_sent']
            ) if self.metrics['requests_sent'] > 0 else response_time
            return success
        except Exception as e:
            response_time = time.time() - start_time
            self.metrics['avg_response_time'] = (
                (self.metrics['avg_response_time'] * (self.metrics['requests_sent'] - 1) + response_time) 
                / self.metrics['requests_sent']
            ) if self.metrics['requests_sent'] > 0 else response_time
            raise e

class AnomalyInjectionScenario(LoadTestScenario):
    """Scenario that injects various anomalies to test detection systems"""
    
    def __init__(self):
        super().__init__(
            "Anomaly Injection",
            "Injects known anomalies to test detection accuracy and response times"
        )
        self.injected_anomalies = []
        self.detected_anomalies = []
    
    async def run(self, duration_minutes: int = 8, max_agents: int = 2000, base_url: str = "http://localhost"):
        logger.info(f"Starting Anomaly Injection scenario for {duration_minutes} minutes with {max_agents} agents")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        async with ObservabilityClient(base_url) as client:
            # Register agents
            logger.info("Registering agents...")
            agents = []
            for i in range(max_agents):
                agent_id = f"anomaly_agent_{i:05d}"
                model_name = random.choice(['gpt-4o', 'claude-3.5-sonnet'])
                agent_type = random.choice(['general', 'research'])
                
                success = await client.register_agent(agent_id, model_name, agent_type)
                if success:
                    agents.append(agent_id)
                    self.metrics['requests_successful'] += 1
                else:
                    self.metrics['requests_failed'] += 1
                self.metrics['requests_sent'] += 1
            
            logger.info(f"Registered {len(agents)} agents")
            
            # Anomaly injection loop
            anomaly_injection_interval = 30  # Inject anomalies every 30 seconds
            last_anomaly_injection = start_time
            
            while time.time() < end_time:
                current_time = time.time()
                
                # Inject anomalies periodically
                if current_time - last_anomaly_injection >= anomaly_injection_interval:
                    await self._inject_anomalies(client, agents)
                    last_anomaly_injection = current_time
                
                # Update all agents with normal or anomalous metrics
                tasks = []
                for agent_id in agents:
                    # 95% normal metrics, 5% anomalous
                    if random.random() < 0.05:
                        metrics, anomaly_type = self._generate_anomalous_metrics()
                        self.injected_anomalies.append({
                            'agent_id': agent_id,
                            'anomaly_type': anomaly_type,
                            'timestamp': datetime.now(),
                            'metrics': metrics
                        })
                    else:
                        metrics = self._generate_normal_metrics()
                    
                    task = self._update_and_detect(client, agent_id, metrics)
                    tasks.append(task)
                
                # Process updates
                batch_size = 200
                for i in range(0, len(tasks), batch_size):
                    batch = tasks[i:i + batch_size]
                    results = await asyncio.gather(*batch, return_exceptions=True)
                    
                    for result in results:
                        if isinstance(result, Exception):
                            self.metrics['requests_failed'] += 1
                            self.metrics['errors'].append(str(result))
                        else:
                            self.metrics['requests_successful'] += 1
                            if result:  # Anomalies detected
                                self.detected_anomalies.extend(result)
                        self.metrics['requests_sent'] += 1
                
                await asyncio.sleep(5)  # Update every 5 seconds
                
                elapsed = current_time - start_time
                progress = (elapsed / (duration_minutes * 60)) * 100
                logger.info(f"Anomaly Injection progress: {progress:.1f}%, "
                          f"injected: {len(self.injected_anomalies)}, detected: {len(self.detected_anomalies)}")
    
    async def _inject_anomalies(self, client: ObservabilityClient, agents: List[str]):
        """Inject specific anomaly patterns"""
        # Select 10% of agents for anomaly injection
        anomaly_agents = random.sample(agents, max(1, len(agents) // 10))
        
        anomaly_types = ['performance_spike', 'memory_leak', 'error_burst', 'intelligence_drop']
        
        for agent_id in anomaly_agents:
            anomaly_type = random.choice(anomaly_types)
            metrics, _ = self._generate_anomalous_metrics(anomaly_type)
            
            self.injected_anomalies.append({
                'agent_id': agent_id,
                'anomaly_type': anomaly_type,
                'timestamp': datetime.now(),
                'metrics': metrics,
                'injection_type': 'forced'
            })
            
            # Send anomalous metrics
            try:
                await client.update_agent_metrics(agent_id, metrics)
                # Check for detection
                anomalies = await client.detect_anomalies(agent_id, metrics)
                if anomalies:
                    self.detected_anomalies.extend(anomalies)
            except Exception as e:
                self.metrics['errors'].append(str(e))
        
        logger.info(f"Injected {len(anomaly_agents)} forced anomalies")
    
    def _generate_normal_metrics(self) -> AgentMetrics:
        """Generate normal agent metrics"""
        return AgentMetrics(
            response_time=random.uniform(0.2, 2.0),
            cpu_usage=random.uniform(20, 70),
            memory_usage=int(random.uniform(100*1024*1024, 800*1024*1024)),
            error_count=int(random.poisson(1)),
            success_count=int(random.uniform(50, 150)),
            queue_length=int(random.uniform(0, 20)),
            intelligence_metrics={
                'accuracy': random.uniform(0.7, 0.95),
                'coherence': random.uniform(0.65, 0.9),
                'efficiency': random.uniform(0.6, 0.85),
                'adaptability': random.uniform(0.5, 0.8)
            },
            input_tokens=int(random.uniform(200, 1000)),
            output_tokens=int(random.uniform(100, 500))
        )
    
    def _generate_anomalous_metrics(self, anomaly_type: str = None) -> tuple:
        """Generate anomalous metrics"""
        if anomaly_type is None:
            anomaly_type = random.choice(['performance_spike', 'memory_leak', 'error_burst', 'intelligence_drop'])
        
        base_metrics = self._generate_normal_metrics()
        
        if anomaly_type == 'performance_spike':
            base_metrics.response_time *= random.uniform(10, 50)
            base_metrics.cpu_usage = min(95, base_metrics.cpu_usage * 2)
            
        elif anomaly_type == 'memory_leak':
            base_metrics.memory_usage *= random.uniform(5, 20)
            
        elif anomaly_type == 'error_burst':
            base_metrics.error_count *= random.randint(20, 100)
            base_metrics.success_count = max(1, base_metrics.success_count // 5)
            
        elif anomaly_type == 'intelligence_drop':
            for key in base_metrics.intelligence_metrics:
                base_metrics.intelligence_metrics[key] *= random.uniform(0.1, 0.4)
        
        return base_metrics, anomaly_type
    
    async def _update_and_detect(self, client: ObservabilityClient, agent_id: str, metrics: AgentMetrics):
        """Update metrics and check for anomaly detection"""
        start_time = time.time()
        try:
            # Update metrics
            await client.update_agent_metrics(agent_id, metrics)
            
            # Check for anomaly detection
            anomalies = await client.detect_anomalies(agent_id, metrics)
            
            response_time = time.time() - start_time
            self.metrics['avg_response_time'] = (
                (self.metrics['avg_response_time'] * (self.metrics['requests_sent'] - 1) + response_time) 
                / self.metrics['requests_sent']
            ) if self.metrics['requests_sent'] > 0 else response_time
            
            return anomalies
            
        except Exception as e:
            response_time = time.time() - start_time
            self.metrics['avg_response_time'] = (
                (self.metrics['avg_response_time'] * (self.metrics['requests_sent'] - 1) + response_time) 
                / self.metrics['requests_sent']
            ) if self.metrics['requests_sent'] > 0 else response_time
            raise e
    
    def get_results(self) -> Dict[str, Any]:
        """Get enhanced results with anomaly detection metrics"""
        base_results = super().get_results()
        
        # Calculate detection accuracy
        detection_rate = 0
        if len(self.injected_anomalies) > 0:
            # Simple detection rate calculation (can be improved with time-window matching)
            detection_rate = min(len(self.detected_anomalies) / len(self.injected_anomalies), 1.0) * 100
        
        base_results.update({
            'injected_anomalies': len(self.injected_anomalies),
            'detected_anomalies': len(self.detected_anomalies),
            'detection_rate': detection_rate,
            'anomaly_types_injected': list(set([a['anomaly_type'] for a in self.injected_anomalies])),
            'anomaly_types_detected': list(set([a.get('anomaly_type', 'unknown') for a in self.detected_anomalies]))
        })
        
        return base_results

class LoadTestRunner:
    """Main load test runner"""
    
    def __init__(self, base_url: str = "http://localhost"):
        self.base_url = base_url
        self.scenarios = {
            'burst': BurstLoadScenario(),
            'sustained': SustainedLoadScenario(),
            'anomaly': AnomalyInjectionScenario()
        }
    
    async def run_scenario(self, scenario_name: str, **kwargs) -> Dict[str, Any]:
        """Run a specific scenario"""
        if scenario_name not in self.scenarios:
            raise ValueError(f"Unknown scenario: {scenario_name}")
        
        scenario = self.scenarios[scenario_name]
        logger.info(f"Starting scenario: {scenario.name}")
        logger.info(f"Description: {scenario.description}")
        
        start_time = time.time()
        try:
            await scenario.run(base_url=self.base_url, **kwargs)
        except Exception as e:
            logger.error(f"Scenario {scenario_name} failed: {e}")
            scenario.metrics['errors'].append(str(e))
        
        end_time = time.time()
        
        results = scenario.get_results()
        results['duration_seconds'] = end_time - start_time
        results['start_time'] = datetime.fromtimestamp(start_time).isoformat()
        results['end_time'] = datetime.fromtimestamp(end_time).isoformat()
        
        return results
    
    async def run_full_suite(self, duration_per_scenario: int = 10) -> Dict[str, Any]:
        """Run all load test scenarios"""
        logger.info("Starting full load test suite")
        
        all_results = {}
        total_start_time = time.time()
        
        for scenario_name in ['burst', 'sustained', 'anomaly']:
            logger.info(f"\n{'='*50}")
            logger.info(f"Running {scenario_name} scenario")
            logger.info(f"{'='*50}")
            
            try:
                results = await self.run_scenario(
                    scenario_name,
                    duration_minutes=duration_per_scenario,
                    max_agents=2000 if scenario_name == 'anomaly' else 5000
                )
                all_results[scenario_name] = results
                
                # Log summary
                logger.info(f"\n{scenario_name.title()} Scenario Results:")
                logger.info(f"  Duration: {results['duration_seconds']:.1f} seconds")
                logger.info(f"  Total Requests: {results['total_requests']:,}")
                logger.info(f"  Success Rate: {results['success_rate']:.1f}%")
                logger.info(f"  Avg Response Time: {results['avg_response_time']:.3f}s")
                logger.info(f"  Error Count: {results['error_count']}")
                
                if scenario_name == 'anomaly':
                    logger.info(f"  Injected Anomalies: {results['injected_anomalies']}")
                    logger.info(f"  Detected Anomalies: {results['detected_anomalies']}")
                    logger.info(f"  Detection Rate: {results['detection_rate']:.1f}%")
                
            except Exception as e:
                logger.error(f"Failed to run {scenario_name} scenario: {e}")
                all_results[scenario_name] = {'error': str(e)}
            
            # Brief pause between scenarios
            if scenario_name != 'anomaly':  # Don't pause after last scenario
                logger.info("Waiting 30 seconds before next scenario...")
                await asyncio.sleep(30)
        
        total_end_time = time.time()
        
        # Calculate overall statistics
        total_requests = sum(r.get('total_requests', 0) for r in all_results.values())
        total_successful = sum(r.get('successful_requests', 0) for r in all_results.values())
        overall_success_rate = (total_successful / total_requests * 100) if total_requests > 0 else 0
        
        summary = {
            'test_suite': 'AI Observability Platform Load Test',
            'total_duration_seconds': total_end_time - total_start_time,
            'total_requests': total_requests,
            'total_successful_requests': total_successful,
            'overall_success_rate': overall_success_rate,
            'scenarios_run': len(all_results),
            'scenarios_successful': len([r for r in all_results.values() if 'error' not in r]),
            'scenario_results': all_results
        }
        
        return summary

def print_results(results: Dict[str, Any]):
    """Print formatted test results"""
    print("\n" + "="*80)
    print(f"🎯 {results['test_suite']} - RESULTS")
    print("="*80)
    print(f"Total Duration: {results['total_duration_seconds']:.1f} seconds")
    print(f"Total Requests: {results['total_requests']:,}")
    print(f"Overall Success Rate: {results['overall_success_rate']:.1f}%")
    print(f"Scenarios Run: {results['scenarios_run']}")
    print(f"Scenarios Successful: {results['scenarios_successful']}")
    
    print("\n📊 Scenario Breakdown:")
    print("-" * 80)
    
    for scenario_name, scenario_results in results['scenario_results'].items():
        if 'error' in scenario_results:
            print(f"❌ {scenario_name.title()}: FAILED - {scenario_results['error']}")
        else:
            print(f"✅ {scenario_name.title()}:")
            print(f"   Duration: {scenario_results['duration_seconds']:.1f}s")
            print(f"   Requests: {scenario_results['total_requests']:,}")
            print(f"   Success Rate: {scenario_results['success_rate']:.1f}%")
            print(f"   Avg Response Time: {scenario_results['avg_response_time']:.3f}s")
            
            if 'detection_rate' in scenario_results:
                print(f"   Anomaly Detection Rate: {scenario_results['detection_rate']:.1f}%")
    
    print("\n" + "="*80)
    
    # Performance assessment
    if results['overall_success_rate'] >= 95:
        print("🏆 EXCELLENT: System performance exceeds expectations")
    elif results['overall_success_rate'] >= 90:
        print("✅ GOOD: System performance meets requirements")
    elif results['overall_success_rate'] >= 80:
        print("⚠️  ACCEPTABLE: System performance needs improvement")
    else:
        print("❌ POOR: System performance is below acceptable levels")
    
    print("="*80)

async def main():
    parser = argparse.ArgumentParser(description='Load Testing for AI Observability Platform')
    parser.add_argument('--scenario', choices=['burst', 'sustained', 'anomaly', 'full'],
                       default='full', help='Load test scenario to run')
    parser.add_argument('--duration', type=int, default=10,
                       help='Duration per scenario in minutes')
    parser.add_argument('--max-agents', type=int, default=5000,
                       help='Maximum number of agents to simulate')
    parser.add_argument('--base-url', default='http://localhost',
                       help='Base URL for the observability platform')
    parser.add_argument('--output', help='Output file for results (JSON format)')
    
    args = parser.parse_args()
    
    runner = LoadTestRunner(base_url=args.base_url)
    
    try:
        if args.scenario == 'full':
            results = await runner.run_full_suite(duration_per_scenario=args.duration)
        else:
            results = await runner.run_scenario(
                args.scenario,
                duration_minutes=args.duration,
                max_agents=args.max_agents
            )
            # Wrap single scenario in suite format
            results = {
                'test_suite': f'AI Observability Platform - {args.scenario.title()} Load Test',
                'total_duration_seconds': results['duration_seconds'],
                'total_requests': results['total_requests'],
                'total_successful_requests': results['successful_requests'],
                'overall_success_rate': results['success_rate'],
                'scenarios_run': 1,
                'scenarios_successful': 1 if results['success_rate'] > 0 else 0,
                'scenario_results': {args.scenario: results}
            }
        
        # Print results
        print_results(results)
        
        # Save results if requested
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"\n💾 Results saved to {args.output}")
        
    except KeyboardInterrupt:
        logger.info("Load test interrupted by user")
    except Exception as e:
        logger.error(f"Load test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())