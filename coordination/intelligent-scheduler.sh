#!/bin/bash
# Intelligent Task Scheduler
# AI-powered task scheduling with priority optimization and dependency management

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
SCHEDULER_DIR="/Users/shaansisodia/DEV/claude-brain-config/coordination/scheduler"
TASK_QUEUE_DIR="/Users/shaansisodia/DEV/claude-brain-config/coordination/task-queue"
SESSION_NAME="BRAIN-MAIN"

# Create scheduler directories
mkdir -p "$SCHEDULER_DIR"/{rules,priorities,dependencies,schedules}

echo -e "${BLUE}🧠 INTELLIGENT TASK SCHEDULER${NC}"
echo -e "${CYAN}=============================${NC}"

# Function to analyze task complexity and auto-assign priority
analyze_task_priority() {
    local task_type="$1"
    local complexity="$2"
    local deadline="$3"
    local user_priority="${4:-auto}"
    
    # Base priority calculation
    local calculated_priority="medium"
    local priority_score=0
    
    # Complexity factor (0-10 scale)
    priority_score=$((priority_score + complexity))
    
    # Task type factor
    case "$task_type" in
        "critical-bug-fix"|"security-patch")
            priority_score=$((priority_score + 8))
            ;;
        "product-development"|"full-stack-development")
            priority_score=$((priority_score + 6))
            ;;
        "research-and-analysis")
            priority_score=$((priority_score + 4))
            ;;
        "optimization"|"refactoring")
            priority_score=$((priority_score + 3))
            ;;
        *)
            priority_score=$((priority_score + 2))
            ;;
    esac
    
    # Deadline factor
    if [ "$deadline" != "none" ]; then
        local deadline_timestamp=$(date -d "$deadline" +%s 2>/dev/null || echo "0")
        local current_timestamp=$(date +%s)
        local days_until_deadline=$(( (deadline_timestamp - current_timestamp) / 86400 ))
        
        if [ $days_until_deadline -le 1 ]; then
            priority_score=$((priority_score + 10))
        elif [ $days_until_deadline -le 3 ]; then
            priority_score=$((priority_score + 6))
        elif [ $days_until_deadline -le 7 ]; then
            priority_score=$((priority_score + 3))
        fi
    fi
    
    # Convert score to priority level
    if [ $priority_score -ge 20 ]; then
        calculated_priority="critical"
    elif [ $priority_score -ge 15 ]; then
        calculated_priority="high"
    elif [ $priority_score -ge 10 ]; then
        calculated_priority="medium"
    else
        calculated_priority="low"
    fi
    
    # Override with user priority if specified
    if [ "$user_priority" != "auto" ]; then
        calculated_priority="$user_priority"
    fi
    
    echo "$calculated_priority"
}

