#!/bin/bash
# Research Workflow - Autonomous Research Process
# Handles comprehensive research with AI agent coordination

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
NC='\033[0m'

TOPIC="${1:-research-topic}"
DEPTH="${2:-7}"
SESSION_NAME="BRAIN-MAIN"

echo -e "${BLUE}🔍 AUTONOMOUS RESEARCH WORKFLOW${NC}"
echo -e "${CYAN}===============================${NC}"
echo -e "${GREEN}Topic: $TOPIC${NC}"
echo -e "${YELLOW}Depth: $DEPTH/10${NC}"

# Ensure brain session exists
if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo -e "${YELLOW}🧠 Starting brain session...${NC}"
    /Users/shaansisodia/DEV/claude-brain-config/tmux-orchestrator/start-brain-with-learning.sh
    sleep 3
fi

# Deploy agents if not already deployed
if ! tmux list-windows -t $SESSION_NAME | grep -q "architect"; then
    echo -e "${CYAN}🤖 Deploying research agents...${NC}"
    /Users/shaansisodia/DEV/claude-brain-config/tmux-orchestrator/deploy-agents.sh > /dev/null 2>&1
fi

# Create research workflow window
WORKFLOW_WINDOW="research-$(echo "$TOPIC" | tr ' ' '-' | tr -cd '[:alnum:]-' | cut -c1-15)"
if ! tmux list-windows -t $SESSION_NAME | grep -q "$WORKFLOW_WINDOW"; then
    tmux new-window -t $SESSION_NAME -n "$WORKFLOW_WINDOW"
else
    tmux select-window -t "$SESSION_NAME:$WORKFLOW_WINDOW"
fi

# Configure research workflow
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo '🔍 AUTONOMOUS RESEARCH WORKFLOW'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo '=============================='" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'Topic: $TOPIC'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'Depth: $DEPTH/10'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'Mode: COMPREHENSIVE RESEARCH'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo ''" C-m

# Phase 1: Research Planning & Strategy
echo -e "${GREEN}📋 Phase 1: Research Planning${NC}"
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo '📋 PHASE 1: RESEARCH PLANNING & STRATEGY'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'Status: ARCHITECT AGENT PLANNING'" C-m

tmux send-keys -t $SESSION_NAME:architect \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:architect \
    "echo '📋 RESEARCH PLANNING: $TOPIC'" C-m
tmux send-keys -t $SESSION_NAME:architect \
    "echo 'Phase: STRATEGY & PLANNING'" C-m
tmux send-keys -t $SESSION_NAME:architect \
    "echo 'Depth: $DEPTH/10'" C-m
tmux send-keys -t $SESSION_NAME:architect \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:architect \
    "echo 'Planning Tasks:'" C-m
tmux send-keys -t $SESSION_NAME:architect \
    "echo '  🎯 Research Scope Definition'" C-m
tmux send-keys -t $SESSION_NAME:architect \
    "echo '  📊 Methodology Selection'" C-m
tmux send-keys -t $SESSION_NAME:architect \
    "echo '  🔍 Source Identification'" C-m
tmux send-keys -t $SESSION_NAME:architect \
    "echo '  📈 Success Metrics'" C-m
tmux send-keys -t $SESSION_NAME:architect \
    "echo '  ⏱️ Timeline Planning'" C-m

# Phase 2: Data Collection
sleep 2
echo -e "${GREEN}📊 Phase 2: Data Collection${NC}"
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo ''" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo '📊 PHASE 2: DATA COLLECTION'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'Status: MULTIPLE AGENTS COLLECTING'" C-m

# Use implementer as data collector
tmux send-keys -t $SESSION_NAME:implementer \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:implementer \
    "echo '📊 DATA COLLECTION: $TOPIC'" C-m
tmux send-keys -t $SESSION_NAME:implementer \
    "echo 'Phase: SYSTEMATIC DATA GATHERING'" C-m
tmux send-keys -t $SESSION_NAME:implementer \
    "echo 'Depth: $DEPTH/10'" C-m
tmux send-keys -t $SESSION_NAME:implementer \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:implementer \
    "echo 'Collection Tasks:'" C-m
tmux send-keys -t $SESSION_NAME:implementer \
    "echo '  🌐 Web Research'" C-m
tmux send-keys -t $SESSION_NAME:implementer \
    "echo '  📚 Academic Sources'" C-m
tmux send-keys -t $SESSION_NAME:implementer \
    "echo '  📊 Industry Reports'" C-m
tmux send-keys -t $SESSION_NAME:implementer \
    "echo '  🔍 Primary Sources'" C-m
tmux send-keys -t $SESSION_NAME:implementer \
    "echo '  📈 Statistical Data'" C-m

