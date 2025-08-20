#!/usr/bin/env python3
"""
Enterprise Telemetry System - Phase 2 Implementation
Based on SuperAGI patterns for production-grade monitoring and optimization
"""

import asyncio
import json
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import statistics
import hashlib
from collections import defaultdict, deque

# Performance Monitoring Classes

class MetricType(Enum):
    """Types of metrics to track"""
    LATENCY = "latency"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    TOKEN_USAGE = "token_usage"
    MEMORY_USAGE = "memory_usage"
    CACHE_HIT_RATE = "cache_hit_rate"
    AGENT_PERFORMANCE = "agent_performance"
    COST = "cost"

class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class PerformanceMetric:
    """Individual performance metric"""
    timestamp: datetime
    metric_type: MetricType
    agent_id: Optional[str]
    value: float
    unit: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Alert:
    """Performance or system alert"""
    id: str
    timestamp: datetime
    severity: AlertSeverity
    metric_type: MetricType
    message: str
    value: float
    threshold: float
    action_required: str

@dataclass
class PerformanceReport:
    """Comprehensive performance analysis report"""
    period_start: datetime
    period_end: datetime
    total_requests: int
    successful_requests: int
    failed_requests: int
    avg_latency: float
    p95_latency: float
    p99_latency: float
    total_tokens_used: int
    total_cost: float
    cache_hit_rate: float
    agent_performance: Dict[str, Dict[str, float]]
    recommendations: List[str]
    alerts_triggered: List[Alert]

