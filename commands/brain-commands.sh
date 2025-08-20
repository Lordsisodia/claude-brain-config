#!/bin/bash
# Quick Brain Commands for Cognitive Enhancement
# Instant access to brain power and cognitive modes

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Configuration
BRAIN_DIR="/Users/shaansisodia/DEV/claude-brain-config"
BRAIN_SCRIPTS="$BRAIN_DIR/tmux-orchestrator"
BRAIN_WORKFLOWS="$BRAIN_DIR/workflows"
AUTONOMOUS_TASKS="$BRAIN_DIR/autonomous-tasks"
BRAIN_STORAGE="$BRAIN_DIR/storage"
LEARNING_ENGINE="$HOME/.learning-engine"

# Helper function to check if brain session exists
check_brain_session() {
    if ! tmux has-session -t BRAIN-MAIN 2>/dev/null; then
        echo -e "${YELLOW}🧠 Starting brain session...${NC}"
        $BRAIN_SCRIPTS/start-brain-with-learning.sh
        return 1
    fi
    return 0
}

# Quick Brain Launcher
brain() {
    case "$1" in
        "start"|"")
            echo -e "${BLUE}🧠 Starting Enhanced Brain...${NC}"
            $BRAIN_SCRIPTS/start-brain-with-learning.sh
            ;;
        "attach"|"connect")
            if check_brain_session; then
                tmux attach-session -t BRAIN-MAIN
            fi
            ;;
        "status")
            if tmux has-session -t BRAIN-MAIN 2>/dev/null; then
                echo -e "${GREEN}🧠 Brain Status: ACTIVE${NC}"
                echo -e "${CYAN}Windows:${NC}"
                tmux list-windows -t BRAIN-MAIN -F '  #{window_index}: #{window_name}'
                if [ -f "$LEARNING_ENGINE/status" ]; then
                    echo -e "${MAGENTA}Learning Engine: $(cat "$LEARNING_ENGINE/status")${NC}"
                fi
            else
                echo -e "${RED}🧠 Brain Status: INACTIVE${NC}"
            fi
            ;;
        "stop")
            if tmux has-session -t BRAIN-MAIN 2>/dev/null; then
                echo -e "${YELLOW}🛑 Stopping brain session...${NC}"
                tmux kill-session -t BRAIN-MAIN
            fi
            if [ -f "$LEARNING_ENGINE/stop_learning_engine.sh" ]; then
                $LEARNING_ENGINE/stop_learning_engine.sh
            fi
            echo -e "${GREEN}✅ Brain stopped${NC}"
            ;;
        "restart")
            brain stop
            sleep 2
            brain start
            ;;
        *)
            echo -e "${BLUE}🧠 Brain Commands:${NC}"
            echo -e "${CYAN}  brain start      - Start enhanced brain${NC}"
            echo -e "${CYAN}  brain attach     - Connect to brain session${NC}"
            echo -e "${CYAN}  brain status     - Check brain status${NC}"
            echo -e "${CYAN}  brain stop       - Stop brain session${NC}"
            echo -e "${CYAN}  brain restart    - Restart brain${NC}"
            ;;
    esac
}

# Quick Cognitive Mode Switching
think() {
    local task="$1"
    local complexity="${2:-6}"
    local mode="${3:-auto}"
    
    if [ -z "$task" ]; then
        echo -e "${BLUE}🧠 Think Commands:${NC}"
        echo -e "${CYAN}  think 'task' [complexity] [mode]${NC}"
        echo -e "${YELLOW}Modes: ultra-think, deep-analysis, quick-response, creative${NC}"
        echo -e "${GREEN}Example: think 'solve authentication bug' 8 ultra-think${NC}"
        return
    fi
    
    check_brain_session
    $BRAIN_SCRIPTS/quick-task.sh "$task" "$complexity" "$mode"
}

# Ultra Think Mode Activator
ultra_think() {
    local problem="$1"
    if [ -z "$problem" ]; then
        echo -e "${RED}🧠 Ultra Think Mode${NC}"
        echo -e "${CYAN}Usage: ultra_think 'complex problem'${NC}"
        return
    fi
    
    check_brain_session
    think "$problem" 9 ultra-think
    tmux select-window -t BRAIN-MAIN:ultra-think
}

