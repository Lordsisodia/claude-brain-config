#!/bin/bash
# Enhanced Brain Orchestrator with Learning Integration
# Starts TMUX brain session with autonomous learning capabilities

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
BRAIN_DIR="/Users/shaansisodia/DEV/claude-brain-config"
LEARNING_ENGINE="$HOME/.learning-engine"
SESSION_NAME="BRAIN-MAIN"

echo -e "${BLUE}🧠 ENHANCED BRAIN ORCHESTRATOR WITH LEARNING${NC}"
echo -e "${CYAN}=============================================${NC}"

# Kill existing session if it exists
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo -e "${YELLOW}🔄 Stopping existing brain session...${NC}"
    tmux kill-session -t $SESSION_NAME
fi

# Create learning engine directory
mkdir -p "$LEARNING_ENGINE"/{patterns,sessions,agents,monitoring,logs}

echo -e "${GREEN}🚀 Starting Enhanced Brain Session...${NC}"

# Create main session with control center
tmux new-session -d -s $SESSION_NAME -n control-center

# Configure control center
tmux send-keys -t $SESSION_NAME:control-center \
    "echo '🧠 ENHANCED BRAIN CONTROL CENTER'" C-m
tmux send-keys -t $SESSION_NAME:control-center \
    "echo '============================'" C-m
tmux send-keys -t $SESSION_NAME:control-center \
    "echo 'Session: $SESSION_NAME'" C-m
tmux send-keys -t $SESSION_NAME:control-center \
    "echo 'Learning Engine: ACTIVE'" C-m
tmux send-keys -t $SESSION_NAME:control-center \
    "echo 'Autonomous Mode: ENABLED'" C-m
tmux send-keys -t $SESSION_NAME:control-center \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:control-center \
    "echo 'Available Commands:'" C-m
tmux send-keys -t $SESSION_NAME:control-center \
    "echo '  brain status     - Check brain status'" C-m
tmux send-keys -t $SESSION_NAME:control-center \
    "echo '  think <task>     - Quick thinking mode'" C-m
tmux send-keys -t $SESSION_NAME:control-center \
    "echo '  ultra_think      - Maximum reasoning'" C-m
tmux send-keys -t $SESSION_NAME:control-center \
    "echo '  autonomous <type> - Autonomous tasks'" C-m
tmux send-keys -t $SESSION_NAME:control-center \
    "echo '  brain_nav <area> - Quick navigation'" C-m

# Create compute hub
echo -e "${GREEN}💻 Creating Compute Hub...${NC}"
tmux new-window -t $SESSION_NAME -n compute-hub
tmux send-keys -t $SESSION_NAME:compute-hub \
    "echo '💻 COMPUTE HUB - MULTI-MODEL INTELLIGENCE'" C-m
tmux send-keys -t $SESSION_NAME:compute-hub \
    "echo 'Status: MONITORING COMPUTE ALLOCATION'" C-m
tmux send-keys -t $SESSION_NAME:compute-hub \
    "echo 'Mode: DYNAMIC OPTIMIZATION'" C-m

# Create MCP servers window
echo -e "${GREEN}🔌 Initializing MCP Servers...${NC}"
tmux new-window -t $SESSION_NAME -n mcp-servers
tmux send-keys -t $SESSION_NAME:mcp-servers \
    "echo '🔌 MCP SERVER MANAGEMENT'" C-m
tmux send-keys -t $SESSION_NAME:mcp-servers \
    "echo 'Servers: AUTO-DETECTING...'" C-m
tmux send-keys -t $SESSION_NAME:mcp-servers \
    "echo 'Status: READY FOR TOOL INTEGRATION'" C-m

# Create agents coordination window
echo -e "${GREEN}🤖 Setting up Agent Coordination...${NC}"
tmux new-window -t $SESSION_NAME -n agents
tmux send-keys -t $SESSION_NAME:agents \
    "echo '🤖 AGENT COORDINATION CENTER'" C-m
tmux send-keys -t $SESSION_NAME:agents \
    "echo 'Mode: AUTONOMOUS MULTI-AGENT'" C-m
tmux send-keys -t $SESSION_NAME:agents \
    "echo 'Status: READY FOR DEPLOYMENT'" C-m
tmux send-keys -t $SESSION_NAME:agents \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:agents \
    "echo 'Deploy agents with: agents deploy'" C-m

# Create memory systems window
echo -e "${GREEN}💾 Initializing Memory Systems...${NC}"
tmux new-window -t $SESSION_NAME -n memory
tmux send-keys -t $SESSION_NAME:memory \
    "echo '💾 MEMORY SYSTEMS'" C-m
tmux send-keys -t $SESSION_NAME:memory \
    "echo 'Working Memory: ACTIVE'" C-m
tmux send-keys -t $SESSION_NAME:memory \
    "echo 'Episodic Memory: LEARNING'" C-m
tmux send-keys -t $SESSION_NAME:memory \
    "echo 'Semantic Memory: GROWING'" C-m
tmux send-keys -t $SESSION_NAME:memory \
    "echo 'Procedural Memory: OPTIMIZING'" C-m

# Create task orchestrator
echo -e "${GREEN}📋 Setting up Task Orchestrator...${NC}"
tmux new-window -t $SESSION_NAME -n task-orchestrator
tmux send-keys -t $SESSION_NAME:task-orchestrator \
    "echo '📋 TASK ORCHESTRATOR'" C-m
