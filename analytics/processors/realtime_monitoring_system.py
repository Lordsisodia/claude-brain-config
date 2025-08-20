#!/usr/bin/env python3
"""
Real-Time Monitoring and Alert System
Complex system designed to trigger maximum agent delegation and tool usage.
"""

import json
import asyncio
import threading
import time
import random
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


class SystemHealthMonitor:
    """Monitors system health and performance metrics."""
    
    def __init__(self, monitor_id: str):
        self.monitor_id = monitor_id
        self.is_running = False
        self.metrics_history = []
        self.alerts_generated = 0
    
    def start_monitoring(self):
        """Start continuous system monitoring."""
        self.is_running = True
        logging.info(f"System Health Monitor {self.monitor_id} started")
        
        while self.is_running:
            try:
                # Simulate system metric collection
                metrics = self._collect_system_metrics()
                self.metrics_history.append(metrics)
                
                # Check for alert conditions
                alerts = self._check_alert_conditions(metrics)
                if alerts:
                    self.alerts_generated += len(alerts)
                    logging.warning(f"Generated {len(alerts)} alerts")
                
                # Keep only recent metrics
                if len(self.metrics_history) > 100:
                    self.metrics_history = self.metrics_history[-100:]
                
                time.sleep(1)  # Monitor every second
                
            except Exception as e:
                logging.error(f"Monitoring error: {str(e)}")
                time.sleep(5)
    
    def stop_monitoring(self):
        """Stop monitoring process."""
        self.is_running = False
        logging.info(f"System Health Monitor {self.monitor_id} stopped")
    
    def _collect_system_metrics(self) -> Dict:
        """Collect comprehensive system metrics."""
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu_usage': random.uniform(10, 95),
            'memory_usage': random.uniform(20, 85),
            'disk_io': random.uniform(0, 100),
            'network_latency': random.uniform(10, 200),
            'active_connections': random.randint(50, 500),
            'error_rate': random.uniform(0, 0.1),
            'response_time': random.uniform(50, 1000)
        }
    
    def _check_alert_conditions(self, metrics: Dict) -> List[Dict]:
        """Check for alert conditions in metrics."""
        alerts = []
        
        if metrics['cpu_usage'] > 80:
            alerts.append({
                'type': 'cpu_high',
                'severity': 'critical' if metrics['cpu_usage'] > 90 else 'warning',
                'value': metrics['cpu_usage'],
                'threshold': 80
            })
        
        if metrics['memory_usage'] > 75:
            alerts.append({
                'type': 'memory_high',
                'severity': 'critical' if metrics['memory_usage'] > 85 else 'warning',
                'value': metrics['memory_usage'],
                'threshold': 75
            })
        
        if metrics['response_time'] > 500:
            alerts.append({
                'type': 'slow_response',
                'severity': 'warning',
                'value': metrics['response_time'],
                'threshold': 500
            })
        
        return alerts


class DataProcessingAgent:
    """Processes data in real-time with complex transformations."""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.processed_count = 0
        self.processing_queue = asyncio.Queue(maxsize=1000)
        self.is_processing = False
    
    async def start_processing(self):
        """Start continuous data processing."""
        self.is_processing = True
        logging.info(f"Data Processing Agent {self.agent_id} started")
        
        while self.is_processing:
            try:
                # Wait for data with timeout
                data_item = await asyncio.wait_for(
                    self.processing_queue.get(), 
                    timeout=1.0
                )
                
                # Process the data item
                processed_item = await self._process_data_item(data_item)
                self.processed_count += 1
                
                # Simulate processing completion notification
                self.processing_queue.task_done()
                
            except asyncio.TimeoutError:
                # No data available, continue monitoring
                pass
            except Exception as e:
                logging.error(f"Processing error in {self.agent_id}: {str(e)}")
                await asyncio.sleep(1)
    
    async def add_to_queue(self, data_item: Dict):
        """Add data item to processing queue."""
        try:
            await asyncio.wait_for(
                self.processing_queue.put(data_item), 
                timeout=0.1
            )
        except asyncio.TimeoutError:
            logging.warning(f"Queue full for agent {self.agent_id}")
    
    def stop_processing(self):
        """Stop processing operations."""
        self.is_processing = False
        logging.info(f"Data Processing Agent {self.agent_id} stopped")
    
    async def _process_data_item(self, item: Dict) -> Dict:
        """Process individual data item with complex transformations."""
        # Simulate complex processing time
        await asyncio.sleep(random.uniform(0.1, 0.5))
        
        processed_item = item.copy()
        processed_item.update({
            'processing_timestamp': datetime.now().isoformat(),
            'processor_id': self.agent_id,
            'processing_duration': random.uniform(0.1, 0.5),
            'data_quality_score': random.uniform(0.7, 1.0),
            'anomaly_score': random.uniform(0.0, 0.3)
        })
        
        # Simulate complex transformations
        if 'sales_amount' in processed_item:
            processed_item['normalized_amount'] = processed_item['sales_amount'] / 100
            processed_item['category_score'] = random.uniform(0.5, 1.0)
        
        return processed_item