# Quick Workflow Launchers
develop() {
    local project="${1:-development-project}"
    local complexity="${2:-6}"
    
    echo -e "${GREEN}💻 Activating Development Workflow${NC}"
    check_brain_session
    $BRAIN_WORKFLOWS/development-workflow.sh "$project" "$complexity"
}

# Autonomous Task Launchers
auto_prd() {
    local product="${1:-new-product}"
    local complexity="${2:-8}"
    local autonomy="${3:-full}"
    
    echo -e "${MAGENTA}🤖 Launching Autonomous PRD Workflow${NC}"
    check_brain_session
    $AUTONOMOUS_TASKS/autonomous-prd-workflow.sh "$product" "$complexity" "$autonomy"
}

# Coordination Commands
coordinate() {
    case "$1" in
        "create"|"task")
            echo -e "${GREEN}🎭 Creating coordinated task...${NC}"
            $BRAIN_DIR/coordination/task-coordinator.sh create "$2" "$3" "${4:-8}" "${5:-medium}" "$6"
            ;;
        "execute")
            echo -e "${BLUE}🚀 Executing coordinated task...${NC}"
            $BRAIN_DIR/coordination/task-coordinator.sh execute "$2"
            ;;
        "full-cycle")
            echo -e "${MAGENTA}🔄 Running full coordination cycle...${NC}"
            $BRAIN_DIR/coordination/task-coordinator.sh full-cycle "$2" "$3" "${4:-8}"
            ;;
        "schedule")
            echo -e "${CYAN}📅 Creating intelligent schedule...${NC}"
            $BRAIN_DIR/coordination/intelligent-scheduler.sh create-schedule "$2" "${3:-8}"
            ;;
        "auto-schedule")
            echo -e "${YELLOW}🤖 Auto-scheduling and executing...${NC}"
            $BRAIN_DIR/coordination/intelligent-scheduler.sh auto-schedule "${2:-8}"
            ;;
        "list")
            $BRAIN_DIR/coordination/task-coordinator.sh list
            ;;
        "status")
            echo -e "${BLUE}🎭 Coordination Status${NC}"
            $BRAIN_DIR/coordination/task-coordinator.sh status
            echo ""
            $BRAIN_DIR/coordination/intelligent-scheduler.sh status
            ;;
        "optimize")
            echo -e "${GREEN}⚡ Optimizing agent allocation...${NC}"
            $BRAIN_DIR/coordination/intelligent-scheduler.sh optimize-agents
            ;;
        *)
            echo -e "${BLUE}🎭 Coordination Commands:${NC}"
            echo -e "${CYAN}  coordinate create <name> <type> [complexity] [priority] [deadline]${NC}"
            echo -e "${CYAN}  coordinate execute <task_id>                         - Execute specific task${NC}"
            echo -e "${CYAN}  coordinate full-cycle <name> <type> [complexity]     - Complete workflow${NC}"
            echo -e "${CYAN}  coordinate schedule [name] [hours]                   - Create schedule${NC}"
            echo -e "${CYAN}  coordinate auto-schedule [hours]                     - Auto-schedule & execute${NC}"
            echo -e "${CYAN}  coordinate list                                      - List all tasks${NC}"
            echo -e "${CYAN}  coordinate status                                    - Show coordination status${NC}"
            echo -e "${CYAN}  coordinate optimize                                  - Optimize agents${NC}"
            echo ""
            echo -e "${YELLOW}Task Types:${NC}"
            echo -e "${MAGENTA}  full-stack-development, research-and-analysis, problem-solving,${NC}"
            echo -e "${MAGENTA}  product-development, system-optimization${NC}"
            echo ""
            echo -e "${GREEN}Examples:${NC}"
            echo -e "${MAGENTA}  coordinate full-cycle 'Build REST API' full-stack-development 8${NC}"
            echo -e "${MAGENTA}  coordinate auto-schedule 6${NC}"
            ;;
    esac
}

