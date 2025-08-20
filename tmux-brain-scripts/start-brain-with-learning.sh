#!/bin/bash
# Enhanced TMUX Brain Starter with Learning Engine Integration

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
TMUX_BRAIN_HOME="${TMUX_BRAIN_HOME:-$HOME/.tmux-brain}"
LEARNING_ENGINE_HOME="${LEARNING_ENGINE_HOME:-$HOME/.learning-engine}"
CLAUDE_CONFIG="${CLAUDE_CONFIG:-$HOME/.claude/CLAUDE.md}"

echo -e "${BLUE}🧠🤖 TMUX BRAIN + LEARNING ENGINE Integration${NC}"
echo -e "${CYAN}Starting Ultimate Self-Improving Development Environment...${NC}"

# Check if learning engine is available
LEARNING_AVAILABLE=false
if [ -f "/Users/shaansisodia/DEV/claude-global-config/learning-engine/init/start_learning_engine.sh" ]; then
    LEARNING_AVAILABLE=true
    echo -e "${GREEN}✅ Learning Engine available${NC}"
else
    echo -e "${YELLOW}⚠️ Learning Engine not available - starting brain only${NC}"
fi

# Start Learning Engine first (if available and not already running)
if [ "$LEARNING_AVAILABLE" = true ]; then
    if [ ! -f "$LEARNING_ENGINE_HOME/status" ] || [ "$(cat "$LEARNING_ENGINE_HOME/status" 2>/dev/null)" != "ACTIVE" ]; then
        echo -e "${MAGENTA}🚀 Starting Learning Engine first...${NC}"
        /Users/shaansisodia/DEV/claude-global-config/learning-engine/init/start_learning_engine.sh --no-dashboard
        
        # Wait for learning engine to initialize
        echo -e "${BLUE}⏳ Waiting for Learning Engine to initialize...${NC}"
        sleep 3
    else
        echo -e "${GREEN}✅ Learning Engine already active${NC}"
    fi
fi

# Check if brain session already exists
if tmux has-session -t BRAIN-MAIN 2>/dev/null; then
    echo -e "${YELLOW}⚠️ Brain session already exists.${NC}"
    
    if [ "$LEARNING_AVAILABLE" = true ]; then
        echo -e "${CYAN}🔗 Connecting learning observer to existing session...${NC}"
        
        # Start session observer for existing session
        if [ ! -f "$LEARNING_ENGINE_HOME/pids/session_observer.pid" ] || ! ps -p $(cat "$LEARNING_ENGINE_HOME/pids/session_observer.pid" 2>/dev/null) > /dev/null 2>&1; then
            nohup python3 "$LEARNING_ENGINE_HOME/observers/session_observer.py" \
                --session BRAIN-MAIN > \
                "$LEARNING_ENGINE_HOME/logs/session_observer.log" 2>&1 &
            echo $! > "$LEARNING_ENGINE_HOME/pids/session_observer.pid"
            echo -e "${GREEN}✅ Learning observer attached${NC}"
        fi
    fi
    
    echo -e "${CYAN}🔗 Attaching to existing brain session...${NC}"
    tmux attach-session -t BRAIN-MAIN
    exit 0
fi

echo -e "${GREEN}🚀 Starting Enhanced TMUX Brain with Learning Integration${NC}"

# Start main brain session with learning integration
tmux new-session -d -s BRAIN-MAIN -n "control-center"

# Set enhanced environment variables
tmux send-keys -t BRAIN-MAIN:control-center \
  "export TMUX_BRAIN_HOME='$TMUX_BRAIN_HOME'" C-m
tmux send-keys -t BRAIN-MAIN:control-center \
  "export LEARNING_ENGINE='ACTIVE'" C-m
tmux send-keys -t BRAIN-MAIN:control-center \
  "export LEARNING_HOME='$LEARNING_ENGINE_HOME'" C-m
tmux send-keys -t BRAIN-MAIN:control-center \
  "export SESSION_ID='$(uuidgen)'" C-m
tmux send-keys -t BRAIN-MAIN:control-center \
  "export THINKING_MODE='MUSK_5_STEP'" C-m
tmux send-keys -t BRAIN-MAIN:control-center \
  "export COMPUTE_MODE='10X_ENHANCED'" C-m
tmux send-keys -t BRAIN-MAIN:control-center \
  "export REASONING_ENGINE='ULTRA_THINK'" C-m

# Display integration status
echo -e "${CYAN}📋 Initializing Brain + Learning Integration...${NC}"
tmux send-keys -t BRAIN-MAIN:control-center \
  "echo '🧠🤖 ENHANCED BRAIN + LEARNING INTEGRATION'" C-m
tmux send-keys -t BRAIN-MAIN:control-center \
  "echo '================================'" C-m
tmux send-keys -t BRAIN-MAIN:control-center \
  "echo 'Brain Power: FULLY ACTIVATED'" C-m