class AlertManager:
    """Manages alerts and notifications across the system."""
    
    def __init__(self):
        self.active_alerts = []
        self.alert_history = []
        self.notification_queue = asyncio.Queue()
    
    async def process_alerts(self):
        """Process alerts and manage notifications."""
        logging.info("Alert Manager started")
        
        while True:
            try:
                alert = await asyncio.wait_for(
                    self.notification_queue.get(),
                    timeout=5.0
                )
                
                # Process the alert
                processed_alert = await self._process_alert(alert)
                self.active_alerts.append(processed_alert)
                self.alert_history.append(processed_alert)
                
                # Keep alert history manageable
                if len(self.alert_history) > 1000:
                    self.alert_history = self.alert_history[-1000:]
                
                logging.info(f"Processed alert: {alert.get('type', 'unknown')}")
                
            except asyncio.TimeoutError:
                # Clean up old alerts
                await self._cleanup_old_alerts()
            except Exception as e:
                logging.error(f"Alert processing error: {str(e)}")
    
    async def add_alert(self, alert: Dict):
        """Add new alert to processing queue."""
        alert['created_timestamp'] = datetime.now().isoformat()
        await self.notification_queue.put(alert)
    
    async def _process_alert(self, alert: Dict) -> Dict:
        """Process and enrich alert information."""
        processed_alert = alert.copy()
        processed_alert.update({
            'alert_id': f"ALERT-{random.randint(1000, 9999)}",
            'processed_timestamp': datetime.now().isoformat(),
            'escalation_level': self._determine_escalation_level(alert),
            'recommended_actions': self._generate_recommended_actions(alert)
        })
        
        return processed_alert
    
    def _determine_escalation_level(self, alert: Dict) -> str:
        """Determine appropriate escalation level."""
        severity = alert.get('severity', 'info')
        alert_type = alert.get('type', '')
        
        if severity == 'critical':
            return 'immediate'
        elif severity == 'warning' and 'high' in alert_type:
            return 'urgent'
        else:
            return 'normal'
    
    def _generate_recommended_actions(self, alert: Dict) -> List[str]:
        """Generate recommended actions for alert."""
        actions = []
        alert_type = alert.get('type', '')
        
        if 'cpu_high' in alert_type:
            actions.extend([
                "Check for resource-intensive processes",
                "Consider scaling up compute resources",
                "Review recent deployment changes"
            ])
        elif 'memory_high' in alert_type:
            actions.extend([
                "Investigate memory leaks",
                "Clear cache if appropriate",
                "Monitor garbage collection"
            ])
        elif 'slow_response' in alert_type:
            actions.extend([
                "Check database performance",
                "Review network connectivity",
                "Analyze application logs"
            ])
        
        return actions
    
    async def _cleanup_old_alerts(self):
        """Clean up old resolved alerts."""
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(minutes=30)
        
        # Keep only recent active alerts
        self.active_alerts = [
            alert for alert in self.active_alerts
            if datetime.fromisoformat(alert.get('created_timestamp', current_time.isoformat())) > cutoff_time
        ]


