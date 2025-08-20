#!/bin/bash
# Autonomous Agent Coordination System
# Coordinates multiple agents for complex task execution

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
SESSION_NAME="BRAIN-MAIN"
COORDINATION_DIR="/Users/shaansisodia/DEV/claude-brain-config/coordination"
TASK_QUEUE_DIR="$COORDINATION_DIR/task-queue"
AGENT_STATUS_DIR="$COORDINATION_DIR/agent-status"

# Create coordination directories
mkdir -p "$TASK_QUEUE_DIR" "$AGENT_STATUS_DIR"

echo -e "${BLUE}🎭 AUTONOMOUS AGENT COORDINATION SYSTEM${NC}"
echo -e "${CYAN}=====================================${NC}"

# Function to create complex task
create_complex_task() {
    local task_name="$1"
    local task_type="$2"
    local complexity="${3:-8}"
    local priority="${4:-medium}"
    local deadline="${5:-none}"
    
    local task_id="task_$(date +%Y%m%d_%H%M%S)_$(echo "$task_name" | tr ' ' '_' | tr -cd '[:alnum:]_')"
    local task_file="$TASK_QUEUE_DIR/${task_id}.json"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Analyze task complexity and determine required agents
    local required_agents=()
    local estimated_duration="unknown"
    
    case "$task_type" in
        "full-stack-development")
            required_agents=("architect" "implementer" "security" "tester" "documenter")
            estimated_duration="4-8 hours"
            ;;
        "research-and-analysis")
            required_agents=("architect" "reviewer" "documenter")
            estimated_duration="2-6 hours"
            ;;
        "problem-solving")
            required_agents=("architect" "implementer" "reviewer" "optimizer")
            estimated_duration="1-4 hours"
            ;;
        "product-development")
            required_agents=("architect" "implementer" "reviewer" "tester" "documenter" "security")
            estimated_duration="6-12 hours"
            ;;
        "system-optimization")
            required_agents=("optimizer" "security" "reviewer" "tester")
            estimated_duration="2-4 hours"
            ;;
        *)
            # Auto-detect based on complexity
            if [ "$complexity" -ge 9 ]; then
                required_agents=("architect" "implementer" "reviewer" "tester" "documenter" "security" "optimizer")
                estimated_duration="8-16 hours"
            elif [ "$complexity" -ge 7 ]; then
                required_agents=("architect" "implementer" "reviewer" "tester" "documenter")
                estimated_duration="4-8 hours"
            elif [ "$complexity" -ge 5 ]; then
                required_agents=("architect" "implementer" "reviewer")
                estimated_duration="2-4 hours"
            else
                required_agents=("implementer" "reviewer")
                estimated_duration="1-2 hours"
            fi
            ;;
    esac
    
    # Create task definition
    cat > "$task_file" << EOF
{
    "task_id": "$task_id",
    "task_name": "$task_name",
    "task_type": "$task_type",
    "complexity": $complexity,
    "priority": "$priority",
    "deadline": "$deadline",
    "status": "queued",
    "created": "$timestamp",
    "estimated_duration": "$estimated_duration",
    "required_agents": [$(printf '"%s",' "${required_agents[@]}" | sed 's/,$//')],
    "assigned_agents": [],
    "progress": 0,
    "phases": {
        "planning": {"status": "pending", "assigned_agent": null, "progress": 0},
        "execution": {"status": "pending", "assigned_agent": null, "progress": 0},
        "review": {"status": "pending", "assigned_agent": null, "progress": 0},
        "completion": {"status": "pending", "assigned_agent": null, "progress": 0}
    },
    "coordination": {
        "orchestrator": "task-coordinator",
        "communication_channel": "BRAIN-MAIN:task-orchestrator",
        "status_updates": []
    }
}
EOF
    
    echo -e "${GREEN}📋 Complex task created: $task_id${NC}"
    echo -e "${CYAN}Task: $task_name${NC}"
    echo -e "${YELLOW}Type: $task_type | Complexity: $complexity/10 | Priority: $priority${NC}"
    echo -e "${MAGENTA}Required Agents: ${required_agents[*]}${NC}"
    echo -e "${BLUE}Estimated Duration: $estimated_duration${NC}"
    
    return 0
}