# Function to detect task dependencies
detect_task_dependencies() {
    local task_name="$1"
    local task_type="$2"
    local dependencies=()
    
    # Keyword-based dependency detection
    case "$task_type" in
        "full-stack-development")
            # Look for existing architecture or design tasks
            for existing_task in "$TASK_QUEUE_DIR"/*.json; do
                if [ -f "$existing_task" ]; then
                    local existing_name=$(jq -r .task_name "$existing_task" 2>/dev/null || echo "")
                    local existing_type=$(jq -r .task_type "$existing_task" 2>/dev/null || echo "")
                    
                    if [[ "$existing_type" == "system-design" ]] || [[ "$existing_name" == *"architecture"* ]]; then
                        dependencies+=($(basename "$existing_task" .json))
                    fi
                fi
            done
            ;;
        "testing"|"deployment")
            # Look for implementation tasks
            for existing_task in "$TASK_QUEUE_DIR"/*.json; do
                if [ -f "$existing_task" ]; then
                    local existing_type=$(jq -r .task_type "$existing_task" 2>/dev/null || echo "")
                    local existing_status=$(jq -r .status "$existing_task" 2>/dev/null || echo "")
                    
                    if [[ "$existing_type" == *"development"* ]] && [[ "$existing_status" != "completed" ]]; then
                        dependencies+=($(basename "$existing_task" .json))
                    fi
                fi
            done
            ;;
        "optimization")
            # Look for baseline implementation
            for existing_task in "$TASK_QUEUE_DIR"/*.json; do
                if [ -f "$existing_task" ]; then
                    local existing_name=$(jq -r .task_name "$existing_task" 2>/dev/null || echo "")
                    
                    if [[ "$existing_name" == *"implement"* ]] || [[ "$existing_name" == *"build"* ]]; then
                        dependencies+=($(basename "$existing_task" .json))
                    fi
                fi
            done
            ;;
    esac
    
    # Output dependencies as JSON array
    if [ ${#dependencies[@]} -gt 0 ]; then
        printf '"%s",' "${dependencies[@]}" | sed 's/,$//'
    fi
}

# Function to create intelligent schedule
create_intelligent_schedule() {
    local schedule_name="${1:-daily-schedule}"
    local time_horizon="${2:-8}"  # hours
    local schedule_file="$SCHEDULER_DIR/schedules/${schedule_name}_$(date +%Y%m%d_%H%M%S).json"
    
    echo -e "${GREEN}🧠 Creating intelligent schedule: $schedule_name${NC}"
    
    # Collect all pending tasks
    local pending_tasks=()
    local task_details=()
    
    for task_file in "$TASK_QUEUE_DIR"/*.json; do
        if [ -f "$task_file" ]; then
            local status=$(jq -r .status "$task_file" 2>/dev/null || echo "unknown")
            if [ "$status" = "queued" ] || [ "$status" = "assigned" ]; then
                local task_id=$(basename "$task_file" .json)
                pending_tasks+=("$task_id")
                
                local task_name=$(jq -r .task_name "$task_file" 2>/dev/null || echo "unknown")
                local priority=$(jq -r .priority "$task_file" 2>/dev/null || echo "medium")
                local complexity=$(jq -r .complexity "$task_file" 2>/dev/null || echo "5")
                local estimated_duration=$(jq -r .estimated_duration "$task_file" 2>/dev/null || echo "2-4 hours")
                
                task_details+=("$task_id:$task_name:$priority:$complexity:$estimated_duration")
            fi
        fi
    done
    
    # Sort tasks by intelligent priority
    local sorted_tasks=()
    
    # Critical tasks first
    for detail in "${task_details[@]}"; do
        IFS=':' read -r task_id task_name priority complexity duration <<< "$detail"
        if [ "$priority" = "critical" ]; then
            sorted_tasks+=("$detail")
        fi
    done
    
    # High priority tasks
    for detail in "${task_details[@]}"; do
        IFS=':' read -r task_id task_name priority complexity duration <<< "$detail"
        if [ "$priority" = "high" ]; then
            sorted_tasks+=("$detail")
        fi
    done
    
    # Medium priority tasks
    for detail in "${task_details[@]}"; do
        IFS=':' read -r task_id task_name priority complexity duration <<< "$detail"
        if [ "$priority" = "medium" ]; then
            sorted_tasks+=("$detail")
        fi
    done
    
    # Low priority tasks
    for detail in "${task_details[@]}"; do
        IFS=':' read -r task_id task_name priority complexity duration <<< "$detail"
        if [ "$priority" = "low" ]; then
            sorted_tasks+=("$detail")
        fi
    done
    
    # Create schedule structure
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local schedule_slots=()
    local current_hour=0
    
    for detail in "${sorted_tasks[@]}"; do
        IFS=':' read -r task_id task_name priority complexity duration <<< "$detail"
        
        # Estimate time slot based on complexity
        local time_slot=1
        if [ "$complexity" -ge 8 ]; then
            time_slot=3
        elif [ "$complexity" -ge 6 ]; then
            time_slot=2
        fi
        
        # Check if we have time left
        if [ $((current_hour + time_slot)) -le "$time_horizon" ]; then
            local start_time=$((current_hour))
            local end_time=$((current_hour + time_slot))
            
            schedule_slots+=("{\"task_id\": \"$task_id\", \"task_name\": \"$task_name\", \"priority\": \"$priority\", \"start_hour\": $start_time, \"end_hour\": $end_time, \"estimated_duration\": \"$time_slot hours\"}")
            
            current_hour=$((current_hour + time_slot))
        fi
        
        # Break if we've filled the time horizon
        if [ $current_hour -ge "$time_horizon" ]; then
            break
        fi
    done
    
    # Create schedule JSON
    cat > "$schedule_file" << EOF
{
    "schedule_name": "$schedule_name",
    "created": "$timestamp",
    "time_horizon_hours": $time_horizon,
    "total_tasks_scheduled": ${#schedule_slots[@]},
    "optimization_strategy": "priority_based_with_complexity_timing",
    "schedule": [
        $(IFS=','; echo "${schedule_slots[*]}")
    ],
    "metadata": {
        "total_pending_tasks": ${#pending_tasks[@]},
        "scheduler_version": "intelligent-v1.0",
        "optimization_factors": ["priority", "complexity", "dependencies", "time_availability"]
    }
}
EOF
    
    echo -e "${GREEN}✅ Intelligent schedule created: $schedule_file${NC}"
    echo -e "${CYAN}Tasks scheduled: ${#schedule_slots[@]}/${#pending_tasks[@]}${NC}"
    echo -e "${YELLOW}Time horizon: $time_horizon hours${NC}"
    
    # Display schedule summary
    echo -e "${BLUE}📅 Schedule Summary:${NC}"
    local slot_num=1
    for detail in "${schedule_slots[@]}"; do
        if command -v jq > /dev/null 2>&1; then
            local task_name=$(echo "$detail" | jq -r .task_name)
            local priority=$(echo "$detail" | jq -r .priority)
            local start_hour=$(echo "$detail" | jq -r .start_hour)
            local end_hour=$(echo "$detail" | jq -r .end_hour)
            
            echo -e "${CYAN}  $slot_num. $task_name${NC}"
            echo -e "${YELLOW}     Priority: $priority | Time: ${start_hour}h-${end_hour}h${NC}"
            slot_num=$((slot_num + 1))
        fi
    done
}

# Function to optimize agent allocation
optimize_agent_allocation() {
    echo -e "${GREEN}🤖 Optimizing agent allocation...${NC}"
    
    # Analyze current agent workload
    local agent_workload=()
    local agents=("architect" "implementer" "reviewer" "tester" "documenter" "security" "optimizer" "orchestrator")
    
    for agent in "${agents[@]}"; do
        local assigned_tasks=0
        local total_complexity=0
        
        # Count tasks assigned to each agent
        for status_file in "$AGENT_STATUS_DIR"/${agent}_*.json; do
            if [ -f "$status_file" ]; then
                local task_id=$(basename "$status_file" | sed "s/${agent}_//" | sed 's/.json$//')
                local task_file="$TASK_QUEUE_DIR/${task_id}.json"
                
                if [ -f "$task_file" ]; then
                    local task_status=$(jq -r .status "$task_file" 2>/dev/null || echo "unknown")
                    if [ "$task_status" != "completed" ]; then
                        assigned_tasks=$((assigned_tasks + 1))
                        local complexity=$(jq -r .complexity "$task_file" 2>/dev/null || echo "5")
                        total_complexity=$((total_complexity + complexity))
                    fi
                fi
            fi
        done
        
        agent_workload+=("$agent:$assigned_tasks:$total_complexity")
        echo -e "${CYAN}  $agent: $assigned_tasks tasks (complexity: $total_complexity)${NC}"
    done
    
    # Find underutilized agents
    echo -e "${YELLOW}Optimization suggestions:${NC}"
    for workload in "${agent_workload[@]}"; do
        IFS=':' read -r agent tasks complexity <<< "$workload"
        
        if [ "$tasks" -eq 0 ]; then
            echo -e "${GREEN}  ✅ $agent: Available for new tasks${NC}"
        elif [ "$tasks" -ge 3 ]; then
            echo -e "${RED}  ⚠️ $agent: Overloaded ($tasks tasks)${NC}"
        fi
    done
}

# Function to execute scheduled tasks
execute_scheduled_tasks() {
    local schedule_file="$1"
    
    if [ ! -f "$schedule_file" ]; then
        echo -e "${RED}❌ Schedule file not found: $schedule_file${NC}"
        return 1
    fi
    
    echo -e "${GREEN}🚀 Executing scheduled tasks from: $(basename "$schedule_file")${NC}"
    
    if command -v jq > /dev/null 2>&1; then
        local schedule_tasks=($(jq -r '.schedule[].task_id' "$schedule_file"))
        
        for task_id in "${schedule_tasks[@]}"; do
            echo -e "${CYAN}📋 Executing task: $task_id${NC}"
            
            # Use the task coordinator to execute the task
            /Users/shaansisodia/DEV/claude-brain-config/coordination/task-coordinator.sh execute "$task_id"
            
            # Wait between tasks
            sleep 2
        done
    fi
    
    echo -e "${GREEN}✅ Scheduled task execution complete${NC}"
}

# Function to show scheduler status
show_scheduler_status() {
    echo -e "${BLUE}🧠 Intelligent Scheduler Status${NC}"
    echo -e "${CYAN}===============================${NC}"
    
    # Count tasks by status
    local queued_count=0
    local assigned_count=0
    local executing_count=0
    local completed_count=0
    
    for task_file in "$TASK_QUEUE_DIR"/*.json; do
        if [ -f "$task_file" ]; then
            local status=$(jq -r .status "$task_file" 2>/dev/null || echo "unknown")
            case "$status" in
                "queued") queued_count=$((queued_count + 1)) ;;
                "assigned") assigned_count=$((assigned_count + 1)) ;;
                "executing") executing_count=$((executing_count + 1)) ;;
                "completed") completed_count=$((completed_count + 1)) ;;
            esac
        fi
    done
    
    echo -e "${GREEN}📊 Task Queue Status:${NC}"
    echo -e "${YELLOW}  Queued: $queued_count${NC}"
    echo -e "${CYAN}  Assigned: $assigned_count${NC}"
    echo -e "${BLUE}  Executing: $executing_count${NC}"
    echo -e "${MAGENTA}  Completed: $completed_count${NC}"
    
    # Show recent schedules
    echo -e "${GREEN}📅 Recent Schedules:${NC}"
    ls -t "$SCHEDULER_DIR/schedules"/*.json 2>/dev/null | head -3 | while read schedule; do
        local schedule_name=$(basename "$schedule" .json)
        echo -e "${CYAN}  $schedule_name${NC}"
    done || echo -e "${YELLOW}  No schedules found${NC}"
    
    # Show optimization recommendations
    optimize_agent_allocation
}

# Main command processing
case "${1:-status}" in
    "create-schedule")
        create_intelligent_schedule "$2" "${3:-8}"
        ;;
    "execute-schedule")
        execute_scheduled_tasks "$2"
        ;;
    "analyze-priority")
        analyze_task_priority "$2" "$3" "$4" "$5"
        ;;
    "optimize-agents")
        optimize_agent_allocation
        ;;
    "auto-schedule")
        # Create and execute schedule in one command
        schedule_name="auto-$(date +%H%M%S)"
        create_intelligent_schedule "$schedule_name" "${2:-8}"
        latest_schedule=$(ls -t "$SCHEDULER_DIR/schedules"/*.json | head -1)
        execute_scheduled_tasks "$latest_schedule"
        ;;
    "status")
        show_scheduler_status
        ;;
    *)
        echo -e "${BLUE}🧠 Intelligent Scheduler Commands:${NC}"
        echo -e "${CYAN}  intelligent-scheduler create-schedule [name] [hours]     - Create optimized schedule${NC}"
        echo -e "${CYAN}  intelligent-scheduler execute-schedule <file>           - Execute scheduled tasks${NC}"
        echo -e "${CYAN}  intelligent-scheduler auto-schedule [hours]             - Create and execute${NC}"
        echo -e "${CYAN}  intelligent-scheduler analyze-priority <type> <complexity> <deadline> [priority]${NC}"
        echo -e "${CYAN}  intelligent-scheduler optimize-agents                   - Optimize agent allocation${NC}"
        echo -e "${CYAN}  intelligent-scheduler status                            - Show scheduler status${NC}"
        echo ""
        echo -e "${GREEN}Examples:${NC}"
        echo -e "${MAGENTA}  intelligent-scheduler create-schedule daily-work 8${NC}"
        echo -e "${MAGENTA}  intelligent-scheduler auto-schedule 6${NC}"
        echo -e "${MAGENTA}  intelligent-scheduler analyze-priority full-stack-development 8 '2024-01-15'${NC}"
        ;;
esac