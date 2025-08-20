#!/bin/bash

# Push local Claude config changes to GitHub
# Usage: ./sync-push.sh

echo "🔄 Syncing Claude config to GitHub..."

# Navigate to repo directory
cd /Users/shaansisodia/DEV/claude-brain-config

# Copy latest changes from global .claude folder
echo "📋 Copying latest changes from ~/.claude..."
rsync -av --delete /Users/shaansisodia/.claude/ . --exclude='.git' --exclude='sync-*.sh' --exclude='README.md'

# Check for changes
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ No changes to sync"
    exit 0
fi

# Show changes
echo "📝 Changes detected:"
git status --short

# Add all changes
git add .

# Commit with timestamp
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
git commit -m "Sync: $TIMESTAMP"

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git push origin main

echo "✅ Sync complete!"
echo "🔗 View at: https://github.com/Lordsisodia/claude-global-config"