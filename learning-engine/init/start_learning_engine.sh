#!/bin/bash
# System-Wide Learning Engine Startup Script
# Initializes the complete learning ecosystem

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
LEARNING_ENGINE_HOME="${LEARNING_ENGINE_HOME:-$HOME/.learning-engine}"
CLAUDE_CONFIG="${CLAUDE_CONFIG:-$HOME/.claude/CLAUDE.md}"
SCRIPT_DIR="/Users/shaansisodia/DEV/claude-global-config/learning-engine"

echo -e "${BLUE}🧠 SYSTEM-WIDE LEARNING ENGINE v2.0${NC}"
echo -e "${CYAN}Initializing Revolutionary Self-Improving AI Ecosystem...${NC}"
echo ""

# Check dependencies
echo -e "${YELLOW}🔍 Checking dependencies...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed${NC}"
    exit 1
fi

# Check TMUX
if ! command -v tmux &> /dev/null; then
    echo -e "${RED}❌ TMUX is required but not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Dependencies satisfied${NC}"

# Create directory structure
echo -e "${BLUE}📁 Creating Learning Engine directory structure...${NC}"
mkdir -p "$LEARNING_ENGINE_HOME"/{sessions,patterns,knowledge,optimizations,predictions}
mkdir -p "$LEARNING_ENGINE_HOME"/{raw,processed,analyzed,optimized}
mkdir -p "$LEARNING_ENGINE_HOME"/{models,weights,configs,backups}
mkdir -p "$LEARNING_ENGINE_HOME"/{agents,observers,analyzers,optimizers,predictors}
mkdir -p "$LEARNING_ENGINE_HOME"/{orchestrator,events,logs}

# Create status file
echo "INITIALIZING" > "$LEARNING_ENGINE_HOME/status"
echo "$(date)" > "$LEARNING_ENGINE_HOME/last_start"