if [ "$LEARNING_AVAILABLE" = true ]; then
    tmux send-keys -t BRAIN-MAIN:control-center \
      "echo 'Learning Engine: ACTIVE'" C-m
    tmux send-keys -t BRAIN-MAIN:control-center \
      "echo 'System Learning: CONTINUOUS'" C-m
    tmux send-keys -t BRAIN-MAIN:control-center \
      "echo 'Auto-Optimization: ENABLED'" C-m
else
    tmux send-keys -t BRAIN-MAIN:control-center \
      "echo 'Learning Engine: NOT AVAILABLE'" C-m
fi

# Initialize Musk's 5-Step Algorithm with Learning
echo -e "${CYAN}📋 Initializing Enhanced Musk's 5-Step Algorithm...${NC}"
tmux send-keys -t BRAIN-MAIN:control-center \
  "echo ''" C-m
tmux send-keys -t BRAIN-MAIN:control-center \
  "echo '🧠 MUSK 5-STEP ALGORITHM + LEARNING'" C-m
tmux send-keys -t BRAIN-MAIN:control-center \
  "echo '1. Question Requirements (+ Learn Patterns)'" C-m
tmux send-keys -t BRAIN-MAIN:control-center \
  "echo '2. Delete/Simplify (+ Auto-Optimize)'" C-m
tmux send-keys -t BRAIN-MAIN:control-center \
  "echo '3. Optimize/Accelerate (+ Predict Needs)'" C-m
tmux send-keys -t BRAIN-MAIN:control-center \
  "echo '4. Automate (+ Learn from Patterns)'" C-m
tmux send-keys -t BRAIN-MAIN:control-center \
  "echo '5. Iterate (+ Continuous Improvement)'" C-m

# Create all the original brain windows
echo -e "${MAGENTA}🔮 Setting up Multi-Model Compute Hub...${NC}"
tmux new-window -t BRAIN-MAIN -n "compute-hub"
tmux send-keys -t BRAIN-MAIN:compute-hub \
  "echo '🔮 MULTI-MODEL COMPUTE HUB (Learning Enhanced)'" C-m

echo -e "${GREEN}🔌 Launching MCP Server Orchestra...${NC}"
tmux new-window -t BRAIN-MAIN -n "mcp-servers"
tmux split-window -h -t BRAIN-MAIN:mcp-servers
tmux split-window -v -t BRAIN-MAIN:mcp-servers.0
tmux split-window -v -t BRAIN-MAIN:mcp-servers.1

echo -e "${YELLOW}🤖 Deploying Multi-Agent System...${NC}"
tmux new-window -t BRAIN-MAIN -n "agents"
tmux split-window -h -t BRAIN-MAIN:agents
tmux split-window -v -t BRAIN-MAIN:agents.0
tmux split-window -v -t BRAIN-MAIN:agents.1

echo -e "${BLUE}💾 Initializing Enhanced Memory Systems...${NC}"
tmux new-window -t BRAIN-MAIN -n "memory"
tmux send-keys -t BRAIN-MAIN:memory \
  "echo '💾 ENHANCED MEMORY SYSTEMS'" C-m
tmux send-keys -t BRAIN-MAIN:memory \
  "echo '  • Working Memory: Active'" C-m
tmux send-keys -t BRAIN-MAIN:memory \
  "echo '  • Episodic Memory: Recording'" C-m
tmux send-keys -t BRAIN-MAIN:memory \
  "echo '  • Semantic Memory: Learning'" C-m
tmux send-keys -t BRAIN-MAIN:memory \
  "echo '  • Procedural Memory: Optimizing'" C-m

if [ "$LEARNING_AVAILABLE" = true ]; then
    tmux send-keys -t BRAIN-MAIN:memory \
      "echo '  • Cross-Session Learning: ACTIVE'" C-m
    tmux send-keys -t BRAIN-MAIN:memory \
      "echo '  • Pattern Recognition: CONTINUOUS'" C-m
    tmux send-keys -t BRAIN-MAIN:memory \
      "echo '  • Auto-Optimization: ENABLED'" C-m
fi

echo -e "${CYAN}📋 Starting Enhanced Task Orchestrator...${NC}"
tmux new-window -t BRAIN-MAIN -n "task-orchestrator"
tmux send-keys -t BRAIN-MAIN:task-orchestrator \
  "echo '📋 ENHANCED TASK ORCHESTRATOR'" C-m

if [ "$LEARNING_AVAILABLE" = true ]; then
    tmux send-keys -t BRAIN-MAIN:task-orchestrator \
      "echo 'Mode: Intelligent Decomposition + Learning'" C-m
    tmux send-keys -t BRAIN-MAIN:task-orchestrator \
      "echo 'Pattern Recognition: ACTIVE'" C-m
    tmux send-keys -t BRAIN-MAIN:task-orchestrator \
      "echo 'Predictive Optimization: ENABLED'" C-m
fi

echo -e "${MAGENTA}📊 Starting Enhanced Performance Monitor...${NC}"
tmux new-window -t BRAIN-MAIN -n "monitor"
tmux split-window -h -t BRAIN-MAIN:monitor
tmux split-window -v -t BRAIN-MAIN:monitor.0
tmux split-window -v -t BRAIN-MAIN:monitor.1

