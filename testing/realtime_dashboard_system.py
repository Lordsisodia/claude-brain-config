#!/usr/bin/env python3
"""
REAL-TIME SYSTEM HEALTH DASHBOARD
Advanced visualization and monitoring interface
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import statistics
import numpy as np

# Web dashboard components
try:
    from flask import Flask, render_template, jsonify, request, Response
    from flask_socketio import SocketIO, emit
    import plotly.graph_objects as go
    import plotly.utils
    WEB_AVAILABLE = True
except ImportError:
    print("⚠️  Web dashboard libraries not available. Install with: pip install flask flask-socketio plotly")
    WEB_AVAILABLE = False

@dataclass
class DashboardMetric:
    """Dashboard metric data point"""
    name: str
    current_value: float
    target_value: float
    unit: str
    trend: str  # "up", "down", "stable"
    status: str  # "healthy", "warning", "critical"
    history: List[float]
    timestamp: datetime

@dataclass
class PerformanceHeatmap:
    """Performance heatmap data"""
    agent_id: str
    metric_type: str
    time_window: str
    data_matrix: List[List[float]]
    x_labels: List[str]
    y_labels: List[str]
    color_scale: str

@dataclass
class SystemOverview:
    """System overview dashboard data"""
    total_agents: int
    healthy_agents: int
    active_orchestrations: int
    total_requests_today: int
    average_quality_score: float
    average_latency_ms: float
    current_cost_per_hour: float
    system_uptime: str
    alerts_count: Dict[str, int]

class RealTimeDashboard:
    """Advanced real-time dashboard with interactive visualizations"""
    
    def __init__(self, monitoring_orchestrator=None):
        self.monitoring_orchestrator = monitoring_orchestrator
        self.app = None
        self.socketio = None
        self.dashboard_data = {}
        self.connected_clients = set()
        
        if WEB_AVAILABLE:
            self._initialize_web_app()
    
    def _initialize_web_app(self):
        """Initialize Flask web application"""
        
        self.app = Flask(__name__, template_folder='templates', static_folder='static')
        self.app.config['SECRET_KEY'] = 'monitoring_dashboard_2024'
        self.socketio = SocketIO(self.app, cors_allowed_origins="*", async_mode='threading')
        
        # Register routes
        self._register_routes()
        self._register_socket_events()
    
    def _register_routes(self):
        """Register web routes"""
        
        @self.app.route('/')
        def index():
            return render_template('dashboard.html')
        
        @self.app.route('/api/overview')
        def api_overview():
            return jsonify(self._get_system_overview())
        
        @self.app.route('/api/metrics/<metric_type>')
        def api_metrics(metric_type):
            return jsonify(self._get_metric_data(metric_type))
        
        @self.app.route('/api/agents')
        def api_agents():
            return jsonify(self._get_agent_data())
        
        @self.app.route('/api/heatmap/<agent_id>/<metric_type>')
        def api_heatmap(agent_id, metric_type):
            return jsonify(self._get_heatmap_data(agent_id, metric_type))
        
        @self.app.route('/api/alerts')
        def api_alerts():
            return jsonify(self._get_alerts_data())
        
        @self.app.route('/api/trends')
        def api_trends():
            return jsonify(self._get_trends_data())
        
        @self.app.route('/api/costs')
        def api_costs():
            return jsonify(self._get_cost_data())
        
        @self.app.route('/api/predictions')
        def api_predictions():
            return jsonify(self._get_predictions_data())
    
    def _register_socket_events(self):
        """Register Socket.IO events"""
        
        @self.socketio.on('connect')
        def handle_connect():
            self.connected_clients.add(request.sid)
            emit('connected', {'status': 'Connected to monitoring dashboard'})
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            self.connected_clients.discard(request.sid)
        
        @self.socketio.on('request_update')
        def handle_request_update(data):
            component = data.get('component', 'overview')
            update_data = self._get_component_update(component)
            emit('update_data', {'component': component, 'data': update_data})
    
    def _get_system_overview(self) -> Dict[str, Any]:
        """Get system overview data"""
        
        if not self.monitoring_orchestrator:
            return self._get_demo_overview()
        
        # Get real data from monitoring orchestrator
        agent_pools = self.monitoring_orchestrator.agent_pools
        total_agents = sum(pool.current_instances for pool in agent_pools.values())
        healthy_agents = sum(pool.healthy_instances for pool in agent_pools.values())
        
        # Calculate current metrics
        quality_buffer = self.monitoring_orchestrator.time_series_buffers.get('quality_score')
        latency_buffer = self.monitoring_orchestrator.time_series_buffers.get('latency')
        
        avg_quality = 0.8  # Default
        avg_latency = 2000  # Default
        
        if quality_buffer:
            recent_quality = quality_buffer.get_recent(minutes=5)
            if recent_quality:
                avg_quality = statistics.mean([p.value for p in recent_quality])
        
        if latency_buffer:
            recent_latency = latency_buffer.get_recent(minutes=5)
            if recent_latency:
                avg_latency = statistics.mean([p.value for p in recent_latency])
        
        # Calculate costs
        current_cost_per_hour = sum(
            pool.current_instances * pool.cost_per_instance * 3600  # Convert to hourly
            for pool in agent_pools.values()
        )
        
        uptime = datetime.now() - self.monitoring_orchestrator.uptime_start
        uptime_str = f"{uptime.days}d {uptime.seconds // 3600}h {(uptime.seconds % 3600) // 60}m"
        
        # Alert counts
        active_alerts = self.monitoring_orchestrator.active_alerts
        alert_counts = {
            'critical': sum(1 for alert in active_alerts.values() if alert.severity.value == 'critical'),
            'warning': sum(1 for alert in active_alerts.values() if alert.severity.value == 'warning'),
            'info': sum(1 for alert in active_alerts.values() if alert.severity.value == 'info')
        }
        
        return {
            'total_agents': total_agents,
            'healthy_agents': healthy_agents,
            'active_orchestrations': len(self.monitoring_orchestrator.scaling_history),
            'total_requests_today': self.monitoring_orchestrator.total_metrics_collected,
            'average_quality_score': round(avg_quality, 3),
            'average_latency_ms': round(avg_latency, 1),
            'current_cost_per_hour': round(current_cost_per_hour, 4),
            'system_uptime': uptime_str,
            'alerts_count': alert_counts,
            'system_status': self.monitoring_orchestrator.system_status.value,
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_demo_overview(self) -> Dict[str, Any]:
        """Get demo system overview data"""
        
        return {
            'total_agents': 8,
            'healthy_agents': 7,
            'active_orchestrations': 15,
            'total_requests_today': 2847,
            'average_quality_score': 0.847,
            'average_latency_ms': 1852.3,
            'current_cost_per_hour': 0.0234,
            'system_uptime': "2d 14h 32m",
            'alerts_count': {'critical': 0, 'warning': 2, 'info': 5},
            'system_status': 'healthy',
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_metric_data(self, metric_type: str) -> Dict[str, Any]:
        """Get time series data for a specific metric"""
        
        if self.monitoring_orchestrator and metric_type in self.monitoring_orchestrator.time_series_buffers:
            buffer = self.monitoring_orchestrator.time_series_buffers[metric_type]
            recent_data = buffer.get_recent(minutes=30)
            
            if recent_data:
                times = [p.timestamp.isoformat() for p in recent_data]
                values = [p.value for p in recent_data]
                
                return {
                    'metric_type': metric_type,
                    'timestamps': times,
                    'values': values,
                    'current_value': values[-1] if values else 0,
                    'min_value': min(values) if values else 0,
                    'max_value': max(values) if values else 0,
                    'avg_value': statistics.mean(values) if values else 0,
                    'trend': self._calculate_trend(values) if len(values) > 2 else 'stable'
                }
        
        # Return demo data
        return self._get_demo_metric_data(metric_type)
    
    def _get_demo_metric_data(self, metric_type: str) -> Dict[str, Any]:
        """Get demo metric data"""
        
        now = datetime.now()
        times = [(now - timedelta(minutes=i)).isoformat() for i in range(30, 0, -1)]
        
        if metric_type == 'quality_score':
            values = [0.8 + 0.15 * np.sin(i/5) + np.random.normal(0, 0.02) for i in range(30)]
        elif metric_type == 'latency':
            values = [2000 + 1000 * np.sin(i/3) + np.random.normal(0, 100) for i in range(30)]
        elif metric_type == 'error_rate':
            values = [0.05 + 0.03 * np.sin(i/4) + abs(np.random.normal(0, 0.01)) for i in range(30)]
        else:
            values = [0.5 + 0.3 * np.sin(i/5) + np.random.normal(0, 0.05) for i in range(30)]
        
        return {
            'metric_type': metric_type,
            'timestamps': times,
            'values': values,
            'current_value': values[-1],
            'min_value': min(values),
            'max_value': max(values),
            'avg_value': statistics.mean(values),
            'trend': self._calculate_trend(values)
        }
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction from values"""
        
        if len(values) < 3:
            return 'stable'
        
        # Simple trend calculation
        recent_avg = statistics.mean(values[-5:])
        earlier_avg = statistics.mean(values[-10:-5])
        
        diff_threshold = 0.05  # 5% change threshold
        
        if recent_avg > earlier_avg * (1 + diff_threshold):
            return 'up'
        elif recent_avg < earlier_avg * (1 - diff_threshold):
            return 'down'
        else:
            return 'stable'
    
    def _get_agent_data(self) -> Dict[str, Any]:
        """Get agent performance data"""
        
        if self.monitoring_orchestrator:
            agent_data = {}
            
            for agent_type, pool in self.monitoring_orchestrator.agent_pools.items():
                # Get load balancer stats for this agent
                lb_stats = self.monitoring_orchestrator.load_balancer.get_load_balancer_stats()
                agent_lb_stats = lb_stats.get('agent_stats', {}).get(agent_type, {})
                
                agent_data[agent_type] = {
                    'current_instances': pool.current_instances,
                    'target_instances': pool.target_instances,
                    'max_instances': pool.max_instances,
                    'state': pool.state.value,
                    'average_load': pool.average_load,
                    'average_latency': pool.average_latency,
                    'error_rate': pool.error_rate,
                    'success_rate': pool.success_rate,
                    'cost_per_instance': pool.cost_per_instance,
                    'total_cost_hour': pool.total_cost_hour,
                    'health_status': agent_lb_stats.get('health_status', {}),
                    'quality_score': agent_lb_stats.get('quality_score', 0.8),
                    'last_scaled': pool.last_scaled.isoformat()
                }
            
            return agent_data
        
        # Return demo data
        return self._get_demo_agent_data()
    
    def _get_demo_agent_data(self) -> Dict[str, Any]:
        """Get demo agent data"""
        
        return {
            'cerebras_ultra': {
                'current_instances': 3,
                'target_instances': 3,
                'max_instances': 8,
                'state': 'healthy',
                'average_load': 0.65,
                'average_latency': 1200,
                'error_rate': 0.02,
                'success_rate': 0.98,
                'cost_per_instance': 0.001,
                'total_cost_hour': 0.0108,
                'quality_score': 0.92,
                'last_scaled': datetime.now().isoformat()
            },
            'gemini_flash': {
                'current_instances': 2,
                'target_instances': 2,
                'max_instances': 6,
                'state': 'healthy',
                'average_load': 0.45,
                'average_latency': 800,
                'error_rate': 0.01,
                'success_rate': 0.99,
                'cost_per_instance': 0.0008,
                'total_cost_hour': 0.00576,
                'quality_score': 0.94,
                'last_scaled': datetime.now().isoformat()
            },
            'groq_lightning': {
                'current_instances': 2,
                'target_instances': 3,
                'max_instances': 10,
                'state': 'scaling',
                'average_load': 0.78,
                'average_latency': 600,
                'error_rate': 0.03,
                'success_rate': 0.97,
                'cost_per_instance': 0.0005,
                'total_cost_hour': 0.0036,
                'quality_score': 0.89,
                'last_scaled': (datetime.now() - timedelta(minutes=2)).isoformat()
            },
            'scaleway_eu': {
                'current_instances': 1,
                'target_instances': 1,
                'max_instances': 4,
                'state': 'healthy',
                'average_load': 0.35,
                'average_latency': 1500,
                'error_rate': 0.01,
                'success_rate': 0.99,
                'cost_per_instance': 0.0012,
                'total_cost_hour': 0.00432,
                'quality_score': 0.91,
                'last_scaled': (datetime.now() - timedelta(hours=2)).isoformat()
            }
        }
    
    def _get_heatmap_data(self, agent_id: str, metric_type: str) -> Dict[str, Any]:
        """Get performance heatmap data"""
        
        # Generate demo heatmap data (24 hours x 7 days)
        hours = list(range(24))
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        # Generate synthetic heatmap data
        data_matrix = []
        for day in range(7):
            day_data = []
            for hour in range(24):
                # Simulate different load patterns
                base_value = 0.3 + 0.4 * np.sin((hour - 6) * np.pi / 12)  # Daily cycle
                weekend_factor = 0.7 if day in [5, 6] else 1.0  # Weekend reduction
                noise = np.random.normal(0, 0.05)
                value = max(0, min(1, base_value * weekend_factor + noise))
                day_data.append(round(value, 3))
            data_matrix.append(day_data)
        
        return {
            'agent_id': agent_id,
            'metric_type': metric_type,
            'time_window': '7_days',
            'data_matrix': data_matrix,
            'x_labels': [f"{h:02d}:00" for h in hours],
            'y_labels': days,
            'color_scale': 'RdYlBu_r',
            'title': f'{metric_type.replace("_", " ").title()} - {agent_id}',
            'min_value': 0,
            'max_value': 1
        }
    
    def _get_alerts_data(self) -> Dict[str, Any]:
        """Get alerts data"""
        
        if self.monitoring_orchestrator:
            active_alerts = list(self.monitoring_orchestrator.active_alerts.values())
            
            alerts_data = []
            for alert in active_alerts[-20:]:  # Last 20 alerts
                alerts_data.append({
                    'id': alert.id,
                    'severity': alert.severity.value,
                    'title': alert.title,
                    'description': alert.description,
                    'source': alert.source,
                    'metric_type': alert.metric_type.value,
                    'timestamp': alert.timestamp.isoformat(),
                    'value': alert.value,
                    'threshold': alert.threshold,
                    'acknowledged': alert.acknowledged,
                    'resolved': alert.resolved,
                    'tags': alert.tags
                })
            
            return {
                'alerts': alerts_data,
                'total_active': len(active_alerts),
                'counts_by_severity': {
                    'critical': sum(1 for a in active_alerts if a.severity.value == 'critical'),
                    'warning': sum(1 for a in active_alerts if a.severity.value == 'warning'),
                    'info': sum(1 for a in active_alerts if a.severity.value == 'info')
                }
            }
        
        # Return demo alerts
        return self._get_demo_alerts_data()
    
    def _get_demo_alerts_data(self) -> Dict[str, Any]:
        """Get demo alerts data"""
        
        demo_alerts = [
            {
                'id': 'alert_001',
                'severity': 'warning',
                'title': 'High Latency Detected',
                'description': 'Average latency exceeded 5000ms threshold',
                'source': 'cerebras_ultra',
                'metric_type': 'latency',
                'timestamp': (datetime.now() - timedelta(minutes=15)).isoformat(),
                'value': 5234.2,
                'threshold': 5000.0,
                'acknowledged': False,
                'resolved': False,
                'tags': {'auto_generated': 'true', 'component': 'agent_pool'}
            },
            {
                'id': 'alert_002',
                'severity': 'info',
                'title': 'Agent Pool Scaled Up',
                'description': 'groq_lightning pool scaled from 2 to 3 instances',
                'source': 'scaling_engine',
                'metric_type': 'agent_load',
                'timestamp': (datetime.now() - timedelta(minutes=5)).isoformat(),
                'value': 0.85,
                'threshold': 0.8,
                'acknowledged': True,
                'resolved': True,
                'tags': {'scaling_action': 'scale_up', 'trigger': 'load_threshold'}
            }
        ]
        
        return {
            'alerts': demo_alerts,
            'total_active': 2,
            'counts_by_severity': {
                'critical': 0,
                'warning': 1,
                'info': 1
            }
        }
    
    def _get_trends_data(self) -> Dict[str, Any]:
        """Get trend analysis data"""
        
        return {
            'quality_trend': {
                'direction': 'stable',
                'strength': 0.3,
                'forecast': 0.84,
                'confidence': 0.82
            },
            'latency_trend': {
                'direction': 'decreasing',
                'strength': 0.6,
                'forecast': 1800,
                'confidence': 0.75
            },
            'cost_trend': {
                'direction': 'increasing',
                'strength': 0.4,
                'forecast': 0.025,
                'confidence': 0.68
            },
            'error_rate_trend': {
                'direction': 'stable',
                'strength': 0.2,
                'forecast': 0.03,
                'confidence': 0.71
            }
        }
    
    def _get_cost_data(self) -> Dict[str, Any]:
        """Get cost analysis data"""
        
        # Generate hourly cost data for the last 24 hours
        now = datetime.now()
        hourly_data = []
        
        for i in range(24):
            timestamp = now - timedelta(hours=23-i)
            # Simulate cost variations throughout the day
            base_cost = 0.02
            daily_variation = 0.01 * np.sin((i - 6) * np.pi / 12)
            random_variation = np.random.normal(0, 0.002)
            cost = max(0, base_cost + daily_variation + random_variation)
            
            hourly_data.append({
                'timestamp': timestamp.isoformat(),
                'cost': round(cost, 4),
                'requests': int(100 + 50 * np.sin(i * np.pi / 12) + np.random.normal(0, 10))
            })
        
        total_cost_today = sum(h['cost'] for h in hourly_data)
        total_requests_today = sum(h['requests'] for h in hourly_data)
        
        return {
            'hourly_data': hourly_data,
            'total_cost_today': round(total_cost_today, 4),
            'total_requests_today': total_requests_today,
            'cost_per_request': round(total_cost_today / max(total_requests_today, 1), 6),
            'budget_utilization': round(total_cost_today / 10.0, 3),  # Assuming $10 daily budget
            'projected_monthly_cost': round(total_cost_today * 30, 2),
            'cost_efficiency_score': 0.87
        }
    
    def _get_predictions_data(self) -> Dict[str, Any]:
        """Get predictive analytics data"""
        
        return {
            'next_hour_predictions': {
                'quality_score': {'value': 0.82, 'confidence': 0.85},
                'latency': {'value': 2100, 'confidence': 0.78},
                'cost': {'value': 0.023, 'confidence': 0.72},
                'agent_load': {'value': 0.68, 'confidence': 0.81}
            },
            'scaling_recommendations': [
                {
                    'agent_type': 'groq_lightning',
                    'action': 'scale_up',
                    'recommended_instances': 3,
                    'reason': 'Predicted load increase in next 30 minutes',
                    'confidence': 0.74
                }
            ],
            'performance_forecast': {
                'quality_trajectory': 'stable_with_slight_improvement',
                'latency_trajectory': 'decreasing',
                'cost_trajectory': 'stable',
                'reliability_score': 0.91
            },
            'maintenance_windows': [
                {
                    'component': 'cerebras_ultra_pool',
                    'predicted_maintenance_time': (datetime.now() + timedelta(hours=72)).isoformat(),
                    'confidence': 0.65,
                    'recommended_action': 'proactive_scaling'
                }
            ]
        }
    
    def _get_component_update(self, component: str) -> Dict[str, Any]:
        """Get real-time update for a specific component"""
        
        if component == 'overview':
            return self._get_system_overview()
        elif component == 'agents':
            return self._get_agent_data()
        elif component == 'alerts':
            return self._get_alerts_data()
        elif component == 'trends':
            return self._get_trends_data()
        elif component == 'costs':
            return self._get_cost_data()
        elif component == 'predictions':
            return self._get_predictions_data()
        else:
            return {}
    
    async def start_real_time_updates(self):
        """Start real-time data updates to connected clients"""
        
        if not WEB_AVAILABLE:
            print("⚠️  Web dashboard not available")
            return
        
        print("📱 Starting real-time dashboard updates...")
        
        while True:
            try:
                if self.connected_clients:
                    # Send updates to all connected clients
                    overview_data = self._get_system_overview()
                    self.socketio.emit('overview_update', overview_data, broadcast=True)
                    
                    # Send metric updates every 5 seconds
                    if int(time.time()) % 5 == 0:
                        agents_data = self._get_agent_data()
                        self.socketio.emit('agents_update', agents_data, broadcast=True)
                    
                    # Send alerts updates every 10 seconds
                    if int(time.time()) % 10 == 0:
                        alerts_data = self._get_alerts_data()
                        self.socketio.emit('alerts_update', alerts_data, broadcast=True)
                
                await asyncio.sleep(1)  # Update every second
                
            except Exception as e:
                print(f"Dashboard update error: {e}")
                await asyncio.sleep(5)
    
    def run_dashboard(self, host='0.0.0.0', port=5000, debug=False):
        """Run the dashboard web server"""
        
        if not WEB_AVAILABLE:
            print("⚠️  Web dashboard libraries not available")
            return
        
        print(f"🌐 STARTING REAL-TIME DASHBOARD SERVER")
        print(f"   📍 URL: http://{host}:{port}")
        print(f"   🔧 Debug mode: {debug}")
        print()
        
        # Start real-time updates in background
        asyncio.create_task(self.start_real_time_updates())
        
        # Run Flask application
        self.socketio.run(self.app, host=host, port=port, debug=debug)