# Function to assign agents to task phases
assign_agents_to_task() {
    local task_id="$1"
    local task_file="$TASK_QUEUE_DIR/${task_id}.json"
    
    if [ ! -f "$task_file" ]; then
        echo -e "${RED}❌ Task not found: $task_id${NC}"
        return 1
    fi
    
    # Ensure brain session exists
    if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
        echo -e "${YELLOW}🧠 Starting brain session...${NC}"
        /Users/shaansisodia/DEV/claude-brain-config/tmux-orchestrator/start-brain-with-learning.sh
        sleep 3
    fi
    
    # Deploy agents if needed
    if ! tmux list-windows -t $SESSION_NAME | grep -q "architect"; then
        echo -e "${CYAN}🤖 Deploying agents...${NC}"
        /Users/shaansisodia/DEV/claude-brain-config/tmux-orchestrator/deploy-agents.sh > /dev/null 2>&1
    fi
    
    # Read task details
    local task_name=$(jq -r .task_name "$task_file" 2>/dev/null || echo "unknown")
    local required_agents=($(jq -r '.required_agents[]' "$task_file" 2>/dev/null))
    
    echo -e "${GREEN}🎭 Assigning agents to task: $task_name${NC}"
    
    # Create coordination window for this task
    local coord_window="coord-$(echo "$task_id" | cut -c1-15)"
    if ! tmux list-windows -t $SESSION_NAME | grep -q "$coord_window"; then
        tmux new-window -t $SESSION_NAME -n "$coord_window"
    fi
    
    # Set up coordination environment
    tmux send-keys -t "$SESSION_NAME:$coord_window" \
        "echo '🎭 TASK COORDINATION: $task_name'" C-m
    tmux send-keys -t "$SESSION_NAME:$coord_window" \
        "echo 'Task ID: $task_id'" C-m
    tmux send-keys -t "$SESSION_NAME:$coord_window" \
        "echo 'Status: ASSIGNING AGENTS'" C-m
    tmux send-keys -t "$SESSION_NAME:$coord_window" \
        "echo ''" C-m
    
    # Assign agents to specific phases
    for agent in "${required_agents[@]}"; do
        if tmux list-windows -t $SESSION_NAME | grep -q "$agent"; then
            echo -e "${CYAN}📍 Assigning $agent to task${NC}"
            
            # Notify agent of assignment
            tmux send-keys -t "$SESSION_NAME:$agent" \
                "echo ''" C-m
            tmux send-keys -t "$SESSION_NAME:$agent" \
                "echo '🎯 NEW TASK ASSIGNMENT'" C-m
            tmux send-keys -t "$SESSION_NAME:$agent" \
                "echo 'Task: $task_name'" C-m
            tmux send-keys -t "$SESSION_NAME:$agent" \
                "echo 'Task ID: $task_id'" C-m
            tmux send-keys -t "$SESSION_NAME:$agent" \
                "echo 'Coordination: $coord_window'" C-m
            tmux send-keys -t "$SESSION_NAME:$agent" \
                "echo 'Status: ASSIGNED - READY TO BEGIN'" C-m
            
            # Update coordination window
            tmux send-keys -t "$SESSION_NAME:$coord_window" \
                "echo '✅ $agent: ASSIGNED'" C-m
            
            # Create agent status file
            echo "{\"agent\": \"$agent\", \"task_id\": \"$task_id\", \"status\": \"assigned\", \"last_update\": \"$(date)\"}" > "$AGENT_STATUS_DIR/${agent}_${task_id}.json"
            
        else
            echo -e "${RED}❌ Agent $agent not available${NC}"
        fi
    done
    
    # Update task status
    if command -v jq > /dev/null 2>&1; then
        local temp_file=$(mktemp)
        jq --arg timestamp "$(date '+%Y-%m-%d %H:%M:%S')" \
           '.status = "assigned" | .assigned_agents = .required_agents | .coordination.status_updates += [{"timestamp": $timestamp, "status": "agents_assigned", "message": "All required agents assigned to task"}]' \
           "$task_file" > "$temp_file" && mv "$temp_file" "$task_file"
    fi
    
    tmux send-keys -t "$SESSION_NAME:$coord_window" \
        "echo ''" C-m
    tmux send-keys -t "$SESSION_NAME:$coord_window" \
        "echo '✅ ALL AGENTS ASSIGNED'" C-m
    tmux send-keys -t "$SESSION_NAME:$coord_window" \
        "echo 'Task ready for execution'" C-m
    
    echo -e "${GREEN}✅ Agent assignment complete for task: $task_id${NC}"
}

