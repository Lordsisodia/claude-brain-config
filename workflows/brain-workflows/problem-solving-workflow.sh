#!/bin/bash
# Problem Solving Cognitive Workflow Template
# Musk's 5-Step Algorithm implemented as a cognitive workflow

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

echo -e "${RED}🎯 Activating Problem Solving Cognitive Workflow${NC}"
echo -e "${CYAN}Problem: ${PROBLEM} | Complexity: ${COMPLEXITY}/10${NC}"

# Ensure brain session exists
if ! tmux has-session -t BRAIN-MAIN 2>/dev/null; then
    echo -e "${YELLOW}Starting brain session...${NC}"
    ~/DEV/claude-global-config/tmux-brain-scripts/start-brain-with-learning.sh
    sleep 3
fi

# STEP 1: QUESTION REQUIREMENTS (Control Center)
echo -e "${GREEN}🤔 Step 1: Question Requirements${NC}"
tmux select-window -t BRAIN-MAIN:control-center
tmux send-keys "echo '🤔 MUSK STEP 1: QUESTION REQUIREMENTS'" C-m
tmux send-keys "echo 'Problem: $PROBLEM'" C-m
tmux send-keys "echo 'Complexity: $COMPLEXITY/10'" C-m
tmux send-keys "echo ''" C-m
tmux send-keys "echo 'Critical Questions:'" C-m
tmux send-keys "echo '  ❓ Is this problem actually necessary to solve?'" C-m
tmux send-keys "echo '  ❓ What are the REAL requirements?'" C-m
tmux send-keys "echo '  ❓ What assumptions am I making?'" C-m
tmux send-keys "echo '  ❓ Who defined this as a problem and why?'" C-m
tmux send-keys "echo '  ❓ What would happen if we did nothing?'" C-m
tmux send-keys "echo ''" C-m
tmux send-keys "echo '🎯 Core Requirement Analysis:'" C-m

sleep 2

# STEP 2: DELETE/SIMPLIFY (Ultra Think)
echo -e "${GREEN}✂️ Step 2: Delete & Simplify${NC}"
tmux select-window -t BRAIN-MAIN:ultra-think
tmux send-keys "echo '✂️ MUSK STEP 2: DELETE & SIMPLIFY'" C-m
tmux send-keys "echo 'Problem: $PROBLEM'" C-m
tmux send-keys "echo ''" C-m
tmux send-keys "echo 'Simplification Protocol:'" C-m
tmux send-keys "echo '  🗑️ What can be removed from this problem?'" C-m
tmux send-keys "echo '  🎯 What is the CORE issue beneath symptoms?'" C-m
tmux send-keys "echo '  ⚡ What is the simplest possible solution?'" C-m
tmux send-keys "echo '  🧹 What complexity can be eliminated?'" C-m
tmux send-keys "echo '  🔍 What is the 80/20 of this problem?'" C-m
tmux send-keys "echo ''" C-m
tmux send-keys "echo 'Ultra Think Analysis:'" C-m
tmux send-keys "echo '  💭 Applying first principles thinking...'" C-m
tmux send-keys "echo '  🔬 Breaking down to fundamental components...'" C-m
tmux send-keys "echo '  🎯 Identifying the minimal viable solution...'" C-m

sleep 2

# STEP 3: OPTIMIZE/ACCELERATE (Agents)
echo -e "${GREEN}🚀 Step 3: Optimize & Accelerate${NC}"
if ! tmux list-windows -t BRAIN-MAIN | grep -q "architect"; then
    ~/DEV/claude-global-config/tmux-brain-scripts/deploy-agents.sh > /dev/null 2>&1
fi

# Repurpose agents for optimization
tmux send-keys -t BRAIN-MAIN:architect "echo '🏗️ OPTIMIZATION ARCHITECT'" C-m
tmux send-keys -t BRAIN-MAIN:architect "echo 'Problem: $PROBLEM'" C-m
tmux send-keys -t BRAIN-MAIN:architect "echo 'Designing optimal solution architecture'" C-m

tmux send-keys -t BRAIN-MAIN:implementer "echo '⚡ ACCELERATION SPECIALIST'" C-m
tmux send-keys -t BRAIN-MAIN:implementer "echo 'How can this be solved FASTER?'" C-m
tmux send-keys -t BRAIN-MAIN:implementer "echo 'What resources can be leveraged?'" C-m

