#!/usr/bin/env python3
"""
PERFORMANCE MONITORING ORCHESTRATOR
Central coordinator for advanced real-time monitoring and adaptive scaling
"""

import asyncio
import time
import json
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, asdict, field
from collections import defaultdict, deque
import threading
import logging
import statistics
from pathlib import Path

# Import our monitoring components
from advanced_performance_monitoring_system import (
    MetricType, AlertSeverity, SystemStatus, MetricPoint, Alert,
    PerformanceTrend, SystemHealthSnapshot, TimeSeriesBuffer,
    AnomalyDetector, TrendAnalyzer, NotificationManager
)
from adaptive_scaling_engine import (
    ScalingAction, ScalingTrigger, ScalingRule, ScalingEvent,
    AgentPool, AgentPoolState, LoadBalancerConfig, QueueManager,
    CircuitBreaker, IntelligentLoadBalancer
)

class MonitoringConfiguration:
    """Central configuration for monitoring system"""
    
    def __init__(self):
        # Monitoring intervals
        self.metric_collection_interval_ms = 100  # Sub-second collection
        self.health_check_interval_seconds = 30
        self.trend_analysis_interval_minutes = 5
        self.anomaly_detection_interval_minutes = 1
        self.scaling_evaluation_interval_seconds = 60
        
        # Data retention
        self.metrics_retention_hours = 72  # 3 days detailed
        self.aggregated_retention_days = 90  # 90 days aggregated
        self.alert_retention_days = 30
        
        # Thresholds
        self.quality_threshold_warning = 0.7
        self.quality_threshold_critical = 0.5
        self.latency_threshold_warning_ms = 5000
        self.latency_threshold_critical_ms = 10000
        self.error_rate_threshold_warning = 0.05  # 5%
        self.error_rate_threshold_critical = 0.15  # 15%
        
        # Scaling parameters
        self.scaling_cooldown_minutes = 5
        self.max_agents_per_pool = 20
        self.min_agents_per_pool = 1
        
        # Cost management
        self.daily_budget_usd = 10.0
        self.cost_alert_threshold_usd = 8.0
        self.cost_emergency_threshold_usd = 9.5

@dataclass
class MonitoringIntegration:
    """Integration points with existing systems"""
    enhanced_real_agent_system: Any = None
    hierarchical_orchestration_system: Any = None
    ml_predictive_routing_system: Any = None
    quality_validation_system: Any = None
    autonomous_learning_system: Any = None
    quantum_optimization_engine: Any = None

