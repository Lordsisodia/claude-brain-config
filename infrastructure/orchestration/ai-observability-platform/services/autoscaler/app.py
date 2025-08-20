import asyncio
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
from prometheus_api_client import PrometheusConnect
from fastapi.responses import Response
import uvicorn
import redis
import requests
import docker
from kubernetes import client, config
from collections import defaultdict, deque
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="AI Autoscaler Service", version="1.0.0")

# External connections
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)
docker_client = docker.from_env()

# Prometheus connection
prometheus_url = "http://prometheus:9090"
prom = PrometheusConnect(url=prometheus_url, disable_ssl=True)

# Kubernetes client (if running in Kubernetes)
try:
    config.load_incluster_config()
    k8s_v1 = client.CoreV1Api()
    k8s_apps_v1 = client.AppsV1Api()
    k8s_available = True
except:
    k8s_available = False
    logger.warning("Kubernetes client not available, using Docker fallback")

# Prometheus metrics
scaling_actions = Counter('scaling_actions_total', 'Total scaling actions', ['action_type', 'resource_type'])
resource_utilization = Gauge('resource_utilization', 'Resource utilization', ['resource_type', 'agent_group'])
scaling_decisions = Gauge('scaling_decisions', 'Scaling decisions made', ['decision_type'])
prediction_accuracy = Gauge('prediction_accuracy', 'Scaling prediction accuracy', ['predictor_type'])
healing_actions = Counter('healing_actions_total', 'Self-healing actions', ['action_type', 'target'])
system_efficiency = Gauge('system_efficiency', 'Overall system efficiency', ['efficiency_type'])

# Data models
class ScalingDecision(BaseModel):
    decision_id: str
    action_type: str  # scale_up, scale_down, heal, optimize
    target_resource: str
    current_instances: int
    target_instances: int
    reason: str
    confidence: float
    timestamp: datetime
    metadata: Dict[str, Any]

class ResourceMetrics(BaseModel):
    resource_type: str
    current_usage: float
    target_usage: float
    capacity: float
    instances: int
    health_score: float

class PredictionModel(BaseModel):
    model_type: str
    accuracy: float
    last_training: datetime
    features: List[str]
    predictions: List[float]

