#!/bin/bash
# Software Development Cognitive Workflow Template
# Optimized brain pattern for coding projects

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

PROJECT_NAME="${1:-development-project}"
COMPLEXITY="${2:-6}"

echo -e "${BLUE}🧠 Activating Development Cognitive Workflow${NC}"
echo -e "${CYAN}Project: ${PROJECT_NAME} | Complexity: ${COMPLEXITY}/10${NC}"

# Ensure brain session exists
if ! tmux has-session -t BRAIN-MAIN 2>/dev/null; then
    echo -e "${YELLOW}Starting brain session...${NC}"
    ~/DEV/claude-global-config/tmux-brain-scripts/start-brain-with-learning.sh
    sleep 3
fi

# 1. ARCHITECTURE PLANNING (Control Center + Ultra Think)
echo -e "${GREEN}Phase 1: Architecture Planning${NC}"
tmux select-window -t BRAIN-MAIN:control-center
tmux send-keys "echo '🏗️ DEVELOPMENT WORKFLOW: ARCHITECTURE PLANNING'" C-m
tmux send-keys "echo 'Project: $PROJECT_NAME'" C-m
tmux send-keys "echo 'Applying Musk Algorithm:'" C-m
tmux send-keys "echo '1. Question: What are the real requirements?'" C-m
tmux send-keys "echo '2. Simplify: What can be removed?'" C-m
tmux send-keys "echo '3. Optimize: How to build this efficiently?'" C-m
tmux send-keys "echo '4. Automate: What can be automated?'" C-m
tmux send-keys "echo '5. Iterate: How to improve continuously?'" C-m

# Switch to ultra-think for deep architecture analysis
tmux select-window -t BRAIN-MAIN:ultra-think
tmux send-keys "echo '🧠 ULTRA THINK: ARCHITECTURE ANALYSIS'" C-m
tmux send-keys "echo 'Project: $PROJECT_NAME'" C-m
tmux send-keys "echo 'Complexity Level: $COMPLEXITY'" C-m
tmux send-keys "echo ''" C-m
tmux send-keys "echo 'Deep Analysis Mode Activated...'" C-m
tmux send-keys "echo 'Analyzing requirements and constraints...'" C-m
tmux send-keys "echo 'Designing optimal system architecture...'" C-m

# 2. AGENT DEPLOYMENT (Multi-Agent Coordination)
echo -e "${GREEN}Phase 2: Agent Deployment${NC}"
tmux select-window -t BRAIN-MAIN:agents
tmux send-keys "echo '🤖 MULTI-AGENT DEVELOPMENT COORDINATION'" C-m
tmux send-keys "echo 'Project: $PROJECT_NAME'" C-m
tmux send-keys "echo ''" C-m
tmux send-keys "echo 'Agent Roles:'" C-m
tmux send-keys "echo '  🏗️ Architect: System design and patterns'" C-m
tmux send-keys "echo '  💻 Implementer: Code generation and logic'" C-m
tmux send-keys "echo '  🔍 Reviewer: Code quality and security'" C-m
tmux send-keys "echo '  🧪 Tester: Test strategies and validation'" C-m

# Deploy specialized agents if not already active
if ! tmux list-windows -t BRAIN-MAIN | grep -q "architect"; then
    ~/DEV/claude-global-config/tmux-brain-scripts/deploy-agents.sh > /dev/null 2>&1
fi

# 3. MCP INTEGRATION (External Tools)
echo -e "${GREEN}Phase 3: MCP Tool Integration${NC}"
tmux select-window -t BRAIN-MAIN:mcp-servers
tmux send-keys -t 0 "echo '🔌 MCP: Development Tools Integration'" C-m
tmux send-keys -t 1 "echo '📝 Documentation System (Notion)'" C-m
tmux send-keys -t 2 "echo '🔍 Research Engine (Exa)'" C-m
tmux send-keys -t 3 "echo '💻 Desktop Operations'" C-m