# Dashboard HTML template (simplified version)
DASHBOARD_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Coordination Platform - Real-Time Dashboard</title>
    <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .metric-card { margin-bottom: 20px; }
        .alert-card { margin-bottom: 10px; }
        .status-healthy { color: #28a745; }
        .status-warning { color: #ffc107; }
        .status-critical { color: #dc3545; }
        .trend-up { color: #28a745; }
        .trend-down { color: #dc3545; }
        .trend-stable { color: #6c757d; }
        .dashboard-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="row dashboard-header text-white p-4 mb-4">
            <div class="col">
                <h1>🤖 AI Coordination Platform - Performance Dashboard</h1>
                <p>Real-time monitoring and adaptive scaling system</p>
            </div>
        </div>
        
        <!-- System Overview -->
        <div class="row mb-4" id="overview-section">
            <div class="col-md-3">
                <div class="card metric-card">
                    <div class="card-body text-center">
                        <h5 class="card-title">Total Agents</h5>
                        <h2 id="total-agents">-</h2>
                        <small class="text-muted">Active instances</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card metric-card">
                    <div class="card-body text-center">
                        <h5 class="card-title">Quality Score</h5>
                        <h2 id="quality-score">-</h2>
                        <small class="text-muted">Average quality</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card metric-card">
                    <div class="card-body text-center">
                        <h5 class="card-title">Avg Latency</h5>
                        <h2 id="avg-latency">-</h2>
                        <small class="text-muted">milliseconds</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card metric-card">
                    <div class="card-body text-center">
                        <h5 class="card-title">Cost/Hour</h5>
                        <h2 id="cost-hour">-</h2>
                        <small class="text-muted">USD</small>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Charts Row -->
        <div class="row mb-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>Performance Metrics</h5>
                    </div>
                    <div class="card-body">
                        <div id="performance-chart"></div>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>Agent Load Distribution</h5>
                    </div>
                    <div class="card-body">
                        <div id="agent-chart"></div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Alerts and Agents Row -->
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>Recent Alerts</h5>
                    </div>
                    <div class="card-body" id="alerts-container">
                        <!-- Alerts will be populated here -->
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>Agent Status</h5>
                    </div>
                    <div class="card-body" id="agents-container">
                        <!-- Agent status will be populated here -->
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Initialize Socket.IO connection
        const socket = io();
        
        socket.on('connect', function() {
            console.log('Connected to dashboard');
            loadInitialData();
        });
        
        socket.on('overview_update', function(data) {
            updateOverview(data);
        });
        
        socket.on('agents_update', function(data) {
            updateAgents(data);
        });
        
        socket.on('alerts_update', function(data) {
            updateAlerts(data);
        });
        
        function loadInitialData() {
            fetch('/api/overview')
                .then(response => response.json())
                .then(data => updateOverview(data));
            
            fetch('/api/agents')
                .then(response => response.json())
                .then(data => updateAgents(data));
            
            fetch('/api/alerts')
                .then(response => response.json())
                .then(data => updateAlerts(data));
        }
        
        function updateOverview(data) {
            document.getElementById('total-agents').textContent = data.total_agents;
            document.getElementById('quality-score').textContent = data.average_quality_score.toFixed(3);
            document.getElementById('avg-latency').textContent = data.average_latency_ms.toFixed(1) + 'ms';
            document.getElementById('cost-hour').textContent = '$' + data.current_cost_per_hour.toFixed(4);
        }
        
        function updateAgents(data) {
            const container = document.getElementById('agents-container');
            container.innerHTML = '';
            
            Object.entries(data).forEach(([agentId, agentData]) => {
                const statusClass = agentData.state === 'healthy' ? 'status-healthy' : 
                                  agentData.state === 'degraded' ? 'status-warning' : 'status-critical';
                
                const html = `
                    <div class="mb-2">
                        <div class="d-flex justify-content-between">
                            <strong>${agentId}</strong>
                            <span class="${statusClass}">${agentData.state}</span>
                        </div>
                        <div class="progress mb-1" style="height: 5px;">
                            <div class="progress-bar" style="width: ${agentData.average_load * 100}%"></div>
                        </div>
                        <small class="text-muted">
                            Instances: ${agentData.current_instances}/${agentData.max_instances} | 
                            Load: ${(agentData.average_load * 100).toFixed(1)}% | 
                            Quality: ${agentData.quality_score.toFixed(2)}
                        </small>
                    </div>
                `;
                container.innerHTML += html;
            });
        }
        
        function updateAlerts(data) {
            const container = document.getElementById('alerts-container');
            container.innerHTML = '';
            
            if (data.alerts.length === 0) {
                container.innerHTML = '<p class="text-muted">No active alerts</p>';
                return;
            }
            
            data.alerts.forEach(alert => {
                const severityClass = alert.severity === 'critical' ? 'border-danger' : 
                                    alert.severity === 'warning' ? 'border-warning' : 'border-info';
                
                const html = `
                    <div class="alert-card border ${severityClass} p-2 mb-2 rounded">
                        <div class="d-flex justify-content-between">
                            <strong>${alert.title}</strong>
                            <small class="text-muted">${new Date(alert.timestamp).toLocaleTimeString()}</small>
                        </div>
                        <p class="mb-1 small">${alert.description}</p>
                        <small class="text-muted">Source: ${alert.source} | Value: ${alert.value}</small>
                    </div>
                `;
                container.innerHTML += html;
            });
        }
        
        // Initialize charts
        function initializeCharts() {
            // Performance chart
            const performanceData = {
                x: [],
                y: [],
                type: 'scatter',
                mode: 'lines+markers',
                name: 'Quality Score'
            };
            
            Plotly.newPlot('performance-chart', [performanceData], {
                title: 'Quality Score Over Time',
                xaxis: { title: 'Time' },
                yaxis: { title: 'Quality Score' }
            });
            
            // Agent load chart
            const agentData = {
                x: ['cerebras_ultra', 'gemini_flash', 'groq_lightning', 'scaleway_eu'],
                y: [0.65, 0.45, 0.78, 0.35],
                type: 'bar',
                name: 'Load'
            };
            
            Plotly.newPlot('agent-chart', [agentData], {
                title: 'Agent Load Distribution',
                xaxis: { title: 'Agent' },
                yaxis: { title: 'Load %' }
            });
        }
        
        // Initialize charts when page loads
        window.onload = function() {
            initializeCharts();
        };
    </script>
</body>
</html>
"""