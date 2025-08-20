#!/bin/bash
# Storage and Persistence Management System
# Handles intelligent storage, backup, archival, and data persistence

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
STORAGE_ROOT="/Users/shaansisodia/DEV/claude-brain-config/storage"
BACKUP_DIR="/Users/shaansisodia/DEV/claude-brain-config/storage/backups"
ARCHIVE_DIR="/Users/shaansisodia/DEV/claude-brain-config/storage/archives"
METADATA_DIR="/Users/shaansisodia/DEV/claude-brain-config/storage/metadata"
LEARNING_ENGINE="$HOME/.learning-engine"

# Create storage directories
mkdir -p "$STORAGE_ROOT"/{prd-projects,research-projects,problem-solutions,development-projects,data-exports}
mkdir -p "$BACKUP_DIR"/{daily,weekly,monthly}
mkdir -p "$ARCHIVE_DIR"/{completed,obsolete,reference}
mkdir -p "$METADATA_DIR"/{indexes,catalogs,statistics}

echo -e "${BLUE}💾 STORAGE AND PERSISTENCE MANAGEMENT SYSTEM${NC}"
echo -e "${CYAN}=============================================${NC}"

# Function to analyze storage usage
analyze_storage_usage() {
    echo -e "${GREEN}📊 Storage Usage Analysis${NC}"
    echo -e "${CYAN}=========================${NC}"
    
    # Overall storage usage
    local total_size=$(du -sh "$STORAGE_ROOT" 2>/dev/null | cut -f1 || echo "0B")
    echo -e "${YELLOW}Total Storage: $total_size${NC}"
    
    # Breakdown by category
    echo -e "${BLUE}Storage Breakdown:${NC}"
    for category in prd-projects research-projects problem-solutions development-projects data-exports; do
        if [ -d "$STORAGE_ROOT/$category" ]; then
            local category_size=$(du -sh "$STORAGE_ROOT/$category" 2>/dev/null | cut -f1 || echo "0B")
            local file_count=$(find "$STORAGE_ROOT/$category" -type f 2>/dev/null | wc -l)
            echo -e "${CYAN}  $category: $category_size ($file_count files)${NC}"
        fi
    done
    
    # Backup storage
    if [ -d "$BACKUP_DIR" ]; then
        local backup_size=$(du -sh "$BACKUP_DIR" 2>/dev/null | cut -f1 || echo "0B")
        local backup_count=$(find "$BACKUP_DIR" -name "*.tar.gz" 2>/dev/null | wc -l)
        echo -e "${MAGENTA}  Backups: $backup_size ($backup_count archives)${NC}"
    fi
    
    # Archive storage
    if [ -d "$ARCHIVE_DIR" ]; then
        local archive_size=$(du -sh "$ARCHIVE_DIR" 2>/dev/null | cut -f1 || echo "0B")
        local archive_count=$(find "$ARCHIVE_DIR" -type f 2>/dev/null | wc -l)
        echo -e "${YELLOW}  Archives: $archive_size ($archive_count files)${NC}"
    fi
    
    # Learning engine storage
    if [ -d "$LEARNING_ENGINE" ]; then
        local learning_size=$(du -sh "$LEARNING_ENGINE" 2>/dev/null | cut -f1 || echo "0B")
        echo -e "${GREEN}  Learning Engine: $learning_size${NC}"
    fi
}