autonomous() {
    local task_type="$1"
    local task_name="${2:-autonomous-task}"
    local complexity="${3:-7}"
    
    case "$task_type" in
        "prd"|"product")
            auto_prd "$task_name" "$complexity" "full"
            ;;
        "research")
            echo -e "${BLUE}🤖 Launching Autonomous Research${NC}"
            check_brain_session
            research "$task_name" "$complexity"
            # Add autonomous monitoring
            ;;
        "develop"|"development")
            echo -e "${GREEN}🤖 Launching Autonomous Development${NC}"
            check_brain_session
            develop "$task_name" "$complexity"
            # Add autonomous monitoring
            ;;
        *)
            echo -e "${BLUE}🤖 Autonomous Task Types:${NC}"
            echo -e "${CYAN}  autonomous prd <product> [complexity]     - Autonomous PRD creation${NC}"
            echo -e "${CYAN}  autonomous research <topic> [depth]       - Autonomous research${NC}"
            echo -e "${CYAN}  autonomous develop <project> [complexity] - Autonomous development${NC}"
            echo -e "${GREEN}Example: autonomous prd 'mobile app' 8${NC}"
            ;;
    esac
}

research() {
    local topic="${1:-research-topic}"
    local depth="${2:-7}"
    
    echo -e "${BLUE}🔍 Activating Research Workflow${NC}"
    check_brain_session
    $BRAIN_WORKFLOWS/research-workflow.sh "$topic" "$depth"
}

solve() {
    local problem="${1:-complex-problem}"
    local complexity="${2:-8}"
    
    echo -e "${RED}🎯 Activating Problem Solving Workflow${NC}"
    check_brain_session
    $BRAIN_WORKFLOWS/problem-solving-workflow.sh "$problem" "$complexity"
}

# Quick Window Navigation
brain_nav() {
    if ! check_brain_session; then
        return
    fi
    
    case "$1" in
        "control"|"command")
            tmux select-window -t BRAIN-MAIN:control-center
            ;;
        "think"|"ultra")
            tmux select-window -t BRAIN-MAIN:ultra-think
            ;;
        "agents"|"team")
            tmux select-window -t BRAIN-MAIN:agents
            ;;
        "memory"|"mem")
            tmux select-window -t BRAIN-MAIN:memory
            ;;
        "tasks"|"orchestrator")
            tmux select-window -t BRAIN-MAIN:task-orchestrator
            ;;
        "monitor"|"stats")
            tmux select-window -t BRAIN-MAIN:monitor
            ;;
        "learning"|"learn")
            if tmux list-windows -t BRAIN-MAIN | grep -q "learning-dashboard"; then
                tmux select-window -t BRAIN-MAIN:learning-dashboard
            else
                echo -e "${YELLOW}Learning dashboard not available${NC}"
            fi
            ;;
        "mcp"|"tools")
            tmux select-window -t BRAIN-MAIN:mcp-servers
            ;;
        *)
            echo -e "${BLUE}🧠 Brain Navigation:${NC}"
            echo -e "${CYAN}  brain_nav control    - Control center${NC}"
            echo -e "${CYAN}  brain_nav think      - Ultra think chamber${NC}"
            echo -e "${CYAN}  brain_nav agents     - Agent coordination${NC}"
            echo -e "${CYAN}  brain_nav memory     - Memory systems${NC}"
            echo -e "${CYAN}  brain_nav tasks      - Task orchestrator${NC}"
            echo -e "${CYAN}  brain_nav monitor    - Performance monitor${NC}"
            echo -e "${CYAN}  brain_nav learning   - Learning dashboard${NC}"
            echo -e "${CYAN}  brain_nav mcp        - MCP servers${NC}"
            ;;
    esac
}