# 4. TASK ORCHESTRATION (Project Planning)
echo -e "${GREEN}Phase 4: Task Orchestration${NC}"
tmux select-window -t BRAIN-MAIN:task-orchestrator
tmux send-keys "echo '📋 DEVELOPMENT TASK ORCHESTRATION'" C-m
tmux send-keys "echo 'Project: $PROJECT_NAME'" C-m
tmux send-keys "echo ''" C-m
tmux send-keys "echo 'Development Phases:'" C-m
tmux send-keys "echo '  1. Requirements Analysis ✓'" C-m
tmux send-keys "echo '  2. Architecture Design ✓'" C-m
tmux send-keys "echo '  3. Implementation Planning ⏳'" C-m
tmux send-keys "echo '  4. Code Development'" C-m
tmux send-keys "echo '  5. Testing & Validation'" C-m
tmux send-keys "echo '  6. Documentation'" C-m
tmux send-keys "echo '  7. Optimization'" C-m

# 5. MEMORY INTEGRATION (Knowledge Base)
echo -e "${GREEN}Phase 5: Memory Integration${NC}"
tmux select-window -t BRAIN-MAIN:memory
tmux send-keys "echo '💾 DEVELOPMENT MEMORY INTEGRATION'" C-m
tmux send-keys "echo 'Project: $PROJECT_NAME'" C-m
tmux send-keys "echo ''" C-m
tmux send-keys "echo 'Memory Systems:'" C-m
tmux send-keys "echo '  • Working Memory: Current development context'" C-m
tmux send-keys "echo '  • Episodic Memory: Similar project experiences'" C-m
tmux send-keys "echo '  • Semantic Memory: Development patterns & best practices'" C-m
tmux send-keys "echo '  • Procedural Memory: Automated development workflows'" C-m

# 6. PERFORMANCE MONITORING (Development Metrics)
echo -e "${GREEN}Phase 6: Performance Monitoring${NC}"
tmux select-window -t BRAIN-MAIN:monitor
tmux send-keys -t 0 "echo '📊 DEVELOPMENT PERFORMANCE MONITORING'" C-m
tmux send-keys -t 1 "echo '🤖 Agent Coordination Status'" C-m
tmux send-keys -t 2 "echo '💾 Memory & Pattern Usage'" C-m
tmux send-keys -t 3 "echo '⚡ Development Efficiency Metrics'" C-m

# 7. LEARNING INTEGRATION (Continuous Improvement)
if tmux list-windows -t BRAIN-MAIN | grep -q "learning-dashboard"; then
    echo -e "${GREEN}Phase 7: Learning Integration${NC}"
    tmux select-window -t BRAIN-MAIN:learning-dashboard
    tmux send-keys "echo '📈 DEVELOPMENT LEARNING INTEGRATION'" C-m
    tmux send-keys "echo 'Project: $PROJECT_NAME'" C-m
    tmux send-keys "echo ''" C-m
    tmux send-keys "echo 'Learning Focus:'" C-m
    tmux send-keys "echo '  • Development pattern recognition'" C-m
    tmux send-keys "echo '  • Optimization opportunity detection'" C-m
    tmux send-keys "echo '  • Error prevention strategies'" C-m
    tmux send-keys "echo '  • Performance improvement tracking'" C-m
fi

# Create project-specific task
echo -e "${CYAN}Creating development task...${NC}"
~/DEV/claude-global-config/tmux-brain-scripts/quick-task.sh "Develop: $PROJECT_NAME" "$COMPLEXITY" "deep-analysis"

echo -e "${GREEN}✅ Development Cognitive Workflow Activated!${NC}"
echo -e "${BLUE}🧠 Your brain is now optimized for: $PROJECT_NAME${NC}"
echo -e "${YELLOW}💡 Next: Switch between windows to coordinate development${NC}"

# Switch to task window
TASK_WINDOW=$(tmux list-windows -t BRAIN-MAIN | grep "task-" | tail -1 | cut -d: -f1)
if [ -n "$TASK_WINDOW" ]; then
    tmux select-window -t "BRAIN-MAIN:$TASK_WINDOW"
fi