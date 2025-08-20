#!/usr/bin/env python3
"""
ADVANCED REAL-TIME PERFORMANCE MONITORING & ADAPTIVE SCALING SYSTEM
Revolutionary enterprise-grade monitoring for multi-agent AI coordination platform
"""

import asyncio
import time
import json
import numpy as np
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Callable, Union
from dataclasses import dataclass, asdict, field
from collections import defaultdict, deque
from pathlib import Path
import logging
import statistics
from enum import Enum
import hashlib
import pickle

# Time series data handling
try:
    from influxdb_client import InfluxDBClient, Point, WritePrecision
    from influxdb_client.client.write_api import SYNCHRONOUS
    INFLUXDB_AVAILABLE = True
except ImportError:
    print("⚠️  InfluxDB client not available. Install with: pip install influxdb-client")
    INFLUXDB_AVAILABLE = False

# ML for anomaly detection
try:
    from sklearn.ensemble import IsolationForest
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import DBSCAN
    import joblib
    ML_AVAILABLE = True
except ImportError:
    print("⚠️  ML libraries not available for anomaly detection")
    ML_AVAILABLE = False

# Notification systems
try:
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import requests  # For webhook notifications
    NOTIFICATION_AVAILABLE = True
except ImportError:
    print("⚠️  Notification libraries not available")
    NOTIFICATION_AVAILABLE = False

class MetricType(Enum):
    """Types of performance metrics"""
    LATENCY = "latency"
    THROUGHPUT = "throughput"
    SUCCESS_RATE = "success_rate"
    QUALITY_SCORE = "quality_score"
    COST_EFFICIENCY = "cost_efficiency"
    AGENT_LOAD = "agent_load"
    SYSTEM_HEALTH = "system_health"
    ERROR_RATE = "error_rate"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"

class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

