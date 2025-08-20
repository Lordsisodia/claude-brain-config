#!/bin/bash
# Research & Analysis Cognitive Workflow Template
# Optimized brain pattern for research and deep analysis

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
MAGENTA='\033[0;35m'
NC='\033[0m'

RESEARCH_TOPIC="${1:-research-topic}"
DEPTH="${2:-7}"

echo -e "${BLUE}🔍 Activating Research Cognitive Workflow${NC}"
echo -e "${CYAN}Topic: ${RESEARCH_TOPIC} | Depth: ${DEPTH}/10${NC}"

# Ensure brain session exists
if ! tmux has-session -t BRAIN-MAIN 2>/dev/null; then
    echo -e "${YELLOW}Starting brain session...${NC}"
    ~/DEV/claude-global-config/tmux-brain-scripts/start-brain-with-learning.sh
    sleep 3
fi

# 1. RESEARCH PLANNING (Control Center)
echo -e "${GREEN}Phase 1: Research Planning & Strategy${NC}"
tmux select-window -t BRAIN-MAIN:control-center
tmux send-keys "echo '🔍 RESEARCH WORKFLOW: STRATEGIC PLANNING'" C-m
tmux send-keys "echo 'Topic: $RESEARCH_TOPIC'" C-m
tmux send-keys "echo 'Research Depth: $DEPTH/10'" C-m
tmux send-keys "echo ''" C-m
tmux send-keys "echo 'Research Strategy (Musk Algorithm):'" C-m
tmux send-keys "echo '1. Question: What do we really need to know?'" C-m
tmux send-keys "echo '2. Simplify: What are the core questions?'" C-m
tmux send-keys "echo '3. Optimize: How to research most efficiently?'" C-m
tmux send-keys "echo '4. Automate: What can be automated?'" C-m
tmux send-keys "echo '5. Iterate: How to improve understanding?'" C-m

# 2. INFORMATION GATHERING (MCP Servers)
echo -e "${GREEN}Phase 2: Information Gathering${NC}"
tmux select-window -t BRAIN-MAIN:mcp-servers
tmux send-keys -t 0 "echo '🔍 PRIMARY RESEARCH ENGINE'" C-m
tmux send-keys -t 0 "echo 'Topic: $RESEARCH_TOPIC'" C-m
tmux send-keys -t 0 "echo 'Status: Ready for deep research'" C-m

tmux send-keys -t 1 "echo '📝 DOCUMENTATION SYSTEM'" C-m
tmux send-keys -t 1 "echo 'Capturing research findings'" C-m
tmux send-keys -t 1 "echo 'Building knowledge base'" C-m

tmux send-keys -t 2 "echo '🔍 EXA DEEP RESEARCH'" C-m
tmux send-keys -t 2 "echo 'Advanced search capabilities'" C-m
tmux send-keys -t 2 "echo 'Pattern recognition across sources'" C-m

tmux send-keys -t 3 "echo '💻 DESKTOP RESEARCH TOOLS'" C-m
tmux send-keys -t 3 "echo 'File analysis and processing'" C-m
tmux send-keys -t 3 "echo 'Local resource integration'" C-m

# 3. DEEP ANALYSIS (Ultra Think)
echo -e "${GREEN}Phase 3: Deep Analysis & Synthesis${NC}"
tmux select-window -t BRAIN-MAIN:ultra-think
tmux send-keys "echo '🧠 ULTRA THINK: RESEARCH ANALYSIS'" C-m
tmux send-keys "echo 'Topic: $RESEARCH_TOPIC'" C-m
tmux send-keys "echo 'Analysis Depth: $DEPTH/10'" C-m
tmux send-keys "echo ''" C-m
tmux send-keys "echo 'Deep Analysis Protocol:'" C-m
tmux send-keys "echo '  🔍 Multi-source information synthesis'" C-m
tmux send-keys "echo '  🧩 Pattern identification across domains'" C-m
tmux send-keys "echo '  🎯 Core insight extraction'" C-m
tmux send-keys "echo '  🔗 Conceptual framework building'" C-m
tmux send-keys "echo '  📊 Evidence evaluation and validation'" C-m

