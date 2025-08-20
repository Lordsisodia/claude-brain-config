#!/bin/bash
# Problem Solving Workflow - Autonomous Problem Resolution
# Handles complex problem solving with multi-agent coordination

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
NC='\033[0m'

PROBLEM="${1:-complex-problem}"
COMPLEXITY="${2:-8}"
SESSION_NAME="BRAIN-MAIN"

echo -e "${BLUE}🎯 AUTONOMOUS PROBLEM SOLVING WORKFLOW${NC}"
echo -e "${CYAN}====================================${NC}"
echo -e "${GREEN}Problem: $PROBLEM${NC}"
echo -e "${YELLOW}Complexity: $COMPLEXITY/10${NC}"

# Ensure brain session exists
if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo -e "${YELLOW}🧠 Starting brain session...${NC}"
    /Users/shaansisodia/DEV/claude-brain-config/tmux-orchestrator/start-brain-with-learning.sh
    sleep 3
fi

# Deploy agents if not already deployed
if ! tmux list-windows -t $SESSION_NAME | grep -q "architect"; then
    echo -e "${CYAN}🤖 Deploying problem-solving agents...${NC}"
    /Users/shaansisodia/DEV/claude-brain-config/tmux-orchestrator/deploy-agents.sh > /dev/null 2>&1
fi

# Create problem-solving workflow window
WORKFLOW_WINDOW="solve-$(echo "$PROBLEM" | tr ' ' '-' | tr -cd '[:alnum:]-' | cut -c1-15)"
if ! tmux list-windows -t $SESSION_NAME | grep -q "$WORKFLOW_WINDOW"; then
    tmux new-window -t $SESSION_NAME -n "$WORKFLOW_WINDOW"
else
    tmux select-window -t "$SESSION_NAME:$WORKFLOW_WINDOW"
fi

# Configure problem-solving workflow
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo '🎯 AUTONOMOUS PROBLEM SOLVING WORKFLOW'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo '==================================='" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'Problem: $PROBLEM'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'Complexity: $COMPLEXITY/10'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'Mode: SYSTEMATIC PROBLEM RESOLUTION'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo ''" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'Framework: MUSK'\''s 5-Step Algorithm'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo '  1. 🎯 Question Requirements'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo '  2. 🗑️ Delete/Simplify'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo '  3. ⚡ Optimize/Accelerate'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo '  4. 🤖 Automate'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo '  5. 🔄 Iterate'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo ''" C-m

# Step 1: Question Requirements (Ultra-Think Mode)
echo -e "${GREEN}🎯 Step 1: Question Requirements${NC}"
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo '🎯 STEP 1: QUESTION REQUIREMENTS'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'Status: ULTRA-THINK MODE ACTIVATED'" C-m

tmux select-window -t $SESSION_NAME:ultra-think
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo '🎯 QUESTIONING REQUIREMENTS: $PROBLEM'" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo 'Step: 1/5 - REQUIREMENTS ANALYSIS'" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo 'Mode: ULTRA-THINK REASONING'" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo 'Complexity: $COMPLEXITY/10'" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo 'Critical Questions:'" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo '  ❓ What is the REAL problem?'" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo '  ❓ Are these requirements actually needed?'" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo '  ❓ What assumptions are we making?'" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo '  ❓ What would happen if we did nothing?'" C-m
tmux send-keys -t $SESSION_NAME:ultra-think \
    "echo '  ❓ Who benefits from solving this?'" C-m

# Step 2: Delete/Simplify (Architect)
sleep 3
echo -e "${GREEN}🗑️ Step 2: Delete/Simplify${NC}"
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo ''" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo '🗑️ STEP 2: DELETE/SIMPLIFY'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'Status: ARCHITECT AGENT SIMPLIFYING'" C-m

tmux send-keys -t $SESSION_NAME:architect \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:architect \
    "echo '🗑️ SIMPLIFICATION: $PROBLEM'" C-m
