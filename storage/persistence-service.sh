#!/bin/bash
# Autonomous Data Persistence Service
# Continuous data protection and intelligent storage management

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
SERVICE_NAME="brain-persistence"
SERVICE_DIR="/Users/shaansisodia/DEV/claude-brain-config/storage/service"
PID_FILE="$SERVICE_DIR/${SERVICE_NAME}.pid"
LOG_FILE="$SERVICE_DIR/${SERVICE_NAME}.log"
CONFIG_FILE="$SERVICE_DIR/${SERVICE_NAME}.conf"

# Create service directories
mkdir -p "$SERVICE_DIR"

echo -e "${BLUE}🔄 AUTONOMOUS DATA PERSISTENCE SERVICE${NC}"
echo -e "${CYAN}=====================================${NC}"

# Function to create service configuration
create_service_config() {
    cat > "$CONFIG_FILE" << 'EOF'
# Brain Persistence Service Configuration

# Backup intervals (in minutes)
DAILY_BACKUP_INTERVAL=1440     # 24 hours
QUICK_BACKUP_INTERVAL=60       # 1 hour
CATALOG_UPDATE_INTERVAL=30     # 30 minutes
HEALTH_CHECK_INTERVAL=5        # 5 minutes

# Retention settings
DAILY_BACKUP_RETENTION=7       # 7 days
WEEKLY_BACKUP_RETENTION=30     # 30 days
MONTHLY_BACKUP_RETENTION=365   # 1 year

# Auto-archive settings
AUTO_ARCHIVE_ENABLED=true
ARCHIVE_AFTER_DAYS=7
PROJECT_COMPLETION_THRESHOLD=0.9

# Storage monitoring
STORAGE_WARNING_THRESHOLD=80   # Percentage
STORAGE_CRITICAL_THRESHOLD=95  # Percentage

# Learning engine protection
LEARNING_BACKUP_ENABLED=true
PATTERN_BACKUP_THRESHOLD=10    # Backup after N new patterns

# Service settings
LOG_ROTATION_SIZE=10M
LOG_RETENTION_DAYS=30
EOF
    
    echo -e "${GREEN}✅ Service configuration created: $CONFIG_FILE${NC}"
}

# Function to load service configuration
load_service_config() {
    if [ -f "$CONFIG_FILE" ]; then
        source "$CONFIG_FILE"
    else
        echo -e "${YELLOW}⚠️ No configuration found, creating default...${NC}"
        create_service_config
        source "$CONFIG_FILE"
    fi
}

# Function to log service messages
log_message() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
    
    # Also output to console if running interactively
    if [ -t 1 ]; then
        case "$level" in
            "INFO") echo -e "${CYAN}[$timestamp] [INFO] $message${NC}" ;;
            "WARN") echo -e "${YELLOW}[$timestamp] [WARN] $message${NC}" ;;
            "ERROR") echo -e "${RED}[$timestamp] [ERROR] $message${NC}" ;;
            "SUCCESS") echo -e "${GREEN}[$timestamp] [SUCCESS] $message${NC}" ;;
            *) echo "[$timestamp] [$level] $message" ;;
        esac
    fi
}

# Function to check storage health
check_storage_health() {
    local storage_root="/Users/shaansisodia/DEV/claude-brain-config/storage"
    
    # Check available disk space
    local disk_usage=$(df "$storage_root" | awk 'NR==2 {print $5}' | sed 's/%//')
    
    if [ "$disk_usage" -ge "${STORAGE_CRITICAL_THRESHOLD:-95}" ]; then
        log_message "ERROR" "CRITICAL: Disk usage at ${disk_usage}% - immediate attention required"
        return 2
    elif [ "$disk_usage" -ge "${STORAGE_WARNING_THRESHOLD:-80}" ]; then
        log_message "WARN" "WARNING: Disk usage at ${disk_usage}% - consider cleanup"
        return 1
    else
        log_message "INFO" "Storage health OK: ${disk_usage}% disk usage"
        return 0
    fi
}

# Function to perform incremental backup
perform_incremental_backup() {
    local backup_type="$1"
    
    log_message "INFO" "Starting $backup_type backup"
    
    # Run storage manager backup
    if /Users/shaansisodia/DEV/claude-brain-config/storage/storage-manager.sh backup "$backup_type" >> "$LOG_FILE" 2>&1; then
        log_message "SUCCESS" "$backup_type backup completed successfully"
        return 0
    else
        log_message "ERROR" "$backup_type backup failed"
        return 1
    fi
}

# Function to update storage catalog
update_storage_catalog() {
    log_message "INFO" "Updating storage catalog"
    
    if /Users/shaansisodia/DEV/claude-brain-config/storage/storage-manager.sh catalog >> "$LOG_FILE" 2>&1; then
        log_message "SUCCESS" "Storage catalog updated"
        return 0
    else
        log_message "ERROR" "Storage catalog update failed"
        return 1
    fi
}

