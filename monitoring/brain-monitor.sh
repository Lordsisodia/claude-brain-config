#!/bin/bash
# Autonomous Brain Monitoring System
# Real-time monitoring and progress tracking for all brain operations

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Configuration
SESSION_NAME="BRAIN-MAIN"
MONITORING_DIR="/Users/shaansisodia/DEV/claude-brain-config/monitoring"
LOGS_DIR="$MONITORING_DIR/logs"
METRICS_DIR="$MONITORING_DIR/metrics"
LEARNING_ENGINE="$HOME/.learning-engine"

# Create monitoring directories
mkdir -p "$LOGS_DIR" "$METRICS_DIR" "$LEARNING_ENGINE/monitoring"

echo -e "${BLUE}📊 AUTONOMOUS BRAIN MONITORING SYSTEM${NC}"
echo -e "${CYAN}===================================${NC}"

# Function to collect brain metrics
collect_brain_metrics() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local metrics_file="$METRICS_DIR/brain_metrics_$(date +%Y%m%d).json"
    
    # Check if brain session exists
    if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
        echo "{\"timestamp\": \"$timestamp\", \"status\": \"inactive\", \"error\": \"Brain session not found\"}" >> "$metrics_file"
        return 1
    fi
    
    # Collect session metrics
    local session_created=$(tmux display-message -t $SESSION_NAME -p "#{session_created}")
    local window_count=$(tmux list-windows -t $SESSION_NAME | wc -l)
    local active_agents=$(tmux list-windows -t $SESSION_NAME | grep -E "(architect|implementer|reviewer|tester|documenter|security|optimizer|orchestrator)" | wc -l)
    local current_window=$(tmux display-message -t $SESSION_NAME -p "#{window_name}")
    
    # Collect learning metrics
    local patterns_count=0
    local learning_status="inactive"
    if [ -f "$LEARNING_ENGINE/status" ]; then
        learning_status=$(cat "$LEARNING_ENGINE/status")
        if [ -d "$LEARNING_ENGINE/patterns" ]; then
            patterns_count=$(find "$LEARNING_ENGINE/patterns" -name "*.json" 2>/dev/null | wc -l)
        fi
    fi
    
    # Collect autonomous task metrics
    local autonomous_tasks=0
    if [ -d "/Users/shaansisodia/DEV/claude-brain-config/storage" ]; then
        autonomous_tasks=$(find "/Users/shaansisodia/DEV/claude-brain-config/storage" -name "autonomous_*" -type f 2>/dev/null | wc -l)
    fi
    
    # Create metrics JSON
    cat > "$metrics_file.tmp" << EOF
{
    "timestamp": "$timestamp",
    "status": "active",
    "session": {
        "name": "$SESSION_NAME",
        "created": $session_created,
        "uptime_hours": $(echo "scale=2; ($(date +%s) - $session_created) / 3600" | bc -l 2>/dev/null || echo "0"),
        "windows_total": $window_count,
        "current_window": "$current_window"
    },
    "agents": {
        "deployed_count": $active_agents,
        "status": "$(if [ $active_agents -gt 0 ]; then echo "active"; else echo "inactive"; fi)"
    },
    "learning": {
        "status": "$learning_status",
        "patterns_discovered": $patterns_count,
        "sessions_recorded": $(find "$LEARNING_ENGINE/sessions" -name "*.log" 2>/dev/null | wc -l || echo "0")
    },
    "autonomous_tasks": {
        "active_count": $autonomous_tasks,
        "storage_size_mb": $(du -sm "/Users/shaansisodia/DEV/claude-brain-config/storage" 2>/dev/null | cut -f1 || echo "0")
    },
    "performance": {
        "memory_usage_mb": $(ps -o rss= -p $$ | awk '{print int($1/1024)}'),
        "cpu_usage": "$(top -l 1 -n 0 | grep "CPU usage" | awk '{print $3}' || echo "0%")"
    }
}
EOF
    
    # Atomically update metrics file
    mv "$metrics_file.tmp" "$metrics_file"
    
    # Also create latest metrics symlink
    ln -sf "$metrics_file" "$METRICS_DIR/latest_metrics.json"
    
    echo -e "${GREEN}📊 Metrics collected: $timestamp${NC}"
}

# Function to monitor agent activity
monitor_agent_activity() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local agent_log="$LOGS_DIR/agent_activity_$(date +%Y%m%d).log"
    
    if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
        return 1
    fi
    
    echo "[$timestamp] Agent Activity Monitoring" >> "$agent_log"
    
    # Monitor each agent window
    for agent in architect implementer reviewer tester documenter security optimizer orchestrator; do
        if tmux list-windows -t $SESSION_NAME | grep -q "$agent"; then
            local last_activity=$(tmux display-message -t "$SESSION_NAME:$agent" -p "#{window_activity}")
            echo "[$timestamp] $agent: active (last_activity: $last_activity)" >> "$agent_log"
        else
            echo "[$timestamp] $agent: not deployed" >> "$agent_log"
        fi
    done
    
    echo -e "${CYAN}🤖 Agent activity logged${NC}"
}