# Agent Commands
agents() {
    if ! check_brain_session; then
        return
    fi
    
    case "$1" in
        "deploy"|"start")
            echo -e "${GREEN}🤖 Deploying agents...${NC}"
            $BRAIN_SCRIPTS/deploy-agents.sh
            ;;
        "status"|"list")
            echo -e "${BLUE}🤖 Agent Status:${NC}"
            tmux list-windows -t BRAIN-MAIN | grep -E "(architect|implementer|reviewer|tester|documenter|optimizer|security|frontend|orchestrator)" || echo "No agents deployed"
            ;;
        "architect")
            tmux select-window -t BRAIN-MAIN:architect 2>/dev/null || echo "Architect not deployed"
            ;;
        "implementer"|"code")
            tmux select-window -t BRAIN-MAIN:implementer 2>/dev/null || echo "Implementer not deployed"
            ;;
        "reviewer"|"review")
            tmux select-window -t BRAIN-MAIN:reviewer 2>/dev/null || echo "Reviewer not deployed"
            ;;
        "tester"|"test")
            tmux select-window -t BRAIN-MAIN:tester 2>/dev/null || echo "Tester not deployed"
            ;;
        "security"|"sec")
            tmux select-window -t BRAIN-MAIN:security 2>/dev/null || echo "Security agent not deployed"
            ;;
        *)
            echo -e "${BLUE}🤖 Agent Commands:${NC}"
            echo -e "${CYAN}  agents deploy        - Deploy all agents${NC}"
            echo -e "${CYAN}  agents status        - Show agent status${NC}"
            echo -e "${CYAN}  agents architect     - Go to architect${NC}"
            echo -e "${CYAN}  agents implementer   - Go to implementer${NC}"
            echo -e "${CYAN}  agents reviewer      - Go to reviewer${NC}"
            echo -e "${CYAN}  agents tester        - Go to tester${NC}"
            echo -e "${CYAN}  agents security      - Go to security${NC}"
            ;;
    esac
}

# Learning Commands
learn() {
    case "$1" in
        "start")
            echo -e "${MAGENTA}📈 Starting Learning Engine...${NC}"
            if [ -f "$BRAIN_DIR/learning-engine/init/start_learning_engine.sh" ]; then
                $BRAIN_DIR/learning-engine/init/start_learning_engine.sh --no-dashboard
            else
                echo -e "${RED}Learning engine not found${NC}"
            fi
            ;;
        "dashboard"|"monitor")
            if [ -f "$LEARNING_ENGINE/monitor_dashboard.sh" ]; then
                $LEARNING_ENGINE/monitor_dashboard.sh
            else
                echo -e "${RED}Learning dashboard not available${NC}"
            fi
            ;;
        "status")
            if [ -f "$LEARNING_ENGINE/status" ]; then
                echo -e "${MAGENTA}Learning Engine: $(cat "$LEARNING_ENGINE/status")${NC}"
                if [ -d "$LEARNING_ENGINE/patterns" ]; then
                    PATTERN_COUNT=$(find "$LEARNING_ENGINE/patterns" -name "*.json" 2>/dev/null | wc -l)
                    echo -e "${CYAN}Patterns Discovered: $PATTERN_COUNT${NC}"
                fi
            else
                echo -e "${RED}Learning engine not initialized${NC}"
            fi
            ;;
        "patterns")
            if [ -d "$LEARNING_ENGINE/patterns" ]; then
                echo -e "${BLUE}🧠 Discovered Patterns:${NC}"
                find "$LEARNING_ENGINE/patterns" -name "*.json" -exec echo "  📊 {}" \;
            else
                echo -e "${YELLOW}No patterns found${NC}"
            fi
            ;;
        "stop")
            if [ -f "$LEARNING_ENGINE/stop_learning_engine.sh" ]; then
                $LEARNING_ENGINE/stop_learning_engine.sh
            fi
            ;;
        *)
            echo -e "${MAGENTA}📈 Learning Commands:${NC}"
            echo -e "${CYAN}  learn start      - Start learning engine${NC}"
            echo -e "${CYAN}  learn dashboard  - Show learning dashboard${NC}"
            echo -e "${CYAN}  learn status     - Check learning status${NC}"
            echo -e "${CYAN}  learn patterns   - Show discovered patterns${NC}"
            echo -e "${CYAN}  learn stop       - Stop learning engine${NC}"
            ;;
    esac
}

# Monitoring Commands
monitor() {
    case "$1" in
        "start")
            echo -e "${BLUE}📊 Starting Brain Monitoring...${NC}"
            $BRAIN_DIR/monitoring/brain-monitor.sh start
            ;;
        "stop")
            echo -e "${YELLOW}🛑 Stopping Brain Monitoring...${NC}"
            $BRAIN_DIR/monitoring/brain-monitor.sh stop
            ;;
        "status")
            $BRAIN_DIR/monitoring/brain-monitor.sh status
            ;;
        "dashboard")
            $BRAIN_DIR/monitoring/brain-monitor.sh dashboard
            ;;
        "progress")
            $BRAIN_DIR/monitoring/progress-tracker.sh summary
            ;;
        "report")
            echo -e "${GREEN}📋 Generating Progress Report...${NC}"
            $BRAIN_DIR/monitoring/progress-tracker.sh report
            ;;
        *)
            echo -e "${BLUE}📊 Monitoring Commands:${NC}"
            echo -e "${CYAN}  monitor start      - Start brain monitoring${NC}"
            echo -e "${CYAN}  monitor stop       - Stop monitoring${NC}"
            echo -e "${CYAN}  monitor status     - Check monitoring status${NC}"
            echo -e "${CYAN}  monitor dashboard  - Open monitoring dashboard${NC}"
            echo -e "${CYAN}  monitor progress   - Show progress summary${NC}"
            echo -e "${CYAN}  monitor report     - Generate full progress report${NC}"
            ;;
    esac
}