# Function to check for new learning patterns
check_learning_patterns() {
    local learning_engine="$HOME/.learning-engine"
    local pattern_count_file="$SERVICE_DIR/last_pattern_count"
    
    if [ ! -d "$learning_engine/patterns" ]; then
        return 0
    fi
    
    local current_count=$(find "$learning_engine/patterns" -name "*.json" 2>/dev/null | wc -l)
    local last_count=0
    
    if [ -f "$pattern_count_file" ]; then
        last_count=$(cat "$pattern_count_file")
    fi
    
    echo "$current_count" > "$pattern_count_file"
    
    local new_patterns=$((current_count - last_count))
    
    if [ "$new_patterns" -ge "${PATTERN_BACKUP_THRESHOLD:-10}" ]; then
        log_message "INFO" "$new_patterns new learning patterns detected, triggering backup"
        perform_incremental_backup "daily"
    elif [ "$new_patterns" -gt 0 ]; then
        log_message "INFO" "$new_patterns new learning patterns detected"
    fi
}

# Function to perform auto-archival
perform_auto_archival() {
    if [ "${AUTO_ARCHIVE_ENABLED:-true}" = "true" ]; then
        log_message "INFO" "Performing auto-archival check"
        
        if /Users/shaansisodia/DEV/claude-brain-config/storage/storage-manager.sh archive >> "$LOG_FILE" 2>&1; then
            log_message "SUCCESS" "Auto-archival completed"
        else
            log_message "ERROR" "Auto-archival failed"
        fi
    fi
}

# Function to rotate logs
rotate_logs() {
    if [ -f "$LOG_FILE" ]; then
        local log_size=$(stat -f%z "$LOG_FILE" 2>/dev/null || echo "0")
        local max_size=$((10 * 1024 * 1024))  # 10MB in bytes
        
        if [ "$log_size" -gt "$max_size" ]; then
            log_message "INFO" "Rotating log file (size: $(numfmt --to=iec $log_size))"
            
            # Keep last 5 rotated logs
            for i in 4 3 2 1; do
                if [ -f "$LOG_FILE.$i" ]; then
                    mv "$LOG_FILE.$i" "$LOG_FILE.$((i + 1))"
                fi
            done
            
            mv "$LOG_FILE" "$LOG_FILE.1"
            touch "$LOG_FILE"
            
            # Remove old logs
            find "$(dirname "$LOG_FILE")" -name "$(basename "$LOG_FILE").6*" -delete 2>/dev/null || true
        fi
    fi
}

# Function to run persistence service
run_persistence_service() {
    load_service_config
    
    log_message "INFO" "Brain Persistence Service starting (PID: $$)"
    
    # Initialize counters
    local daily_backup_counter=0
    local quick_backup_counter=0
    local catalog_counter=0
    local health_counter=0
    
    # Main service loop
    while true; do
        # Health check
        health_counter=$((health_counter + 1))
        if [ $((health_counter * 60)) -ge "${HEALTH_CHECK_INTERVAL:-5}" ]; then
            check_storage_health
            health_counter=0
        fi
        
        # Catalog update
        catalog_counter=$((catalog_counter + 1))
        if [ $((catalog_counter * 60)) -ge "${CATALOG_UPDATE_INTERVAL:-30}" ]; then
            update_storage_catalog
            catalog_counter=0
        fi
        
        # Quick backup
        quick_backup_counter=$((quick_backup_counter + 1))
        if [ $((quick_backup_counter * 60)) -ge "${QUICK_BACKUP_INTERVAL:-60}" ]; then
            perform_incremental_backup "daily"
            check_learning_patterns
            quick_backup_counter=0
        fi
        
        # Daily backup
        daily_backup_counter=$((daily_backup_counter + 1))
        if [ $((daily_backup_counter * 60)) -ge "${DAILY_BACKUP_INTERVAL:-1440}" ]; then
            perform_incremental_backup "weekly"
            perform_auto_archival
            daily_backup_counter=0
        fi
        
        # Log rotation
        rotate_logs
        
        # Sleep for 1 minute
        sleep 60
    done
}

# Function to start service
start_service() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            echo -e "${YELLOW}⚠️ Service already running (PID: $pid)${NC}"
            return 1
        else
            echo -e "${YELLOW}⚠️ Removing stale PID file${NC}"
            rm -f "$PID_FILE"
        fi
    fi
    
    echo -e "${GREEN}🚀 Starting Brain Persistence Service...${NC}"
    
    # Start service in background
    (run_persistence_service) &
    local service_pid=$!
    
    # Save PID
    echo "$service_pid" > "$PID_FILE"
    
    # Wait a moment to ensure it started properly
    sleep 2
    
    if ps -p "$service_pid" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Service started successfully (PID: $service_pid)${NC}"
        echo -e "${CYAN}Log file: $LOG_FILE${NC}"
        return 0
    else
        echo -e "${RED}❌ Failed to start service${NC}"
        rm -f "$PID_FILE"
        return 1
    fi
}