tmux send-keys -t $SESSION_NAME:task-orchestrator \
    "echo 'Mode: AUTONOMOUS TASK MANAGEMENT'" C-m
tmux send-keys -t $SESSION_NAME:task-orchestrator \
    "echo 'Status: READY FOR COMPLEX WORKFLOWS'" C-m

# Create performance monitor
echo -e "${GREEN}📊 Starting Performance Monitor...${NC}"
tmux new-window -t $SESSION_NAME -n monitor
tmux send-keys -t $SESSION_NAME:monitor \
    "echo '📊 PERFORMANCE MONITOR'" C-m
tmux send-keys -t $SESSION_NAME:monitor \
    "echo 'Real-time Brain Metrics:'" C-m
tmux send-keys -t $SESSION_NAME:monitor \
    "echo '  Session Uptime: $(date)'" C-m
tmux send-keys -t $SESSION_NAME:monitor \
    "echo '  Windows Active: Monitoring...'" C-m
tmux send-keys -t $SESSION_NAME:monitor \
    "echo '  Learning Status: ACTIVE'" C-m

# Create ultra-think chamber
echo -e "${GREEN}🧠 Setting up Ultra-Think Chamber...${NC}"
tmux new-window -t $SESSION_NAME -n ultra-think
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo '🧠 ULTRA-THINK CHAMBER'" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo 'Mode: MAXIMUM REASONING POWER'" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo 'Status: READY FOR DEEP ANALYSIS'" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo 'Cognitive Modes Available:'" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo '  🔬 Deep Analysis'" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo '  ⚡ Quick Response'" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo '  🎨 Creative Synthesis'" C-m

# Initialize learning engine
echo -e "${GREEN}📈 Initializing Learning Engine...${NC}"

# Create learning engine status
echo "ACTIVE" > "$LEARNING_ENGINE/status"
echo "$(date): Enhanced Brain session started" > "$LEARNING_ENGINE/sessions/session_$(date +%Y%m%d_%H%M%S).log"

# Create learning dashboard if not exists
if ! tmux list-windows -t $SESSION_NAME | grep -q "learning-dashboard"; then
    tmux new-window -t $SESSION_NAME -n learning-dashboard
    tmux send-keys -t $SESSION_NAME:learning-dashboard \
        "echo '📈 LEARNING DASHBOARD'" C-m
    tmux send-keys -t $SESSION_NAME:learning-dashboard \
        "echo 'System-wide Learning: ACTIVE'" C-m
    tmux send-keys -t $SESSION_NAME:learning-dashboard \
        "echo 'Pattern Recognition: ENABLED'" C-m
    tmux send-keys -t $SESSION_NAME:learning-dashboard \
        "echo 'Auto-optimization: RUNNING'" C-m
    tmux send-keys -t $SESSION_NAME:learning-dashboard \
        "echo ''" C-m
    tmux send-keys -t $SESSION_NAME:learning-dashboard \
        "echo 'Learning Metrics:'" C-m
    tmux send-keys -t $SESSION_NAME:learning-dashboard \
        "echo '  Patterns: 0 (Starting)'" C-m
    tmux send-keys -t $SESSION_NAME:learning-dashboard \
        "echo '  Sessions: 1 (Current)'" C-m
    tmux send-keys -t $SESSION_NAME:learning-dashboard \
        "echo '  Optimizations: 0 (Learning)'" C-m
fi

# Start learning observers in background
if [ -f "$BRAIN_DIR/learning-engine/observers/session_observer.py" ]; then
    echo -e "${MAGENTA}🔍 Starting Learning Observers...${NC}"
    nohup python3 "$BRAIN_DIR/learning-engine/observers/session_observer.py" > "$LEARNING_ENGINE/logs/observer.log" 2>&1 &
    echo $! > "$LEARNING_ENGINE/observer.pid"
fi

# Return to control center
tmux select-window -t $SESSION_NAME:control-center

echo -e "${GREEN}✅ Enhanced Brain Session Ready!${NC}"
echo -e "${CYAN}Session: $SESSION_NAME${NC}"
echo -e "${YELLOW}Windows Created:${NC}"
echo -e "${BLUE}  🎯 control-center     - Main command center${NC}"
echo -e "${BLUE}  💻 compute-hub        - Multi-model intelligence${NC}"
echo -e "${BLUE}  🔌 mcp-servers        - Tool integration${NC}"
echo -e "${BLUE}  🤖 agents             - Multi-agent coordination${NC}"
echo -e "${BLUE}  💾 memory             - Memory systems${NC}"
echo -e "${BLUE}  📋 task-orchestrator  - Autonomous workflows${NC}"
echo -e "${BLUE}  📊 monitor            - Performance metrics${NC}"
echo -e "${BLUE}  🧠 ultra-think        - Maximum reasoning${NC}"
echo -e "${BLUE}  📈 learning-dashboard - Learning intelligence${NC}"
echo ""
echo -e "${MAGENTA}🚀 Ready for autonomous operation!${NC}"
echo -e "${CYAN}Connect with: tmux attach-session -t $SESSION_NAME${NC}"
echo -e "${YELLOW}Or use: brain attach${NC}"