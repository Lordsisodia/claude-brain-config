#!/bin/bash

# Cleanup script for old Claude data
# Run this after verifying backups

CLAUDE_BRAIN="/Users/shaansisodia/DEV/claude-brain-config"
BACKUP_DIR="$CLAUDE_BRAIN/archived_data"

echo "=== Claude Data Cleanup Script ==="
echo "This will archive and clean up old data"
echo

# Create backup directory
mkdir -p "$BACKUP_DIR"

# 1. Archive the 902 todo files (they're not actively used)
if [ -d "$CLAUDE_BRAIN/todos" ]; then
    echo "📦 Archiving todos folder (902 files)..."
    tar -czf "$BACKUP_DIR/todos_archive_$(date +%Y%m%d).tar.gz" -C "$CLAUDE_BRAIN" todos/
    
    echo -n "Delete original todo files? (y/n): "
    read -r response
    if [[ "$response" == "y" ]]; then
        rm -rf "$CLAUDE_BRAIN/todos"/*.json
        echo "✅ Deleted todo JSON files"
    fi
fi

# 2. Clean up statsig cache (these auto-regenerate)
if [ -d "$CLAUDE_BRAIN/statsig" ]; then
    echo "🗑️  Cleaning statsig cache files..."
    find "$CLAUDE_BRAIN/statsig" -name "*.cached.*" -mtime +7 -delete
    echo "✅ Removed old statsig cache files"
fi

# 3. Archive old analytics (keep only recent)
if [ -d "$CLAUDE_BRAIN/analytics" ]; then
    echo "📊 Checking analytics folder..."
    # These are just copies of ~/.claude/analytics, can be removed
    echo "Note: Analytics in claude-brain-config are duplicates of ~/.claude/analytics"
fi

# 4. Clean up empty directories
echo "🧹 Removing empty directories..."
find "$CLAUDE_BRAIN" -type d -empty -delete

# 5. Show disk usage
echo
echo "=== Disk Usage Summary ==="
du -sh "$CLAUDE_BRAIN"/* | sort -hr | head -10

echo
echo "=== Cleanup Complete ==="
echo "Backups saved to: $BACKUP_DIR"
echo
echo "💡 Recommendations:"
echo "  1. The todos/ folder contained 902 archived agent files - now backed up"
echo "  2. Real analytics are in ~/.claude/analytics/ (not in claude-brain-config)"
echo "  3. Consider using the conversation database for ~/.claude/projects/"
echo "  4. Set up a monthly cron job to archive old data automatically"