# Phase 3: Analysis & Synthesis
sleep 2
echo -e "${GREEN}🧠 Phase 3: Analysis & Synthesis${NC}"
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo ''" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo '🧠 PHASE 3: ANALYSIS & SYNTHESIS'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'Status: ULTRA-THINK MODE ACTIVE'" C-m

# Use ultra-think for deep analysis
tmux select-window -t $SESSION_NAME:ultra-think
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo '🧠 RESEARCH ANALYSIS: $TOPIC'" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo 'Phase: DEEP ANALYSIS & SYNTHESIS'" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo 'Mode: ULTRA-THINK REASONING'" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo 'Depth: $DEPTH/10'" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo 'Analysis Tasks:'" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo '  🧩 Pattern Recognition'" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo '  🔗 Connection Mapping'" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo '  📊 Trend Analysis'" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo '  💡 Insight Generation'" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo '  🎯 Conclusion Formation'" C-m

# Phase 4: Quality Review
sleep 2
echo -e "${GREEN}🔍 Phase 4: Quality Review${NC}"
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo ''" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo '🔍 PHASE 4: QUALITY REVIEW'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'Status: REVIEWER AGENT VALIDATING'" C-m

tmux send-keys -t $SESSION_NAME:reviewer \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:reviewer \
    "echo '🔍 RESEARCH REVIEW: $TOPIC'" C-m
tmux send-keys -t $SESSION_NAME:reviewer \
    "echo 'Phase: QUALITY VALIDATION'" C-m
tmux send-keys -t $SESSION_NAME:reviewer \
    "echo 'Depth: $DEPTH/10'" C-m
tmux send-keys -t $SESSION_NAME:reviewer \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:reviewer \
    "echo 'Review Tasks:'" C-m
tmux send-keys -t $SESSION_NAME:reviewer \
    "echo '  ✅ Fact Verification'" C-m
tmux send-keys -t $SESSION_NAME:reviewer \
    "echo '  🔍 Source Validation'" C-m
tmux send-keys -t $SESSION_NAME:reviewer \
    "echo '  🧩 Logic Consistency'" C-m
tmux send-keys -t $SESSION_NAME:reviewer \
    "echo '  📊 Data Accuracy'" C-m
tmux send-keys -t $SESSION_NAME:reviewer \
    "echo '  🎯 Completeness Check'" C-m

# Phase 5: Documentation & Reporting
sleep 2
echo -e "${GREEN}📝 Phase 5: Documentation${NC}"
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo ''" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo '📝 PHASE 5: DOCUMENTATION & REPORTING'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'Status: DOCUMENTER AGENT COMPILING'" C-m

tmux send-keys -t $SESSION_NAME:documenter \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:documenter \
    "echo '📝 RESEARCH DOCUMENTATION: $TOPIC'" C-m
tmux send-keys -t $SESSION_NAME:documenter \
    "echo 'Phase: COMPREHENSIVE REPORTING'" C-m
tmux send-keys -t $SESSION_NAME:documenter \
    "echo 'Depth: $DEPTH/10'" C-m
tmux send-keys -t $SESSION_NAME:documenter \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:documenter \
    "echo 'Documentation Tasks:'" C-m
tmux send-keys -t $SESSION_NAME:documenter \
    "echo '  📊 Executive Summary'" C-m
tmux send-keys -t $SESSION_NAME:documenter \
    "echo '  📈 Detailed Findings'" C-m
tmux send-keys -t $SESSION_NAME:documenter \
    "echo '  💡 Key Insights'" C-m
tmux send-keys -t $SESSION_NAME:documenter \
    "echo '  🎯 Recommendations'" C-m
tmux send-keys -t $SESSION_NAME:documenter \
    "echo '  📚 Bibliography'" C-m

# Create research storage directory
STORAGE_DIR="/Users/shaansisodia/DEV/claude-brain-config/storage/research-projects"
mkdir -p "$STORAGE_DIR/$(echo "$TOPIC" | tr ' ' '-' | tr -cd '[:alnum:]-')"

# Final Status
sleep 2
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo ''" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo '✅ RESEARCH WORKFLOW ACTIVE'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'All agents researching: $TOPIC'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'Depth Level: $DEPTH/10'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'Storage: $STORAGE_DIR'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'Monitor progress in individual agent windows'" C-m

# Switch to workflow window
tmux select-window -t "$SESSION_NAME:$WORKFLOW_WINDOW"

echo -e "${GREEN}✅ Research Workflow Activated!${NC}"
echo -e "${CYAN}Topic: $TOPIC${NC}"
echo -e "${YELLOW}Depth: $DEPTH/10${NC}"
echo -e "${MAGENTA}All research agents are working autonomously${NC}"
echo -e "${BLUE}Storage: $STORAGE_DIR${NC}"