class EnterpriseTelemetrySystem:
    """
    Production-grade telemetry system for monitoring agent performance,
    resource usage, and system health
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._default_config()
        self.metrics_buffer = deque(maxlen=10000)  # Circular buffer for metrics
        self.alerts = []
        self.agent_profiles = {}
        self.cost_calculator = CostCalculator()
        self.anomaly_detector = AnomalyDetector()
        self.optimization_engine = OptimizationEngine()
        
    def _default_config(self) -> Dict[str, Any]:
        """Default telemetry configuration"""
        return {
            "metrics_retention_days": 30,
            "alert_thresholds": {
                "latency_p95": 5.0,  # 5 seconds
                "error_rate": 0.05,  # 5%
                "token_usage_per_request": 10000,
                "cost_per_request": 0.50,
                "memory_usage_mb": 1024
            },
            "sampling_rate": 1.0,  # Sample 100% of requests
            "export_destinations": ["prometheus", "grafana", "datadog"],
            "anomaly_detection_enabled": True
        }
    
    async def track_agent_execution(self, agent_id: str, execution_data: Dict[str, Any]):
        """Track individual agent execution metrics"""
        
        # Record latency
        latency_metric = PerformanceMetric(
            timestamp=datetime.utcnow(),
            metric_type=MetricType.LATENCY,
            agent_id=agent_id,
            value=execution_data.get("execution_time", 0),
            unit="seconds",
            metadata={"task": execution_data.get("task", "")}
        )
        self.metrics_buffer.append(latency_metric)
        
        # Record token usage
        token_metric = PerformanceMetric(
            timestamp=datetime.utcnow(),
            metric_type=MetricType.TOKEN_USAGE,
            agent_id=agent_id,
            value=execution_data.get("tokens_used", 0),
            unit="tokens",
            metadata={
                "input_tokens": execution_data.get("input_tokens", 0),
                "output_tokens": execution_data.get("output_tokens", 0)
            }
        )
        self.metrics_buffer.append(token_metric)
        
        # Update agent profile
        self._update_agent_profile(agent_id, execution_data)
        
        # Check for anomalies
        if self.config["anomaly_detection_enabled"]:
            anomalies = await self.anomaly_detector.detect(latency_metric)
            if anomalies:
                await self._handle_anomalies(anomalies)
        
        # Check thresholds and create alerts
        await self._check_thresholds(latency_metric, token_metric)
    
    def _update_agent_profile(self, agent_id: str, execution_data: Dict[str, Any]):
        """Update agent performance profile"""
        
        if agent_id not in self.agent_profiles:
            self.agent_profiles[agent_id] = {
                "total_executions": 0,
                "successful_executions": 0,
                "failed_executions": 0,
                "total_latency": 0.0,
                "total_tokens": 0,
                "latency_history": deque(maxlen=100),
                "error_types": defaultdict(int)
            }
        
        profile = self.agent_profiles[agent_id]
        profile["total_executions"] += 1
        
        if execution_data.get("success", True):
            profile["successful_executions"] += 1
        else:
            profile["failed_executions"] += 1
            error_type = execution_data.get("error_type", "unknown")
            profile["error_types"][error_type] += 1
        
        latency = execution_data.get("execution_time", 0)
        profile["total_latency"] += latency
        profile["latency_history"].append(latency)
        profile["total_tokens"] += execution_data.get("tokens_used", 0)
    
    async def _check_thresholds(self, *metrics: PerformanceMetric):
        """Check metrics against configured thresholds"""
        
        thresholds = self.config["alert_thresholds"]
        
        for metric in metrics:
            alert = None
            
            if metric.metric_type == MetricType.LATENCY:
                if metric.value > thresholds["latency_p95"]:
                    alert = Alert(
                        id=self._generate_alert_id(),
                        timestamp=datetime.utcnow(),
                        severity=AlertSeverity.WARNING,
                        metric_type=MetricType.LATENCY,
                        message=f"High latency detected for agent {metric.agent_id}",
                        value=metric.value,
                        threshold=thresholds["latency_p95"],
                        action_required="Investigate agent performance or scale resources"
                    )
            
            elif metric.metric_type == MetricType.TOKEN_USAGE:
                if metric.value > thresholds["token_usage_per_request"]:
                    alert = Alert(
                        id=self._generate_alert_id(),
                        timestamp=datetime.utcnow(),
                        severity=AlertSeverity.WARNING,
                        metric_type=MetricType.TOKEN_USAGE,
                        message=f"High token usage for agent {metric.agent_id}",
                        value=metric.value,
                        threshold=thresholds["token_usage_per_request"],
                        action_required="Optimize prompts or implement caching"
                    )
            
            if alert:
                self.alerts.append(alert)
                await self._send_alert(alert)
    
    async def _send_alert(self, alert: Alert):
        """Send alert to configured destinations"""
        # In production, integrate with PagerDuty, Slack, etc.
        print(f"⚠️ ALERT [{alert.severity.value}]: {alert.message}")
    
    def generate_performance_report(self, period_hours: int = 24) -> PerformanceReport:
        """Generate comprehensive performance report"""
        
        now = datetime.utcnow()
        period_start = now - timedelta(hours=period_hours)
        
        # Filter metrics for reporting period
        period_metrics = [
            m for m in self.metrics_buffer 
            if m.timestamp >= period_start
        ]
        
        # Calculate statistics
        latency_values = [
            m.value for m in period_metrics 
            if m.metric_type == MetricType.LATENCY
        ]
        
        token_values = [
            m.value for m in period_metrics
            if m.metric_type == MetricType.TOKEN_USAGE
        ]
        
        # Calculate percentiles
        avg_latency = statistics.mean(latency_values) if latency_values else 0
        p95_latency = self._calculate_percentile(latency_values, 95) if latency_values else 0
        p99_latency = self._calculate_percentile(latency_values, 99) if latency_values else 0
        
        # Calculate costs
        total_tokens = sum(token_values)
        total_cost = self.cost_calculator.calculate_cost(total_tokens)
        
        # Generate agent performance summary
        agent_performance = self._generate_agent_performance_summary()
        
        # Generate recommendations
        recommendations = self.optimization_engine.generate_recommendations(
            latency_values, token_values, agent_performance
        )
        
        # Get recent alerts
        recent_alerts = [
            alert for alert in self.alerts
            if alert.timestamp >= period_start
        ]
        
        return PerformanceReport(
            period_start=period_start,
            period_end=now,
            total_requests=len(latency_values),
            successful_requests=sum(1 for p in self.agent_profiles.values() 
                                   for _ in range(p["successful_executions"])),
            failed_requests=sum(1 for p in self.agent_profiles.values()
                              for _ in range(p["failed_executions"])),
            avg_latency=avg_latency,
            p95_latency=p95_latency,
            p99_latency=p99_latency,
            total_tokens_used=total_tokens,
            total_cost=total_cost,
            cache_hit_rate=self._calculate_cache_hit_rate(),
            agent_performance=agent_performance,
            recommendations=recommendations,
            alerts_triggered=recent_alerts
        )
    
    def _generate_agent_performance_summary(self) -> Dict[str, Dict[str, float]]:
        """Generate performance summary for each agent"""
        
        summary = {}
        
        for agent_id, profile in self.agent_profiles.items():
            if profile["total_executions"] > 0:
                summary[agent_id] = {
                    "success_rate": profile["successful_executions"] / profile["total_executions"],
                    "avg_latency": profile["total_latency"] / profile["total_executions"],
                    "total_tokens": profile["total_tokens"],
                    "avg_tokens_per_execution": profile["total_tokens"] / profile["total_executions"],
                    "error_rate": profile["failed_executions"] / profile["total_executions"]
                }
        
        return summary
    
    def _calculate_percentile(self, values: List[float], percentile: int) -> float:
        """Calculate percentile value"""
        if not values:
            return 0
        
        sorted_values = sorted(values)
        index = int(len(sorted_values) * percentile / 100)
        return sorted_values[min(index, len(sorted_values) - 1)]
    
    def _calculate_cache_hit_rate(self) -> float:
        """Calculate cache hit rate from metrics"""
        cache_metrics = [
            m for m in self.metrics_buffer
            if m.metric_type == MetricType.CACHE_HIT_RATE
        ]
        
        if not cache_metrics:
            return 0.0
        
        return statistics.mean([m.value for m in cache_metrics])
    
    def _generate_alert_id(self) -> str:
        """Generate unique alert ID"""
        return hashlib.md5(
            f"{datetime.utcnow().isoformat()}{len(self.alerts)}".encode()
        ).hexdigest()[:8]
    
    async def _handle_anomalies(self, anomalies: List[Dict[str, Any]]):
        """Handle detected anomalies"""
        for anomaly in anomalies:
            alert = Alert(
                id=self._generate_alert_id(),
                timestamp=datetime.utcnow(),
                severity=AlertSeverity.WARNING,
                metric_type=MetricType.LATENCY,
                message=f"Anomaly detected: {anomaly['description']}",
                value=anomaly['value'],
                threshold=anomaly['expected'],
                action_required="Investigate unusual pattern"
            )
            self.alerts.append(alert)
            await self._send_alert(alert)

class CostCalculator:
    """Calculate costs based on token usage and resource consumption"""
    
    def __init__(self):
        self.pricing = {
            "gpt-4": 0.03 / 1000,  # $0.03 per 1K tokens
            "claude-3-opus": 0.015 / 1000,  # $0.015 per 1K tokens
            "claude-3-sonnet": 0.003 / 1000,  # $0.003 per 1K tokens
            "embedding": 0.0001 / 1000,  # $0.0001 per 1K tokens
        }
    
    def calculate_cost(self, tokens: int, model: str = "claude-3-sonnet") -> float:
        """Calculate cost for token usage"""
        rate = self.pricing.get(model, 0.003 / 1000)
        return tokens * rate

class AnomalyDetector:
    """Detect anomalies in performance metrics"""
    
    def __init__(self):
        self.baseline_window = deque(maxlen=100)
        self.sensitivity = 2.0  # Standard deviations for anomaly
    
    async def detect(self, metric: PerformanceMetric) -> List[Dict[str, Any]]:
        """Detect anomalies in metric"""
        
        anomalies = []
        
        # Add to baseline
        self.baseline_window.append(metric.value)
        
        if len(self.baseline_window) < 10:
            return anomalies  # Not enough data
        
        # Calculate statistics
        mean = statistics.mean(self.baseline_window)
        stdev = statistics.stdev(self.baseline_window)
        
        # Check for anomaly
        if abs(metric.value - mean) > self.sensitivity * stdev:
            anomalies.append({
                "metric_type": metric.metric_type.value,
                "value": metric.value,
                "expected": mean,
                "deviation": abs(metric.value - mean) / stdev,
                "description": f"Value {metric.value:.2f} deviates {abs(metric.value - mean) / stdev:.1f} standard deviations from mean {mean:.2f}"
            })
        
        return anomalies

class OptimizationEngine:
    """Generate optimization recommendations based on telemetry data"""
    
    def generate_recommendations(self, latency_values: List[float], 
                                token_values: List[float],
                                agent_performance: Dict[str, Dict[str, float]]) -> List[str]:
        """Generate actionable optimization recommendations"""
        
        recommendations = []
        
        # Latency recommendations
        if latency_values:
            avg_latency = statistics.mean(latency_values)
            if avg_latency > 3.0:
                recommendations.append(
                    "High average latency detected. Consider:\n"
                    "  • Implementing response caching for repeated queries\n"
                    "  • Using faster models for simple tasks\n"
                    "  • Parallelizing independent agent operations"
                )
        
        # Token usage recommendations
        if token_values:
            avg_tokens = statistics.mean(token_values)
            if avg_tokens > 5000:
                recommendations.append(
                    "High token usage detected. Consider:\n"
                    "  • Implementing prompt compression techniques\n"
                    "  • Using context window management strategies\n"
                    "  • Caching intermediate results"
                )
        
        # Agent-specific recommendations
        for agent_id, performance in agent_performance.items():
            if performance.get("error_rate", 0) > 0.1:
                recommendations.append(
                    f"Agent {agent_id} has high error rate ({performance['error_rate']:.1%}). Consider:\n"
                    f"  • Reviewing agent configuration and error handling\n"
                    f"  • Implementing retry mechanisms with exponential backoff\n"
                    f"  • Adding fallback strategies"
                )
            
            if performance.get("avg_latency", 0) > 5.0:
                recommendations.append(
                    f"Agent {agent_id} has high latency ({performance['avg_latency']:.1f}s). Consider:\n"
                    f"  • Optimizing agent prompts and instructions\n"
                    f"  • Using specialized models for this agent's tasks\n"
                    f"  • Implementing agent-specific caching"
                )
        
        # Cost optimization
        if token_values:
            total_tokens = sum(token_values)
            estimated_cost = CostCalculator().calculate_cost(total_tokens)
            if estimated_cost > 10.0:  # $10 threshold
                recommendations.append(
                    f"High cost detected (${estimated_cost:.2f}). Consider:\n"
                    f"  • Using cheaper models for non-critical tasks\n"
                    f"  • Implementing aggressive caching strategies\n"
                    f"  • Batching similar requests"
                )
        
        return recommendations if recommendations else ["System performing optimally. No recommendations at this time."]

# Real-time Monitoring Dashboard

class TelemetryDashboard:
    """Real-time monitoring dashboard for telemetry data"""
    
    def __init__(self, telemetry_system: EnterpriseTelemetrySystem):
        self.telemetry = telemetry_system
        self.refresh_interval = 5  # seconds
    
    async def display_metrics(self):
        """Display real-time metrics dashboard"""
        
        while True:
            # Clear screen (in production, use proper UI framework)
            print("\033[2J\033[H")  # Clear screen
            
            print("=" * 80)
            print(" " * 25 + "🎯 ENTERPRISE TELEMETRY DASHBOARD")
            print("=" * 80)
            
            # Generate current report
            report = self.telemetry.generate_performance_report(period_hours=1)
            
            # Display key metrics
            print(f"\n📊 Performance Metrics (Last Hour)")
            print(f"  Total Requests: {report.total_requests}")
            print(f"  Success Rate: {(report.successful_requests / max(report.total_requests, 1)) * 100:.1f}%")
            print(f"  Average Latency: {report.avg_latency:.2f}s")
            print(f"  P95 Latency: {report.p95_latency:.2f}s")
            print(f"  P99 Latency: {report.p99_latency:.2f}s")
            
            print(f"\n💰 Resource Usage")
            print(f"  Total Tokens: {report.total_tokens_used:,}")
            print(f"  Estimated Cost: ${report.total_cost:.2f}")
            print(f"  Cache Hit Rate: {report.cache_hit_rate * 100:.1f}%")
            
            print(f"\n🤖 Agent Performance")
            for agent_id, performance in report.agent_performance.items():
                print(f"  {agent_id}:")
                print(f"    • Success Rate: {performance['success_rate'] * 100:.1f}%")
                print(f"    • Avg Latency: {performance['avg_latency']:.2f}s")
                print(f"    • Avg Tokens: {performance['avg_tokens_per_execution']:.0f}")
            
            if report.alerts_triggered:
                print(f"\n⚠️  Active Alerts ({len(report.alerts_triggered)})")
                for alert in report.alerts_triggered[-3:]:  # Show last 3 alerts
                    print(f"  [{alert.severity.value.upper()}] {alert.message}")
            
            print(f"\n💡 Optimization Recommendations")
            for i, rec in enumerate(report.recommendations[:3], 1):
                print(f"  {i}. {rec.split('.')[0]}...")  # Show first sentence
            
            print("\n" + "=" * 80)
            print("Refreshing in 5 seconds... Press Ctrl+C to exit")
            
            await asyncio.sleep(self.refresh_interval)

# Export Integrations

class TelemetryExporter:
    """Export telemetry data to external monitoring systems"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.exporters = self._initialize_exporters()
    
    def _initialize_exporters(self) -> Dict[str, Any]:
        """Initialize export destinations"""
        exporters = {}
        
        for destination in self.config.get("export_destinations", []):
            if destination == "prometheus":
                exporters["prometheus"] = PrometheusExporter()
            elif destination == "grafana":
                exporters["grafana"] = GrafanaExporter()
            elif destination == "datadog":
                exporters["datadog"] = DatadogExporter()
        
        return exporters
    
    async def export_metrics(self, metrics: List[PerformanceMetric]):
        """Export metrics to configured destinations"""
        
        for name, exporter in self.exporters.items():
            try:
                await exporter.export(metrics)
            except Exception as e:
                print(f"Failed to export to {name}: {e}")

