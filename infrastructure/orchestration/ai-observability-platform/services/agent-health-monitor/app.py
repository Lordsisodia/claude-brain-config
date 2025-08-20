import asyncio
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import redis
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import uvicorn
import psutil
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenTelemetry
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

metrics.set_meter_provider(MeterProvider())
meter = metrics.get_meter(__name__)

# Initialize FastAPI
app = FastAPI(title="AI Agent Health Monitor", version="1.0.0")
FastAPIInstrumentor.instrument_app(app)

# Redis connection
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

# Prometheus metrics
agent_health_score = Gauge('ai_agent_health_score', 'Health score of AI agents', ['agent_id', 'model', 'type'])
agent_response_time = Histogram('ai_agent_response_time_seconds', 'Response time of AI agents', ['agent_id', 'operation'])
agent_requests_total = Counter('ai_agent_requests_total', 'Total requests processed by AI agents', ['agent_id', 'status'])
agent_memory_usage = Gauge('ai_agent_memory_usage_bytes', 'Memory usage of AI agents', ['agent_id'])
agent_cpu_usage = Gauge('ai_agent_cpu_usage_percent', 'CPU usage of AI agents', ['agent_id'])
agent_inference_latency = Histogram('ai_agent_inference_latency_seconds', 'Inference latency', ['agent_id', 'model'])
agent_token_usage = Counter('ai_agent_tokens_total', 'Total tokens processed', ['agent_id', 'token_type'])
agent_error_rate = Gauge('ai_agent_error_rate', 'Error rate of AI agents', ['agent_id'])
agent_queue_length = Gauge('ai_agent_queue_length', 'Queue length for AI agents', ['agent_id'])
agent_intelligence_score = Gauge('ai_agent_intelligence_score', 'Intelligence score based on performance', ['agent_id'])

# Data models
class AgentMetrics(BaseModel):
    agent_id: str
    model_name: str
    agent_type: str
    health_score: float
    response_time: float
    memory_usage: int
    cpu_usage: float
    error_count: int
    success_count: int
    queue_length: int
    last_activity: datetime
    intelligence_metrics: Dict[str, float]

class AgentStatus(BaseModel):
    agent_id: str
    status: str
    last_heartbeat: datetime
    metadata: Dict[str, any]