tmux send-keys -t BRAIN-MAIN:optimizer "echo '🚀 PERFORMANCE OPTIMIZER'" C-m
tmux send-keys -t BRAIN-MAIN:optimizer "echo 'Maximizing solution efficiency'" C-m
tmux send-keys -t BRAIN-MAIN:optimizer "echo 'Identifying bottlenecks and constraints'" C-m

tmux send-keys -t BRAIN-MAIN:reviewer "echo '🔍 SOLUTION VALIDATOR'" C-m
tmux send-keys -t BRAIN-MAIN:reviewer "echo 'Ensuring optimization quality'" C-m
tmux send-keys -t BRAIN-MAIN:reviewer "echo 'Risk assessment and mitigation'" C-m

# Display optimization coordination
tmux select-window -t BRAIN-MAIN:agents
tmux send-keys "echo '🚀 MUSK STEP 3: OPTIMIZE & ACCELERATE'" C-m
tmux send-keys "echo 'Problem: $PROBLEM'" C-m
tmux send-keys "echo ''" C-m
tmux send-keys "echo 'Optimization Questions:'" C-m
tmux send-keys "echo '  ⚡ How can this be faster?'" C-m
tmux send-keys "echo '  🔧 What tools can help?'" C-m
tmux send-keys "echo '  🤝 What parallel approaches are possible?'" C-m
tmux send-keys "echo '  📊 How to measure optimization success?'" C-m

sleep 2

# STEP 4: AUTOMATE (Task Orchestrator)
echo -e "${GREEN}🤖 Step 4: Automate${NC}"
tmux select-window -t BRAIN-MAIN:task-orchestrator
tmux send-keys "echo '🤖 MUSK STEP 4: AUTOMATE'" C-m
tmux send-keys "echo 'Problem: $PROBLEM'" C-m
tmux send-keys "echo ''" C-m
tmux send-keys "echo 'Automation Analysis:'" C-m
tmux send-keys "echo '  🔄 What parts can be automated?'" C-m
tmux send-keys "echo '  🛠️ What tools can handle routine aspects?'" C-m
tmux send-keys "echo '  📋 How can this be systematized?'" C-m
tmux send-keys "echo '  🔗 What workflows can be created?'" C-m
tmux send-keys "echo '  🎯 How to prevent this problem in future?'" C-m
tmux send-keys "echo ''" C-m
tmux send-keys "echo 'Automation Strategy:'" C-m
tmux send-keys "echo '  1. Identify repetitive elements'" C-m
tmux send-keys "echo '  2. Design automation workflow'" C-m
tmux send-keys "echo '  3. Implement systematic approach'" C-m
tmux send-keys "echo '  4. Monitor and optimize automation'" C-m

sleep 2

# STEP 5: ITERATE (Learning Dashboard + Memory)
echo -e "${GREEN}🔄 Step 5: Iterate & Learn${NC}"
if tmux list-windows -t BRAIN-MAIN | grep -q "learning-dashboard"; then
    tmux select-window -t BRAIN-MAIN:learning-dashboard
    tmux send-keys "echo '🔄 MUSK STEP 5: ITERATE & LEARN'" C-m
    tmux send-keys "echo 'Problem: $PROBLEM'" C-m
    tmux send-keys "echo ''" C-m
    tmux send-keys "echo 'Learning Questions:'" C-m
    tmux send-keys "echo '  📚 What did we learn from this solution?'" C-m
    tmux send-keys "echo '  🔄 How can the approach be improved?'" C-m
    tmux send-keys "echo '  🎯 What patterns can be extracted?'" C-m
    tmux send-keys "echo '  🚀 How to solve similar problems faster?'" C-m
    tmux send-keys "echo '  🧠 What can be automated for next time?'" C-m
fi