# Storage Commands
storage() {
    case "$1" in
        "analyze"|"usage")
            $BRAIN_DIR/storage/storage-manager.sh analyze
            ;;
        "backup")
            echo -e "${GREEN}📦 Creating backup...${NC}"
            $BRAIN_DIR/storage/storage-manager.sh backup "${2:-daily}"
            ;;
        "export")
            echo -e "${BLUE}📤 Exporting data...${NC}"
            $BRAIN_DIR/storage/storage-manager.sh export "${2:-json}" "$3"
            ;;
        "catalog")
            echo -e "${CYAN}📋 Creating storage catalog...${NC}"
            $BRAIN_DIR/storage/storage-manager.sh catalog
            ;;
        "cleanup")
            echo -e "${YELLOW}🧹 Running storage cleanup...${NC}"
            $BRAIN_DIR/storage/storage-manager.sh cleanup
            ;;
        "service")
            case "$2" in
                "start")
                    echo -e "${GREEN}🚀 Starting persistence service...${NC}"
                    $BRAIN_DIR/storage/persistence-service.sh start
                    ;;
                "stop")
                    echo -e "${YELLOW}🛑 Stopping persistence service...${NC}"
                    $BRAIN_DIR/storage/persistence-service.sh stop
                    ;;
                "status")
                    $BRAIN_DIR/storage/persistence-service.sh status
                    ;;
                *)
                    echo -e "${BLUE}🔄 Storage Service Commands:${NC}"
                    echo -e "${CYAN}  storage service start    - Start persistence service${NC}"
                    echo -e "${CYAN}  storage service stop     - Stop persistence service${NC}"
                    echo -e "${CYAN}  storage service status   - Show service status${NC}"
                    ;;
            esac
            ;;
        "status"|"stats")
            $BRAIN_DIR/storage/storage-manager.sh status
            ;;
        "maintenance")
            echo -e "${GREEN}🔧 Running full storage maintenance...${NC}"
            $BRAIN_DIR/storage/storage-manager.sh full-maintenance
            ;;
        *)
            echo -e "${BLUE}💾 Storage Commands:${NC}"
            echo -e "${CYAN}  storage analyze                       - Analyze storage usage${NC}"
            echo -e "${CYAN}  storage backup [daily|weekly|monthly] - Create backup${NC}"
            echo -e "${CYAN}  storage export [json|csv|archive] [path] - Export data${NC}"
            echo -e "${CYAN}  storage catalog                       - Create storage catalog${NC}"
            echo -e "${CYAN}  storage cleanup                       - Cleanup old files${NC}"
            echo -e "${CYAN}  storage service <start|stop|status>   - Manage persistence service${NC}"
            echo -e "${CYAN}  storage status                        - Show storage statistics${NC}"
            echo -e "${CYAN}  storage maintenance                   - Full maintenance cycle${NC}"
            echo ""
            echo -e "${GREEN}Examples:${NC}"
            echo -e "${MAGENTA}  storage backup weekly${NC}"
            echo -e "${MAGENTA}  storage export json /tmp/brain-export${NC}"
            echo -e "${MAGENTA}  storage service start${NC}"
            ;;
    esac
}

