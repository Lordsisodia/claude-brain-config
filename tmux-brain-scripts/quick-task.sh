#!/bin/bash
# Quick Task Launcher with Cognitive Mode Selection

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Parse arguments
TASK="${1:-}"
COMPLEXITY="${2:-5}"
MODE="${3:-auto}"

# Show usage if no task provided
if [ -z "$TASK" ]; then
    echo -e "${YELLOW}Usage: $0 <task> [complexity:1-10] [mode]${NC}"
    echo -e "${CYAN}Modes: auto, deep-analysis, quick-response, creative, ultra-think${NC}"
    echo -e "${GREEN}Example: $0 'implement auth system' 7 deep-analysis${NC}"
    exit 1
fi

# Auto-detect cognitive mode based on complexity
if [ "$MODE" = "auto" ]; then
    if [ "$COMPLEXITY" -ge 8 ]; then
        MODE="ultra-think"
    elif [ "$COMPLEXITY" -ge 6 ]; then
        MODE="deep-analysis"
    elif [ "$COMPLEXITY" -le 3 ]; then
        MODE="quick-response"
    else
        MODE="balanced"
    fi
fi

echo -e "${BLUE}🚀 Launching Task: ${TASK}${NC}"
echo -e "${MAGENTA}📊 Complexity: ${COMPLEXITY}/10${NC}"
echo -e "${CYAN}🧠 Cognitive Mode: ${MODE}${NC}"

# Ensure brain session exists
if ! tmux has-session -t BRAIN-MAIN 2>/dev/null; then
    echo -e "${YELLOW}Starting brain session first...${NC}"
    $(dirname "$0")/start-brain.sh &
    sleep 3
fi

# Generate unique window name
WINDOW_NAME="task-$(date +%s)"

# Create task window with appropriate configuration
case "$MODE" in
    "ultra-think")
        tmux new-window -t BRAIN-MAIN -n "$WINDOW_NAME" \; \
            send-keys "echo '🧠 ULTRA THINK MODE ACTIVATED'" C-m \; \
            send-keys "export COGNITIVE_MODE='ULTRA_THINK'" C-m \; \
            send-keys "export REASONING_TOKENS='MAXIMUM'" C-m \; \
            send-keys "export THINKING_DEPTH='DEEPEST'" C-m \; \
            send-keys "# Task: $TASK" C-m \; \
            send-keys "# Applying maximum reasoning power..." C-m
        ;;
    
    "deep-analysis")
        tmux new-window -t BRAIN-MAIN -n "$WINDOW_NAME" \; \
            split-window -h -p 30 \; \
            send-keys -t 0 "echo '🔍 DEEP ANALYSIS MODE'" C-m \; \
            send-keys -t 0 "export COGNITIVE_MODE='DEEP_ANALYSIS'" C-m \; \
            send-keys -t 0 "export VERIFICATION='ENABLED'" C-m \; \
            send-keys -t 0 "# Task: $TASK" C-m \; \
            send-keys -t 1 "echo '📊 Analysis Monitor'" C-m
        ;;
    
    "quick-response")
        tmux new-window -t BRAIN-MAIN -n "$WINDOW_NAME" \; \
            send-keys "echo '⚡ QUICK RESPONSE MODE'" C-m \; \
            send-keys "export COGNITIVE_MODE='QUICK_RESPONSE'" C-m \; \
            send-keys "export TOKEN_BUDGET='MINIMAL'" C-m \; \
            send-keys "# Task: $TASK" C-m \; \
            send-keys "# Optimizing for speed..." C-m
        ;;
    
    "creative")
        tmux new-window -t BRAIN-MAIN -n "$WINDOW_NAME" \; \
            split-window -v -p 50 \; \
            send-keys -t 0 "echo '🎨 CREATIVE SYNTHESIS MODE'" C-m \; \
            send-keys -t 0 "export COGNITIVE_MODE='CREATIVE'" C-m \; \
            send-keys -t 0 "export THINKING='DIVERGENT'" C-m \; \
            send-keys -t 1 "echo '💡 Brainstorming Panel'" C-m \; \
            send-keys -t 1 "# Ideas and connections..." C-m
        ;;
    
    *)
        tmux new-window -t BRAIN-MAIN -n "$WINDOW_NAME" \; \
            send-keys "echo '⚖️ BALANCED MODE'" C-m \; \
            send-keys "export COGNITIVE_MODE='BALANCED'" C-m \; \
            send-keys "# Task: $TASK" C-m
        ;;
esac

# Apply Musk's 5-step algorithm
tmux send-keys -t "BRAIN-MAIN:$WINDOW_NAME" \
    "# Applying Musk's 5-Step Algorithm:" C-m \
    "# 1. Question: Is this requirement necessary?" C-m \
    "# 2. Delete: What can be simplified?" C-m \
    "# 3. Optimize: How to make this faster?" C-m \
    "# 4. Automate: What can be scripted?" C-m \
    "# 5. Iterate: Continuous improvement" C-m

# Log task initiation
TMUX_BRAIN_HOME="${TMUX_BRAIN_HOME:-$HOME/.tmux-brain}"
mkdir -p "$TMUX_BRAIN_HOME/logs"
echo "[$(date)] Task: $TASK | Complexity: $COMPLEXITY | Mode: $MODE" >> "$TMUX_BRAIN_HOME/logs/tasks.log"

# Switch to the new window
tmux select-window -t "BRAIN-MAIN:$WINDOW_NAME"

echo -e "${GREEN}✅ Task launched in window: $WINDOW_NAME${NC}"
echo -e "${YELLOW}💡 Switching to BRAIN-MAIN session...${NC}"

# Attach if not in tmux
if [ -z "$TMUX" ]; then
    tmux attach-session -t BRAIN-MAIN
fi