# Memory integration
tmux select-window -t BRAIN-MAIN:memory
tmux send-keys "echo '💾 PROBLEM-SOLVING MEMORY INTEGRATION'" C-m
tmux send-keys "echo 'Problem: $PROBLEM'" C-m
tmux send-keys "echo 'Solution Process: Musk 5-Step Algorithm'" C-m
tmux send-keys "echo ''" C-m
tmux send-keys "echo 'Memory Capture:'" C-m
tmux send-keys "echo '  📝 Problem definition and requirements'" C-m
tmux send-keys "echo '  ✂️ Simplification insights'" C-m
tmux send-keys "echo '  🚀 Optimization strategies'" C-m
tmux send-keys "echo '  🤖 Automation opportunities'" C-m
tmux send-keys "echo '  🔄 Learning outcomes'" C-m

sleep 2

# MONITORING & COORDINATION (Monitor)
echo -e "${GREEN}📊 Solution Monitoring${NC}"
tmux select-window -t BRAIN-MAIN:monitor
tmux send-keys -t 0 "echo '📊 PROBLEM-SOLVING MONITORING'" C-m
tmux send-keys -t 0 "echo 'Problem: $PROBLEM'" C-m
tmux send-keys -t 0 "echo 'Algorithm: Musk 5-Step Process'" C-m

tmux send-keys -t 1 "echo '🎯 SOLUTION PROGRESS'" C-m
tmux send-keys -t 1 "echo '  ✅ Step 1: Requirements Questioned'" C-m
tmux send-keys -t 1 "echo '  ✅ Step 2: Problem Simplified'" C-m
tmux send-keys -t 1 "echo '  ✅ Step 3: Solution Optimized'" C-m
tmux send-keys -t 1 "echo '  ✅ Step 4: Automation Identified'" C-m
tmux send-keys -t 1 "echo '  ⏳ Step 5: Learning Integration'" C-m

tmux send-keys -t 2 "echo '🧠 COGNITIVE LOAD'" C-m
tmux send-keys -t 2 "echo '  Problem Complexity: $COMPLEXITY/10'" C-m
tmux send-keys -t 2 "echo '  Cognitive Distribution: Optimized'" C-m

tmux send-keys -t 3 "echo '⚡ SOLUTION METRICS'" C-m
tmux send-keys -t 3 "echo '  Approach: Systematic'" C-m
tmux send-keys -t 3 "echo '  Learning: Continuous'" C-m

# MCP INTEGRATION (External Resources)
echo -e "${GREEN}🔌 External Resource Integration${NC}"
tmux select-window -t BRAIN-MAIN:mcp-servers
tmux send-keys -t 0 "echo '🔍 RESEARCH SUPPORT'" C-m
tmux send-keys -t 0 "echo 'Finding relevant information'" C-m

tmux send-keys -t 1 "echo '📝 DOCUMENTATION'" C-m
tmux send-keys -t 1 "echo 'Capturing solution process'" C-m

tmux send-keys -t 2 "echo '🔍 PATTERN ANALYSIS'" C-m
tmux send-keys -t 2 "echo 'Similar problem research'" C-m

tmux send-keys -t 3 "echo '💻 TOOL INTEGRATION'" C-m
tmux send-keys -t 3 "echo 'Leveraging external resources'" C-m

# Create problem-solving task
echo -e "${CYAN}Creating problem-solving task...${NC}"
~/DEV/claude-global-config/tmux-brain-scripts/quick-task.sh "Solve: $PROBLEM" "$COMPLEXITY" "ultra-think"

echo -e "${GREEN}✅ Problem Solving Cognitive Workflow Activated!${NC}"
echo -e "${RED}🎯 Problem: $PROBLEM${NC}"
echo -e "${BLUE}🧠 Algorithm: Musk's 5-Step Process${NC}"
echo -e "${YELLOW}💡 Workflow Navigation:${NC}"
echo -e "${CYAN}  Step 1: control-center (Question Requirements)${NC}"
echo -e "${CYAN}  Step 2: ultra-think (Delete & Simplify)${NC}"
echo -e "${CYAN}  Step 3: agents (Optimize & Accelerate)${NC}"
echo -e "${CYAN}  Step 4: task-orchestrator (Automate)${NC}"
echo -e "${CYAN}  Step 5: learning-dashboard (Iterate & Learn)${NC}"

# Switch to the problem-solving task window
TASK_WINDOW=$(tmux list-windows -t BRAIN-MAIN | grep "task-" | tail -1 | cut -d: -f1)
if [ -n "$TASK_WINDOW" ]; then
    tmux select-window -t "BRAIN-MAIN:$TASK_WINDOW"
fi