# Performance Monitoring
brain_stats() {
    if ! check_brain_session; then
        return
    fi
    
    echo -e "${BLUE}🧠 Brain Performance Statistics${NC}"
    echo -e "${CYAN}================================${NC}"
    
    # Session info
    SESSION_INFO=$(tmux display-message -t BRAIN-MAIN -p "Created: #{session_created_string} | Windows: #{session_windows}")
    echo -e "${GREEN}Session: $SESSION_INFO${NC}"
    
    # Window count
    WINDOW_COUNT=$(tmux list-windows -t BRAIN-MAIN | wc -l)
    echo -e "${CYAN}Active Windows: $WINDOW_COUNT${NC}"
    
    # Agent status
    AGENT_COUNT=$(tmux list-windows -t BRAIN-MAIN | grep -E "(architect|implementer|reviewer|tester|documenter)" | wc -l)
    echo -e "${MAGENTA}Active Agents: $AGENT_COUNT${NC}"
    
    # Learning engine status
    if [ -f "$LEARNING_ENGINE/status" ]; then
        LEARNING_STATUS=$(cat "$LEARNING_ENGINE/status")
        echo -e "${YELLOW}Learning Engine: $LEARNING_STATUS${NC}"
        
        if [ -d "$LEARNING_ENGINE/patterns" ]; then
            PATTERN_COUNT=$(find "$LEARNING_ENGINE/patterns" -name "*.json" 2>/dev/null | wc -l)
            echo -e "${BLUE}Patterns Learned: $PATTERN_COUNT${NC}"
        fi
    fi
    
    # Recent activity
    echo -e "${CYAN}Recent Windows:${NC}"
    tmux list-windows -t BRAIN-MAIN -F '  #{window_index}: #{window_name} #{?window_active,(active),}' | tail -5
}

# Quick Help
brain_help() {
    echo -e "${BLUE}🧠 ULTIMATE BRAIN COMMAND REFERENCE${NC}"
    echo -e "${CYAN}=====================================${NC}"
    echo ""
    echo -e "${GREEN}🚀 Core Commands:${NC}"
    echo -e "${CYAN}  brain            - Brain session management${NC}"
    echo -e "${CYAN}  think            - Quick task launcher${NC}"
    echo -e "${CYAN}  ultra_think      - Maximum reasoning mode${NC}"
    echo ""
    echo -e "${GREEN}📋 Workflows:${NC}"
    echo -e "${CYAN}  develop          - Development workflow${NC}"
    echo -e "${CYAN}  research         - Research workflow${NC}"
    echo -e "${CYAN}  solve            - Problem solving workflow${NC}"
    echo ""
    echo -e "${GREEN}🤖 Agent Control & Coordination:${NC}"
    echo -e "${CYAN}  agents           - Agent management${NC}"
    echo -e "${CYAN}  coordinate       - Multi-agent task coordination${NC}"
    echo -e "${CYAN}  brain_nav        - Quick window navigation${NC}"
    echo ""
    echo -e "${GREEN}📈 Learning, Monitoring & Storage:${NC}"
    echo -e "${CYAN}  learn            - Learning engine control${NC}"
    echo -e "${CYAN}  monitor          - Brain monitoring & progress tracking${NC}"
    echo -e "${CYAN}  storage          - Storage management & persistence${NC}"
    echo -e "${CYAN}  brain_stats      - Performance statistics${NC}"
    echo ""
    echo -e "${YELLOW}💡 Quick Examples:${NC}"
    echo -e "${MAGENTA}  think 'debug memory leak' 8 ultra-think${NC}"
    echo -e "${MAGENTA}  develop 'user authentication system' 7${NC}"
    echo -e "${MAGENTA}  research 'machine learning algorithms' 8${NC}"
    echo -e "${MAGENTA}  solve 'performance bottleneck' 9${NC}"
}

# Aliases for convenience
alias b='brain'
alias t='think'
alias ut='ultra_think'
alias dev='develop'
alias res='research'
alias nav='brain_nav'
alias bnav='brain_nav'
alias bstats='brain_stats'
alias bhelp='brain_help'
alias mon='monitor'
alias prog='monitor progress'
alias coord='coordinate'
alias auto='autonomous'
alias store='storage'

# Export functions for use in subshells
export -f brain think ultra_think develop research solve brain_nav agents learn monitor coordinate autonomous storage brain_stats brain_help check_brain_session

# Display quick help on source
echo -e "${GREEN}🧠 Brain Commands Loaded!${NC}"
echo -e "${CYAN}Type 'brain_help' for full command reference${NC}"
echo -e "${YELLOW}Quick start: brain start${NC}"