tmux send-keys -t $SESSION_NAME:architect \
    "echo 'Step: 2/5 - DELETE & SIMPLIFY'" C-m
tmux send-keys -t $SESSION_NAME:architect \
    "echo 'Complexity: $COMPLEXITY/10'" C-m
tmux send-keys -t $SESSION_NAME:architect \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:architect \
    "echo 'Simplification Tasks:'" C-m
tmux send-keys -t $SESSION_NAME:architect \
    "echo '  ✂️ Remove unnecessary complexity'" C-m
tmux send-keys -t $SESSION_NAME:architect \
    "echo '  🎯 Focus on core problem'" C-m
tmux send-keys -t $SESSION_NAME:architect \
    "echo '  📐 Simplify constraints'" C-m
tmux send-keys -t $SESSION_NAME:architect \
    "echo '  🔍 Identify minimal viable solution'" C-m
tmux send-keys -t $SESSION_NAME:architect \
    "echo '  💡 Apply first principles thinking'" C-m

# Step 3: Optimize/Accelerate (Optimizer)
sleep 3
echo -e "${GREEN}⚡ Step 3: Optimize/Accelerate${NC}"
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo ''" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo '⚡ STEP 3: OPTIMIZE/ACCELERATE'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'Status: OPTIMIZER AGENT ACCELERATING'" C-m

tmux send-keys -t $SESSION_NAME:optimizer \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:optimizer \
    "echo '⚡ OPTIMIZATION: $PROBLEM'" C-m
tmux send-keys -t $SESSION_NAME:optimizer \
    "echo 'Step: 3/5 - OPTIMIZE & ACCELERATE'" C-m
tmux send-keys -t $SESSION_NAME:optimizer \
    "echo 'Complexity: $COMPLEXITY/10'" C-m
tmux send-keys -t $SESSION_NAME:optimizer \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:optimizer \
    "echo 'Optimization Tasks:'" C-m
tmux send-keys -t $SESSION_NAME:optimizer \
    "echo '  🚀 Speed up critical paths'" C-m
tmux send-keys -t $SESSION_NAME:optimizer \
    "echo '  💾 Optimize resource usage'" C-m
tmux send-keys -t $SESSION_NAME:optimizer \
    "echo '  📊 Improve efficiency'" C-m
tmux send-keys -t $SESSION_NAME:optimizer \
    "echo '  🎯 Eliminate bottlenecks'" C-m
tmux send-keys -t $SESSION_NAME:optimizer \
    "echo '  ⚡ Parallel processing opportunities'" C-m

# Step 4: Automate (Implementer)
sleep 3
echo -e "${GREEN}🤖 Step 4: Automate${NC}"
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo ''" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo '🤖 STEP 4: AUTOMATE'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'Status: IMPLEMENTER AGENT AUTOMATING'" C-m

tmux send-keys -t $SESSION_NAME:implementer \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:implementer \
    "echo '🤖 AUTOMATION: $PROBLEM'" C-m
tmux send-keys -t $SESSION_NAME:implementer \
    "echo 'Step: 4/5 - AUTOMATE PROCESSES'" C-m
tmux send-keys -t $SESSION_NAME:implementer \
    "echo 'Complexity: $COMPLEXITY/10'" C-m
tmux send-keys -t $SESSION_NAME:implementer \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:implementer \
    "echo 'Automation Tasks:'" C-m
tmux send-keys -t $SESSION_NAME:implementer \
    "echo '  🔧 Automate repetitive tasks'" C-m
tmux send-keys -t $SESSION_NAME:implementer \
    "echo '  📊 Implement monitoring'" C-m
tmux send-keys -t $SESSION_NAME:implementer \
    "echo '  🎯 Create feedback loops'" C-m
tmux send-keys -t $SESSION_NAME:implementer \
    "echo '  ⚡ Build self-healing systems'" C-m
tmux send-keys -t $SESSION_NAME:implementer \
    "echo '  🤖 Deploy autonomous agents'" C-m

