#!/bin/bash
# Quick Task Execution System
# Handles rapid cognitive mode switching for tasks

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Parameters
TASK="$1"
COMPLEXITY="${2:-6}"
MODE="${3:-auto}"
SESSION_NAME="BRAIN-MAIN"

if [ -z "$TASK" ]; then
    echo -e "${RED}❌ No task specified${NC}"
    echo -e "${CYAN}Usage: quick-task.sh 'task description' [complexity 1-10] [mode]${NC}"
    echo -e "${YELLOW}Modes: ultra-think, deep-analysis, quick-response, creative${NC}"
    exit 1
fi

echo -e "${BLUE}🧠 QUICK TASK EXECUTION${NC}"
echo -e "${CYAN}======================${NC}"
echo -e "${GREEN}Task: $TASK${NC}"
echo -e "${YELLOW}Complexity: $COMPLEXITY/10${NC}"
echo -e "${MAGENTA}Mode: $MODE${NC}"

# Check if brain session exists
if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo -e "${YELLOW}🧠 Starting brain session...${NC}"
    /Users/shaansisodia/DEV/claude-brain-config/tmux-orchestrator/start-brain-with-learning.sh
    sleep 3
fi

# Determine optimal cognitive mode based on complexity and mode
if [ "$MODE" = "auto" ]; then
    if [ "$COMPLEXITY" -ge 8 ]; then
        MODE="ultra-think"
    elif [ "$COMPLEXITY" -ge 6 ]; then
        MODE="deep-analysis"
    elif [ "$COMPLEXITY" -ge 4 ]; then
        MODE="quick-response"
    else
        MODE="quick-response"
    fi
    echo -e "${CYAN}🤖 Auto-selected mode: $MODE${NC}"
fi

# Create or switch to task-specific window
TASK_WINDOW="task-$(echo "$TASK" | tr ' ' '-' | tr -cd '[:alnum:]-' | cut -c1-20)"

# Create task window if it doesn't exist
if ! tmux list-windows -t $SESSION_NAME | grep -q "$TASK_WINDOW"; then
    tmux new-window -t $SESSION_NAME -n "$TASK_WINDOW"
else
    tmux select-window -t "$SESSION_NAME:$TASK_WINDOW"
fi

# Configure task environment based on mode
case "$MODE" in
    "ultra-think")
        echo -e "${MAGENTA}🧠 Activating Ultra-Think Mode...${NC}"
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '🧠 ULTRA-THINK MODE ACTIVATED'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '============================'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo 'Task: $TASK'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo 'Complexity: $COMPLEXITY/10 (Ultra-Think Required)'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo 'Mode: MAXIMUM REASONING POWER'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo ''" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo 'Ultra-Think Process:'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '  1. 🎯 Problem Analysis'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '  2. 🔍 Constraint Identification'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '  3. 💡 Solution Generation'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '  4. ⚖️ Option Evaluation'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '  5. ✅ Solution Selection'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '  6. 🔬 Verification'" C-m
        ;;
    "deep-analysis")
        echo -e "${BLUE}🔬 Activating Deep Analysis Mode...${NC}"
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '🔬 DEEP ANALYSIS MODE'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '=================='" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo 'Task: $TASK'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo 'Complexity: $COMPLEXITY/10 (Deep Analysis)'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo 'Mode: SYSTEMATIC REASONING'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo ''" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo 'Analysis Framework:'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '  📊 Data Gathering'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '  🧩 Pattern Recognition'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '  🎯 Solution Design'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '  ✅ Validation'" C-m
        ;;
    "quick-response")
        echo -e "${GREEN}⚡ Activating Quick Response Mode...${NC}"
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '⚡ QUICK RESPONSE MODE'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '==================='" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo 'Task: $TASK'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo 'Complexity: $COMPLEXITY/10 (Quick Response)'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo 'Mode: EFFICIENT EXECUTION'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo ''" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo 'Quick Process:'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '  🎯 Identify Core Problem'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '  💡 Apply Best Practice'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '  ⚡ Execute Solution'" C-m
        ;;
    "creative")
        echo -e "${YELLOW}🎨 Activating Creative Synthesis Mode...${NC}"
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '🎨 CREATIVE SYNTHESIS MODE'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '========================='" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo 'Task: $TASK'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo 'Complexity: $COMPLEXITY/10 (Creative Mode)'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo 'Mode: INNOVATIVE THINKING'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo ''" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo 'Creative Process:'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '  🌟 Brainstorm Ideas'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '  🔗 Find Novel Connections'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '  🎯 Synthesize Solutions'" C-m
        tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
            "echo '  💡 Innovate & Experiment'" C-m
        ;;
esac

# Add task status indicators
tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
    "echo ''" C-m
tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
    "echo '📋 Task Status: READY FOR EXECUTION'" C-m
tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
    "echo '🕒 Started: $(date)'" C-m
tmux send-keys -t "$SESSION_NAME:$TASK_WINDOW" \
    "echo '🧠 Cognitive Mode: $MODE'" C-m

# Log task execution
LEARNING_ENGINE="$HOME/.learning-engine"
mkdir -p "$LEARNING_ENGINE/tasks"
echo "$(date): Task '$TASK' | Complexity: $COMPLEXITY | Mode: $MODE" >> "$LEARNING_ENGINE/tasks/task_log.txt"

# Switch to the task window
tmux select-window -t "$SESSION_NAME:$TASK_WINDOW"

echo -e "${GREEN}✅ Task Environment Ready!${NC}"
echo -e "${CYAN}Window: $TASK_WINDOW${NC}"
echo -e "${YELLOW}Access with: tmux select-window -t $SESSION_NAME:$TASK_WINDOW${NC}"
echo -e "${MAGENTA}Or use: brain_nav $TASK_WINDOW${NC}"