# Function to track autonomous tasks
track_autonomous_tasks() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local task_log="$LOGS_DIR/autonomous_tasks_$(date +%Y%m%d).log"
    
    echo "[$timestamp] Autonomous Task Tracking" >> "$task_log"
    
    # Track PRD projects
    if [ -d "/Users/shaansisodia/DEV/claude-brain-config/storage/prd-projects" ]; then
        local prd_count=$(find "/Users/shaansisodia/DEV/claude-brain-config/storage/prd-projects" -type d -maxdepth 1 2>/dev/null | wc -l)
        echo "[$timestamp] PRD Projects: $prd_count" >> "$task_log"
    fi
    
    # Track research projects
    if [ -d "/Users/shaansisodia/DEV/claude-brain-config/storage/research-projects" ]; then
        local research_count=$(find "/Users/shaansisodia/DEV/claude-brain-config/storage/research-projects" -type d -maxdepth 1 2>/dev/null | wc -l)
        echo "[$timestamp] Research Projects: $research_count" >> "$task_log"
    fi
    
    # Track problem solutions
    if [ -d "/Users/shaansisodia/DEV/claude-brain-config/storage/problem-solutions" ]; then
        local problem_count=$(find "/Users/shaansisodia/DEV/claude-brain-config/storage/problem-solutions" -type d -maxdepth 1 2>/dev/null | wc -l)
        echo "[$timestamp] Problem Solutions: $problem_count" >> "$task_log"
    fi
    
    echo -e "${MAGENTA}📋 Autonomous tasks tracked${NC}"
}