class RealTimeOrchestrator:
    """Orchestrates all real-time monitoring and processing components."""
    
    def __init__(self):
        self.components = {}
        self.is_running = False
        self.metrics_summary = {}
    
    async def initialize_system(self):
        """Initialize all system components."""
        logging.info("Initializing Real-Time Monitoring System...")
        
        # Initialize components
        self.components['alert_manager'] = AlertManager()
        self.components['processing_agents'] = [
            DataProcessingAgent(f'PROC-{i:03d}') for i in range(3)
        ]
        self.components['health_monitors'] = [
            SystemHealthMonitor(f'HEALTH-{i:03d}') for i in range(2)
        ]
        
        logging.info("All components initialized successfully")
    
    async def start_system(self, duration_seconds: int = 30):
        """Start the complete real-time system."""
        self.is_running = True
        start_time = time.time()
        
        logging.info(f"Starting real-time system for {duration_seconds} seconds...")
        
        # Start all async components
        tasks = []
        
        # Start alert manager
        tasks.append(asyncio.create_task(self.components['alert_manager'].process_alerts()))
        
        # Start data processing agents
        for agent in self.components['processing_agents']:
            tasks.append(asyncio.create_task(agent.start_processing()))
        
        # Start health monitors in separate threads
        monitor_threads = []
        for monitor in self.components['health_monitors']:
            thread = threading.Thread(target=monitor.start_monitoring)
            thread.daemon = True
            thread.start()
            monitor_threads.append(thread)
        
        # Start data generation and feeding
        tasks.append(asyncio.create_task(self._generate_test_data()))
        
        # Run system for specified duration
        try:
            await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=duration_seconds
            )
        except asyncio.TimeoutError:
            logging.info("System runtime completed")
        
        # Stop all components
        await self._stop_all_components()
        
        # Calculate final metrics
        total_time = time.time() - start_time
        self.metrics_summary = self._calculate_final_metrics(total_time)
        
        logging.info(f"Real-time system completed after {total_time:.2f} seconds")
    
    async def _generate_test_data(self):
        """Generate continuous test data for processing."""
        data_counter = 0
        
        while self.is_running:
            try:
                # Generate test data item
                test_data = {
                    'data_id': f'DATA-{data_counter:06d}',
                    'timestamp': datetime.now().isoformat(),
                    'sales_amount': random.uniform(10, 500),
                    'category': random.choice(['Electronics', 'Accessories', 'Software']),
                    'region': random.choice(['North America', 'Europe', 'Asia Pacific'])
                }
                
                # Distribute data to processing agents
                agent = random.choice(self.components['processing_agents'])
                await agent.add_to_queue(test_data)
                
                data_counter += 1
                
                # Generate occasional alerts
                if random.random() < 0.1:  # 10% chance of alert
                    alert = {
                        'type': random.choice(['cpu_high', 'memory_high', 'slow_response']),
                        'severity': random.choice(['warning', 'critical']),
                        'source': 'test_data_generator',
                        'value': random.uniform(80, 95)
                    }
                    await self.components['alert_manager'].add_alert(alert)
                
                await asyncio.sleep(random.uniform(0.1, 0.3))
                
            except Exception as e:
                logging.error(f"Data generation error: {str(e)}")
                await asyncio.sleep(1)
    
    async def _stop_all_components(self):
        """Stop all system components gracefully."""
        self.is_running = False
        
        # Stop processing agents
        for agent in self.components['processing_agents']:
            agent.stop_processing()
        
        # Stop health monitors
        for monitor in self.components['health_monitors']:
            monitor.stop_monitoring()
        
        logging.info("All components stopped gracefully")
    
    def _calculate_final_metrics(self, total_time: float) -> Dict:
        """Calculate comprehensive final metrics."""
        total_processed = sum(
            agent.processed_count for agent in self.components['processing_agents']
        )
        total_alerts = sum(
            monitor.alerts_generated for monitor in self.components['health_monitors']
        )
        
        return {
            'execution_summary': {
                'total_runtime': total_time,
                'components_active': len(self.components),
                'processing_agents': len(self.components['processing_agents']),
                'health_monitors': len(self.components['health_monitors'])
            },
            'processing_metrics': {
                'total_items_processed': total_processed,
                'processing_rate': total_processed / total_time if total_time > 0 else 0,
                'average_per_agent': total_processed / len(self.components['processing_agents'])
            },
            'alert_metrics': {
                'total_alerts_generated': total_alerts,
                'alert_rate': total_alerts / total_time if total_time > 0 else 0,
                'active_alerts': len(self.components['alert_manager'].active_alerts)
            },
            'system_health': {
                'uptime': total_time,
                'error_rate': random.uniform(0, 0.05),
                'overall_performance': 'excellent' if total_processed > 50 else 'good'
            }
        }


async def main():
    """Main execution pipeline."""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('/Users/shaansisodia/DEV/realtime_monitoring.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize orchestrator
        orchestrator = RealTimeOrchestrator()
        await orchestrator.initialize_system()
        
        # Run the system
        await orchestrator.start_system(duration_seconds=20)  # Run for 20 seconds
        
        # Save results
        results = {
            'system_metrics': orchestrator.metrics_summary,
            'execution_timestamp': datetime.now().isoformat(),
            'system_configuration': {
                'processing_agents': len(orchestrator.components['processing_agents']),
                'health_monitors': len(orchestrator.components['health_monitors']),
                'runtime_duration': 20
            }
        }
        
        output_file = '/Users/shaansisodia/DEV/realtime_monitoring_results.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Display summary
        print("\n" + "="*70)
        print("REAL-TIME MONITORING SYSTEM SUMMARY")
        print("="*70)
        metrics = orchestrator.metrics_summary
        print(f"Runtime: {metrics['execution_summary']['total_runtime']:.2f}s")
        print(f"Items Processed: {metrics['processing_metrics']['total_items_processed']}")
        print(f"Processing Rate: {metrics['processing_metrics']['processing_rate']:.2f} items/sec")
        print(f"Alerts Generated: {metrics['alert_metrics']['total_alerts_generated']}")
        print(f"System Performance: {metrics['system_health']['overall_performance'].title()}")
        print(f"Active Components: {metrics['execution_summary']['components_active']}")
        print("="*70)
        
        logger.info(f"Results saved to: {output_file}")
        return True
        
    except Exception as e:
        logger.error(f"Real-time monitoring system failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)