class SystemStatus(Enum):
    """Overall system status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    FAILING = "failing"

@dataclass
class MetricPoint:
    """Single metric data point"""
    timestamp: datetime
    value: float
    metric_type: MetricType
    source: str
    tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Alert:
    """System alert"""
    id: str
    severity: AlertSeverity
    title: str
    description: str
    source: str
    metric_type: MetricType
    timestamp: datetime
    value: float
    threshold: float
    tags: Dict[str, str] = field(default_factory=dict)
    acknowledged: bool = False
    resolved: bool = False
    resolution_time: Optional[datetime] = None

@dataclass
class PerformanceTrend:
    """Performance trend analysis"""
    metric_type: MetricType
    source: str
    trend_direction: str  # "increasing", "decreasing", "stable", "volatile"
    trend_strength: float  # 0.0 to 1.0
    change_rate: float  # percentage change per minute
    significance: float  # statistical significance
    forecast_next_hour: float
    confidence_interval: Tuple[float, float]

@dataclass
class SystemHealthSnapshot:
    """Complete system health snapshot"""
    timestamp: datetime
    overall_status: SystemStatus
    quality_score: float
    performance_score: float
    efficiency_score: float
    active_alerts: List[Alert]
    agent_status: Dict[str, Dict[str, float]]
    resource_utilization: Dict[str, float]
    orchestration_metrics: Dict[str, float]
    predictions: Dict[str, float]

class TimeSeriesBuffer:
    """High-performance time series buffer with automatic aggregation"""
    
    def __init__(self, max_size: int = 10000, retention_hours: int = 24):
        self.max_size = max_size
        self.retention_hours = retention_hours
        self.data = deque(maxlen=max_size)
        self.lock = threading.RLock()
        
        # Pre-computed aggregations for fast retrieval
        self._minute_aggregates = {}
        self._hour_aggregates = {}
        self._last_cleanup = datetime.now()
    
    def add_point(self, point: MetricPoint):
        """Add a metric point to the buffer"""
        with self.lock:
            self.data.append(point)
            self._update_aggregates(point)
            self._cleanup_if_needed()
    
    def add_points(self, points: List[MetricPoint]):
        """Add multiple points efficiently"""
        with self.lock:
            for point in points:
                self.data.append(point)
                self._update_aggregates(point)
            self._cleanup_if_needed()
    
    def get_recent(self, minutes: int = 5) -> List[MetricPoint]:
        """Get recent data points"""
        cutoff = datetime.now() - timedelta(minutes=minutes)
        with self.lock:
            return [p for p in self.data if p.timestamp >= cutoff]
    
    def get_range(self, start_time: datetime, end_time: datetime) -> List[MetricPoint]:
        """Get data points in time range"""
        with self.lock:
            return [p for p in self.data if start_time <= p.timestamp <= end_time]
    
    def get_statistics(self, minutes: int = 5) -> Dict[str, float]:
        """Get statistical summary of recent data"""
        recent_data = self.get_recent(minutes)
        if not recent_data:
            return {}
        
        values = [p.value for p in recent_data]
        
        return {
            'count': len(values),
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'std_dev': statistics.stdev(values) if len(values) > 1 else 0.0,
            'min': min(values),
            'max': max(values),
            'p95': np.percentile(values, 95),
            'p99': np.percentile(values, 99)
        }
    
    def _update_aggregates(self, point: MetricPoint):
        """Update pre-computed aggregations"""
        minute_key = point.timestamp.strftime('%Y-%m-%d_%H:%M')
        hour_key = point.timestamp.strftime('%Y-%m-%d_%H')
        
        # Update minute aggregates
        if minute_key not in self._minute_aggregates:
            self._minute_aggregates[minute_key] = {
                'values': [],
                'count': 0,
                'sum': 0.0,
                'min': float('inf'),
                'max': float('-inf')
            }
        
        agg = self._minute_aggregates[minute_key]
        agg['values'].append(point.value)
        agg['count'] += 1
        agg['sum'] += point.value
        agg['min'] = min(agg['min'], point.value)
        agg['max'] = max(agg['max'], point.value)
        
        # Update hour aggregates similarly
        if hour_key not in self._hour_aggregates:
            self._hour_aggregates[hour_key] = {
                'values': [],
                'count': 0,
                'sum': 0.0,
                'min': float('inf'),
                'max': float('-inf')
            }
        
        hour_agg = self._hour_aggregates[hour_key]
        hour_agg['values'].append(point.value)
        hour_agg['count'] += 1
        hour_agg['sum'] += point.value
        hour_agg['min'] = min(hour_agg['min'], point.value)
        hour_agg['max'] = max(hour_agg['max'], point.value)
    
    def _cleanup_if_needed(self):
        """Clean up old aggregates periodically"""
        now = datetime.now()
        if (now - self._last_cleanup).total_seconds() > 300:  # Every 5 minutes
            cutoff = now - timedelta(hours=self.retention_hours)
            
            # Clean minute aggregates
            cutoff_minute = cutoff.strftime('%Y-%m-%d_%H:%M')
            self._minute_aggregates = {
                k: v for k, v in self._minute_aggregates.items() 
                if k >= cutoff_minute
            }
            
            # Clean hour aggregates
            cutoff_hour = cutoff.strftime('%Y-%m-%d_%H')
            self._hour_aggregates = {
                k: v for k, v in self._hour_aggregates.items()
                if k >= cutoff_hour
            }
            
            self._last_cleanup = now

class AnomalyDetector:
    """ML-powered anomaly detection system"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.baseline_stats = {}
        self.anomaly_history = defaultdict(list)
        
        if ML_AVAILABLE:
            self._initialize_models()
    
    def _initialize_models(self):
        """Initialize ML models for different metric types"""
        
        # Isolation Forest for each metric type
        for metric_type in MetricType:
            self.models[metric_type] = IsolationForest(
                contamination=0.1,  # Expected 10% anomalies
                random_state=42,
                n_estimators=100
            )
            self.scalers[metric_type] = StandardScaler()
    
    def update_baseline(self, metric_type: MetricType, data_points: List[float]):
        """Update baseline statistics for a metric type"""
        
        if not data_points:
            return
        
        self.baseline_stats[metric_type] = {
            'mean': statistics.mean(data_points),
            'std': statistics.stdev(data_points) if len(data_points) > 1 else 0.0,
            'p95': np.percentile(data_points, 95),
            'p99': np.percentile(data_points, 99),
            'updated': datetime.now()
        }
        
        if ML_AVAILABLE and len(data_points) >= 10:
            # Train anomaly detection model
            features = np.array(data_points).reshape(-1, 1)
            scaled_features = self.scalers[metric_type].fit_transform(features)
            self.models[metric_type].fit(scaled_features)
    
    def detect_anomalies(self, metric_type: MetricType, recent_values: List[float],
                        current_value: float) -> Dict[str, Any]:
        """Detect if current value is anomalous"""
        
        if metric_type not in self.baseline_stats:
            return {'is_anomaly': False, 'confidence': 0.0, 'method': 'no_baseline'}
        
        baseline = self.baseline_stats[metric_type]
        anomaly_result = {
            'is_anomaly': False,
            'confidence': 0.0,
            'method': 'statistical',
            'details': {}
        }
        
        # Statistical anomaly detection
        z_score = abs(current_value - baseline['mean']) / max(baseline['std'], 0.001)
        
        # Consider anomalous if beyond 3 standard deviations
        if z_score > 3.0:
            anomaly_result['is_anomaly'] = True
            anomaly_result['confidence'] = min(1.0, z_score / 5.0)
            anomaly_result['details']['z_score'] = z_score
        
        # ML-based detection if available
        if ML_AVAILABLE and len(recent_values) >= 5:
            try:
                features = np.array([current_value]).reshape(1, -1)
                scaled_features = self.scalers[metric_type].transform(features)
                
                # Get anomaly score (-1 for anomaly, 1 for normal)
                ml_prediction = self.models[metric_type].predict(scaled_features)[0]
                ml_score = self.models[metric_type].decision_function(scaled_features)[0]
                
                if ml_prediction == -1:
                    ml_confidence = min(1.0, abs(ml_score) / 2.0)
                    if ml_confidence > anomaly_result['confidence']:
                        anomaly_result['is_anomaly'] = True
                        anomaly_result['confidence'] = ml_confidence
                        anomaly_result['method'] = 'ml_isolation_forest'
                        anomaly_result['details']['ml_score'] = ml_score
                        
            except Exception as e:
                logging.warning(f"ML anomaly detection failed: {e}")
        
        # Record anomaly if detected
        if anomaly_result['is_anomaly']:
            self.anomaly_history[metric_type].append({
                'timestamp': datetime.now(),
                'value': current_value,
                'confidence': anomaly_result['confidence'],
                'method': anomaly_result['method']
            })
            
            # Keep only recent anomalies
            cutoff = datetime.now() - timedelta(hours=24)
            self.anomaly_history[metric_type] = [
                a for a in self.anomaly_history[metric_type]
                if a['timestamp'] >= cutoff
            ]
        
        return anomaly_result

