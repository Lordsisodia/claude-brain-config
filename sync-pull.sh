#!/bin/bash

# Pull Claude config changes from GitHub and apply locally
# Usage: ./sync-pull.sh

echo "🔄 Pulling Claude config from GitHub..."

# Navigate to repo directory
cd /Users/shaansisodia/DEV/claude-brain-config

# Backup current local config
BACKUP_DIR="/Users/shaansisodia/.claude-backup-$(date +%Y%m%d-%H%M%S)"
echo "💾 Backing up current config to $BACKUP_DIR..."
cp -r /Users/shaansisodia/.claude "$BACKUP_DIR"

# Pull latest changes
echo "⬇️  Pulling from GitHub..."
git pull origin main

# Show what will be updated
echo "📝 Changes to apply:"
diff -rq /Users/shaansisodia/.claude . --exclude='.git' --exclude='sync-*.sh' --exclude='README.md' | head -20

# Ask for confirmation
read -p "Apply these changes to ~/.claude? (y/N): " confirm
if [[ $confirm != [yY] ]]; then
    echo "❌ Cancelled. Your backup is at: $BACKUP_DIR"
    exit 1
fi

# Apply changes to local .claude folder
echo "📋 Applying changes to ~/.claude..."
rsync -av --delete . /Users/shaansisodia/.claude/ --exclude='.git' --exclude='sync-*.sh' --exclude='README.md'

echo "✅ Sync complete!"
echo "💾 Backup saved at: $BACKUP_DIR"