# 4. RESEARCH AGENTS (Specialized Analysis)
echo -e "${GREEN}Phase 4: Specialized Research Agents${NC}"
if ! tmux list-windows -t BRAIN-MAIN | grep -q "architect"; then
    ~/DEV/claude-global-config/tmux-brain-scripts/deploy-agents.sh > /dev/null 2>&1
fi

# Repurpose agents for research
tmux send-keys -t BRAIN-MAIN:architect "echo '🏗️ RESEARCH ARCHITECT'" C-m
tmux send-keys -t BRAIN-MAIN:architect "echo 'Designing research framework'" C-m
tmux send-keys -t BRAIN-MAIN:architect "echo 'Structuring investigation approach'" C-m

tmux send-keys -t BRAIN-MAIN:implementer "echo '💻 DATA PROCESSOR'" C-m
tmux send-keys -t BRAIN-MAIN:implementer "echo 'Processing and organizing findings'" C-m
tmux send-keys -t BRAIN-MAIN:implementer "echo 'Creating analysis workflows'" C-m

tmux send-keys -t BRAIN-MAIN:reviewer "echo '🔍 RESEARCH VALIDATOR'" C-m
tmux send-keys -t BRAIN-MAIN:reviewer "echo 'Fact-checking and source validation'" C-m
tmux send-keys -t BRAIN-MAIN:reviewer "echo 'Ensuring research quality'" C-m

tmux send-keys -t BRAIN-MAIN:documenter "echo '📝 KNOWLEDGE SYNTHESIZER'" C-m
tmux send-keys -t BRAIN-MAIN:documenter "echo 'Creating comprehensive documentation'" C-m
tmux send-keys -t BRAIN-MAIN:documenter "echo 'Building knowledge artifacts'" C-m

# 5. KNOWLEDGE INTEGRATION (Memory Systems)
echo -e "${GREEN}Phase 5: Knowledge Integration${NC}"
tmux select-window -t BRAIN-MAIN:memory
tmux send-keys "echo '💾 RESEARCH MEMORY INTEGRATION'" C-m
tmux send-keys "echo 'Topic: $RESEARCH_TOPIC'" C-m
tmux send-keys "echo ''" C-m
tmux send-keys "echo 'Memory Integration Strategy:'" C-m
tmux send-keys "echo '  • Working Memory: Current research context'" C-m
tmux send-keys "echo '  • Episodic Memory: Research session recordings'" C-m
tmux send-keys "echo '  • Semantic Memory: Conceptual frameworks & models'" C-m
tmux send-keys "echo '  • Procedural Memory: Research methodologies'" C-m
tmux send-keys "echo ''" C-m
tmux send-keys "echo 'Cross-Reference Systems:'" C-m
tmux send-keys "echo '  🔗 Topic interconnections'" C-m
tmux send-keys "echo '  📚 Source correlation mapping'" C-m
tmux send-keys "echo '  🎯 Insight pattern recognition'" C-m

# 6. RESEARCH ORCHESTRATION (Task Coordination)
echo -e "${GREEN}Phase 6: Research Orchestration${NC}"
tmux select-window -t BRAIN-MAIN:task-orchestrator
tmux send-keys "echo '📋 RESEARCH TASK ORCHESTRATION'" C-m
tmux send-keys "echo 'Topic: $RESEARCH_TOPIC'" C-m
tmux send-keys "echo ''" C-m
tmux send-keys "echo 'Research Phases:'" C-m
tmux send-keys "echo '  1. Topic Definition & Scope ✓'" C-m
tmux send-keys "echo '  2. Information Architecture ✓'" C-m
tmux send-keys "echo '  3. Data Gathering ⏳'" C-m
tmux send-keys "echo '  4. Deep Analysis'" C-m
tmux send-keys "echo '  5. Pattern Recognition'" C-m
tmux send-keys "echo '  6. Synthesis & Integration'" C-m
tmux send-keys "echo '  7. Knowledge Artifact Creation'" C-m
tmux send-keys "echo '  8. Validation & Verification'" C-m

