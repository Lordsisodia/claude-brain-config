#!/bin/bash
# TMUX BRAIN ORCHESTRATOR - Master Startup Script
# Enhanced with Global Brain Intelligence

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
export TMUX_BRAIN_HOME="${TMUX_BRAIN_HOME:-$HOME/.tmux-brain}"
export CLAUDE_CONFIG="${CLAUDE_CONFIG:-$HOME/.claude/CLAUDE.md}"
export THINKING_MODE="MUSK_5_STEP"
export COMPUTE_MODE="10X_ENHANCED"
export REASONING_ENGINE="ULTRA_THINK"

# Create directory structure
echo -e "${BLUE}🧠 Initializing TMUX Brain Environment...${NC}"
mkdir -p "$TMUX_BRAIN_HOME"/{memory,logs,metrics,modes,scripts,config}
mkdir -p "$TMUX_BRAIN_HOME"/memory/{episodic,semantic,procedural,working}

# Check if brain session already exists
if tmux has-session -t BRAIN-MAIN 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Brain session already exists. Attaching...${NC}"
    tmux attach-session -t BRAIN-MAIN
    exit 0
fi

echo -e "${GREEN}🚀 Starting TMUX BRAIN ORCHESTRATOR v3.0${NC}"

# Start main brain session
tmux new-session -d -s BRAIN-MAIN -n "control-center"

# Set environment variables
tmux send-keys -t BRAIN-MAIN:control-center \
  "export TMUX_BRAIN_HOME='$TMUX_BRAIN_HOME'" C-m
tmux send-keys -t BRAIN-MAIN:control-center \
  "export THINKING_MODE='$THINKING_MODE'" C-m
tmux send-keys -t BRAIN-MAIN:control-center \
  "export COMPUTE_MODE='$COMPUTE_MODE'" C-m
tmux send-keys -t BRAIN-MAIN:control-center \
  "export REASONING_ENGINE='$REASONING_ENGINE'" C-m

# Initialize Musk's 5-Step Algorithm
echo -e "${CYAN}📋 Initializing Musk's 5-Step Algorithm...${NC}"
tmux send-keys -t BRAIN-MAIN:control-center \
  "echo '🧠 MUSK 5-STEP ALGORITHM ACTIVE'" C-m
tmux send-keys -t BRAIN-MAIN:control-center \
  "echo '1. Question Requirements'" C-m
tmux send-keys -t BRAIN-MAIN:control-center \
  "echo '2. Delete/Simplify'" C-m
tmux send-keys -t BRAIN-MAIN:control-center \
  "echo '3. Optimize/Accelerate'" C-m
tmux send-keys -t BRAIN-MAIN:control-center \
  "echo '4. Automate'" C-m
tmux send-keys -t BRAIN-MAIN:control-center \
  "echo '5. Iterate'" C-m

# Window 2: Multi-Model Compute Hub
echo -e "${MAGENTA}🔮 Setting up Multi-Model Compute Hub...${NC}"
tmux new-window -t BRAIN-MAIN -n "compute-hub"
tmux send-keys -t BRAIN-MAIN:compute-hub \
  "echo '🔮 MULTI-MODEL COMPUTE HUB'" C-m
tmux send-keys -t BRAIN-MAIN:compute-hub \
  "echo 'Available Models:'" C-m
tmux send-keys -t BRAIN-MAIN:compute-hub \
  "echo '  • Opus 4.1 (Complex Reasoning)'" C-m
tmux send-keys -t BRAIN-MAIN:compute-hub \
  "echo '  • Sonnet (Code Generation)'" C-m
tmux send-keys -t BRAIN-MAIN:compute-hub \
  "echo '  • Haiku (Quick Responses)'" C-m
tmux send-keys -t BRAIN-MAIN:compute-hub \
  "echo '  • Local Ollama (Background)'" C-m

# Window 3: MCP Server Orchestra
echo -e "${GREEN}🔌 Launching MCP Server Orchestra...${NC}"
tmux new-window -t BRAIN-MAIN -n "mcp-servers"
tmux split-window -h -t BRAIN-MAIN:mcp-servers
tmux split-window -v -t BRAIN-MAIN:mcp-servers.0
tmux split-window -v -t BRAIN-MAIN:mcp-servers.1

# Label MCP panes
tmux send-keys -t BRAIN-MAIN:mcp-servers.0 \
  "echo '🗄️ MCP: Supabase Database'" C-m
tmux send-keys -t BRAIN-MAIN:mcp-servers.1 \
  "echo '📝 MCP: Notion Docs'" C-m
tmux send-keys -t BRAIN-MAIN:mcp-servers.2 \
  "echo '🔍 MCP: Exa Research'" C-m
tmux send-keys -t BRAIN-MAIN:mcp-servers.3 \
  "echo '💻 MCP: Desktop Commander'" C-m