# Step 5: Iterate (Tester + Reviewer)
sleep 3
echo -e "${GREEN}🔄 Step 5: Iterate${NC}"
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo ''" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo '🔄 STEP 5: ITERATE'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'Status: TESTER & REVIEWER ITERATING'" C-m

tmux send-keys -t $SESSION_NAME:tester \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:tester \
    "echo '🔄 ITERATION TESTING: $PROBLEM'" C-m
tmux send-keys -t $SESSION_NAME:tester \
    "echo 'Step: 5/5 - ITERATE & IMPROVE'" C-m
tmux send-keys -t $SESSION_NAME:tester \
    "echo 'Complexity: $COMPLEXITY/10'" C-m
tmux send-keys -t $SESSION_NAME:tester \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:tester \
    "echo 'Testing Tasks:'" C-m
tmux send-keys -t $SESSION_NAME:tester \
    "echo '  🧪 Test solution effectiveness'" C-m
tmux send-keys -t $SESSION_NAME:tester \
    "echo '  📊 Measure improvements'" C-m
tmux send-keys -t $SESSION_NAME:tester \
    "echo '  🎯 Validate assumptions'" C-m
tmux send-keys -t $SESSION_NAME:tester \
    "echo '  🔍 Find edge cases'" C-m
tmux send-keys -t $SESSION_NAME:tester \
    "echo '  📈 Performance validation'" C-m

tmux send-keys -t $SESSION_NAME:reviewer \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:reviewer \
    "echo '🔄 ITERATION REVIEW: $PROBLEM'" C-m
tmux send-keys -t $SESSION_NAME:reviewer \
    "echo 'Step: 5/5 - CONTINUOUS IMPROVEMENT'" C-m
tmux send-keys -t $SESSION_NAME:reviewer \
    "echo 'Complexity: $COMPLEXITY/10'" C-m
tmux send-keys -t $SESSION_NAME:reviewer \
    "echo ''" C-m
tmux send-keys -t $SESSION_NAME:reviewer \
    "echo 'Review Tasks:'" C-m
tmux send-keys -t $SESSION_NAME:reviewer \
    "echo '  🔍 Solution quality assessment'" C-m
tmux send-keys -t $SESSION_NAME:reviewer \
    "echo '  📊 Impact measurement'" C-m
tmux send-keys -t $SESSION_NAME:reviewer \
    "echo '  💡 Improvement suggestions'" C-m
tmux send-keys -t $SESSION_NAME:reviewer \
    "echo '  🎯 Next iteration planning'" C-m
tmux send-keys -t $SESSION_NAME:reviewer \
    "echo '  ✅ Success criteria validation'" C-m

# Create problem storage directory
STORAGE_DIR="/Users/shaansisodia/DEV/claude-brain-config/storage/problem-solutions"
mkdir -p "$STORAGE_DIR/$(echo "$PROBLEM" | tr ' ' '-' | tr -cd '[:alnum:]-')"

# Final Status
sleep 3
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo ''" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo '✅ PROBLEM SOLVING WORKFLOW ACTIVE'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'Problem: $PROBLEM'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'Framework: MUSK'\''s 5-Step Algorithm'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'All agents working systematically'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'Storage: $STORAGE_DIR'" C-m
tmux send-keys -t "$SESSION_NAME:$WORKFLOW_WINDOW" \
    "echo 'Monitor progress in individual agent windows'" C-m

# Switch to workflow window
tmux select-window -t "$SESSION_NAME:$WORKFLOW_WINDOW"

echo -e "${GREEN}✅ Problem Solving Workflow Activated!${NC}"
echo -e "${CYAN}Problem: $PROBLEM${NC}"
echo -e "${YELLOW}Complexity: $COMPLEXITY/10${NC}"
echo -e "${MAGENTA}Framework: MUSK's 5-Step Algorithm${NC}"
echo -e "${BLUE}All agents working systematically on solution${NC}"
echo -e "${GREEN}Storage: $STORAGE_DIR${NC}"