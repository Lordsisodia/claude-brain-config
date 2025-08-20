#!/bin/bash
# Deploy Multi-Agent System with Specialized Roles

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}🤖 Deploying Multi-Agent System...${NC}"

# Check if brain session exists
if ! tmux has-session -t BRAIN-MAIN 2>/dev/null; then
    echo -e "${RED}❌ Brain session not found. Starting...${NC}"
    $(dirname "$0")/start-brain.sh
    exit 1
fi

# Function to deploy an agent
deploy_agent() {
    local window_name=$1
    local agent_type=$2
    local description=$3
    local color=$4
    
    echo -e "${color}🚀 Deploying ${description}...${NC}"
    
    # Check if window already exists
    if tmux list-windows -t BRAIN-MAIN | grep -q "$window_name"; then
        echo -e "${YELLOW}⚠️  ${window_name} already exists, redeploying...${NC}"
        tmux kill-window -t "BRAIN-MAIN:$window_name" 2>/dev/null || true
    fi
    
    # Create agent window
    tmux new-window -t BRAIN-MAIN -n "$window_name"
    
    # Configure agent
    tmux send-keys -t "BRAIN-MAIN:$window_name" \
        "echo '${description}'" C-m \
        "echo '================================'" C-m \
        "export AGENT_TYPE='$agent_type'" C-m \
        "export AGENT_NAME='$window_name'" C-m \
        "export COGNITIVE_MODE='SPECIALIZED'" C-m \
        "export AUTONOMOUS='true'" C-m \
        "echo 'Status: READY'" C-m \
        "echo 'Waiting for tasks...'" C-m
}

# Deploy core agents
deploy_agent "architect" "SYSTEM_ARCHITECT" "🏗️ System Architect Agent" "$BLUE"
deploy_agent "implementer" "CODE_IMPLEMENTER" "💻 Code Implementation Agent" "$GREEN"
deploy_agent "reviewer" "CODE_REVIEWER" "🔍 Code Review Agent" "$YELLOW"
deploy_agent "tester" "TEST_ENGINEER" "🧪 Testing Agent" "$CYAN"
deploy_agent "documenter" "DOCUMENTATION" "📝 Documentation Agent" "$MAGENTA"
deploy_agent "optimizer" "PERFORMANCE" "⚡ Performance Optimizer Agent" "$RED"

# Deploy specialized agents
echo -e "${CYAN}🎯 Deploying Specialized Agents...${NC}"

# Database specialist
deploy_agent "db-expert" "DATABASE_EXPERT" "🗄️ Database Expert Agent" "$BLUE"
tmux send-keys -t "BRAIN-MAIN:db-expert" \
    "export MCP_TOOLS='supabase,postgres'" C-m \
    "echo 'Specialization: Database Operations'" C-m

# Security specialist
deploy_agent "security" "SECURITY_EXPERT" "🔐 Security Expert Agent" "$RED"
tmux send-keys -t "BRAIN-MAIN:security" \
    "export FOCUS='OWASP,vulnerabilities,encryption'" C-m \
    "echo 'Specialization: Security Analysis'" C-m

# Frontend specialist
deploy_agent "frontend" "FRONTEND_EXPERT" "🎨 Frontend Expert Agent" "$MAGENTA"
tmux send-keys -t "BRAIN-MAIN:frontend" \
    "export FRAMEWORKS='react,vue,nextjs'" C-m \
    "echo 'Specialization: UI/UX Development'" C-m

# Deploy orchestrator (master agent)
echo -e "${GREEN}👑 Deploying Master Orchestrator...${NC}"
deploy_agent "orchestrator" "TECH_LEAD_ORCHESTRATOR" "👑 Master Orchestrator" "$GREEN"

# Configure orchestrator with special privileges
tmux send-keys -t "BRAIN-MAIN:orchestrator" \
    "export ROLE='ORCHESTRATOR'" C-m \
    "export PRIVILEGES='COORDINATE_ALL'" C-m \
    "export AGENTS='architect,implementer,reviewer,tester,documenter,optimizer,db-expert,security,frontend'" C-m \
    "echo ''" C-m \
    "echo 'Orchestrator Capabilities:'" C-m \
    "echo '  • Task distribution'" C-m \
    "echo '  • Agent coordination'" C-m \
    "echo '  • Result aggregation'" C-m \
    "echo '  • Conflict resolution'" C-m \
    "echo '  • Performance monitoring'" C-m

# Set up inter-agent communication
echo -e "${BLUE}🔗 Setting up Inter-Agent Communication...${NC}"

TMUX_BRAIN_HOME="${TMUX_BRAIN_HOME:-$HOME/.tmux-brain}"
mkdir -p "$TMUX_BRAIN_HOME/agents/messages"

# Create message bus
mkfifo "$TMUX_BRAIN_HOME/agents/message-bus" 2>/dev/null || true

# Create agent registry
cat > "$TMUX_BRAIN_HOME/agents/registry.json" << EOF
{
  "agents": [
    {"name": "architect", "type": "SYSTEM_ARCHITECT", "status": "active"},
    {"name": "implementer", "type": "CODE_IMPLEMENTER", "status": "active"},
    {"name": "reviewer", "type": "CODE_REVIEWER", "status": "active"},
    {"name": "tester", "type": "TEST_ENGINEER", "status": "active"},
    {"name": "documenter", "type": "DOCUMENTATION", "status": "active"},
    {"name": "optimizer", "type": "PERFORMANCE", "status": "active"},
    {"name": "db-expert", "type": "DATABASE_EXPERT", "status": "active"},
    {"name": "security", "type": "SECURITY_EXPERT", "status": "active"},
    {"name": "frontend", "type": "FRONTEND_EXPERT", "status": "active"},
    {"name": "orchestrator", "type": "TECH_LEAD_ORCHESTRATOR", "status": "active"}
  ],
  "communication": {
    "protocol": "async",
    "bus": "$TMUX_BRAIN_HOME/agents/message-bus",
    "format": "json"
  }
}
EOF

# Display agent status
echo -e "${GREEN}✅ Multi-Agent System Deployed Successfully!${NC}"
echo -e "${CYAN}📊 Agent Status:${NC}"
tmux list-windows -t BRAIN-MAIN | grep -E "architect|implementer|reviewer|tester|documenter|optimizer|db-expert|security|frontend|orchestrator" | while read line; do
    echo -e "  ${GREEN}✓${NC} $line"
done

echo -e "${YELLOW}💡 Tip: Use 'tmux select-window -t BRAIN-MAIN:<agent>' to view specific agents${NC}"
echo -e "${MAGENTA}🚀 All agents are autonomous and ready for tasks!${NC}"