class TrendAnalyzer:
    """Advanced trend analysis system"""
    
    def __init__(self):
        self.trend_history = defaultdict(list)
        self.trend_models = {}
    
    def analyze_trend(self, metric_type: MetricType, time_series: List[MetricPoint],
                     window_minutes: int = 30) -> PerformanceTrend:
        """Analyze performance trend for a metric"""
        
        if len(time_series) < 3:
            return self._no_trend_result(metric_type, "insufficient_data")
        
        # Sort by timestamp
        sorted_data = sorted(time_series, key=lambda x: x.timestamp)
        values = [p.value for p in sorted_data]
        timestamps = [p.timestamp for p in sorted_data]
        
        # Calculate time deltas in minutes
        start_time = timestamps[0]
        time_deltas = [(ts - start_time).total_seconds() / 60 for ts in timestamps]
        
        # Linear regression for trend analysis
        if len(values) >= 2:
            # Simple linear trend calculation
            n = len(values)
            sum_x = sum(time_deltas)
            sum_y = sum(values)
            sum_xy = sum(x * y for x, y in zip(time_deltas, values))
            sum_x2 = sum(x * x for x in time_deltas)
            
            # Calculate slope (trend direction and strength)
            denominator = n * sum_x2 - sum_x * sum_x
            if abs(denominator) > 0.0001:
                slope = (n * sum_xy - sum_x * sum_y) / denominator
                intercept = (sum_y - slope * sum_x) / n
                
                # Calculate correlation coefficient (trend strength)
                mean_x = sum_x / n
                mean_y = sum_y / n
                numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(time_deltas, values))
                var_x = sum((x - mean_x) ** 2 for x in time_deltas)
                var_y = sum((y - mean_y) ** 2 for y in values)
                
                if var_x > 0 and var_y > 0:
                    correlation = numerator / (var_x * var_y) ** 0.5
                    trend_strength = abs(correlation)
                else:
                    trend_strength = 0.0
                
                # Determine trend direction
                if abs(slope) < 0.001:
                    trend_direction = "stable"
                elif slope > 0:
                    trend_direction = "increasing"
                else:
                    trend_direction = "decreasing"
                
                # Calculate change rate (percentage per minute)
                current_value = values[-1]
                if current_value != 0:
                    change_rate = (slope / abs(current_value)) * 100
                else:
                    change_rate = 0.0
                
                # Statistical significance test (simplified)
                significance = min(1.0, trend_strength * (n / 10.0))
                
                # Forecast next hour (extrapolate trend)
                next_hour_time = time_deltas[-1] + 60  # 60 minutes ahead
                forecast = slope * next_hour_time + intercept
                
                # Confidence interval (simplified)
                std_error = statistics.stdev(values) if len(values) > 1 else 0.0
                confidence_interval = (
                    forecast - 1.96 * std_error,
                    forecast + 1.96 * std_error
                )
                
                return PerformanceTrend(
                    metric_type=metric_type,
                    source=sorted_data[0].source,
                    trend_direction=trend_direction,
                    trend_strength=trend_strength,
                    change_rate=change_rate,
                    significance=significance,
                    forecast_next_hour=forecast,
                    confidence_interval=confidence_interval
                )
        
        return self._no_trend_result(metric_type, "calculation_failed")
    
    def _no_trend_result(self, metric_type: MetricType, reason: str) -> PerformanceTrend:
        """Return a default trend result when analysis fails"""
        
        return PerformanceTrend(
            metric_type=metric_type,
            source="unknown",
            trend_direction="stable",
            trend_strength=0.0,
            change_rate=0.0,
            significance=0.0,
            forecast_next_hour=0.0,
            confidence_interval=(0.0, 0.0)
        )
    
    def detect_performance_degradation(self, trends: List[PerformanceTrend]) -> Dict[str, Any]:
        """Detect if system performance is degrading"""
        
        degradation_indicators = []
        
        for trend in trends:
            # Check for negative trends in key performance metrics
            if trend.metric_type in [MetricType.QUALITY_SCORE, MetricType.SUCCESS_RATE, 
                                   MetricType.COST_EFFICIENCY]:
                if (trend.trend_direction == "decreasing" and 
                    trend.trend_strength > 0.5 and 
                    trend.significance > 0.7):
                    degradation_indicators.append({
                        'metric': trend.metric_type.value,
                        'severity': 'high' if trend.change_rate < -5 else 'medium',
                        'change_rate': trend.change_rate,
                        'forecast': trend.forecast_next_hour
                    })
            
            # Check for positive trends in negative metrics
            elif trend.metric_type in [MetricType.LATENCY, MetricType.ERROR_RATE]:
                if (trend.trend_direction == "increasing" and 
                    trend.trend_strength > 0.5 and 
                    trend.significance > 0.7):
                    degradation_indicators.append({
                        'metric': trend.metric_type.value,
                        'severity': 'high' if trend.change_rate > 10 else 'medium',
                        'change_rate': trend.change_rate,
                        'forecast': trend.forecast_next_hour
                    })
        
        # Calculate overall degradation risk
        if not degradation_indicators:
            risk_level = "low"
            risk_score = 0.0
        else:
            high_severity_count = sum(1 for ind in degradation_indicators if ind['severity'] == 'high')
            risk_score = min(1.0, (len(degradation_indicators) + high_severity_count * 2) / 10.0)
            
            if risk_score > 0.8:
                risk_level = "critical"
            elif risk_score > 0.5:
                risk_level = "high"
            elif risk_score > 0.2:
                risk_level = "medium"
            else:
                risk_level = "low"
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'degradation_indicators': degradation_indicators,
            'recommendation': self._get_degradation_recommendation(risk_level, degradation_indicators)
        }
    
    def _get_degradation_recommendation(self, risk_level: str, indicators: List[Dict]) -> str:
        """Get recommendation based on degradation analysis"""
        
        if risk_level == "critical":
            return "Immediate intervention required - implement emergency scaling and investigate root causes"
        elif risk_level == "high":
            return "Proactive scaling recommended - monitor closely and prepare contingency plans"
        elif risk_level == "medium":
            return "Monitor performance trends - consider optimization if degradation continues"
        else:
            return "Performance stable - continue normal monitoring"

