#!/bin/bash
# Autonomous Progress Tracking System
# Tracks progress across all brain activities and autonomous tasks

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
PROGRESS_DIR="/Users/shaansisodia/DEV/claude-brain-config/monitoring/progress"
STORAGE_DIR="/Users/shaansisodia/DEV/claude-brain-config/storage"
LEARNING_ENGINE="$HOME/.learning-engine"

# Create progress directories
mkdir -p "$PROGRESS_DIR"/{tasks,projects,learning,reports}

echo -e "${BLUE}📈 AUTONOMOUS PROGRESS TRACKING SYSTEM${NC}"
echo -e "${CYAN}=====================================${NC}"

# Function to track task progress
track_task_progress() {
    local task_id="$1"
    local task_type="$2"
    local status="$3"
    local progress_percent="${4:-0}"
    local notes="${5:-}"
    
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local task_file="$PROGRESS_DIR/tasks/${task_id}.json"
    
    # Create or update task progress
    cat > "$task_file" << EOF
{
    "task_id": "$task_id",
    "task_type": "$task_type",
    "status": "$status",
    "progress_percent": $progress_percent,
    "notes": "$notes",
    "last_updated": "$timestamp",
    "created": "$(if [ -f "$task_file" ]; then jq -r .created "$task_file" 2>/dev/null || echo "$timestamp"; else echo "$timestamp"; fi)",
    "history": $(if [ -f "$task_file" ]; then jq -r .history "$task_file" 2>/dev/null || echo "[]"; else echo "[]"; fi)
}
EOF
    
    # Add to history
    if command -v jq > /dev/null 2>&1; then
        local temp_file=$(mktemp)
        jq --arg timestamp "$timestamp" --arg status "$status" --argjson progress "$progress_percent" --arg notes "$notes" \
           '.history += [{"timestamp": $timestamp, "status": $status, "progress": $progress, "notes": $notes}]' \
           "$task_file" > "$temp_file" && mv "$temp_file" "$task_file"
    fi
    
    echo -e "${GREEN}📈 Task progress updated: $task_id ($progress_percent%)${NC}"
}

# Function to track project progress
track_project_progress() {
    local project_name="$1"
    local project_type="$2"
    local phase="$3"
    local completion_percent="${4:-0}"
    
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local project_file="$PROGRESS_DIR/projects/${project_name}.json"
    
    # Analyze project files for automatic progress detection
    local files_created=0
    local total_size=0
    
    case "$project_type" in
        "prd")
            if [ -d "$STORAGE_DIR/prd-projects/$project_name" ]; then
                files_created=$(find "$STORAGE_DIR/prd-projects/$project_name" -type f | wc -l)
                total_size=$(du -s "$STORAGE_DIR/prd-projects/$project_name" 2>/dev/null | cut -f1 || echo "0")
            fi
            ;;
        "research")
            if [ -d "$STORAGE_DIR/research-projects/$project_name" ]; then
                files_created=$(find "$STORAGE_DIR/research-projects/$project_name" -type f | wc -l)
                total_size=$(du -s "$STORAGE_DIR/research-projects/$project_name" 2>/dev/null | cut -f1 || echo "0")
            fi
            ;;
        "problem-solving")
            if [ -d "$STORAGE_DIR/problem-solutions/$project_name" ]; then
                files_created=$(find "$STORAGE_DIR/problem-solutions/$project_name" -type f | wc -l)
                total_size=$(du -s "$STORAGE_DIR/problem-solutions/$project_name" 2>/dev/null | cut -f1 || echo "0")
            fi
            ;;
    esac
    
    # Create project progress record
    cat > "$project_file" << EOF
{
    "project_name": "$project_name",
    "project_type": "$project_type",
    "current_phase": "$phase",
    "completion_percent": $completion_percent,
    "files_created": $files_created,
    "total_size_kb": $total_size,
    "last_updated": "$timestamp",
    "created": "$(if [ -f "$project_file" ]; then jq -r .created "$project_file" 2>/dev/null || echo "$timestamp"; else echo "$timestamp"; fi)",
    "phases": {
        "planning": $(if [ "$phase" = "planning" ]; then echo "\"in_progress\""; elif [ "$completion_percent" -gt 20 ]; then echo "\"completed\""; else echo "\"pending\""; fi),
        "execution": $(if [ "$phase" = "execution" ]; then echo "\"in_progress\""; elif [ "$completion_percent" -gt 60 ]; then echo "\"completed\""; else echo "\"pending\""; fi),
        "review": $(if [ "$phase" = "review" ]; then echo "\"in_progress\""; elif [ "$completion_percent" -gt 80 ]; then echo "\"completed\""; else echo "\"pending\""; fi),
        "completion": $(if [ "$completion_percent" -ge 100 ]; then echo "\"completed\""; else echo "\"pending\""; fi)
    }
}
EOF
    
    echo -e "${GREEN}📊 Project progress updated: $project_name ($completion_percent%)${NC}"
}