class HealthMonitor:
    def __init__(self):
        self.agents: Dict[str, AgentMetrics] = {}
        self.health_thresholds = {
            'response_time': 5.0,  # seconds
            'error_rate': 0.05,    # 5%
            'memory_usage': 1024 * 1024 * 1024,  # 1GB
            'cpu_usage': 80.0,     # 80%
        }
        
    async def register_agent(self, agent_id: str, metadata: Dict[str, any]):
        """Register a new AI agent for monitoring"""
        with tracer.start_as_current_span("register_agent") as span:
            span.set_attribute("agent_id", agent_id)
            
            agent_data = {
                'agent_id': agent_id,
                'model_name': metadata.get('model_name', 'unknown'),
                'agent_type': metadata.get('type', 'general'),
                'health_score': 1.0,
                'response_time': 0.0,
                'memory_usage': 0,
                'cpu_usage': 0.0,
                'error_count': 0,
                'success_count': 0,
                'queue_length': 0,
                'last_activity': datetime.now(),
                'intelligence_metrics': {
                    'accuracy': 0.0,
                    'coherence': 0.0,
                    'efficiency': 0.0,
                    'adaptability': 0.0
                }
            }
            
            # Store in Redis for persistence
            await self._store_agent_data(agent_id, agent_data)
            
            # Update Prometheus metrics
            agent_health_score.labels(
                agent_id=agent_id,
                model=agent_data['model_name'],
                type=agent_data['agent_type']
            ).set(1.0)
            
            logger.info(f"Registered agent {agent_id} with model {agent_data['model_name']}")
            return agent_data

    async def update_agent_metrics(self, agent_id: str, metrics: Dict[str, any]):
        """Update metrics for an AI agent"""
        with tracer.start_as_current_span("update_agent_metrics") as span:
            span.set_attribute("agent_id", agent_id)
            
            # Get existing agent data
            agent_data = await self._get_agent_data(agent_id)
            if not agent_data:
                raise HTTPException(status_code=404, f"Agent {agent_id} not found")
            
            # Update metrics
            agent_data.update({
                'response_time': metrics.get('response_time', agent_data['response_time']),
                'memory_usage': metrics.get('memory_usage', agent_data['memory_usage']),
                'cpu_usage': metrics.get('cpu_usage', agent_data['cpu_usage']),
                'error_count': metrics.get('error_count', agent_data['error_count']),
                'success_count': metrics.get('success_count', agent_data['success_count']),
                'queue_length': metrics.get('queue_length', agent_data['queue_length']),
                'last_activity': datetime.now(),
            })
            
            # Update intelligence metrics if provided
            if 'intelligence_metrics' in metrics:
                agent_data['intelligence_metrics'].update(metrics['intelligence_metrics'])
            
            # Calculate health score
            health_score = await self._calculate_health_score(agent_data)
            agent_data['health_score'] = health_score
            
            # Store updated data
            await self._store_agent_data(agent_id, agent_data)
            
            # Update Prometheus metrics
            self._update_prometheus_metrics(agent_data)
            
            return agent_data

    async def _calculate_health_score(self, agent_data: Dict[str, any]) -> float:
        """Calculate health score based on multiple factors"""
        scores = []
        
        # Response time score (lower is better)
        response_time_score = max(0, 1 - (agent_data['response_time'] / self.health_thresholds['response_time']))
        scores.append(response_time_score)
        
        # Error rate score
        total_requests = agent_data['error_count'] + agent_data['success_count']
        if total_requests > 0:
            error_rate = agent_data['error_count'] / total_requests
            error_rate_score = max(0, 1 - (error_rate / self.health_thresholds['error_rate']))
        else:
            error_rate_score = 1.0
        scores.append(error_rate_score)
        
        # Resource usage scores
        memory_score = max(0, 1 - (agent_data['memory_usage'] / self.health_thresholds['memory_usage']))
        cpu_score = max(0, 1 - (agent_data['cpu_usage'] / self.health_thresholds['cpu_usage']))
        scores.append(memory_score)
        scores.append(cpu_score)
        
        # Intelligence metrics score
        intelligence_score = np.mean(list(agent_data['intelligence_metrics'].values())) if agent_data['intelligence_metrics'] else 0.5
        scores.append(intelligence_score)
        
        # Calculate weighted average
        weights = [0.3, 0.3, 0.15, 0.15, 0.1]  # Prioritize response time and error rate
        health_score = np.average(scores, weights=weights)
        
        return float(health_score)

    def _update_prometheus_metrics(self, agent_data: Dict[str, any]):
        """Update all Prometheus metrics for an agent"""
        agent_id = agent_data['agent_id']
        
        agent_health_score.labels(
            agent_id=agent_id,
            model=agent_data['model_name'],
            type=agent_data['agent_type']
        ).set(agent_data['health_score'])
        
        agent_memory_usage.labels(agent_id=agent_id).set(agent_data['memory_usage'])
        agent_cpu_usage.labels(agent_id=agent_id).set(agent_data['cpu_usage'])
        agent_queue_length.labels(agent_id=agent_id).set(agent_data['queue_length'])
        
        # Calculate and set error rate
        total_requests = agent_data['error_count'] + agent_data['success_count']
        if total_requests > 0:
            error_rate = agent_data['error_count'] / total_requests
            agent_error_rate.labels(agent_id=agent_id).set(error_rate)
        
        # Set intelligence score
        intelligence_score = np.mean(list(agent_data['intelligence_metrics'].values())) if agent_data['intelligence_metrics'] else 0.0
        agent_intelligence_score.labels(agent_id=agent_id).set(intelligence_score)

    async def _store_agent_data(self, agent_id: str, data: Dict[str, any]):
        """Store agent data in Redis"""
        # Convert datetime to ISO string for JSON serialization
        if isinstance(data.get('last_activity'), datetime):
            data['last_activity'] = data['last_activity'].isoformat()
        
        redis_client.hset('agents', agent_id, json.dumps(data))
        
        # Store recent metrics for trend analysis
        timestamp = int(time.time())
        metrics_key = f"agent_metrics:{agent_id}"
        redis_client.zadd(metrics_key, {json.dumps({
            'timestamp': timestamp,
            'health_score': data['health_score'],
            'response_time': data['response_time'],
            'error_rate': data['error_count'] / max(1, data['error_count'] + data['success_count'])
        }): timestamp})
        
        # Keep only last 1000 data points
        redis_client.zremrangebyrank(metrics_key, 0, -1001)

    async def _get_agent_data(self, agent_id: str) -> Optional[Dict[str, any]]:
        """Get agent data from Redis"""
        data = redis_client.hget('agents', agent_id)
        if data:
            parsed_data = json.loads(data)
            # Convert ISO string back to datetime
            if 'last_activity' in parsed_data:
                parsed_data['last_activity'] = datetime.fromisoformat(parsed_data['last_activity'])
            return parsed_data
        return None

    async def get_all_agents(self) -> List[Dict[str, any]]:
        """Get all registered agents"""
        agent_data = redis_client.hgetall('agents')
        agents = []
        for agent_id, data in agent_data.items():
            parsed_data = json.loads(data)
            if 'last_activity' in parsed_data:
                parsed_data['last_activity'] = datetime.fromisoformat(parsed_data['last_activity'])
            agents.append(parsed_data)
        return agents

    async def get_agent_trends(self, agent_id: str, hours: int = 24) -> List[Dict[str, any]]:
        """Get agent performance trends"""
        since_timestamp = int(time.time()) - (hours * 3600)
        metrics_key = f"agent_metrics:{agent_id}"
        
        trend_data = redis_client.zrangebyscore(
            metrics_key, since_timestamp, '+inf', withscores=True
        )
        
        trends = []
        for data, timestamp in trend_data:
            metrics = json.loads(data)
            trends.append(metrics)
        
        return trends