# Window 4: Agent Deployment Center
echo -e "${YELLOW}🤖 Deploying Multi-Agent System...${NC}"
tmux new-window -t BRAIN-MAIN -n "agents"
tmux split-window -h -t BRAIN-MAIN:agents
tmux split-window -v -t BRAIN-MAIN:agents.0
tmux split-window -v -t BRAIN-MAIN:agents.1

# Deploy agents
tmux send-keys -t BRAIN-MAIN:agents.0 \
  "echo '🏗️ Agent: Architect (System Design)'" C-m
tmux send-keys -t BRAIN-MAIN:agents.1 \
  "echo '💻 Agent: Implementer (Code Generation)'" C-m
tmux send-keys -t BRAIN-MAIN:agents.2 \
  "echo '🔍 Agent: Reviewer (Quality Assurance)'" C-m
tmux send-keys -t BRAIN-MAIN:agents.3 \
  "echo '🧪 Agent: Tester (Validation)'" C-m

# Window 5: Memory & Learning System
echo -e "${BLUE}💾 Initializing Memory Systems...${NC}"
tmux new-window -t BRAIN-MAIN -n "memory"
tmux send-keys -t BRAIN-MAIN:memory \
  "echo '💾 MEMORY SYSTEMS ONLINE'" C-m
tmux send-keys -t BRAIN-MAIN:memory \
  "echo '  • Working Memory: Active'" C-m
tmux send-keys -t BRAIN-MAIN:memory \
  "echo '  • Episodic Memory: Recording'" C-m
tmux send-keys -t BRAIN-MAIN:memory \
  "echo '  • Semantic Memory: Learning'" C-m
tmux send-keys -t BRAIN-MAIN:memory \
  "echo '  • Procedural Memory: Optimizing'" C-m

# Window 6: Task Orchestrator
echo -e "${CYAN}📋 Starting Task Orchestrator...${NC}"
tmux new-window -t BRAIN-MAIN -n "task-orchestrator"
tmux send-keys -t BRAIN-MAIN:task-orchestrator \
  "echo '📋 TASK ORCHESTRATOR'" C-m
tmux send-keys -t BRAIN-MAIN:task-orchestrator \
  "echo 'Mode: Intelligent Decomposition'" C-m
tmux send-keys -t BRAIN-MAIN:task-orchestrator \
  "echo 'Batch Size: 5-10 tasks'" C-m
tmux send-keys -t BRAIN-MAIN:task-orchestrator \
  "echo 'Execution: Parallel'" C-m

# Window 7: Performance Monitor
echo -e "${MAGENTA}📊 Starting Performance Monitor...${NC}"
tmux new-window -t BRAIN-MAIN -n "monitor"
tmux split-window -h -t BRAIN-MAIN:monitor
tmux split-window -v -t BRAIN-MAIN:monitor.0
tmux split-window -v -t BRAIN-MAIN:monitor.1

# Set up monitoring panes
tmux send-keys -t BRAIN-MAIN:monitor.0 \
  "echo '📊 TOKEN USAGE MONITOR'" C-m
tmux send-keys -t BRAIN-MAIN:monitor.1 \
  "echo '🤖 AGENT STATUS'" C-m
tmux send-keys -t BRAIN-MAIN:monitor.2 \
  "echo '💾 MEMORY USAGE'" C-m
tmux send-keys -t BRAIN-MAIN:monitor.3 \
  "echo '⚡ PERFORMANCE METRICS'" C-m

# Window 8: Ultra Think Chamber
echo -e "${RED}🧠 Creating Ultra Think Chamber...${NC}"
tmux new-window -t BRAIN-MAIN -n "ultra-think"
tmux send-keys -t BRAIN-MAIN:ultra-think \
  "echo '🧠 ULTRA THINK CHAMBER'" C-m
tmux send-keys -t BRAIN-MAIN:ultra-think \
  "echo 'Mode: 10x Reasoning Power'" C-m
tmux send-keys -t BRAIN-MAIN:ultra-think \
  "echo 'Token Allocation: MAXIMUM'" C-m
tmux send-keys -t BRAIN-MAIN:ultra-think \
  "echo 'Ready for deep reasoning tasks...'" C-m

# Create status file
echo "ACTIVE" > "$TMUX_BRAIN_HOME/status"
echo "$(date)" > "$TMUX_BRAIN_HOME/last_start"

# Final setup message
echo -e "${GREEN}✅ TMUX BRAIN ORCHESTRATOR Started Successfully!${NC}"
echo -e "${CYAN}📍 Session: BRAIN-MAIN${NC}"
echo -e "${YELLOW}💡 Tip: Use 'tmux attach -t BRAIN-MAIN' to connect${NC}"
echo -e "${MAGENTA}🚀 Brain Power: FULLY ACTIVATED${NC}"

# Auto-attach if not in tmux already
if [ -z "$TMUX" ]; then
    echo -e "${BLUE}🔗 Attaching to brain session...${NC}"
    sleep 1
    tmux attach-session -t BRAIN-MAIN
else
    echo -e "${YELLOW}⚠️  Already in tmux. Use prefix+s to switch to BRAIN-MAIN${NC}"
fi