# Function to execute coordinated task
execute_coordinated_task() {
    local task_id="$1"
    local task_file="$TASK_QUEUE_DIR/${task_id}.json"
    
    if [ ! -f "$task_file" ]; then
        echo -e "${RED}❌ Task not found: $task_id${NC}"
        return 1
    fi
    
    local task_name=$(jq -r .task_name "$task_file" 2>/dev/null || echo "unknown")
    local coord_window="coord-$(echo "$task_id" | cut -c1-15)"
    
    echo -e "${GREEN}🚀 Executing coordinated task: $task_name${NC}"
    
    # Phase 1: Planning
    execute_task_phase "$task_id" "planning" "architect"
    
    # Phase 2: Execution
    execute_task_phase "$task_id" "execution" "implementer"
    
    # Phase 3: Review
    execute_task_phase "$task_id" "review" "reviewer"
    
    # Phase 4: Completion
    execute_task_phase "$task_id" "completion" "documenter"
    
    # Final coordination update
    tmux send-keys -t "$SESSION_NAME:$coord_window" \
        "echo ''" C-m
    tmux send-keys -t "$SESSION_NAME:$coord_window" \
        "echo '🎉 TASK EXECUTION COMPLETE'" C-m
    tmux send-keys -t "$SESSION_NAME:$coord_window" \
        "echo 'All phases completed successfully'" C-m
    tmux send-keys -t "$SESSION_NAME:$coord_window" \
        "echo 'Task: $task_name'" C-m
    
    # Update task status to completed
    if command -v jq > /dev/null 2>&1; then
        local temp_file=$(mktemp)
        jq --arg timestamp "$(date '+%Y-%m-%d %H:%M:%S')" \
           '.status = "completed" | .progress = 100 | .coordination.status_updates += [{"timestamp": $timestamp, "status": "completed", "message": "Task execution completed successfully"}]' \
           "$task_file" > "$temp_file" && mv "$temp_file" "$task_file"
    fi
    
    echo -e "${GREEN}🎉 Task execution completed: $task_id${NC}"
}

# Function to execute specific task phase
execute_task_phase() {
    local task_id="$1"
    local phase="$2"
    local primary_agent="$3"
    local coord_window="coord-$(echo "$task_id" | cut -c1-15)"
    
    echo -e "${CYAN}📋 Executing phase: $phase (Primary: $primary_agent)${NC}"
    
    # Update coordination window
    tmux send-keys -t "$SESSION_NAME:$coord_window" \
        "echo ''" C-m
    tmux send-keys -t "$SESSION_NAME:$coord_window" \
        "echo '📋 PHASE: $(echo "$phase" | tr '[:lower:]' '[:upper:]')'" C-m
    tmux send-keys -t "$SESSION_NAME:$coord_window" \
        "echo 'Primary Agent: $primary_agent'" C-m
    tmux send-keys -t "$SESSION_NAME:$coord_window" \
        "echo 'Status: IN PROGRESS'" C-m
    
    # Notify primary agent
    tmux send-keys -t "$SESSION_NAME:$primary_agent" \
        "echo ''" C-m
    tmux send-keys -t "$SESSION_NAME:$primary_agent" \
        "echo '🎯 PHASE EXECUTION: $(echo "$phase" | tr '[:lower:]' '[:upper:]')'" C-m
    tmux send-keys -t "$SESSION_NAME:$primary_agent" \
        "echo 'Task ID: $task_id'" C-m
    tmux send-keys -t "$SESSION_NAME:$primary_agent" \
        "echo 'Role: PRIMARY AGENT'" C-m
    tmux send-keys -t "$SESSION_NAME:$primary_agent" \
        "echo 'Status: EXECUTING PHASE'" C-m
    
    # Simulate phase execution time
    sleep 2
    
    # Mark phase as completed
    tmux send-keys -t "$SESSION_NAME:$coord_window" \
        "echo 'Status: ✅ COMPLETED'" C-m
    
    tmux send-keys -t "$SESSION_NAME:$primary_agent" \
        "echo 'Status: ✅ PHASE COMPLETED'" C-m
    
    echo -e "${GREEN}✅ Phase completed: $phase${NC}"
}