# Function to track learning progress
track_learning_progress() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local learning_file="$PROGRESS_DIR/learning/learning_progress.json"
    
    # Collect learning metrics
    local patterns_count=0
    local sessions_count=0
    local learning_status="inactive"
    
    if [ -f "$LEARNING_ENGINE/status" ]; then
        learning_status=$(cat "$LEARNING_ENGINE/status")
    fi
    
    if [ -d "$LEARNING_ENGINE/patterns" ]; then
        patterns_count=$(find "$LEARNING_ENGINE/patterns" -name "*.json" 2>/dev/null | wc -l)
    fi
    
    if [ -d "$LEARNING_ENGINE/sessions" ]; then
        sessions_count=$(find "$LEARNING_ENGINE/sessions" -name "*.log" 2>/dev/null | wc -l)
    fi
    
    # Calculate learning progress metrics
    local learning_efficiency=0
    if [ $sessions_count -gt 0 ]; then
        learning_efficiency=$(echo "scale=2; $patterns_count / $sessions_count * 100" | bc -l 2>/dev/null || echo "0")
    fi
    
    cat > "$learning_file" << EOF
{
    "learning_status": "$learning_status",
    "patterns_discovered": $patterns_count,
    "sessions_recorded": $sessions_count,
    "learning_efficiency": $learning_efficiency,
    "last_updated": "$timestamp",
    "milestones": {
        "first_pattern": $(if [ $patterns_count -gt 0 ]; then echo "\"achieved\""; else echo "\"pending\""; fi),
        "ten_patterns": $(if [ $patterns_count -ge 10 ]; then echo "\"achieved\""; else echo "\"pending\""; fi),
        "hundred_patterns": $(if [ $patterns_count -ge 100 ]; then echo "\"achieved\""; else echo "\"pending\""; fi),
        "optimization_active": $(if [ "$learning_status" = "ACTIVE" ]; then echo "\"achieved\""; else echo "\"pending\""; fi)
    }
}
EOF
    
    echo -e "${GREEN}📈 Learning progress updated: $patterns_count patterns, $sessions_count sessions${NC}"
}