# Initialize health monitor
health_monitor = HealthMonitor()

# API endpoints
@app.post("/agents/{agent_id}/register")
async def register_agent(agent_id: str, metadata: Dict[str, any]):
    """Register a new AI agent"""
    return await health_monitor.register_agent(agent_id, metadata)

@app.post("/agents/{agent_id}/metrics")
async def update_metrics(agent_id: str, metrics: Dict[str, any]):
    """Update metrics for an AI agent"""
    return await health_monitor.update_agent_metrics(agent_id, metrics)

@app.get("/agents")
async def get_agents():
    """Get all registered agents"""
    return await health_monitor.get_all_agents()

@app.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Get specific agent data"""
    agent_data = await health_monitor._get_agent_data(agent_id)
    if not agent_data:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent_data

@app.get("/agents/{agent_id}/trends")
async def get_agent_trends(agent_id: str, hours: int = 24):
    """Get agent performance trends"""
    return await health_monitor.get_agent_trends(agent_id, hours)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Background task to clean up stale agents
async def cleanup_stale_agents():
    """Remove agents that haven't reported in for too long"""
    while True:
        try:
            cutoff_time = datetime.now() - timedelta(hours=1)
            agents = await health_monitor.get_all_agents()
            
            for agent in agents:
                if agent['last_activity'] < cutoff_time:
                    logger.warning(f"Agent {agent['agent_id']} appears stale, last activity: {agent['last_activity']}")
                    # Mark as unhealthy but don't remove completely
                    agent_health_score.labels(
                        agent_id=agent['agent_id'],
                        model=agent['model_name'],
                        type=agent['agent_type']
                    ).set(0.0)
            
            await asyncio.sleep(300)  # Check every 5 minutes
        except Exception as e:
            logger.error(f"Error in cleanup task: {e}")
            await asyncio.sleep(300)

@app.on_event("startup")
async def startup_event():
    """Start background tasks"""
    asyncio.create_task(cleanup_stale_agents())
    logger.info("AI Agent Health Monitor started")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)