class PerformanceMonitoringOrchestrator:
    """Revolutionary performance monitoring and adaptive scaling orchestrator"""
    
    def __init__(self, config: MonitoringConfiguration = None):
        self.config = config or MonitoringConfiguration()
        
        # Core components
        self.time_series_buffers = {}
        self.anomaly_detector = AnomalyDetector()
        self.trend_analyzer = TrendAnalyzer()
        self.notification_manager = NotificationManager()
        self.load_balancer = None
        
        # Agent pools and scaling
        self.agent_pools = {}
        self.scaling_rules = []
        self.scaling_history = deque(maxlen=1000)
        
        # System state
        self.system_status = SystemStatus.HEALTHY
        self.active_alerts = {}
        self.performance_baselines = {}
        self.monitoring_tasks = []
        
        # Integration with existing systems
        self.integrations = MonitoringIntegration()
        
        # Performance tracking
        self.total_metrics_collected = 0
        self.total_alerts_generated = 0
        self.total_scaling_actions = 0
        self.uptime_start = datetime.now()
        
        # Thread-safe locks
        self.metrics_lock = threading.RLock()
        self.alerts_lock = threading.RLock()
        self.scaling_lock = threading.RLock()
        
        self._initialize_components()
        
        print("🎯 PERFORMANCE MONITORING ORCHESTRATOR INITIALIZED")
        print(f"   📊 Metric collection interval: {self.config.metric_collection_interval_ms}ms")
        print(f"   🔍 Health check interval: {self.config.health_check_interval_seconds}s")
        print(f"   📈 Trend analysis interval: {self.config.trend_analysis_interval_minutes}m")
        print(f"   🚨 Anomaly detection interval: {self.config.anomaly_detection_interval_minutes}m")
        print(f"   ⚖️  Scaling evaluation interval: {self.config.scaling_evaluation_interval_seconds}s")
        print()
    
    def _initialize_components(self):
        """Initialize monitoring components"""
        
        # Initialize time series buffers for each metric type
        for metric_type in MetricType:
            self.time_series_buffers[metric_type] = TimeSeriesBuffer(
                max_size=50000,  # ~14 hours at 100ms intervals
                retention_hours=self.config.metrics_retention_hours
            )
        
        # Initialize load balancer
        lb_config = LoadBalancerConfig(
            algorithm="quality_weighted",
            health_check_interval=self.config.health_check_interval_seconds,
            circuit_breaker_enabled=True
        )
        self.load_balancer = IntelligentLoadBalancer(lb_config)
        
        # Initialize default scaling rules
        self._create_default_scaling_rules()
        
        # Initialize agent pools for existing systems
        self._initialize_agent_pools()
    
    def _create_default_scaling_rules(self):
        """Create intelligent default scaling rules"""
        
        self.scaling_rules = [
            # Quality-based scaling
            ScalingRule(
                name="quality_degradation_scale_up",
                trigger=ScalingTrigger.QUALITY_DEGRADATION,
                condition="quality_score < 0.7 AND trend_direction == 'decreasing'",
                action=ScalingAction.SCALE_UP,
                cooldown_minutes=3,
                max_instances=15,
                priority=9
            ),
            
            # Latency-based scaling
            ScalingRule(
                name="high_latency_scale_up",
                trigger=ScalingTrigger.LATENCY_THRESHOLD,
                condition="avg_latency > 5000 AND p95_latency > 8000",
                action=ScalingAction.SCALE_UP,
                cooldown_minutes=2,
                max_instances=12,
                priority=8
            ),
            
            # Error rate scaling
            ScalingRule(
                name="high_error_rate_scale_up",
                trigger=ScalingTrigger.ERROR_RATE,
                condition="error_rate > 0.1 AND trend_direction == 'increasing'",
                action=ScalingAction.SCALE_UP,
                cooldown_minutes=1,
                max_instances=10,
                priority=10  # Highest priority
            ),
            
            # Queue length scaling
            ScalingRule(
                name="queue_overflow_scale_up",
                trigger=ScalingTrigger.QUEUE_LENGTH,
                condition="queue_length > 100 AND wait_time > 30",
                action=ScalingAction.SCALE_UP,
                cooldown_minutes=2,
                max_instances=8,
                priority=7
            ),
            
            # Cost optimization scaling down
            ScalingRule(
                name="low_utilization_scale_down",
                trigger=ScalingTrigger.COST_OPTIMIZATION,
                condition="avg_load < 0.3 AND quality_score > 0.8",
                action=ScalingAction.SCALE_DOWN,
                cooldown_minutes=10,
                min_instances=2,
                priority=3
            ),
            
            # Predictive scaling
            ScalingRule(
                name="predictive_scale_up",
                trigger=ScalingTrigger.PREDICTIVE,
                condition="forecast_load > 0.8 AND confidence > 0.7",
                action=ScalingAction.SCALE_UP,
                cooldown_minutes=5,
                max_instances=15,
                priority=6
            ),
            
            # Circuit breaker trigger
            ScalingRule(
                name="circuit_breaker_failover",
                trigger=ScalingTrigger.ERROR_RATE,
                condition="circuit_breaker_open_count > 2",
                action=ScalingAction.FAILOVER,
                cooldown_minutes=1,
                priority=10
            )
        ]
    
    def _initialize_agent_pools(self):
        """Initialize agent pools for existing systems"""
        
        # Define agent pools based on existing architecture
        agent_pool_configs = [
            {
                'agent_type': 'cerebras_ultra',
                'initial_instances': 2,
                'max_instances': 8,
                'min_instances': 1,
                'cost_per_instance': 0.001,
                'specialization': 'architecture'
            },
            {
                'agent_type': 'gemini_flash',
                'initial_instances': 2,
                'max_instances': 6,
                'min_instances': 1,
                'cost_per_instance': 0.0008,
                'specialization': 'reasoning'
            },
            {
                'agent_type': 'groq_lightning',
                'initial_instances': 2,
                'max_instances': 10,
                'min_instances': 1,
                'cost_per_instance': 0.0005,
                'specialization': 'documentation'
            },
            {
                'agent_type': 'scaleway_eu',
                'initial_instances': 1,
                'max_instances': 4,
                'min_instances': 1,
                'cost_per_instance': 0.0012,
                'specialization': 'security'
            }
        ]
        
        for pool_config in agent_pool_configs:
            agent_pool = AgentPool(
                agent_type=pool_config['agent_type'],
                current_instances=pool_config['initial_instances'],
                target_instances=pool_config['initial_instances'],
                max_instances=pool_config['max_instances'],
                min_instances=pool_config['min_instances'],
                state=AgentPoolState.HEALTHY,
                last_scaled=datetime.now(),
                scaling_cooldown=self.config.scaling_cooldown_minutes,
                cost_per_instance=pool_config['cost_per_instance']
            )
            
            self.agent_pools[pool_config['agent_type']] = agent_pool
            
            # Register with load balancer
            self.load_balancer.register_agent(
                pool_config['agent_type'],
                {'weight': 1.0, 'specialization': pool_config['specialization']}
            )
    
    async def start_monitoring(self):
        """Start the comprehensive monitoring system"""
        
        print("🚀 STARTING ADVANCED PERFORMANCE MONITORING SYSTEM")
        print("=" * 80)
        print()
        
        # Start load balancer
        await self.load_balancer.start()
        
        # Start monitoring tasks
        monitoring_tasks = [
            self._metric_collection_loop(),
            self._health_monitoring_loop(),
            self._anomaly_detection_loop(),
            self._trend_analysis_loop(),
            self._scaling_evaluation_loop(),
            self._cost_monitoring_loop(),
            self._quality_monitoring_loop(),
            self._predictive_maintenance_loop()
        ]
        
        self.monitoring_tasks = [asyncio.create_task(task) for task in monitoring_tasks]
        
        print("✅ ALL MONITORING SYSTEMS STARTED")
        print(f"   📊 {len(self.monitoring_tasks)} monitoring loops active")
        print(f"   🤖 {len(self.agent_pools)} agent pools initialized")
        print(f"   📋 {len(self.scaling_rules)} scaling rules configured")
        print()
        
        # Wait for all monitoring tasks
        try:
            await asyncio.gather(*self.monitoring_tasks)
        except asyncio.CancelledError:
            print("🛑 Monitoring system shutdown requested")
            await self.stop_monitoring()
    
    async def stop_monitoring(self):
        """Stop the monitoring system gracefully"""
        
        print("🛑 STOPPING PERFORMANCE MONITORING SYSTEM")
        
        # Cancel monitoring tasks
        for task in self.monitoring_tasks:
            if not task.done():
                task.cancel()
        
        # Wait for tasks to complete
        await asyncio.gather(*self.monitoring_tasks, return_exceptions=True)
        
        # Stop load balancer
        await self.load_balancer.stop()
        
        # Save final state
        await self._save_monitoring_state()
        
        print("✅ MONITORING SYSTEM STOPPED GRACEFULLY")
    
    async def _metric_collection_loop(self):
        """High-frequency metric collection loop"""
        
        print("📊 Starting metric collection loop...")
        
        while True:
            try:
                start_time = time.time()
                
                # Collect metrics from all integrated systems
                await self._collect_system_metrics()
                
                # Update performance baselines
                self._update_performance_baselines()
                
                collection_time = (time.time() - start_time) * 1000  # ms
                
                # Sleep for remaining interval time
                sleep_time = max(0, (self.config.metric_collection_interval_ms - collection_time) / 1000)
                await asyncio.sleep(sleep_time)
                
                self.total_metrics_collected += 1
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(f"Metric collection error: {e}")
                await asyncio.sleep(1)  # Brief pause before retry
    
    async def _collect_system_metrics(self):
        """Collect metrics from all integrated systems"""
        
        current_time = datetime.now()
        
        # Simulate metric collection (in production, integrate with actual systems)
        metrics_to_collect = [
            # System performance metrics
            MetricPoint(current_time, np.random.uniform(0.7, 0.95), MetricType.QUALITY_SCORE, "system", {"component": "overall"}),
            MetricPoint(current_time, np.random.uniform(1000, 8000), MetricType.LATENCY, "system", {"component": "orchestration"}),
            MetricPoint(current_time, np.random.uniform(0.01, 0.1), MetricType.ERROR_RATE, "system", {"component": "agents"}),
            MetricPoint(current_time, np.random.uniform(0.3, 0.9), MetricType.SUCCESS_RATE, "system", {"component": "orchestration"}),
            
            # Agent-specific metrics
            MetricPoint(current_time, np.random.uniform(0.2, 0.8), MetricType.AGENT_LOAD, "cerebras_ultra", {"pool": "cerebras"}),
            MetricPoint(current_time, np.random.uniform(0.1, 0.7), MetricType.AGENT_LOAD, "gemini_flash", {"pool": "gemini"}),
            MetricPoint(current_time, np.random.uniform(0.15, 0.85), MetricType.AGENT_LOAD, "groq_lightning", {"pool": "groq"}),
            MetricPoint(current_time, np.random.uniform(0.1, 0.6), MetricType.AGENT_LOAD, "scaleway_eu", {"pool": "scaleway"}),
            
            # Cost metrics
            MetricPoint(current_time, np.random.uniform(0.001, 0.005), MetricType.COST_EFFICIENCY, "system", {"component": "overall"}),
            
            # System health
            MetricPoint(current_time, np.random.uniform(0.8, 1.0), MetricType.SYSTEM_HEALTH, "system", {"component": "infrastructure"}),
        ]
        
        # Add metrics to time series buffers
        with self.metrics_lock:
            for metric in metrics_to_collect:
                if metric.metric_type in self.time_series_buffers:
                    self.time_series_buffers[metric.metric_type].add_point(metric)
    
    def _update_performance_baselines(self):
        """Update performance baselines for anomaly detection"""
        
        # Update baselines every 1000 metric collections
        if self.total_metrics_collected % 1000 == 0:
            for metric_type, buffer in self.time_series_buffers.items():
                recent_data = buffer.get_recent(minutes=60)  # Last hour
                if len(recent_data) >= 10:
                    values = [point.value for point in recent_data]
                    self.anomaly_detector.update_baseline(metric_type, values)
    
    async def _health_monitoring_loop(self):
        """System health monitoring loop"""
        
        print("🏥 Starting health monitoring loop...")
        
        while True:
            try:
                await self._perform_health_checks()
                await self._update_system_status()
                await asyncio.sleep(self.config.health_check_interval_seconds)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(f"Health monitoring error: {e}")
                await asyncio.sleep(5)
    
    async def _perform_health_checks(self):
        """Perform comprehensive health checks"""
        
        health_results = {}
        
        # Check agent pools
        for agent_type, pool in self.agent_pools.items():
            pool_health = await self._check_agent_pool_health(pool)
            health_results[f"agent_pool_{agent_type}"] = pool_health
        
        # Check system components
        system_health = await self._check_system_component_health()
        health_results["system_components"] = system_health
        
        # Generate alerts for unhealthy components
        for component, health in health_results.items():
            if not health.get("healthy", True):
                await self._generate_health_alert(component, health)
    
    async def _check_agent_pool_health(self, pool: AgentPool) -> Dict[str, Any]:
        """Check health of an agent pool"""
        
        # Get recent metrics for this pool
        recent_metrics = {}
        for metric_type in [MetricType.AGENT_LOAD, MetricType.ERROR_RATE, MetricType.LATENCY]:
            if metric_type in self.time_series_buffers:
                recent_data = self.time_series_buffers[metric_type].get_recent(minutes=5)
                pool_data = [p for p in recent_data if p.source == pool.agent_type]
                if pool_data:
                    values = [p.value for p in pool_data]
                    recent_metrics[metric_type.value] = {
                        'current': values[-1] if values else 0,
                        'average': statistics.mean(values),
                        'max': max(values),
                        'trend': 'stable'  # Simplified
                    }
        
        # Determine health status
        is_healthy = True
        health_score = 1.0
        issues = []
        
        # Check load
        if MetricType.AGENT_LOAD.value in recent_metrics:
            load = recent_metrics[MetricType.AGENT_LOAD.value]['average']
            pool.average_load = load
            
            if load > 0.9:
                is_healthy = False
                health_score *= 0.5
                issues.append("High load detected")
            elif load > 0.8:
                health_score *= 0.8
                issues.append("Moderate load detected")
        
        # Check error rate
        if MetricType.ERROR_RATE.value in recent_metrics:
            error_rate = recent_metrics[MetricType.ERROR_RATE.value]['average']
            pool.error_rate = error_rate
            
            if error_rate > 0.15:
                is_healthy = False
                health_score *= 0.3
                issues.append("High error rate")
            elif error_rate > 0.05:
                health_score *= 0.7
                issues.append("Moderate error rate")
        
        # Update pool state
        if not is_healthy:
            if pool.state == AgentPoolState.HEALTHY:
                pool.state = AgentPoolState.DEGRADED
        else:
            if pool.state == AgentPoolState.DEGRADED:
                pool.state = AgentPoolState.HEALTHY
        
        return {
            'healthy': is_healthy,
            'health_score': health_score,
            'issues': issues,
            'metrics': recent_metrics,
            'pool_state': pool.state.value
        }
    
    async def _check_system_component_health(self) -> Dict[str, Any]:
        """Check health of system components"""
        
        # Check overall system metrics
        system_health = {
            'healthy': True,
            'components': {}
        }
        
        # Check quality score
        quality_buffer = self.time_series_buffers.get(MetricType.QUALITY_SCORE)
        if quality_buffer:
            recent_quality = quality_buffer.get_recent(minutes=5)
            if recent_quality:
                avg_quality = statistics.mean([p.value for p in recent_quality])
                system_health['components']['quality'] = {
                    'healthy': avg_quality >= self.config.quality_threshold_warning,
                    'score': avg_quality,
                    'status': 'healthy' if avg_quality >= self.config.quality_threshold_warning else 'degraded'
                }
                
                if avg_quality < self.config.quality_threshold_critical:
                    system_health['healthy'] = False
        
        # Check latency
        latency_buffer = self.time_series_buffers.get(MetricType.LATENCY)
        if latency_buffer:
            recent_latency = latency_buffer.get_recent(minutes=5)
            if recent_latency:
                avg_latency = statistics.mean([p.value for p in recent_latency])
                system_health['components']['latency'] = {
                    'healthy': avg_latency <= self.config.latency_threshold_warning_ms,
                    'value': avg_latency,
                    'status': 'healthy' if avg_latency <= self.config.latency_threshold_warning_ms else 'degraded'
                }
                
                if avg_latency > self.config.latency_threshold_critical_ms:
                    system_health['healthy'] = False
        
        return system_health
    
    async def _generate_health_alert(self, component: str, health_info: Dict[str, Any]):
        """Generate alert for unhealthy component"""
        
        severity = AlertSeverity.WARNING
        if health_info.get('health_score', 1.0) < 0.5:
            severity = AlertSeverity.CRITICAL
        
        alert = Alert(
            id=f"health_{component}_{int(time.time())}",
            severity=severity,
            title=f"Health Issue Detected: {component}",
            description=f"Component {component} is unhealthy. Issues: {', '.join(health_info.get('issues', ['Unknown']))}",
            source=component,
            metric_type=MetricType.SYSTEM_HEALTH,
            timestamp=datetime.now(),
            value=health_info.get('health_score', 0.0),
            threshold=0.8,
            tags={'component': component, 'health_check': 'automated'}
        )
        
        await self._process_alert(alert)
    
    async def _anomaly_detection_loop(self):
        """ML-powered anomaly detection loop"""
        
        print("🔍 Starting anomaly detection loop...")
        
        while True:
            try:
                await self._detect_anomalies()
                await asyncio.sleep(self.config.anomaly_detection_interval_minutes * 60)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(f"Anomaly detection error: {e}")
                await asyncio.sleep(30)
    
    async def _detect_anomalies(self):
        """Detect anomalies across all metrics"""
        
        anomalies_detected = []
        
        for metric_type, buffer in self.time_series_buffers.items():
            recent_data = buffer.get_recent(minutes=10)
            if len(recent_data) >= 5:
                # Get values for analysis
                values = [p.value for p in recent_data]
                current_value = values[-1]
                
                # Detect anomalies
                anomaly_result = self.anomaly_detector.detect_anomalies(
                    metric_type, values[:-1], current_value
                )
                
                if anomaly_result['is_anomaly']:
                    anomalies_detected.append({
                        'metric_type': metric_type,
                        'current_value': current_value,
                        'confidence': anomaly_result['confidence'],
                        'method': anomaly_result['method'],
                        'details': anomaly_result['details']
                    })
        
        # Generate anomaly alerts
        for anomaly in anomalies_detected:
            await self._generate_anomaly_alert(anomaly)
    
    async def _generate_anomaly_alert(self, anomaly: Dict[str, Any]):
        """Generate alert for detected anomaly"""
        
        confidence = anomaly['confidence']
        severity = AlertSeverity.INFO
        
        if confidence > 0.9:
            severity = AlertSeverity.CRITICAL
        elif confidence > 0.7:
            severity = AlertSeverity.WARNING
        
        alert = Alert(
            id=f"anomaly_{anomaly['metric_type'].value}_{int(time.time())}",
            severity=severity,
            title=f"Anomaly Detected: {anomaly['metric_type'].value}",
            description=f"Anomalous behavior detected in {anomaly['metric_type'].value}. Current value: {anomaly['current_value']:.3f}. Detection method: {anomaly['method']}",
            source="anomaly_detector",
            metric_type=anomaly['metric_type'],
            timestamp=datetime.now(),
            value=anomaly['current_value'],
            threshold=0.0,  # Anomaly detection doesn't use fixed thresholds
            tags={'anomaly_confidence': str(confidence), 'detection_method': anomaly['method']}
        )
        
        await self._process_alert(alert)

# Continue with remaining monitoring loops and system integration...