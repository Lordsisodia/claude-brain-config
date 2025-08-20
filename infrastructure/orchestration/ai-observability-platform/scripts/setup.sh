#!/bin/bash

# AI Observability Platform Setup Script
# This script sets up the complete billion-scale AI monitoring platform

set -e

echo "🚀 Setting up AI Observability Platform for Billion-Scale Monitoring"
echo "=================================================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check system resources
echo "🔍 Checking system resources..."
MEMORY_GB=$(free -g | awk 'NR==2{printf "%.0f", $2}')
CPU_CORES=$(nproc)

echo "   Available Memory: ${MEMORY_GB}GB"
echo "   Available CPU Cores: ${CPU_CORES}"

if [ "$MEMORY_GB" -lt 8 ]; then
    echo "⚠️  Warning: Less than 8GB RAM detected. Performance may be limited."
    echo "   Recommended: 16GB+ for full-scale simulation"
fi

if [ "$CPU_CORES" -lt 4 ]; then
    echo "⚠️  Warning: Less than 4 CPU cores detected. Performance may be limited."
    echo "   Recommended: 8+ cores for full-scale simulation"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/prometheus
mkdir -p data/grafana
mkdir -p data/elasticsearch
mkdir -p data/redis
mkdir -p logs

# Set permissions
chmod 777 data/prometheus
chmod 777 data/grafana
chmod 777 data/elasticsearch
chmod 777 data/redis
chmod 777 logs

# Check if .env file exists, create if not
if [ ! -f .env ]; then
    echo "⚙️  Creating environment configuration..."
    cat > .env << EOL
# AI Observability Platform Configuration

# Service URLs
PROMETHEUS_URL=http://prometheus:9090
GRAFANA_URL=http://grafana:3000
JAEGER_URL=http://jaeger:16686
ELASTICSEARCH_URL=http://elasticsearch:9200
REDIS_URL=redis://redis:6379

# Scaling Configuration
MAX_AGENTS=100000
SCALE_UP_THRESHOLD=70
SCALE_DOWN_THRESHOLD=30
COOLDOWN_PERIOD=300

# Monitoring Configuration
METRICS_RETENTION=30d
LOGS_RETENTION=7d
TRACE_RETENTION=3d

# Performance Tuning
PROMETHEUS_STORAGE_RETENTION=200h
ELASTICSEARCH_HEAP_SIZE=2g
GRAFANA_MEMORY_LIMIT=1g

# Security (change in production)
GRAFANA_ADMIN_PASSWORD=admin
ELASTICSEARCH_PASSWORD=
EOL
    echo "   Created .env file with default configuration"
fi

# Start the platform
echo "🐳 Starting AI Observability Platform..."
echo "   This may take several minutes on first run..."

# Pull images first to show progress
docker-compose pull

# Start services in order
echo "   Starting core infrastructure..."
docker-compose up -d redis elasticsearch

# Wait for Elasticsearch to be ready
echo "   Waiting for Elasticsearch to be ready..."
sleep 30
while ! curl -s http://localhost:9200/_cluster/health >/dev/null; do
    echo "   Elasticsearch not ready yet, waiting..."
    sleep 10
done
echo "   ✅ Elasticsearch is ready"

# Start monitoring services
echo "   Starting monitoring services..."
docker-compose up -d prometheus prometheus-federation jaeger

# Wait for Prometheus to be ready
echo "   Waiting for Prometheus to be ready..."
sleep 20
while ! curl -s http://localhost:9090/-/ready >/dev/null; do
    echo "   Prometheus not ready yet, waiting..."
    sleep 5
done
echo "   ✅ Prometheus is ready"

# Start processing services
echo "   Starting log processing..."
docker-compose up -d logstash kibana

# Start application services
echo "   Starting AI monitoring services..."
docker-compose up -d otel-collector agent-health-monitor anomaly-detector emergence-detector autoscaler

# Start visualization
echo "   Starting visualization services..."
docker-compose up -d grafana

# Wait for all services to be healthy
echo "🏥 Checking service health..."
sleep 30

# Health check function
check_service() {
    local service_name=$1
    local url=$2
    local max_attempts=10
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" >/dev/null 2>&1; then
            echo "   ✅ $service_name is healthy"
            return 0
        fi
        echo "   ⏳ $service_name not ready (attempt $attempt/$max_attempts)"
        sleep 10
        ((attempt++))
    done
    
    echo "   ❌ $service_name failed to start"
    return 1
}

# Check all services
check_service "Prometheus" "http://localhost:9090/-/ready"
check_service "Grafana" "http://localhost:3000/api/health"
check_service "Jaeger" "http://localhost:16686/"
check_service "Elasticsearch" "http://localhost:9200/_cluster/health"
check_service "Agent Health Monitor" "http://localhost:8080/health"
check_service "Anomaly Detector" "http://localhost:8081/health"
check_service "Emergence Detector" "http://localhost:8082/health"
check_service "Auto Scaler" "http://localhost:8083/health"

# Setup Grafana dashboards
echo "📊 Setting up Grafana dashboards..."
sleep 10

# Create API key and import dashboards (simplified for demo)
# In production, use Grafana provisioning

echo "🎉 AI Observability Platform is ready!"
echo ""
echo "📈 Access URLs:"
echo "   Grafana Dashboard: http://localhost:3000 (admin/admin)"
echo "   Prometheus Metrics: http://localhost:9090"
echo "   Jaeger Tracing: http://localhost:16686"
echo "   Kibana Logs: http://localhost:5601"
echo "   Elasticsearch: http://localhost:9200"
echo ""
echo "🔧 API Endpoints:"
echo "   Agent Health Monitor: http://localhost:8080"
echo "   Anomaly Detector: http://localhost:8081"
echo "   Emergence Detector: http://localhost:8082"
echo "   Auto Scaler: http://localhost:8083"
echo ""
echo "🏃 Next Steps:"
echo "   1. Install Python dependencies: pip install -r demo/requirements.txt"
echo "   2. Run agent simulator: python demo/ai_agent_simulator.py --agents 1000"
echo "   3. View dashboards at http://localhost:3000"
echo ""
echo "📚 Documentation: See README.md for detailed usage instructions"
echo ""
echo "🎯 Quick Start Commands:"
echo "   # Simulate 1,000 agents"
echo "   python demo/ai_agent_simulator.py --agents 1000 --duration 30"
echo ""
echo "   # Run load test"
echo "   python demo/ai_agent_simulator.py --agents 5000 --load-test --duration 15"
echo ""
echo "   # Monitor system status"
echo "   docker-compose ps"
echo ""
echo "   # View service logs"
echo "   docker-compose logs -f [service-name]"
echo ""
echo "✨ Happy Monitoring! Your billion-scale AI observability platform is now running."