# Copy learning engine scripts
echo -e "${MAGENTA}📋 Installing learning engine components...${NC}"
cp -r "$SCRIPT_DIR"/* "$LEARNING_ENGINE_HOME/"

# Make scripts executable
chmod +x "$LEARNING_ENGINE_HOME"/observers/*.py
chmod +x "$LEARNING_ENGINE_HOME"/agents/*.py
chmod +x "$LEARNING_ENGINE_HOME"/init/*.sh

# Install Python dependencies
echo -e "${CYAN}📦 Installing Python dependencies...${NC}"
pip3 install --user asyncio psutil > /dev/null 2>&1 || echo -e "${YELLOW}⚠️ Some Python packages may not be available${NC}"

# Initialize knowledge graph database
echo -e "${GREEN}🧠 Initializing Knowledge Graph...${NC}"
cat > "$LEARNING_ENGINE_HOME/knowledge/knowledge_graph.json" << 'EOF'
{
  "nodes": {
    "patterns": {},
    "contexts": {},
    "outcomes": {},
    "optimizations": {}
  },
  "edges": {
    "causes": {},
    "correlates": {},
    "optimizes": {},
    "predicts": {}
  },
  "metadata": {
    "created_at": "TIMESTAMP",
    "version": "2.0.0",
    "node_count": 0,
    "edge_count": 0
  }
}
EOF

# Replace timestamp
sed -i.bak "s/TIMESTAMP/$(date -Iseconds)/" "$LEARNING_ENGINE_HOME/knowledge/knowledge_graph.json"
rm "$LEARNING_ENGINE_HOME/knowledge/knowledge_graph.json.bak"

# Create configuration files
echo -e "${BLUE}⚙️ Creating configuration files...${NC}"

# Learning engine config
cat > "$LEARNING_ENGINE_HOME/configs/learning_engine.json" << 'EOF'
{
  "learning_engine": {
    "version": "2.0.0",
    "learning_rate": 0.1,
    "pattern_threshold": 0.7,
    "optimization_threshold": 0.8,
    "auto_apply_threshold": 0.9,
    "session_monitoring": true,
    "real_time_learning": true,
    "predictive_optimization": true
  },
  "agents": {
    "session_observer": {
      "enabled": true,
      "monitoring_interval": 1,
      "pattern_extraction_interval": 30
    },
    "learning_orchestrator": {
      "enabled": true,
      "coordination_interval": 10,
      "synthesis_interval": 30
    },
    "performance_analyzer": {
      "enabled": true,
      "metric_collection_interval": 60,
      "analysis_interval": 300
    }
  },
  "optimization": {
    "auto_apply_safe_optimizations": true,
    "backup_before_changes": true,
    "rollback_on_failure": true,
    "optimization_queue_size": 100
  }
}
EOF

# TMUX integration config
cat > "$LEARNING_ENGINE_HOME/configs/tmux_integration.json" << 'EOF'
{
  "tmux_integration": {
    "monitor_sessions": ["BRAIN-MAIN"],
    "capture_commands": true,
    "capture_window_switches": true,
    "capture_pane_content": false,
    "learning_hooks": {
      "window_creation": true,
      "command_execution": true,
      "session_end": true
    }
  },
  "brain_integration": {
    "cognitive_mode_detection": true,
    "agent_interaction_monitoring": true,
    "performance_correlation": true,
    "optimization_suggestion": true
  }
}
EOF

# Start learning agents
echo -e "${GREEN}🤖 Starting Learning Agents...${NC}"

# Start Learning Orchestrator
echo -e "${CYAN}👑 Starting Learning Orchestrator...${NC}"
nohup python3 "$LEARNING_ENGINE_HOME/agents/learning_orchestrator.py" > \
    "$LEARNING_ENGINE_HOME/logs/orchestrator.log" 2>&1 &
ORCHESTRATOR_PID=$!
echo $ORCHESTRATOR_PID > "$LEARNING_ENGINE_HOME/pids/orchestrator.pid"
echo -e "${GREEN}✅ Learning Orchestrator started (PID: $ORCHESTRATOR_PID)${NC}"

# Wait a moment for orchestrator to initialize
sleep 2

# Start Session Observer (if BRAIN-MAIN session exists)
if tmux has-session -t BRAIN-MAIN 2>/dev/null; then
    echo -e "${BLUE}👁️ Starting Session Observer for BRAIN-MAIN...${NC}"
    nohup python3 "$LEARNING_ENGINE_HOME/observers/session_observer.py" \
        --session BRAIN-MAIN > \
        "$LEARNING_ENGINE_HOME/logs/session_observer.log" 2>&1 &
    OBSERVER_PID=$!
    echo $OBSERVER_PID > "$LEARNING_ENGINE_HOME/pids/session_observer.pid"
    echo -e "${GREEN}✅ Session Observer started (PID: $OBSERVER_PID)${NC}"
else
    echo -e "${YELLOW}⚠️ BRAIN-MAIN session not found. Session Observer will start when available.${NC}"
fi

# Create monitoring dashboard script
echo -e "${MAGENTA}📊 Creating monitoring dashboard...${NC}"
cat > "$LEARNING_ENGINE_HOME/monitor_dashboard.sh" << 'EOF'
#!/bin/bash
# Learning Engine Monitoring Dashboard

LEARNING_ENGINE_HOME="${LEARNING_ENGINE_HOME:-$HOME/.learning-engine}"

echo "🧠 SYSTEM-WIDE LEARNING ENGINE - Live Dashboard"
echo "================================================"
echo ""

while true; do
    clear
    echo "🧠 SYSTEM-WIDE LEARNING ENGINE - Live Dashboard"
    echo "================================================"
    echo "📅 $(date)"
    echo ""
    
    # Status
    if [ -f "$LEARNING_ENGINE_HOME/status" ]; then
        echo "🔋 Status: $(cat "$LEARNING_ENGINE_HOME/status")"
    fi
    
    # Active Processes
    echo ""
    echo "🤖 Active Learning Agents:"
    if [ -f "$LEARNING_ENGINE_HOME/pids/orchestrator.pid" ]; then
        PID=$(cat "$LEARNING_ENGINE_HOME/pids/orchestrator.pid")
        if ps -p $PID > /dev/null 2>&1; then
            echo "  ✅ Learning Orchestrator (PID: $PID)"
        else
            echo "  ❌ Learning Orchestrator (stopped)"
        fi
    fi
    
    if [ -f "$LEARNING_ENGINE_HOME/pids/session_observer.pid" ]; then
        PID=$(cat "$LEARNING_ENGINE_HOME/pids/session_observer.pid")
        if ps -p $PID > /dev/null 2>&1; then
            echo "  ✅ Session Observer (PID: $PID)"
        else
            echo "  ❌ Session Observer (stopped)"
        fi
    fi
    
    # Learning Metrics
    echo ""
    echo "📊 Learning Metrics:"
    
    # Count patterns
    if [ -d "$LEARNING_ENGINE_HOME/patterns" ]; then
        PATTERN_COUNT=$(find "$LEARNING_ENGINE_HOME/patterns" -name "*.json" | wc -l)
        echo "  🔍 Patterns Discovered: $PATTERN_COUNT"
    fi
    
    # Count sessions
    if [ -d "$LEARNING_ENGINE_HOME/sessions" ]; then
        SESSION_COUNT=$(find "$LEARNING_ENGINE_HOME/sessions" -name "*.jsonl" | wc -l)
        echo "  🎯 Sessions Monitored: $SESSION_COUNT"
    fi
    
    # Count optimizations
    if [ -d "$LEARNING_ENGINE_HOME/optimizations" ]; then
        OPT_COUNT=$(find "$LEARNING_ENGINE_HOME/optimizations" -name "*.jsonl" | wc -l)
        echo "  🚀 Optimizations Generated: $OPT_COUNT"
    fi
    
    # Recent Activity
    echo ""
    echo "📈 Recent Activity:"
    if [ -f "$LEARNING_ENGINE_HOME/logs/orchestrator.log" ]; then
        echo "  Last Orchestrator Activity:"
        tail -3 "$LEARNING_ENGINE_HOME/logs/orchestrator.log" | sed 's/^/    /'
    fi
    
    echo ""
    echo "Press Ctrl+C to exit dashboard"
    sleep 5
done
EOF

chmod +x "$LEARNING_ENGINE_HOME/monitor_dashboard.sh"

# Create stop script
cat > "$LEARNING_ENGINE_HOME/stop_learning_engine.sh" << 'EOF'
#!/bin/bash
# Stop Learning Engine

LEARNING_ENGINE_HOME="${LEARNING_ENGINE_HOME:-$HOME/.learning-engine}"

echo "🛑 Stopping Learning Engine..."

# Stop orchestrator
if [ -f "$LEARNING_ENGINE_HOME/pids/orchestrator.pid" ]; then
    PID=$(cat "$LEARNING_ENGINE_HOME/pids/orchestrator.pid")
    if ps -p $PID > /dev/null 2>&1; then
        kill $PID
        echo "✅ Learning Orchestrator stopped"
    fi
    rm -f "$LEARNING_ENGINE_HOME/pids/orchestrator.pid"
fi

# Stop session observer
if [ -f "$LEARNING_ENGINE_HOME/pids/session_observer.pid" ]; then
    PID=$(cat "$LEARNING_ENGINE_HOME/pids/session_observer.pid")
    if ps -p $PID > /dev/null 2>&1; then
        kill $PID
        echo "✅ Session Observer stopped"
    fi
    rm -f "$LEARNING_ENGINE_HOME/pids/session_observer.pid"
fi

echo "STOPPED" > "$LEARNING_ENGINE_HOME/status"
echo "💾 Learning Engine stopped and state saved"
EOF

chmod +x "$LEARNING_ENGINE_HOME/stop_learning_engine.sh"

# Create PIDs directory
mkdir -p "$LEARNING_ENGINE_HOME/pids"

# Update status
echo "ACTIVE" > "$LEARNING_ENGINE_HOME/status"

# Final setup
echo ""
echo -e "${GREEN}🎉 SYSTEM-WIDE LEARNING ENGINE SUCCESSFULLY INITIALIZED!${NC}"
echo ""
echo -e "${CYAN}📍 Learning Engine Home: ${LEARNING_ENGINE_HOME}${NC}"
echo -e "${MAGENTA}🚀 Status: ACTIVE and LEARNING${NC}"
echo ""
echo -e "${YELLOW}💡 Quick Commands:${NC}"
echo -e "  📊 Monitor: ${LEARNING_ENGINE_HOME}/monitor_dashboard.sh"
echo -e "  🛑 Stop: ${LEARNING_ENGINE_HOME}/stop_learning_engine.sh"
echo -e "  📁 Data: ${LEARNING_ENGINE_HOME}/"
echo ""
echo -e "${BLUE}🧠 The Learning Engine is now actively learning from every interaction!${NC}"
echo -e "${GREEN}🌟 Your system will continuously improve and optimize itself.${NC}"
echo ""

# Optionally start dashboard
read -p "🖥️ Start monitoring dashboard? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    "$LEARNING_ENGINE_HOME/monitor_dashboard.sh"
fi