class AutoScaler:
    def __init__(self):
        self.scaling_policies = {
            'cpu_threshold_up': 70.0,
            'cpu_threshold_down': 30.0,
            'memory_threshold_up': 80.0,
            'memory_threshold_down': 40.0,
            'response_time_threshold': 5.0,
            'error_rate_threshold': 0.05,
            'queue_length_threshold': 100,
            'min_instances': 1,
            'max_instances': 1000,
            'scale_up_factor': 1.5,
            'scale_down_factor': 0.7,
            'cooldown_period': 300,  # 5 minutes
        }
        
        self.resource_groups = {
            'ai-agents': {
                'metrics': ['cpu_usage', 'memory_usage', 'response_time', 'queue_length'],
                'scaling_targets': ['agent-deployment', 'model-inference-service'],
                'priority': 'high'
            },
            'monitoring': {
                'metrics': ['cpu_usage', 'memory_usage', 'disk_usage'],
                'scaling_targets': ['prometheus', 'grafana', 'elasticsearch'],
                'priority': 'medium'
            },
            'infrastructure': {
                'metrics': ['network_bandwidth', 'storage_iops'],
                'scaling_targets': ['redis', 'database'],
                'priority': 'low'
            }
        }
        
        self.last_scaling_actions = {}
        self.prediction_models = {}
        self.performance_history = defaultdict(deque)
        self.initialize_prediction_models()

    def initialize_prediction_models(self):
        """Initialize machine learning models for prediction"""
        self.prediction_models = {
            'load_predictor': {
                'type': 'moving_average',
                'window_size': 10,
                'accuracy': 0.0,
                'last_training': datetime.now(),
                'data': deque(maxlen=100)
            },
            'anomaly_predictor': {
                'type': 'statistical',
                'threshold_multiplier': 2.0,
                'accuracy': 0.0,
                'last_training': datetime.now(),
                'baseline': {}
            },
            'capacity_predictor': {
                'type': 'trend_analysis',
                'forecast_horizon': 3600,  # 1 hour
                'accuracy': 0.0,
                'last_training': datetime.now(),
                'trends': {}
            }
        }

    async def analyze_and_scale(self) -> List[ScalingDecision]:
        """Main autoscaling logic"""
        decisions = []
        
        try:
            # Get current metrics from Prometheus
            current_metrics = await self._get_current_metrics()
            
            # Analyze each resource group
            for group_name, group_config in self.resource_groups.items():
                group_decisions = await self._analyze_resource_group(group_name, group_config, current_metrics)
                decisions.extend(group_decisions)
            
            # Execute scaling decisions
            for decision in decisions:
                await self._execute_scaling_decision(decision)
                
                # Update metrics
                scaling_actions.labels(
                    action_type=decision.action_type,
                    resource_type=decision.target_resource
                ).inc()
            
            # Update prediction models
            await self._update_prediction_models(current_metrics)
            
            # Store decisions for analysis
            await self._store_scaling_decisions(decisions)
            
            return decisions
            
        except Exception as e:
            logger.error(f"Error in autoscaling analysis: {e}")
            return []

    async def _get_current_metrics(self) -> Dict[str, Any]:
        """Get current metrics from Prometheus"""
        metrics = {}
        
        try:
            # Query Prometheus for key metrics
            queries = {
                'cpu_usage': 'avg(rate(cpu_usage_percent[5m])) by (agent_id)',
                'memory_usage': 'avg(ai_agent_memory_usage_bytes) by (agent_id)',
                'response_time': 'avg(ai_agent_response_time_seconds) by (agent_id)',
                'error_rate': 'rate(ai_agent_requests_total{status!="200"}[5m]) / rate(ai_agent_requests_total[5m])',
                'queue_length': 'avg(ai_agent_queue_length) by (agent_id)',
                'health_score': 'avg(ai_agent_health_score) by (agent_id)',
                'request_rate': 'rate(ai_agent_requests_total[5m])',
                'inference_latency': 'avg(ai_agent_inference_latency_seconds) by (agent_id)',
            }
            
            for metric_name, query in queries.items():
                try:
                    result = prom.custom_query(query)
                    metrics[metric_name] = self._parse_prometheus_result(result)
                except Exception as e:
                    logger.warning(f"Failed to query {metric_name}: {e}")
                    metrics[metric_name] = []
            
            # Add system-level metrics
            system_queries = {
                'total_agents': 'count(ai_agent_health_score)',
                'active_agents': 'count(ai_agent_health_score > 0.5)',
                'average_health': 'avg(ai_agent_health_score)',
                'emergence_events': 'increase(emergence_events_total[1h])',
                'anomalies': 'increase(anomalies_detected_total[1h])',
            }
            
            for metric_name, query in system_queries.items():
                try:
                    result = prom.custom_query(query)
                    metrics[metric_name] = self._parse_prometheus_scalar_result(result)
                except Exception as e:
                    logger.warning(f"Failed to query {metric_name}: {e}")
                    metrics[metric_name] = 0
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting metrics from Prometheus: {e}")
            return {}

    def _parse_prometheus_result(self, result: List[Dict]) -> List[Dict]:
        """Parse Prometheus query result"""
        parsed = []
        for item in result:
            metric = item.get('metric', {})
            value = float(item.get('value', [0, 0])[1])
            parsed.append({
                'labels': metric,
                'value': value,
                'timestamp': time.time()
            })
        return parsed

    def _parse_prometheus_scalar_result(self, result: List[Dict]) -> float:
        """Parse Prometheus scalar result"""
        if result and len(result) > 0:
            return float(result[0].get('value', [0, 0])[1])
        return 0.0

    async def _analyze_resource_group(self, group_name: str, group_config: Dict, current_metrics: Dict) -> List[ScalingDecision]:
        """Analyze a specific resource group for scaling needs"""
        decisions = []
        
        try:
            # Calculate aggregate metrics for the group
            group_metrics = await self._calculate_group_metrics(group_name, group_config, current_metrics)
            
            # Check scaling conditions
            scaling_needed = await self._check_scaling_conditions(group_name, group_metrics)
            
            if scaling_needed:
                # Generate scaling decisions
                for target in group_config['scaling_targets']:
                    decision = await self._generate_scaling_decision(group_name, target, group_metrics, scaling_needed)
                    if decision:
                        decisions.append(decision)
            
            # Check for self-healing needs
            healing_decisions = await self._check_self_healing_needs(group_name, group_metrics)
            decisions.extend(healing_decisions)
            
            # Update resource utilization metrics
            for metric_name, value in group_metrics.items():
                if isinstance(value, (int, float)):
                    resource_utilization.labels(
                        resource_type=metric_name,
                        agent_group=group_name
                    ).set(value)
            
            return decisions
            
        except Exception as e:
            logger.error(f"Error analyzing resource group {group_name}: {e}")
            return []

    async def _calculate_group_metrics(self, group_name: str, group_config: Dict, current_metrics: Dict) -> Dict[str, Any]:
        """Calculate aggregate metrics for a resource group"""
        group_metrics = {}
        
        try:
            # Aggregate metrics across agents in the group
            for metric_name in group_config['metrics']:
                metric_data = current_metrics.get(metric_name, [])
                
                if metric_data:
                    values = [item['value'] for item in metric_data]
                    group_metrics[f'{metric_name}_avg'] = np.mean(values)
                    group_metrics[f'{metric_name}_max'] = np.max(values)
                    group_metrics[f'{metric_name}_min'] = np.min(values)
                    group_metrics[f'{metric_name}_std'] = np.std(values)
                    group_metrics[f'{metric_name}_count'] = len(values)
                else:
                    group_metrics[f'{metric_name}_avg'] = 0.0
                    group_metrics[f'{metric_name}_max'] = 0.0
                    group_metrics[f'{metric_name}_min'] = 0.0
                    group_metrics[f'{metric_name}_std'] = 0.0
                    group_metrics[f'{metric_name}_count'] = 0
            
            # Add derived metrics
            group_metrics['total_instances'] = current_metrics.get('total_agents', 0)
            group_metrics['active_instances'] = current_metrics.get('active_agents', 0)
            group_metrics['health_ratio'] = group_metrics['active_instances'] / max(group_metrics['total_instances'], 1)
            
            # Calculate efficiency metrics
            if group_metrics.get('request_rate_avg', 0) > 0 and group_metrics.get('response_time_avg', 0) > 0:
                group_metrics['throughput_efficiency'] = group_metrics['request_rate_avg'] / group_metrics['response_time_avg']
            else:
                group_metrics['throughput_efficiency'] = 0.0
            
            # Calculate resource efficiency
            if group_metrics.get('cpu_usage_avg', 0) > 0:
                group_metrics['resource_efficiency'] = group_metrics.get('throughput_efficiency', 0) / group_metrics['cpu_usage_avg']
            else:
                group_metrics['resource_efficiency'] = 0.0
            
            return group_metrics
            
        except Exception as e:
            logger.error(f"Error calculating group metrics: {e}")
            return {}

    async def _check_scaling_conditions(self, group_name: str, group_metrics: Dict) -> Optional[str]:
        """Check if scaling is needed and return the type of scaling"""
        try:
            # Check CPU-based scaling
            cpu_avg = group_metrics.get('cpu_usage_avg', 0)
            if cpu_avg > self.scaling_policies['cpu_threshold_up']:
                return 'scale_up_cpu'
            elif cpu_avg < self.scaling_policies['cpu_threshold_down']:
                return 'scale_down_cpu'
            
            # Check memory-based scaling
            memory_avg = group_metrics.get('memory_usage_avg', 0)
            memory_threshold_bytes = self.scaling_policies['memory_threshold_up'] * 1024 * 1024 * 1024  # Convert to bytes
            if memory_avg > memory_threshold_bytes:
                return 'scale_up_memory'
            
            # Check response time-based scaling
            response_time_avg = group_metrics.get('response_time_avg', 0)
            if response_time_avg > self.scaling_policies['response_time_threshold']:
                return 'scale_up_latency'
            
            # Check error rate-based scaling
            error_rate_avg = group_metrics.get('error_rate_avg', 0)
            if error_rate_avg > self.scaling_policies['error_rate_threshold']:
                return 'scale_up_errors'
            
            # Check queue length-based scaling
            queue_length_avg = group_metrics.get('queue_length_avg', 0)
            if queue_length_avg > self.scaling_policies['queue_length_threshold']:
                return 'scale_up_queue'
            
            # Check cooldown period
            last_action_time = self.last_scaling_actions.get(group_name, 0)
            if time.time() - last_action_time < self.scaling_policies['cooldown_period']:
                return None
            
            # Predictive scaling based on trends
            predicted_load = await self._predict_future_load(group_name, group_metrics)
            if predicted_load > 1.2:  # 20% increase predicted
                return 'scale_up_predicted'
            elif predicted_load < 0.8:  # 20% decrease predicted
                return 'scale_down_predicted'
            
            return None
            
        except Exception as e:
            logger.error(f"Error checking scaling conditions: {e}")
            return None

    async def _predict_future_load(self, group_name: str, current_metrics: Dict) -> float:
        """Predict future load using machine learning"""
        try:
            # Get historical data
            history_key = f"metrics_history:{group_name}"
            historical_data = redis_client.lrange(history_key, 0, 99)  # Last 100 data points
            
            if len(historical_data) < 10:
                return 1.0  # No change predicted
            
            # Parse historical data
            historical_values = []
            for data_point in historical_data:
                parsed = json.loads(data_point)
                # Create a composite load score
                load_score = (
                    parsed.get('cpu_usage_avg', 0) * 0.3 +
                    parsed.get('memory_usage_avg', 0) / (1024**3) * 100 * 0.2 +  # Convert to percentage
                    parsed.get('response_time_avg', 0) * 10 * 0.2 +  # Scale response time
                    parsed.get('queue_length_avg', 0) / 100 * 0.2 +  # Scale queue length
                    (1 - parsed.get('health_ratio', 1)) * 100 * 0.1  # Inverse health as load indicator
                )
                historical_values.append(load_score)
            
            # Simple moving average prediction
            if len(historical_values) >= 5:
                recent_avg = np.mean(historical_values[-5:])
                older_avg = np.mean(historical_values[-10:-5]) if len(historical_values) >= 10 else recent_avg
                
                if older_avg > 0:
                    trend_ratio = recent_avg / older_avg
                    return trend_ratio
            
            return 1.0
            
        except Exception as e:
            logger.error(f"Error predicting future load: {e}")
            return 1.0

    async def _generate_scaling_decision(self, group_name: str, target: str, group_metrics: Dict, scaling_reason: str) -> Optional[ScalingDecision]:
        """Generate a scaling decision"""
        try:
            current_instances = group_metrics.get('total_instances', 1)
            
            # Determine target instances based on scaling reason
            if 'scale_up' in scaling_reason:
                target_instances = min(
                    int(current_instances * self.scaling_policies['scale_up_factor']),
                    self.scaling_policies['max_instances']
                )
                action_type = 'scale_up'
            elif 'scale_down' in scaling_reason:
                target_instances = max(
                    int(current_instances * self.scaling_policies['scale_down_factor']),
                    self.scaling_policies['min_instances']
                )
                action_type = 'scale_down'
            else:
                return None
            
            # Don't scale if target is same as current
            if target_instances == current_instances:
                return None
            
            # Calculate confidence based on metric severity
            confidence = await self._calculate_scaling_confidence(group_metrics, scaling_reason)
            
            decision = ScalingDecision(
                decision_id=f"{group_name}_{target}_{int(time.time())}",
                action_type=action_type,
                target_resource=target,
                current_instances=current_instances,
                target_instances=target_instances,
                reason=scaling_reason,
                confidence=confidence,
                timestamp=datetime.now(),
                metadata={
                    'group_name': group_name,
                    'metrics_snapshot': group_metrics,
                    'scaling_trigger': scaling_reason,
                    'policy_used': self.scaling_policies
                }
            )
            
            return decision
            
        except Exception as e:
            logger.error(f"Error generating scaling decision: {e}")
            return None

    async def _calculate_scaling_confidence(self, group_metrics: Dict, scaling_reason: str) -> float:
        """Calculate confidence in scaling decision"""
        try:
            confidence_factors = []
            
            # Base confidence on metric severity
            if 'cpu' in scaling_reason:
                cpu_usage = group_metrics.get('cpu_usage_avg', 0)
                if 'scale_up' in scaling_reason:
                    severity = (cpu_usage - self.scaling_policies['cpu_threshold_up']) / self.scaling_policies['cpu_threshold_up']
                else:
                    severity = (self.scaling_policies['cpu_threshold_down'] - cpu_usage) / self.scaling_policies['cpu_threshold_down']
                confidence_factors.append(min(severity, 1.0))
            
            if 'memory' in scaling_reason:
                memory_usage = group_metrics.get('memory_usage_avg', 0)
                memory_threshold = self.scaling_policies['memory_threshold_up'] * 1024**3
                severity = (memory_usage - memory_threshold) / memory_threshold
                confidence_factors.append(min(severity, 1.0))
            
            if 'latency' in scaling_reason:
                response_time = group_metrics.get('response_time_avg', 0)
                severity = (response_time - self.scaling_policies['response_time_threshold']) / self.scaling_policies['response_time_threshold']
                confidence_factors.append(min(severity, 1.0))
            
            # Factor in metric stability (lower std dev = higher confidence)
            cpu_std = group_metrics.get('cpu_usage_std', 0)
            cpu_avg = group_metrics.get('cpu_usage_avg', 1)
            if cpu_avg > 0:
                stability_factor = 1.0 - min(cpu_std / cpu_avg, 1.0)
                confidence_factors.append(stability_factor)
            
            # Factor in health ratio
            health_ratio = group_metrics.get('health_ratio', 1.0)
            confidence_factors.append(health_ratio)
            
            # Calculate overall confidence
            if confidence_factors:
                confidence = np.mean(confidence_factors)
                return max(0.1, min(confidence, 1.0))
            
            return 0.5  # Default confidence
            
        except Exception as e:
            logger.error(f"Error calculating scaling confidence: {e}")
            return 0.5

    async def _check_self_healing_needs(self, group_name: str, group_metrics: Dict) -> List[ScalingDecision]:
        """Check for self-healing needs"""
        healing_decisions = []
        
        try:
            # Check for unhealthy agents
            health_ratio = group_metrics.get('health_ratio', 1.0)
            if health_ratio < 0.8:  # Less than 80% healthy
                # Generate healing decision
                decision = ScalingDecision(
                    decision_id=f"heal_{group_name}_{int(time.time())}",
                    action_type='heal',
                    target_resource=group_name,
                    current_instances=group_metrics.get('total_instances', 0),
                    target_instances=group_metrics.get('active_instances', 0),
                    reason=f"Health ratio below threshold: {health_ratio:.2f}",
                    confidence=1.0 - health_ratio,
                    timestamp=datetime.now(),
                    metadata={
                        'group_name': group_name,
                        'health_ratio': health_ratio,
                        'healing_type': 'restart_unhealthy'
                    }
                )
                healing_decisions.append(decision)
            
            # Check for stuck agents (high queue, low throughput)
            queue_length_avg = group_metrics.get('queue_length_avg', 0)
            throughput_efficiency = group_metrics.get('throughput_efficiency', 0)
            
            if queue_length_avg > 50 and throughput_efficiency < 1.0:
                decision = ScalingDecision(
                    decision_id=f"unstuck_{group_name}_{int(time.time())}",
                    action_type='heal',
                    target_resource=group_name,
                    current_instances=group_metrics.get('total_instances', 0),
                    target_instances=group_metrics.get('total_instances', 0),
                    reason=f"Agents appear stuck: queue={queue_length_avg}, efficiency={throughput_efficiency}",
                    confidence=0.8,
                    timestamp=datetime.now(),
                    metadata={
                        'group_name': group_name,
                        'queue_length': queue_length_avg,
                        'efficiency': throughput_efficiency,
                        'healing_type': 'restart_stuck'
                    }
                )
                healing_decisions.append(decision)
            
            # Check for memory leaks (increasing memory over time)
            memory_trend = await self._detect_memory_leak(group_name)
            if memory_trend > 1.5:  # 50% increase over time
                decision = ScalingDecision(
                    decision_id=f"memory_leak_{group_name}_{int(time.time())}",
                    action_type='heal',
                    target_resource=group_name,
                    current_instances=group_metrics.get('total_instances', 0),
                    target_instances=group_metrics.get('total_instances', 0),
                    reason=f"Memory leak detected: trend={memory_trend:.2f}",
                    confidence=0.9,
                    timestamp=datetime.now(),
                    metadata={
                        'group_name': group_name,
                        'memory_trend': memory_trend,
                        'healing_type': 'restart_memory_leak'
                    }
                )
                healing_decisions.append(decision)
            
            return healing_decisions
            
        except Exception as e:
            logger.error(f"Error checking self-healing needs: {e}")
            return []

    async def _detect_memory_leak(self, group_name: str) -> float:
        """Detect memory leak trends"""
        try:
            # Get memory usage history
            history_key = f"metrics_history:{group_name}"
            historical_data = redis_client.lrange(history_key, 0, 19)  # Last 20 data points
            
            if len(historical_data) < 10:
                return 1.0
            
            memory_values = []
            for data_point in historical_data:
                parsed = json.loads(data_point)
                memory_avg = parsed.get('memory_usage_avg', 0)
                memory_values.append(memory_avg)
            
            if len(memory_values) < 2:
                return 1.0
            
            # Calculate trend (ratio of recent to older values)
            recent_avg = np.mean(memory_values[:5])  # Most recent 5
            older_avg = np.mean(memory_values[-5:])  # Oldest 5
            
            if older_avg > 0:
                return recent_avg / older_avg
            
            return 1.0
            
        except Exception as e:
            logger.error(f"Error detecting memory leak: {e}")
            return 1.0

    async def _execute_scaling_decision(self, decision: ScalingDecision):
        """Execute a scaling decision"""
        try:
            logger.info(f"Executing scaling decision: {decision.decision_id}")
            
            if decision.action_type in ['scale_up', 'scale_down']:
                await self._execute_scaling_action(decision)
            elif decision.action_type == 'heal':
                await self._execute_healing_action(decision)
            elif decision.action_type == 'optimize':
                await self._execute_optimization_action(decision)
            
            # Update last scaling action timestamp
            group_name = decision.metadata.get('group_name', decision.target_resource)
            self.last_scaling_actions[group_name] = time.time()
            
            # Update scaling decisions metric
            scaling_decisions.labels(decision_type=decision.action_type).inc()
            
        except Exception as e:
            logger.error(f"Error executing scaling decision {decision.decision_id}: {e}")

    async def _execute_scaling_action(self, decision: ScalingDecision):
        """Execute scaling action (scale up/down)"""
        try:
            if k8s_available:
                await self._scale_kubernetes_deployment(decision)
            else:
                await self._scale_docker_service(decision)
                
        except Exception as e:
            logger.error(f"Error executing scaling action: {e}")

    async def _scale_kubernetes_deployment(self, decision: ScalingDecision):
        """Scale Kubernetes deployment"""
        try:
            deployment_name = decision.target_resource
            namespace = decision.metadata.get('namespace', 'default')
            
            # Get current deployment
            deployment = k8s_apps_v1.read_namespaced_deployment(
                name=deployment_name,
                namespace=namespace
            )
            
            # Update replica count
            deployment.spec.replicas = decision.target_instances
            
            # Apply the update
            k8s_apps_v1.patch_namespaced_deployment(
                name=deployment_name,
                namespace=namespace,
                body=deployment
            )
            
            logger.info(f"Scaled Kubernetes deployment {deployment_name} to {decision.target_instances} replicas")
            
        except Exception as e:
            logger.error(f"Error scaling Kubernetes deployment: {e}")

    async def _scale_docker_service(self, decision: ScalingDecision):
        """Scale Docker service"""
        try:
            service_name = decision.target_resource
            
            # List containers with the service label
            containers = docker_client.containers.list(
                filters={'label': f'service={service_name}'}
            )
            
            current_count = len(containers)
            target_count = decision.target_instances
            
            if target_count > current_count:
                # Scale up - start new containers
                for i in range(target_count - current_count):
                    # Get base container configuration
                    if containers:
                        base_container = containers[0]
                        image = base_container.image.tags[0] if base_container.image.tags else base_container.image.id
                        
                        # Start new container
                        docker_client.containers.run(
                            image=image,
                            detach=True,
                            labels={'service': service_name},
                            name=f"{service_name}-{int(time.time())}-{i}"
                        )
                        
            elif target_count < current_count:
                # Scale down - stop excess containers
                containers_to_stop = containers[target_count:]
                for container in containers_to_stop:
                    container.stop()
                    container.remove()
            
            logger.info(f"Scaled Docker service {service_name} to {target_count} containers")
            
        except Exception as e:
            logger.error(f"Error scaling Docker service: {e}")

    async def _execute_healing_action(self, decision: ScalingDecision):
        """Execute healing action"""
        try:
            healing_type = decision.metadata.get('healing_type', 'restart_unhealthy')
            
            if healing_type == 'restart_unhealthy':
                await self._restart_unhealthy_agents(decision)
            elif healing_type == 'restart_stuck':
                await self._restart_stuck_agents(decision)
            elif healing_type == 'restart_memory_leak':
                await self._restart_leaking_agents(decision)
            
            # Update healing actions metric
            healing_actions.labels(
                action_type=healing_type,
                target=decision.target_resource
            ).inc()
            
        except Exception as e:
            logger.error(f"Error executing healing action: {e}")

    async def _restart_unhealthy_agents(self, decision: ScalingDecision):
        """Restart unhealthy agents"""
        try:
            # Query Prometheus for unhealthy agents
            query = 'ai_agent_health_score < 0.5'
            result = prom.custom_query(query)
            
            unhealthy_agents = [item['metric'].get('agent_id') for item in result]
            
            for agent_id in unhealthy_agents:
                await self._restart_agent(agent_id, 'unhealthy')
                
            logger.info(f"Restarted {len(unhealthy_agents)} unhealthy agents")
            
        except Exception as e:
            logger.error(f"Error restarting unhealthy agents: {e}")

    async def _restart_stuck_agents(self, decision: ScalingDecision):
        """Restart stuck agents"""
        try:
            # Query for agents with high queue length and low throughput
            query = 'ai_agent_queue_length > 50'
            result = prom.custom_query(query)
            
            stuck_agents = [item['metric'].get('agent_id') for item in result]
            
            for agent_id in stuck_agents:
                await self._restart_agent(agent_id, 'stuck')
                
            logger.info(f"Restarted {len(stuck_agents)} stuck agents")
            
        except Exception as e:
            logger.error(f"Error restarting stuck agents: {e}")

    async def _restart_leaking_agents(self, decision: ScalingDecision):
        """Restart agents with memory leaks"""
        try:
            # Query for agents with high memory usage
            memory_threshold = 1024 * 1024 * 1024  # 1GB
            query = f'ai_agent_memory_usage_bytes > {memory_threshold}'
            result = prom.custom_query(query)
            
            leaking_agents = [item['metric'].get('agent_id') for item in result]
            
            for agent_id in leaking_agents:
                await self._restart_agent(agent_id, 'memory_leak')
                
            logger.info(f"Restarted {len(leaking_agents)} agents with memory leaks")
            
        except Exception as e:
            logger.error(f"Error restarting leaking agents: {e}")

    async def _restart_agent(self, agent_id: str, reason: str):
        """Restart a specific agent"""
        try:
            if k8s_available:
                # Restart Kubernetes pod
                pods = k8s_v1.list_namespaced_pod(
                    namespace='default',
                    label_selector=f'agent_id={agent_id}'
                )
                
                for pod in pods.items:
                    k8s_v1.delete_namespaced_pod(
                        name=pod.metadata.name,
                        namespace='default'
                    )
                    
            else:
                # Restart Docker container
                containers = docker_client.containers.list(
                    filters={'label': f'agent_id={agent_id}'}
                )
                
                for container in containers:
                    container.restart()
            
            logger.info(f"Restarted agent {agent_id} due to {reason}")
            
        except Exception as e:
            logger.error(f"Error restarting agent {agent_id}: {e}")

    async def _execute_optimization_action(self, decision: ScalingDecision):
        """Execute optimization action"""
        try:
            # Placeholder for optimization actions
            # Could include:
            # - Load balancing adjustments
            # - Resource allocation optimization
            # - Network topology optimization
            # - Cache configuration tuning
            
            logger.info(f"Executed optimization action for {decision.target_resource}")
            
        except Exception as e:
            logger.error(f"Error executing optimization action: {e}")

    async def _update_prediction_models(self, current_metrics: Dict):
        """Update machine learning models with current data"""
        try:
            # Store current metrics for model training
            timestamp = time.time()
            
            for group_name in self.resource_groups.keys():
                history_key = f"metrics_history:{group_name}"
                
                # Create metrics snapshot
                snapshot = {
                    'timestamp': timestamp,
                    'cpu_usage_avg': np.mean([item['value'] for item in current_metrics.get('cpu_usage', [])]),
                    'memory_usage_avg': np.mean([item['value'] for item in current_metrics.get('memory_usage', [])]),
                    'response_time_avg': np.mean([item['value'] for item in current_metrics.get('response_time', [])]),
                    'queue_length_avg': np.mean([item['value'] for item in current_metrics.get('queue_length', [])]),
                    'health_score_avg': np.mean([item['value'] for item in current_metrics.get('health_score', [])]),
                }
                
                # Store in Redis
                redis_client.lpush(history_key, json.dumps(snapshot))
                redis_client.ltrim(history_key, 0, 199)  # Keep last 200 data points
            
            # Update prediction model accuracy
            await self._evaluate_prediction_accuracy()
            
        except Exception as e:
            logger.error(f"Error updating prediction models: {e}")

    async def _evaluate_prediction_accuracy(self):
        """Evaluate and update prediction model accuracy"""
        try:
            # Simple accuracy evaluation based on recent predictions vs actual outcomes
            for model_name, model_config in self.prediction_models.items():
                # Get recent predictions and actual values
                predictions_key = f"predictions:{model_name}"
                recent_predictions = redis_client.lrange(predictions_key, 0, 9)
                
                if len(recent_predictions) >= 5:
                    # Calculate simple accuracy metric
                    accuracy_scores = []
                    for pred_data in recent_predictions:
                        parsed = json.loads(pred_data)
                        predicted = parsed.get('predicted_value', 0)
                        actual = parsed.get('actual_value', 0)
                        
                        if actual > 0:
                            error = abs(predicted - actual) / actual
                            accuracy = max(0, 1 - error)
                            accuracy_scores.append(accuracy)
                    
                    if accuracy_scores:
                        model_accuracy = np.mean(accuracy_scores)
                        self.prediction_models[model_name]['accuracy'] = model_accuracy
                        
                        # Update Prometheus metric
                        prediction_accuracy.labels(predictor_type=model_name).set(model_accuracy)
            
        except Exception as e:
            logger.error(f"Error evaluating prediction accuracy: {e}")

    async def _store_scaling_decisions(self, decisions: List[ScalingDecision]):
        """Store scaling decisions for analysis"""
        try:
            for decision in decisions:
                decision_data = {
                    'decision_id': decision.decision_id,
                    'action_type': decision.action_type,
                    'target_resource': decision.target_resource,
                    'current_instances': decision.current_instances,
                    'target_instances': decision.target_instances,
                    'reason': decision.reason,
                    'confidence': decision.confidence,
                    'timestamp': decision.timestamp.isoformat(),
                    'metadata': decision.metadata
                }
                
                # Store in Redis
                decisions_key = "scaling_decisions"
                redis_client.zadd(decisions_key, {json.dumps(decision_data): time.time()})
                
                # Keep only recent decisions (last 7 days)
                cutoff_time = time.time() - (7 * 24 * 3600)
                redis_client.zremrangebyscore(decisions_key, 0, cutoff_time)
                
        except Exception as e:
            logger.error(f"Error storing scaling decisions: {e}")