class PrometheusExporter:
    """Export metrics to Prometheus"""
    
    async def export(self, metrics: List[PerformanceMetric]):
        """Export metrics in Prometheus format"""
        # In production, implement actual Prometheus push gateway integration
        pass

class GrafanaExporter:
    """Export metrics to Grafana"""
    
    async def export(self, metrics: List[PerformanceMetric]):
        """Export metrics to Grafana"""
        # In production, implement Grafana Loki/Tempo integration
        pass

class DatadogExporter:
    """Export metrics to Datadog"""
    
    async def export(self, metrics: List[PerformanceMetric]):
        """Export metrics to Datadog"""
        # In production, implement Datadog API integration
        pass

# Example Usage

async def main():
    """Example usage of enterprise telemetry system"""
    
    # Initialize telemetry system
    telemetry = EnterpriseTelemetrySystem()
    
    # Simulate agent executions
    agents = ["product_manager", "architect", "developer", "qa_engineer"]
    
    for i in range(10):
        for agent in agents:
            # Simulate execution data
            execution_data = {
                "task": f"Task_{i}",
                "execution_time": 2.5 + (i % 3),  # Variable latency
                "tokens_used": 3000 + (i * 500),
                "input_tokens": 2000 + (i * 300),
                "output_tokens": 1000 + (i * 200),
                "success": i % 5 != 0,  # 80% success rate
                "error_type": "timeout" if i % 5 == 0 else None
            }
            
            await telemetry.track_agent_execution(agent, execution_data)
            await asyncio.sleep(0.1)
    
    # Generate performance report
    report = telemetry.generate_performance_report(period_hours=1)
    
    print("📊 Performance Report Generated:")
    print(f"  Period: {report.period_start} to {report.period_end}")
    print(f"  Total Requests: {report.total_requests}")
    print(f"  Average Latency: {report.avg_latency:.2f}s")
    print(f"  P95 Latency: {report.p95_latency:.2f}s")
    print(f"  Total Cost: ${report.total_cost:.2f}")
    print(f"  Recommendations: {len(report.recommendations)}")
    
    # Start dashboard (comment out for testing)
    # dashboard = TelemetryDashboard(telemetry)
    # await dashboard.display_metrics()

if __name__ == "__main__":
    asyncio.run(main())