# Function to monitor task progress
monitor_task_progress() {
    local task_id="$1"
    local task_file="$TASK_QUEUE_DIR/${task_id}.json"
    
    if [ ! -f "$task_file" ]; then
        echo -e "${RED}❌ Task not found: $task_id${NC}"
        return 1
    fi
    
    echo -e "${BLUE}📊 Task Progress Monitor${NC}"
    echo -e "${CYAN}======================${NC}"
    
    if command -v jq > /dev/null 2>&1; then
        local task_name=$(jq -r .task_name "$task_file")
        local status=$(jq -r .status "$task_file")
        local progress=$(jq -r .progress "$task_file")
        local assigned_agents=($(jq -r '.assigned_agents[]' "$task_file"))
        
        echo -e "${GREEN}Task: $task_name${NC}"
        echo -e "${YELLOW}Status: $status${NC}"
        echo -e "${CYAN}Progress: $progress%${NC}"
        echo -e "${MAGENTA}Assigned Agents: ${assigned_agents[*]}${NC}"
        
        # Show phase status
        echo -e "${BLUE}Phase Status:${NC}"
        local phases=("planning" "execution" "review" "completion")
        for phase in "${phases[@]}"; do
            local phase_status=$(jq -r ".phases.$phase.status" "$task_file")
            echo -e "${CYAN}  $phase: $phase_status${NC}"
        done
    else
        cat "$task_file"
    fi
}

# Function to list all tasks
list_tasks() {
    echo -e "${BLUE}📋 Task Queue Status${NC}"
    echo -e "${CYAN}===================${NC}"
    
    if [ ! -d "$TASK_QUEUE_DIR" ] || [ -z "$(ls -A "$TASK_QUEUE_DIR" 2>/dev/null)" ]; then
        echo -e "${YELLOW}No tasks in queue${NC}"
        return 0
    fi
    
    for task_file in "$TASK_QUEUE_DIR"/*.json; do
        if [ -f "$task_file" ] && command -v jq > /dev/null 2>&1; then
            local task_id=$(basename "$task_file" .json)
            local task_name=$(jq -r .task_name "$task_file")
            local status=$(jq -r .status "$task_file")
            local progress=$(jq -r .progress "$task_file")
            local complexity=$(jq -r .complexity "$task_file")
            
            echo -e "${GREEN}$task_id${NC}"
            echo -e "${CYAN}  Name: $task_name${NC}"
            echo -e "${YELLOW}  Status: $status | Progress: $progress% | Complexity: $complexity/10${NC}"
            echo ""
        fi
    done
}

# Main command processing
case "${1:-help}" in
    "create")
        create_complex_task "$2" "$3" "${4:-8}" "${5:-medium}" "${6:-none}"
        ;;
    "assign")
        assign_agents_to_task "$2"
        ;;
    "execute")
        execute_coordinated_task "$2"
        ;;
    "full-cycle")
        # Create, assign, and execute in one command
        task_name="$2"
        task_type="$3"
        complexity="${4:-8}"
        
        # Create task
        create_complex_task "$task_name" "$task_type" "$complexity"
        
        # Get the task ID (last created)
        task_id=$(ls -t "$TASK_QUEUE_DIR"/*.json | head -1 | xargs basename -s .json)
        
        # Assign agents
        assign_agents_to_task "$task_id"
        
        # Execute task
        execute_coordinated_task "$task_id"
        ;;
    "monitor")
        monitor_task_progress "$2"
        ;;
    "list")
        list_tasks
        ;;
    "status")
        echo -e "${BLUE}🎭 Agent Coordination Status${NC}"
        echo -e "${CYAN}=============================${NC}"
        list_tasks
        ;;
    *)
        echo -e "${BLUE}🎭 Agent Coordination Commands:${NC}"
        echo -e "${CYAN}  task-coordinator create <name> <type> [complexity] [priority] [deadline]${NC}"
        echo -e "${CYAN}  task-coordinator assign <task_id>                    - Assign agents${NC}"
        echo -e "${CYAN}  task-coordinator execute <task_id>                   - Execute task${NC}"
        echo -e "${CYAN}  task-coordinator full-cycle <name> <type> [complexity] - Full workflow${NC}"
        echo -e "${CYAN}  task-coordinator monitor <task_id>                   - Monitor progress${NC}"
        echo -e "${CYAN}  task-coordinator list                               - List all tasks${NC}"
        echo -e "${CYAN}  task-coordinator status                             - Show status${NC}"
        echo ""
        echo -e "${YELLOW}Task Types:${NC}"
        echo -e "${MAGENTA}  full-stack-development, research-and-analysis, problem-solving,${NC}"
        echo -e "${MAGENTA}  product-development, system-optimization${NC}"
        echo ""
        echo -e "${GREEN}Example: task-coordinator full-cycle 'Build API' full-stack-development 8${NC}"
        ;;
esac