# 7. RESEARCH MONITORING (Progress Tracking)
echo -e "${GREEN}Phase 7: Research Progress Monitoring${NC}"
tmux select-window -t BRAIN-MAIN:monitor
tmux send-keys -t 0 "echo '📊 RESEARCH PROGRESS MONITORING'" C-m
tmux send-keys -t 0 "echo 'Topic: $RESEARCH_TOPIC'" C-m

tmux send-keys -t 1 "echo '🔍 SOURCE ANALYSIS STATUS'" C-m
tmux send-keys -t 1 "echo '  📚 Sources processed: 0'" C-m
tmux send-keys -t 1 "echo '  🎯 Key insights identified: 0'" C-m

tmux send-keys -t 2 "echo '💾 KNOWLEDGE ACCUMULATION'" C-m
tmux send-keys -t 2 "echo '  📝 Concepts documented'" C-m
tmux send-keys -t 2 "echo '  🔗 Connections mapped'" C-m

tmux send-keys -t 3 "echo '⚡ RESEARCH EFFICIENCY'" C-m
tmux send-keys -t 3 "echo '  ⏱️ Research velocity'" C-m
tmux send-keys -t 3 "echo '  🎯 Insight density'" C-m

# 8. LEARNING INTEGRATION (Research Enhancement)
if tmux list-windows -t BRAIN-MAIN | grep -q "learning-dashboard"; then
    echo -e "${GREEN}Phase 8: Research Learning Integration${NC}"
    tmux select-window -t BRAIN-MAIN:learning-dashboard
    tmux send-keys "echo '📈 RESEARCH LEARNING INTEGRATION'" C-m
    tmux send-keys "echo 'Topic: $RESEARCH_TOPIC'" C-m
    tmux send-keys "echo ''" C-m
    tmux send-keys "echo 'Learning Objectives:'" C-m
    tmux send-keys "echo '  🔍 Research methodology optimization'" C-m
    tmux send-keys "echo '  📊 Information processing acceleration'" C-m
    tmux send-keys "echo '  🎯 Pattern recognition enhancement'" C-m
    tmux send-keys "echo '  🧠 Knowledge synthesis improvement'" C-m
    tmux send-keys "echo ''" C-m
    tmux send-keys "echo 'Adaptive Systems:'" C-m
    tmux send-keys "echo '  🤖 Auto-optimization of search strategies'" C-m
    tmux send-keys "echo '  📚 Predictive source recommendation'" C-m
    tmux send-keys "echo '  🔄 Continuous methodology refinement'" C-m
fi

# Create research-specific task
echo -e "${CYAN}Creating research task...${NC}"
~/DEV/claude-global-config/tmux-brain-scripts/quick-task.sh "Research: $RESEARCH_TOPIC" "$DEPTH" "deep-analysis"

echo -e "${GREEN}✅ Research Cognitive Workflow Activated!${NC}"
echo -e "${BLUE}🔍 Your brain is now optimized for: $RESEARCH_TOPIC${NC}"
echo -e "${YELLOW}💡 Next Steps:${NC}"
echo -e "${CYAN}  1. Use MCP servers for information gathering${NC}"
echo -e "${CYAN}  2. Apply ultra-think for deep analysis${NC}"
echo -e "${CYAN}  3. Coordinate agents for specialized tasks${NC}"
echo -e "${CYAN}  4. Monitor progress and adapt strategy${NC}"

# Switch to the research task window
TASK_WINDOW=$(tmux list-windows -t BRAIN-MAIN | grep "task-" | tail -1 | cut -d: -f1)
if [ -n "$TASK_WINDOW" ]; then
    tmux select-window -t "BRAIN-MAIN:$TASK_WINDOW"
fi