# Initialize autoscaler
autoscaler = AutoScaler()

# Background task for continuous monitoring
async def continuous_monitoring():
    """Background task for continuous autoscaling"""
    while True:
        try:
            logger.info("Running autoscaling analysis...")
            decisions = await autoscaler.analyze_and_scale()
            
            if decisions:
                logger.info(f"Made {len(decisions)} scaling decisions")
                for decision in decisions:
                    logger.info(f"Decision: {decision.action_type} {decision.target_resource} "
                              f"from {decision.current_instances} to {decision.target_instances} "
                              f"(reason: {decision.reason})")
            
            # Calculate and update system efficiency
            await update_system_efficiency()
            
            # Wait before next analysis
            await asyncio.sleep(60)  # Run every minute
            
        except Exception as e:
            logger.error(f"Error in continuous monitoring: {e}")
            await asyncio.sleep(60)

async def update_system_efficiency():
    """Update system efficiency metrics"""
    try:
        # Get current system state
        current_metrics = await autoscaler._get_current_metrics()
        
        # Calculate various efficiency metrics
        total_agents = current_metrics.get('total_agents', 0)
        active_agents = current_metrics.get('active_agents', 0)
        
        if total_agents > 0:
            # Utilization efficiency
            utilization_efficiency = active_agents / total_agents
            system_efficiency.labels(efficiency_type='utilization').set(utilization_efficiency)
            
            # Performance efficiency
            avg_health = current_metrics.get('average_health', 0)
            system_efficiency.labels(efficiency_type='performance').set(avg_health)
            
            # Resource efficiency (placeholder - would need more detailed resource metrics)
            resource_efficiency = min(utilization_efficiency * avg_health, 1.0)
            system_efficiency.labels(efficiency_type='resource').set(resource_efficiency)
        
    except Exception as e:
        logger.error(f"Error updating system efficiency: {e}")