# Enhanced monitoring panes
tmux send-keys -t BRAIN-MAIN:monitor.0 \
  "echo '📊 ENHANCED MONITORING'" C-m
tmux send-keys -t BRAIN-MAIN:monitor.1 \
  "echo '🤖 AGENT + LEARNING STATUS'" C-m
tmux send-keys -t BRAIN-MAIN:monitor.2 \
  "echo '💾 MEMORY + PATTERNS'" C-m
tmux send-keys -t BRAIN-MAIN:monitor.3 \
  "echo '⚡ PERFORMANCE + OPTIMIZATION'" C-m

echo -e "${RED}🧠 Creating Ultra Think Chamber...${NC}"
tmux new-window -t BRAIN-MAIN -n "ultra-think"
tmux send-keys -t BRAIN-MAIN:ultra-think \
  "echo '🧠 ULTRA THINK CHAMBER (Learning Enhanced)'" C-m
tmux send-keys -t BRAIN-MAIN:ultra-think \
  "echo 'Mode: 10x Reasoning Power + Pattern Learning'" C-m

# Add Learning Dashboard window (if learning engine is available)
if [ "$LEARNING_AVAILABLE" = true ]; then
    echo -e "${MAGENTA}📈 Creating Learning Dashboard...${NC}"
    tmux new-window -t BRAIN-MAIN -n "learning-dashboard"
    tmux send-keys -t BRAIN-MAIN:learning-dashboard \
      "echo '📈 LEARNING ENGINE DASHBOARD'" C-m
    tmux send-keys -t BRAIN-MAIN:learning-dashboard \
      "echo '========================'" C-m
    tmux send-keys -t BRAIN-MAIN:learning-dashboard \
      "echo 'System Learning: ACTIVE'" C-m
    tmux send-keys -t BRAIN-MAIN:learning-dashboard \
      "echo 'Pattern Recognition: CONTINUOUS'" C-m
    tmux send-keys -t BRAIN-MAIN:learning-dashboard \
      "echo 'Auto-Optimization: ENABLED'" C-m
    tmux send-keys -t BRAIN-MAIN:learning-dashboard \
      "echo ''" C-m
    tmux send-keys -t BRAIN-MAIN:learning-dashboard \
      "echo 'Run: $LEARNING_ENGINE_HOME/monitor_dashboard.sh'" C-m
fi

# Start learning observer (if available)
if [ "$LEARNING_AVAILABLE" = true ]; then
    echo -e "${BLUE}👁️ Starting Learning Observer...${NC}"
    
    # Make sure learning engine is ready
    sleep 1
    
    # Start session observer
    nohup python3 "$LEARNING_ENGINE_HOME/observers/session_observer.py" \
        --session BRAIN-MAIN > \
        "$LEARNING_ENGINE_HOME/logs/session_observer.log" 2>&1 &
    OBSERVER_PID=$!
    echo $OBSERVER_PID > "$LEARNING_ENGINE_HOME/pids/session_observer.pid"
    
    echo -e "${GREEN}✅ Learning Observer started (PID: $OBSERVER_PID)${NC}"
    
    # Notify brain session about learning integration
    tmux send-keys -t BRAIN-MAIN:control-center \
      "echo ''" C-m
    tmux send-keys -t BRAIN-MAIN:control-center \
      "echo '🎯 Learning Observer: ATTACHED'" C-m
    tmux send-keys -t BRAIN-MAIN:control-center \
      "echo '📊 Pattern Recognition: ACTIVE'" C-m
    tmux send-keys -t BRAIN-MAIN:control-center \
      "echo '🚀 Auto-Optimization: ENABLED'" C-m
fi

# Create status files
echo "ACTIVE" > "$TMUX_BRAIN_HOME/status"
echo "$(date)" > "$TMUX_BRAIN_HOME/last_start"

if [ "$LEARNING_AVAILABLE" = true ]; then
    echo "BRAIN_INTEGRATED" > "$LEARNING_ENGINE_HOME/brain_status"
fi

# Final setup message
echo ""
echo -e "${GREEN}🎉 ENHANCED TMUX BRAIN + LEARNING ENGINE STARTED!${NC}"
echo ""
echo -e "${CYAN}📍 Brain Session: BRAIN-MAIN${NC}"
if [ "$LEARNING_AVAILABLE" = true ]; then
    echo -e "${MAGENTA}🧠 Learning Engine: ACTIVE${NC}"
    echo -e "${BLUE}📊 Learning Dashboard: learning-dashboard window${NC}"
fi
echo -e "${YELLOW}💡 Tip: Use 'tmux attach -t BRAIN-MAIN' to connect${NC}"
echo -e "${GREEN}🚀 Revolutionary AI Development Environment: FULLY ACTIVATED${NC}"
echo ""

# Auto-attach if not in tmux already
if [ -z "$TMUX" ]; then
    echo -e "${BLUE}🔗 Attaching to enhanced brain session...${NC}"
    sleep 1
    tmux attach-session -t BRAIN-MAIN
else
    echo -e "${YELLOW}⚠️ Already in tmux. Use prefix+s to switch to BRAIN-MAIN${NC}"
fi