# Function to generate monitoring dashboard
generate_dashboard() {
    local dashboard_file="$MONITORING_DIR/dashboard.html"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    cat > "$dashboard_file" << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Brain Monitoring Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: monospace; background: #1a1a1a; color: #00ff00; margin: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; border-bottom: 2px solid #00ff00; padding-bottom: 10px; margin-bottom: 20px; }
        .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .metric-card { border: 1px solid #00ff00; padding: 15px; border-radius: 5px; background: #0a0a0a; }
        .metric-title { color: #00ffff; font-weight: bold; margin-bottom: 10px; }
        .metric-value { font-size: 1.2em; margin: 5px 0; }
        .status-active { color: #00ff00; }
        .status-inactive { color: #ff0000; }
        .status-warning { color: #ffff00; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 AUTONOMOUS BRAIN MONITORING DASHBOARD</h1>
            <p>Real-time intelligence and performance metrics</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-title">🎯 Brain Session Status</div>
                <div class="metric-value status-active" id="session-status">Loading...</div>
                <div class="metric-value">Uptime: <span id="uptime">Loading...</span></div>
                <div class="metric-value">Windows: <span id="windows">Loading...</span></div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">🤖 Agent Deployment</div>
                <div class="metric-value">Active Agents: <span id="agents">Loading...</span></div>
                <div class="metric-value status-active" id="agent-status">Loading...</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">📈 Learning Engine</div>
                <div class="metric-value">Status: <span id="learning-status">Loading...</span></div>
                <div class="metric-value">Patterns: <span id="patterns">Loading...</span></div>
                <div class="metric-value">Sessions: <span id="sessions">Loading...</span></div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">🚀 Autonomous Tasks</div>
                <div class="metric-value">Active: <span id="tasks">Loading...</span></div>
                <div class="metric-value">Storage: <span id="storage">Loading...</span> MB</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">⚡ Performance</div>
                <div class="metric-value">Memory: <span id="memory">Loading...</span> MB</div>
                <div class="metric-value">CPU: <span id="cpu">Loading...</span></div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">🕒 Last Updated</div>
                <div class="metric-value" id="last-updated">Loading...</div>
            </div>
        </div>
    </div>
    
    <script>
        function loadMetrics() {
            fetch('metrics/latest_metrics.json')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('session-status').textContent = data.status.toUpperCase();
                    document.getElementById('uptime').textContent = data.session.uptime_hours + ' hours';
                    document.getElementById('windows').textContent = data.session.windows_total;
                    document.getElementById('agents').textContent = data.agents.deployed_count;
                    document.getElementById('agent-status').textContent = data.agents.status.toUpperCase();
                    document.getElementById('learning-status').textContent = data.learning.status.toUpperCase();
                    document.getElementById('patterns').textContent = data.learning.patterns_discovered;
                    document.getElementById('sessions').textContent = data.learning.sessions_recorded;
                    document.getElementById('tasks').textContent = data.autonomous_tasks.active_count;
                    document.getElementById('storage').textContent = data.autonomous_tasks.storage_size_mb;
                    document.getElementById('memory').textContent = data.performance.memory_usage_mb;
                    document.getElementById('cpu').textContent = data.performance.cpu_usage;
                    document.getElementById('last-updated').textContent = data.timestamp;
                })
                .catch(error => {
                    console.error('Error loading metrics:', error);
                });
        }
        
        // Load metrics immediately and then every 30 seconds
        loadMetrics();
        setInterval(loadMetrics, 30000);
    </script>
</body>
</html>
EOF
    
    echo -e "${BLUE}📊 Dashboard generated: $dashboard_file${NC}"
}

# Function to start continuous monitoring
start_continuous_monitoring() {
    local monitor_pid_file="$MONITORING_DIR/monitor.pid"
    
    echo -e "${GREEN}🔄 Starting continuous monitoring...${NC}"
    
    # Create monitoring loop
    (
        while true; do
            collect_brain_metrics
            monitor_agent_activity
            track_autonomous_tasks
            generate_dashboard
            sleep 60  # Monitor every minute
        done
    ) &
    
    # Save PID for stopping later
    echo $! > "$monitor_pid_file"
    
    echo -e "${GREEN}✅ Continuous monitoring started (PID: $(cat "$monitor_pid_file"))${NC}"
    echo -e "${CYAN}📊 Dashboard: file://$MONITORING_DIR/dashboard.html${NC}"
    echo -e "${YELLOW}Stop with: kill $(cat "$monitor_pid_file")${NC}"
}

# Function to stop monitoring
stop_monitoring() {
    local monitor_pid_file="$MONITORING_DIR/monitor.pid"
    
    if [ -f "$monitor_pid_file" ]; then
        local pid=$(cat "$monitor_pid_file")
        if kill "$pid" 2>/dev/null; then
            echo -e "${GREEN}✅ Monitoring stopped (PID: $pid)${NC}"
            rm -f "$monitor_pid_file"
        else
            echo -e "${RED}❌ Failed to stop monitoring process${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️ No monitoring process found${NC}"
    fi
}

# Function to show monitoring status
show_status() {
    local monitor_pid_file="$MONITORING_DIR/monitor.pid"
    
    echo -e "${BLUE}📊 BRAIN MONITORING STATUS${NC}"
    echo -e "${CYAN}=========================${NC}"
    
    if [ -f "$monitor_pid_file" ]; then
        local pid=$(cat "$monitor_pid_file")
        if ps -p "$pid" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Monitoring: ACTIVE (PID: $pid)${NC}"
        else
            echo -e "${RED}❌ Monitoring: STALE PID${NC}"
            rm -f "$monitor_pid_file"
        fi
    else
        echo -e "${YELLOW}⚠️ Monitoring: INACTIVE${NC}"
    fi
    
    echo -e "${CYAN}Dashboard: file://$MONITORING_DIR/dashboard.html${NC}"
    echo -e "${CYAN}Logs: $LOGS_DIR${NC}"
    echo -e "${CYAN}Metrics: $METRICS_DIR${NC}"
    
    # Show latest metrics if available
    if [ -f "$METRICS_DIR/latest_metrics.json" ]; then
        echo -e "${YELLOW}Latest Metrics:${NC}"
        if command -v jq > /dev/null 2>&1; then
            cat "$METRICS_DIR/latest_metrics.json" | jq .
        else
            cat "$METRICS_DIR/latest_metrics.json"
        fi
    fi
}

# Main command processing
case "${1:-status}" in
    "start")
        start_continuous_monitoring
        ;;
    "stop")
        stop_monitoring
        ;;
    "status")
        show_status
        ;;
    "collect")
        collect_brain_metrics
        monitor_agent_activity
        track_autonomous_tasks
        generate_dashboard
        ;;
    "dashboard")
        generate_dashboard
        echo -e "${CYAN}📊 Dashboard: file://$MONITORING_DIR/dashboard.html${NC}"
        ;;
    *)
        echo -e "${BLUE}📊 Brain Monitoring Commands:${NC}"
        echo -e "${CYAN}  brain-monitor start      - Start continuous monitoring${NC}"
        echo -e "${CYAN}  brain-monitor stop       - Stop monitoring${NC}"
        echo -e "${CYAN}  brain-monitor status     - Show monitoring status${NC}"
        echo -e "${CYAN}  brain-monitor collect    - Collect metrics once${NC}"
        echo -e "${CYAN}  brain-monitor dashboard  - Generate dashboard${NC}"
        ;;
esac