class NotificationManager:
    """Multi-channel notification system"""
    
    def __init__(self):
        self.notification_channels = {}
        self.notification_history = deque(maxlen=1000)
        self.rate_limits = defaultdict(lambda: {'count': 0, 'window_start': datetime.now()})
        
        # Default rate limiting: max 10 notifications per metric per hour
        self.default_rate_limit = {'max_count': 10, 'window_minutes': 60}
    
    def configure_email(self, smtp_server: str, smtp_port: int, username: str, 
                       password: str, from_email: str):
        """Configure email notifications"""
        
        if not NOTIFICATION_AVAILABLE:
            logging.warning("Notification libraries not available")
            return
        
        self.notification_channels['email'] = {
            'type': 'email',
            'smtp_server': smtp_server,
            'smtp_port': smtp_port,
            'username': username,
            'password': password,
            'from_email': from_email,
            'enabled': True
        }
    
    def configure_webhook(self, webhook_url: str, headers: Dict[str, str] = None):
        """Configure webhook notifications"""
        
        if not NOTIFICATION_AVAILABLE:
            logging.warning("Notification libraries not available")
            return
        
        self.notification_channels['webhook'] = {
            'type': 'webhook',
            'url': webhook_url,
            'headers': headers or {},
            'enabled': True
        }
    
    def configure_slack(self, webhook_url: str):
        """Configure Slack notifications"""
        
        if not NOTIFICATION_AVAILABLE:
            logging.warning("Notification libraries not available")
            return
        
        self.notification_channels['slack'] = {
            'type': 'slack',
            'webhook_url': webhook_url,
            'enabled': True
        }
    
    async def send_alert(self, alert: Alert, channels: List[str] = None) -> Dict[str, bool]:
        """Send alert through specified channels"""
        
        channels = channels or list(self.notification_channels.keys())
        results = {}
        
        # Check rate limiting
        rate_limit_key = f"{alert.source}_{alert.metric_type.value}"
        if not self._check_rate_limit(rate_limit_key):
            logging.warning(f"Rate limit exceeded for {rate_limit_key}")
            return {'rate_limited': True}
        
        for channel in channels:
            if channel in self.notification_channels:
                try:
                    success = await self._send_to_channel(alert, channel)
                    results[channel] = success
                    
                    if success:
                        self._update_rate_limit(rate_limit_key)
                        
                except Exception as e:
                    logging.error(f"Failed to send alert to {channel}: {e}")
                    results[channel] = False
        
        # Record notification
        self.notification_history.append({
            'timestamp': datetime.now(),
            'alert_id': alert.id,
            'channels': channels,
            'results': results,
            'severity': alert.severity.value
        })
        
        return results
    
    async def _send_to_channel(self, alert: Alert, channel: str) -> bool:
        """Send alert to specific channel"""
        
        channel_config = self.notification_channels[channel]
        
        if not channel_config.get('enabled', False):
            return False
        
        if channel_config['type'] == 'email':
            return await self._send_email(alert, channel_config)
        elif channel_config['type'] == 'webhook':
            return await self._send_webhook(alert, channel_config)
        elif channel_config['type'] == 'slack':
            return await self._send_slack(alert, channel_config)
        
        return False
    
    async def _send_email(self, alert: Alert, config: Dict) -> bool:
        """Send email notification"""
        
        try:
            msg = MIMEMultipart()
            msg['From'] = config['from_email']
            msg['To'] = config.get('to_email', config['from_email'])
            msg['Subject'] = f"[{alert.severity.value.upper()}] {alert.title}"
            
            body = f"""
Alert: {alert.title}
Severity: {alert.severity.value.upper()}
Source: {alert.source}
Metric: {alert.metric_type.value}
Value: {alert.value}
Threshold: {alert.threshold}
Time: {alert.timestamp.isoformat()}

Description:
{alert.description}

Tags: {alert.tags}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
            server.starttls()
            server.login(config['username'], config['password'])
            
            text = msg.as_string()
            server.sendmail(config['from_email'], config['to_email'], text)
            server.quit()
            
            return True
            
        except Exception as e:
            logging.error(f"Email notification failed: {e}")
            return False
    
    async def _send_webhook(self, alert: Alert, config: Dict) -> bool:
        """Send webhook notification"""
        
        try:
            payload = {
                'alert': asdict(alert),
                'timestamp': alert.timestamp.isoformat(),
                'severity': alert.severity.value,
                'type': 'performance_alert'
            }
            
            response = requests.post(
                config['url'],
                json=payload,
                headers=config.get('headers', {}),
                timeout=10
            )
            
            return response.status_code < 400
            
        except Exception as e:
            logging.error(f"Webhook notification failed: {e}")
            return False
    
    async def _send_slack(self, alert: Alert, config: Dict) -> bool:
        """Send Slack notification"""
        
        try:
            # Slack color coding based on severity
            color_map = {
                AlertSeverity.INFO: 'good',
                AlertSeverity.WARNING: 'warning',
                AlertSeverity.CRITICAL: 'danger',
                AlertSeverity.EMERGENCY: 'danger'
            }
            
            payload = {
                'attachments': [{
                    'color': color_map.get(alert.severity, 'warning'),
                    'title': f"{alert.severity.value.upper()}: {alert.title}",
                    'text': alert.description,
                    'fields': [
                        {'title': 'Source', 'value': alert.source, 'short': True},
                        {'title': 'Metric', 'value': alert.metric_type.value, 'short': True},
                        {'title': 'Value', 'value': str(alert.value), 'short': True},
                        {'title': 'Threshold', 'value': str(alert.threshold), 'short': True}
                    ],
                    'timestamp': int(alert.timestamp.timestamp())
                }]
            }
            
            response = requests.post(
                config['webhook_url'],
                json=payload,
                timeout=10
            )
            
            return response.status_code < 400
            
        except Exception as e:
            logging.error(f"Slack notification failed: {e}")
            return False
    
    def _check_rate_limit(self, key: str) -> bool:
        """Check if rate limit is exceeded"""
        
        now = datetime.now()
        rate_info = self.rate_limits[key]
        
        # Reset window if expired
        if (now - rate_info['window_start']).total_seconds() > (self.default_rate_limit['window_minutes'] * 60):
            rate_info['count'] = 0
            rate_info['window_start'] = now
        
        return rate_info['count'] < self.default_rate_limit['max_count']
    
    def _update_rate_limit(self, key: str):
        """Update rate limit counter"""
        self.rate_limits[key]['count'] += 1

# Continue in next part due to length...