# API endpoints
@app.post("/analyze")
async def analyze_system():
    """Trigger immediate autoscaling analysis"""
    decisions = await autoscaler.analyze_and_scale()
    return {"decisions": decisions, "count": len(decisions)}

@app.get("/decisions")
async def get_scaling_decisions(hours: int = 24):
    """Get recent scaling decisions"""
    try:
        decisions_key = "scaling_decisions"
        cutoff_time = time.time() - (hours * 3600)
        
        decision_data = redis_client.zrangebyscore(
            decisions_key, cutoff_time, '+inf', withscores=True
        )
        
        decisions = []
        for data, timestamp in decision_data:
            parsed_data = json.loads(data)
            decisions.append(parsed_data)
        
        return {"decisions": decisions, "count": len(decisions)}
        
    except Exception as e:
        logger.error(f"Error getting scaling decisions: {e}")
        return {"decisions": [], "count": 0}

@app.get("/policies")
async def get_scaling_policies():
    """Get current scaling policies"""
    return {"policies": autoscaler.scaling_policies}

@app.post("/policies")
async def update_scaling_policies(policies: Dict[str, Any]):
    """Update scaling policies"""
    try:
        # Validate and update policies
        for key, value in policies.items():
            if key in autoscaler.scaling_policies:
                autoscaler.scaling_policies[key] = value
        
        return {"status": "updated", "policies": autoscaler.scaling_policies}
        
    except Exception as e:
        logger.error(f"Error updating policies: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/efficiency")
async def get_system_efficiency():
    """Get current system efficiency metrics"""
    try:
        current_metrics = await autoscaler._get_current_metrics()
        
        total_agents = current_metrics.get('total_agents', 0)
        active_agents = current_metrics.get('active_agents', 0)
        avg_health = current_metrics.get('average_health', 0)
        
        efficiency_metrics = {
            'utilization_rate': active_agents / max(total_agents, 1),
            'health_score': avg_health,
            'total_agents': total_agents,
            'active_agents': active_agents,
            'recent_scaling_actions': len(autoscaler.last_scaling_actions),
            'prediction_accuracy': {
                model_name: model_config['accuracy']
                for model_name, model_config in autoscaler.prediction_models.items()
            }
        }
        
        return efficiency_metrics
        
    except Exception as e:
        logger.error(f"Error getting system efficiency: {e}")
        return {"error": str(e)}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.on_event("startup")
async def startup_event():
    """Start background tasks"""
    asyncio.create_task(continuous_monitoring())
    logger.info("Autoscaler service started")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8083)