# Function to generate progress report
generate_progress_report() {
    local report_file="$PROGRESS_DIR/reports/progress_report_$(date +%Y%m%d_%H%M%S).md"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    cat > "$report_file" << EOF
# 🧠 Autonomous Brain Progress Report

**Generated:** $timestamp

## 📊 Executive Summary

### Overall System Status
- **Brain Session:** $(if tmux has-session -t BRAIN-MAIN 2>/dev/null; then echo "🟢 ACTIVE"; else echo "🔴 INACTIVE"; fi)
- **Learning Engine:** $(if [ -f "$LEARNING_ENGINE/status" ]; then cat "$LEARNING_ENGINE/status"; else echo "INACTIVE"; fi)
- **Autonomous Tasks:** $(find "$STORAGE_DIR" -name "autonomous_*" -type f 2>/dev/null | wc -l) active

## 📋 Active Projects

### PRD Projects
EOF
    
    # Add PRD projects
    if [ -d "$STORAGE_DIR/prd-projects" ]; then
        for project in "$STORAGE_DIR/prd-projects"/*; do
            if [ -d "$project" ]; then
                local project_name=$(basename "$project")
                local files_count=$(find "$project" -type f | wc -l)
                echo "- **$project_name:** $files_count files created" >> "$report_file"
            fi
        done
    fi
    
    cat >> "$report_file" << EOF

### Research Projects
EOF
    
    # Add research projects
    if [ -d "$STORAGE_DIR/research-projects" ]; then
        for project in "$STORAGE_DIR/research-projects"/*; do
            if [ -d "$project" ]; then
                local project_name=$(basename "$project")
                local files_count=$(find "$project" -type f | wc -l)
                echo "- **$project_name:** $files_count files created" >> "$report_file"
            fi
        done
    fi
    
    cat >> "$report_file" << EOF

### Problem Solutions
EOF
    
    # Add problem solutions
    if [ -d "$STORAGE_DIR/problem-solutions" ]; then
        for project in "$STORAGE_DIR/problem-solutions"/*; do
            if [ -d "$project" ]; then
                local project_name=$(basename "$project")
                local files_count=$(find "$project" -type f | wc -l)
                echo "- **$project_name:** $files_count files created" >> "$report_file"
            fi
        done
    fi
    
    # Add learning metrics
    local patterns_count=0
    if [ -d "$LEARNING_ENGINE/patterns" ]; then
        patterns_count=$(find "$LEARNING_ENGINE/patterns" -name "*.json" 2>/dev/null | wc -l)
    fi
    
    cat >> "$report_file" << EOF

## 📈 Learning Intelligence

- **Patterns Discovered:** $patterns_count
- **Learning Status:** $(if [ -f "$LEARNING_ENGINE/status" ]; then cat "$LEARNING_ENGINE/status"; else echo "INACTIVE"; fi)
- **Knowledge Base Size:** $(du -sh "$LEARNING_ENGINE" 2>/dev/null | cut -f1 || echo "0B")

## 🤖 Agent Deployment

EOF
    
    # Add agent status
    if tmux has-session -t BRAIN-MAIN 2>/dev/null; then
        for agent in architect implementer reviewer tester documenter security optimizer orchestrator; do
            if tmux list-windows -t BRAIN-MAIN | grep -q "$agent"; then
                echo "- **$agent:** 🟢 DEPLOYED" >> "$report_file"
            else
                echo "- **$agent:** 🔴 NOT DEPLOYED" >> "$report_file"
            fi
        done
    fi
    
    cat >> "$report_file" << EOF

## 📊 Performance Metrics

- **Storage Usage:** $(du -sh "$STORAGE_DIR" 2>/dev/null | cut -f1 || echo "0B")
- **Progress Tracking Files:** $(find "$PROGRESS_DIR" -name "*.json" | wc -l)
- **Report Generation:** AUTOMATED ✅

---
*Generated by Autonomous Brain Progress Tracking System*
EOF
    
    echo -e "${GREEN}📋 Progress report generated: $report_file${NC}"
    echo -e "${CYAN}View with: cat $report_file${NC}"
}

# Function to show current progress summary
show_progress_summary() {
    echo -e "${BLUE}📈 PROGRESS SUMMARY${NC}"
    echo -e "${CYAN}==================${NC}"
    
    # Active projects
    local prd_count=0
    local research_count=0
    local problem_count=0
    
    if [ -d "$STORAGE_DIR/prd-projects" ]; then
        prd_count=$(find "$STORAGE_DIR/prd-projects" -maxdepth 1 -type d | wc -l)
        if [ $prd_count -gt 0 ]; then
            prd_count=$((prd_count - 1))  # Subtract the parent directory
        fi
    fi
    
    if [ -d "$STORAGE_DIR/research-projects" ]; then
        research_count=$(find "$STORAGE_DIR/research-projects" -maxdepth 1 -type d | wc -l)
        if [ $research_count -gt 0 ]; then
            research_count=$((research_count - 1))
        fi
    fi
    
    if [ -d "$STORAGE_DIR/problem-solutions" ]; then
        problem_count=$(find "$STORAGE_DIR/problem-solutions" -maxdepth 1 -type d | wc -l)
        if [ $problem_count -gt 0 ]; then
            problem_count=$((problem_count - 1))
        fi
    fi
    
    echo -e "${GREEN}📋 Active Projects:${NC}"
    echo -e "${YELLOW}  PRD Projects: $prd_count${NC}"
    echo -e "${YELLOW}  Research Projects: $research_count${NC}"
    echo -e "${YELLOW}  Problem Solutions: $problem_count${NC}"
    
    # Learning progress
    local patterns_count=0
    if [ -d "$LEARNING_ENGINE/patterns" ]; then
        patterns_count=$(find "$LEARNING_ENGINE/patterns" -name "*.json" 2>/dev/null | wc -l)
    fi
    
    echo -e "${GREEN}📈 Learning Progress:${NC}"
    echo -e "${YELLOW}  Patterns Discovered: $patterns_count${NC}"
    echo -e "${YELLOW}  Learning Status: $(if [ -f "$LEARNING_ENGINE/status" ]; then cat "$LEARNING_ENGINE/status"; else echo "INACTIVE"; fi)${NC}"
    
    # System status
    echo -e "${GREEN}🧠 System Status:${NC}"
    echo -e "${YELLOW}  Brain Session: $(if tmux has-session -t BRAIN-MAIN 2>/dev/null; then echo "ACTIVE"; else echo "INACTIVE"; fi)${NC}"
    echo -e "${YELLOW}  Storage Usage: $(du -sh "$STORAGE_DIR" 2>/dev/null | cut -f1 || echo "0B")${NC}"
    
    # Recent activity
    echo -e "${GREEN}📊 Recent Activity:${NC}"
    local recent_files=$(find "$STORAGE_DIR" -type f -mtime -1 2>/dev/null | wc -l)
    echo -e "${YELLOW}  Files Created Today: $recent_files${NC}"
}

# Function to auto-detect project progress
auto_detect_progress() {
    echo -e "${CYAN}🔍 Auto-detecting project progress...${NC}"
    
    # Auto-detect PRD projects
    if [ -d "$STORAGE_DIR/prd-projects" ]; then
        for project_dir in "$STORAGE_DIR/prd-projects"/*; do
            if [ -d "$project_dir" ]; then
                local project_name=$(basename "$project_dir")
                local files_count=$(find "$project_dir" -type f | wc -l)
                local completion=0
                
                # Estimate completion based on files created
                if [ $files_count -ge 5 ]; then
                    completion=100
                elif [ $files_count -ge 3 ]; then
                    completion=80
                elif [ $files_count -ge 1 ]; then
                    completion=40
                fi
                
                track_project_progress "$project_name" "prd" "auto-detected" "$completion"
            fi
        done
    fi
    
    # Auto-detect research projects
    if [ -d "$STORAGE_DIR/research-projects" ]; then
        for project_dir in "$STORAGE_DIR/research-projects"/*; do
            if [ -d "$project_dir" ]; then
                local project_name=$(basename "$project_dir")
                local files_count=$(find "$project_dir" -type f | wc -l)
                local completion=$((files_count * 20))  # Rough estimation
                if [ $completion -gt 100 ]; then
                    completion=100
                fi
                
                track_project_progress "$project_name" "research" "auto-detected" "$completion"
            fi
        done
    fi
    
    # Track learning progress
    track_learning_progress
    
    echo -e "${GREEN}✅ Auto-detection complete${NC}"
}

# Main command processing
case "${1:-summary}" in
    "track-task")
        track_task_progress "$2" "$3" "$4" "${5:-0}" "$6"
        ;;
    "track-project")
        track_project_progress "$2" "$3" "$4" "${5:-0}"
        ;;
    "track-learning")
        track_learning_progress
        ;;
    "report")
        generate_progress_report
        ;;
    "summary")
        show_progress_summary
        ;;
    "auto-detect")
        auto_detect_progress
        ;;
    "monitor")
        echo -e "${CYAN}🔄 Starting continuous progress monitoring...${NC}"
        while true; do
            auto_detect_progress
            sleep 300  # Auto-detect every 5 minutes
        done
        ;;
    *)
        echo -e "${BLUE}📈 Progress Tracking Commands:${NC}"
        echo -e "${CYAN}  progress-tracker summary          - Show progress summary${NC}"
        echo -e "${CYAN}  progress-tracker report           - Generate full report${NC}"
        echo -e "${CYAN}  progress-tracker auto-detect      - Auto-detect progress${NC}"
        echo -e "${CYAN}  progress-tracker monitor          - Continuous monitoring${NC}"
        echo -e "${CYAN}  progress-tracker track-task <id> <type> <status> [%] [notes]${NC}"
        echo -e "${CYAN}  progress-tracker track-project <name> <type> <phase> [%]${NC}"
        echo -e "${CYAN}  progress-tracker track-learning   - Update learning metrics${NC}"
        ;;
esac