# Function to stop service
stop_service() {
    if [ ! -f "$PID_FILE" ]; then
        echo -e "${YELLOW}⚠️ Service not running (no PID file)${NC}"
        return 1
    fi
    
    local pid=$(cat "$PID_FILE")
    
    if ! ps -p "$pid" > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️ Service not running (stale PID file)${NC}"
        rm -f "$PID_FILE"
        return 1
    fi
    
    echo -e "${YELLOW}🛑 Stopping Brain Persistence Service (PID: $pid)...${NC}"
    
    # Send TERM signal
    kill "$pid" 2>/dev/null || {
        echo -e "${RED}❌ Failed to stop service${NC}"
        return 1
    }
    
    # Wait for graceful shutdown
    local wait_count=0
    while ps -p "$pid" > /dev/null 2>&1 && [ $wait_count -lt 10 ]; do
        sleep 1
        wait_count=$((wait_count + 1))
    done
    
    # Force kill if still running
    if ps -p "$pid" > /dev/null 2>&1; then
        echo -e "${RED}⚠️ Force killing service...${NC}"
        kill -9 "$pid" 2>/dev/null || true
    fi
    
    rm -f "$PID_FILE"
    echo -e "${GREEN}✅ Service stopped${NC}"
}

# Function to show service status
show_service_status() {
    echo -e "${BLUE}🔄 Brain Persistence Service Status${NC}"
    echo -e "${CYAN}===================================${NC}"
    
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            local uptime=$(ps -p "$pid" -o etime= | tr -d ' ')
            echo -e "${GREEN}Status: RUNNING${NC}"
            echo -e "${CYAN}PID: $pid${NC}"
            echo -e "${CYAN}Uptime: $uptime${NC}"
        else
            echo -e "${RED}Status: STOPPED (stale PID file)${NC}"
            rm -f "$PID_FILE"
        fi
    else
        echo -e "${YELLOW}Status: STOPPED${NC}"
    fi
    
    # Show configuration
    if [ -f "$CONFIG_FILE" ]; then
        echo -e "${BLUE}Configuration:${NC}"
        echo -e "${CYAN}  Config file: $CONFIG_FILE${NC}"
        echo -e "${CYAN}  Log file: $LOG_FILE${NC}"
        
        load_service_config
        echo -e "${CYAN}  Quick backup interval: ${QUICK_BACKUP_INTERVAL} minutes${NC}"
        echo -e "${CYAN}  Daily backup interval: ${DAILY_BACKUP_INTERVAL} minutes${NC}"
        echo -e "${CYAN}  Auto-archive: ${AUTO_ARCHIVE_ENABLED}${NC}"
    fi
    
    # Show recent log entries
    if [ -f "$LOG_FILE" ]; then
        echo -e "${BLUE}Recent Log Entries:${NC}"
        tail -5 "$LOG_FILE" | while read line; do
            echo -e "${CYAN}  $line${NC}"
        done
    fi
}

# Function to show service logs
show_service_logs() {
    local lines="${1:-50}"
    
    if [ ! -f "$LOG_FILE" ]; then
        echo -e "${YELLOW}⚠️ No log file found${NC}"
        return 1
    fi
    
    echo -e "${BLUE}📋 Service Logs (last $lines lines)${NC}"
    echo -e "${CYAN}====================================${NC}"
    
    tail -"$lines" "$LOG_FILE"
}

# Main command processing
case "${1:-status}" in
    "start")
        start_service
        ;;
    "stop")
        stop_service
        ;;
    "restart")
        stop_service
        sleep 2
        start_service
        ;;
    "status")
        show_service_status
        ;;
    "logs")
        show_service_logs "${2:-50}"
        ;;
    "config")
        if [ ! -f "$CONFIG_FILE" ]; then
            create_service_config
        fi
        echo -e "${CYAN}Configuration file: $CONFIG_FILE${NC}"
        cat "$CONFIG_FILE"
        ;;
    "install")
        echo -e "${GREEN}📦 Installing Brain Persistence Service...${NC}"
        create_service_config
        echo -e "${GREEN}✅ Service installed${NC}"
        echo -e "${CYAN}Configuration: $CONFIG_FILE${NC}"
        echo -e "${YELLOW}Start with: persistence-service start${NC}"
        ;;
    *)
        echo -e "${BLUE}🔄 Brain Persistence Service Commands:${NC}"
        echo -e "${CYAN}  persistence-service start              - Start the service${NC}"
        echo -e "${CYAN}  persistence-service stop               - Stop the service${NC}"
        echo -e "${CYAN}  persistence-service restart            - Restart the service${NC}"
        echo -e "${CYAN}  persistence-service status             - Show service status${NC}"
        echo -e "${CYAN}  persistence-service logs [lines]       - Show service logs${NC}"
        echo -e "${CYAN}  persistence-service config             - Show configuration${NC}"
        echo -e "${CYAN}  persistence-service install            - Install service${NC}"
        echo ""
        echo -e "${GREEN}Service Features:${NC}"
        echo -e "${MAGENTA}  • Automatic backups (hourly/daily/weekly)${NC}"
        echo -e "${MAGENTA}  • Storage health monitoring${NC}"
        echo -e "${MAGENTA}  • Learning pattern protection${NC}"
        echo -e "${MAGENTA}  • Auto-archival of completed projects${NC}"
        echo -e "${MAGENTA}  • Intelligent storage catalogs${NC}"
        ;;
esac