# Function to create intelligent backup
create_intelligent_backup() {
    local backup_type="${1:-daily}"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="$BACKUP_DIR/$backup_type/brain_backup_${backup_type}_${timestamp}.tar.gz"
    
    echo -e "${GREEN}📦 Creating $backup_type backup...${NC}"
    
    # Create backup directory
    mkdir -p "$BACKUP_DIR/$backup_type"
    
    # Determine what to backup based on type
    local backup_sources=()
    case "$backup_type" in
        "daily")
            # Daily: Recent projects and active data
            backup_sources+=("$STORAGE_ROOT/prd-projects")
            backup_sources+=("$STORAGE_ROOT/research-projects")
            backup_sources+=("$STORAGE_ROOT/problem-solutions")
            backup_sources+=("$METADATA_DIR")
            ;;
        "weekly")
            # Weekly: Everything except archives
            backup_sources+=("$STORAGE_ROOT")
            backup_sources+=("$LEARNING_ENGINE")
            ;;
        "monthly")
            # Monthly: Complete system backup
            backup_sources+=("$STORAGE_ROOT")
            backup_sources+=("$LEARNING_ENGINE")
            backup_sources+=("/Users/shaansisodia/DEV/claude-brain-config")
            ;;
    esac
    
    # Create backup with compression
    echo -e "${CYAN}Creating compressed archive...${NC}"
    tar -czf "$backup_file" "${backup_sources[@]}" 2>/dev/null || {
        echo -e "${RED}❌ Backup creation failed${NC}"
        return 1
    }
    
    # Create backup metadata
    local backup_metadata="$BACKUP_DIR/$backup_type/backup_${timestamp}.json"
    cat > "$backup_metadata" << EOF
{
    "backup_type": "$backup_type",
    "created": "$(date '+%Y-%m-%d %H:%M:%S')",
    "timestamp": "$timestamp",
    "backup_file": "$backup_file",
    "file_size": "$(du -h "$backup_file" | cut -f1)",
    "sources": [$(printf '"%s",' "${backup_sources[@]}" | sed 's/,$//')],
    "compression": "gzip",
    "checksum": "$(shasum -a 256 "$backup_file" | cut -d' ' -f1)",
    "retention_days": $(case "$backup_type" in "daily") echo "7";; "weekly") echo "30";; "monthly") echo "365";; esac)
}
EOF
    
    echo -e "${GREEN}✅ Backup created: $backup_file${NC}"
    echo -e "${CYAN}Size: $(du -h "$backup_file" | cut -f1)${NC}"
    echo -e "${YELLOW}Metadata: $backup_metadata${NC}"
}

# Function to manage retention and cleanup
manage_retention() {
    echo -e "${YELLOW}🧹 Managing backup retention...${NC}"
    
    # Daily backup retention (keep 7 days)
    find "$BACKUP_DIR/daily" -name "*.tar.gz" -mtime +7 -exec rm -f {} \; 2>/dev/null
    find "$BACKUP_DIR/daily" -name "*.json" -mtime +7 -exec rm -f {} \; 2>/dev/null
    
    # Weekly backup retention (keep 4 weeks)
    find "$BACKUP_DIR/weekly" -name "*.tar.gz" -mtime +28 -exec rm -f {} \; 2>/dev/null
    find "$BACKUP_DIR/weekly" -name "*.json" -mtime +28 -exec rm -f {} \; 2>/dev/null
    
    # Monthly backup retention (keep 12 months)
    find "$BACKUP_DIR/monthly" -name "*.tar.gz" -mtime +365 -exec rm -f {} \; 2>/dev/null
    find "$BACKUP_DIR/monthly" -name "*.json" -mtime +365 -exec rm -f {} \; 2>/dev/null
    
    echo -e "${GREEN}✅ Retention cleanup complete${NC}"
}

# Function to archive completed projects
archive_completed_projects() {
    echo -e "${MAGENTA}📚 Archiving completed projects...${NC}"
    
    local archived_count=0
    
    # Look for completed PRD projects
    if [ -d "$STORAGE_ROOT/prd-projects" ]; then
        for project_dir in "$STORAGE_ROOT/prd-projects"/*; do
            if [ -d "$project_dir" ]; then
                local project_name=$(basename "$project_dir")
                
                # Check if project has completion indicators
                if [ -f "$project_dir/autonomous_monitor.sh" ] && [ -f "$project_dir/documentation/01-executive-summary.md" ]; then
                    # Check if project hasn't been modified in 7 days
                    local last_modified=$(find "$project_dir" -type f -printf '%T@\n' | sort -n | tail -1)
                    local current_time=$(date +%s)
                    local days_old=$(( (current_time - ${last_modified%.*}) / 86400 ))
                    
                    if [ $days_old -ge 7 ]; then
                        echo -e "${CYAN}  Archiving PRD project: $project_name${NC}"
                        
                        # Create archive
                        local archive_file="$ARCHIVE_DIR/completed/prd_${project_name}_$(date +%Y%m%d).tar.gz"
                        tar -czf "$archive_file" -C "$(dirname "$project_dir")" "$(basename "$project_dir")"
                        
                        # Create archive metadata
                        cat > "$ARCHIVE_DIR/completed/prd_${project_name}_$(date +%Y%m%d).json" << EOF
{
    "project_name": "$project_name",
    "project_type": "prd",
    "archived_date": "$(date '+%Y-%m-%d %H:%M:%S')",
    "original_path": "$project_dir",
    "archive_file": "$archive_file",
    "archive_size": "$(du -h "$archive_file" | cut -f1)",
    "reason": "auto_archive_completed"
}
EOF
                        
                        # Remove original
                        rm -rf "$project_dir"
                        archived_count=$((archived_count + 1))
                    fi
                fi
            fi
        done
    fi
    
    echo -e "${GREEN}✅ Archived $archived_count projects${NC}"
}

# Function to create storage catalog
create_storage_catalog() {
    local catalog_file="$METADATA_DIR/catalogs/storage_catalog_$(date +%Y%m%d_%H%M%S).json"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo -e "${BLUE}📋 Creating storage catalog...${NC}"
    
    # Create catalog directory
    mkdir -p "$METADATA_DIR/catalogs"
    
    # Initialize catalog
    cat > "$catalog_file" << EOF
{
    "catalog_created": "$timestamp",
    "catalog_version": "1.0",
    "storage_root": "$STORAGE_ROOT",
    "categories": {
EOF
    
    # Catalog each category
    local first_category=true
    for category in prd-projects research-projects problem-solutions development-projects data-exports; do
        if [ ! "$first_category" = true ]; then
            echo "," >> "$catalog_file"
        fi
        first_category=false
        
        echo "        \"$category\": {" >> "$catalog_file"
        echo "            \"path\": \"$STORAGE_ROOT/$category\"," >> "$catalog_file"
        
        if [ -d "$STORAGE_ROOT/$category" ]; then
            local category_size=$(du -sb "$STORAGE_ROOT/$category" 2>/dev/null | cut -f1 || echo "0")
            local file_count=$(find "$STORAGE_ROOT/$category" -type f 2>/dev/null | wc -l)
            local project_count=$(find "$STORAGE_ROOT/$category" -maxdepth 1 -type d 2>/dev/null | wc -l)
            if [ $project_count -gt 0 ]; then
                project_count=$((project_count - 1))  # Subtract parent directory
            fi
            
            echo "            \"size_bytes\": $category_size," >> "$catalog_file"
            echo "            \"file_count\": $file_count," >> "$catalog_file"
            echo "            \"project_count\": $project_count," >> "$catalog_file"
            echo "            \"last_modified\": \"$(find "$STORAGE_ROOT/$category" -type f -printf '%TY-%Tm-%Td %TH:%TM:%TS\n' 2>/dev/null | sort | tail -1 || echo 'never')\"," >> "$catalog_file"
            
            # List projects
            echo "            \"projects\": [" >> "$catalog_file"
            local first_project=true
            for project_dir in "$STORAGE_ROOT/$category"/*; do
                if [ -d "$project_dir" ]; then
                    if [ ! "$first_project" = true ]; then
                        echo "," >> "$catalog_file"
                    fi
                    first_project=false
                    
                    local project_name=$(basename "$project_dir")
                    local project_size=$(du -sb "$project_dir" 2>/dev/null | cut -f1 || echo "0")
                    local project_files=$(find "$project_dir" -type f 2>/dev/null | wc -l)
                    
                    echo "                {" >> "$catalog_file"
                    echo "                    \"name\": \"$project_name\"," >> "$catalog_file"
                    echo "                    \"size_bytes\": $project_size," >> "$catalog_file"
                    echo "                    \"file_count\": $project_files" >> "$catalog_file"
                    echo -n "                }" >> "$catalog_file"
                fi
            done
            echo "" >> "$catalog_file"
            echo "            ]" >> "$catalog_file"
        else
            echo "            \"size_bytes\": 0," >> "$catalog_file"
            echo "            \"file_count\": 0," >> "$catalog_file"
            echo "            \"project_count\": 0," >> "$catalog_file"
            echo "            \"projects\": []" >> "$catalog_file"
        fi
        
        echo -n "        }" >> "$catalog_file"
    done
    
    # Close catalog
    cat >> "$catalog_file" << EOF

    },
    "summary": {
        "total_size_bytes": $(du -sb "$STORAGE_ROOT" 2>/dev/null | cut -f1 || echo "0"),
        "total_files": $(find "$STORAGE_ROOT" -type f 2>/dev/null | wc -l),
        "backup_count": $(find "$BACKUP_DIR" -name "*.tar.gz" 2>/dev/null | wc -l),
        "archive_count": $(find "$ARCHIVE_DIR" -type f 2>/dev/null | wc -l)
    }
}
EOF
    
    # Create latest catalog symlink
    ln -sf "$catalog_file" "$METADATA_DIR/catalogs/latest_catalog.json"
    
    echo -e "${GREEN}✅ Storage catalog created: $catalog_file${NC}"
}

# Function to export data in various formats
export_data() {
    local export_type="$1"
    local target_path="${2:-$STORAGE_ROOT/data-exports}"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    
    echo -e "${CYAN}📤 Exporting data ($export_type)...${NC}"
    
    mkdir -p "$target_path"
    
    case "$export_type" in
        "json")
            # Export as JSON
            local export_file="$target_path/brain_export_${timestamp}.json"
            
            cat > "$export_file" << EOF
{
    "export_created": "$(date '+%Y-%m-%d %H:%M:%S')",
    "export_type": "json",
    "brain_config": "/Users/shaansisodia/DEV/claude-brain-config",
    "storage_catalog": $(cat "$METADATA_DIR/catalogs/latest_catalog.json" 2>/dev/null || echo "null"),
    "learning_status": {
        "status": "$(cat "$LEARNING_ENGINE/status" 2>/dev/null || echo 'inactive')",
        "patterns_count": $(find "$LEARNING_ENGINE/patterns" -name "*.json" 2>/dev/null | wc -l),
        "sessions_count": $(find "$LEARNING_ENGINE/sessions" -name "*.log" 2>/dev/null | wc -l)
    }
}
EOF
            echo -e "${GREEN}✅ JSON export: $export_file${NC}"
            ;;
        "csv")
            # Export project summary as CSV
            local export_file="$target_path/projects_summary_${timestamp}.csv"
            
            echo "Project Name,Type,File Count,Size (bytes),Last Modified" > "$export_file"
            
            for category in prd-projects research-projects problem-solutions development-projects; do
                if [ -d "$STORAGE_ROOT/$category" ]; then
                    for project_dir in "$STORAGE_ROOT/$category"/*; do
                        if [ -d "$project_dir" ]; then
                            local project_name=$(basename "$project_dir")
                            local file_count=$(find "$project_dir" -type f 2>/dev/null | wc -l)
                            local size_bytes=$(du -sb "$project_dir" 2>/dev/null | cut -f1 || echo "0")
                            local last_modified=$(find "$project_dir" -type f -printf '%TY-%Tm-%Td %TH:%TM:%TS\n' 2>/dev/null | sort | tail -1 || echo 'never')
                            
                            echo "$project_name,$category,$file_count,$size_bytes,$last_modified" >> "$export_file"
                        fi
                    done
                fi
            done
            
            echo -e "${GREEN}✅ CSV export: $export_file${NC}"
            ;;
        "archive")
            # Export as complete archive
            local export_file="$target_path/brain_complete_${timestamp}.tar.gz"
            
            tar -czf "$export_file" \
                "$STORAGE_ROOT" \
                "$LEARNING_ENGINE" \
                "/Users/shaansisodia/DEV/claude-brain-config" \
                2>/dev/null
            
            echo -e "${GREEN}✅ Archive export: $export_file${NC}"
            echo -e "${CYAN}Size: $(du -h "$export_file" | cut -f1)${NC}"
            ;;
        *)
            echo -e "${RED}❌ Unknown export type: $export_type${NC}"
            echo -e "${YELLOW}Available types: json, csv, archive${NC}"
            return 1
            ;;
    esac
}

# Function to restore from backup
restore_from_backup() {
    local backup_file="$1"
    local restore_path="${2:-$STORAGE_ROOT}"
    
    if [ ! -f "$backup_file" ]; then
        echo -e "${RED}❌ Backup file not found: $backup_file${NC}"
        return 1
    fi
    
    echo -e "${YELLOW}⚠️ Restoring from backup: $(basename "$backup_file")${NC}"
    echo -e "${RED}This will overwrite existing data. Continue? (y/N)${NC}"
    
    # In automated mode, skip confirmation
    if [ "${AUTO_CONFIRM:-false}" = "true" ]; then
        echo "AUTO_CONFIRM enabled, proceeding..."
    else
        read -r confirmation
        if [ "$confirmation" != "y" ] && [ "$confirmation" != "Y" ]; then
            echo -e "${YELLOW}Restore cancelled${NC}"
            return 0
        fi
    fi
    
    echo -e "${CYAN}Extracting backup...${NC}"
    tar -xzf "$backup_file" -C "$(dirname "$restore_path")" 2>/dev/null || {
        echo -e "${RED}❌ Restore failed${NC}"
        return 1
    }
    
    echo -e "${GREEN}✅ Restore completed from: $backup_file${NC}"
}

# Function to show storage statistics
show_storage_statistics() {
    echo -e "${BLUE}📊 Storage Statistics${NC}"
    echo -e "${CYAN}====================${NC}"
    
    # Load latest catalog if available
    if [ -f "$METADATA_DIR/catalogs/latest_catalog.json" ]; then
        if command -v jq > /dev/null 2>&1; then
            local total_size=$(jq -r .summary.total_size_bytes "$METADATA_DIR/catalogs/latest_catalog.json")
            local total_files=$(jq -r .summary.total_files "$METADATA_DIR/catalogs/latest_catalog.json")
            local backup_count=$(jq -r .summary.backup_count "$METADATA_DIR/catalogs/latest_catalog.json")
            local archive_count=$(jq -r .summary.archive_count "$METADATA_DIR/catalogs/latest_catalog.json")
            
            echo -e "${GREEN}Storage Overview:${NC}"
            echo -e "${YELLOW}  Total Size: $(numfmt --to=iec $total_size 2>/dev/null || echo "${total_size} bytes")${NC}"
            echo -e "${YELLOW}  Total Files: $total_files${NC}"
            echo -e "${YELLOW}  Backups: $backup_count${NC}"
            echo -e "${YELLOW}  Archives: $archive_count${NC}"
            
            echo -e "${GREEN}Categories:${NC}"
            for category in prd-projects research-projects problem-solutions development-projects; do
                local cat_size=$(jq -r ".categories.\"$category\".size_bytes" "$METADATA_DIR/catalogs/latest_catalog.json")
                local cat_projects=$(jq -r ".categories.\"$category\".project_count" "$METADATA_DIR/catalogs/latest_catalog.json")
                echo -e "${CYAN}  $category: $(numfmt --to=iec $cat_size 2>/dev/null || echo "${cat_size} bytes") ($cat_projects projects)${NC}"
            done
        else
            echo -e "${YELLOW}Catalog found but jq not available for detailed analysis${NC}"
        fi
    else
        echo -e "${YELLOW}No catalog found. Run 'storage-manager catalog' to generate statistics.${NC}"
    fi
}

# Main command processing
case "${1:-status}" in
    "analyze"|"usage")
        analyze_storage_usage
        ;;
    "backup")
        create_intelligent_backup "${2:-daily}"
        ;;
    "archive")
        archive_completed_projects
        ;;
    "catalog")
        create_storage_catalog
        ;;
    "export")
        export_data "${2:-json}" "$3"
        ;;
    "restore")
        restore_from_backup "$2" "$3"
        ;;
    "cleanup")
        manage_retention
        archive_completed_projects
        ;;
    "status"|"stats")
        show_storage_statistics
        ;;
    "full-maintenance")
        echo -e "${GREEN}🔧 Running full storage maintenance...${NC}"
        create_storage_catalog
        create_intelligent_backup "daily"
        manage_retention
        archive_completed_projects
        analyze_storage_usage
        ;;
    *)
        echo -e "${BLUE}💾 Storage Management Commands:${NC}"
        echo -e "${CYAN}  storage-manager analyze                    - Analyze storage usage${NC}"
        echo -e "${CYAN}  storage-manager backup [daily|weekly|monthly] - Create backup${NC}"
        echo -e "${CYAN}  storage-manager archive                    - Archive completed projects${NC}"
        echo -e "${CYAN}  storage-manager catalog                    - Create storage catalog${NC}"
        echo -e "${CYAN}  storage-manager export [json|csv|archive] [path] - Export data${NC}"
        echo -e "${CYAN}  storage-manager restore <backup_file> [path] - Restore from backup${NC}"
        echo -e "${CYAN}  storage-manager cleanup                    - Cleanup and retention${NC}"
        echo -e "${CYAN}  storage-manager status                     - Show storage statistics${NC}"
        echo -e "${CYAN}  storage-manager full-maintenance           - Complete maintenance cycle${NC}"
        echo ""
        echo -e "${GREEN}Examples:${NC}"
        echo -e "${MAGENTA}  storage-manager backup weekly${NC}"
        echo -e "${MAGENTA}  storage-manager export json /tmp/export${NC}"
        echo -e "${MAGENTA}  storage-manager restore /path/to/backup.tar.gz${NC}"
        ;;
esac