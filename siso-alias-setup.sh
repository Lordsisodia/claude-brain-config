#!/bin/bash

# SISO Claude Code Alias Setup
# This script adds a 'siso-claude' alias to your shell profile

# Detect shell
SHELL_TYPE=$(basename "$SHELL")
PROFILE_FILE=""

case "$SHELL_TYPE" in
    "bash")
        if [[ -f ~/.bash_profile ]]; then
            PROFILE_FILE=~/.bash_profile
        else
            PROFILE_FILE=~/.bashrc
        fi
        ;;
    "zsh")
        PROFILE_FILE=~/.zshrc
        ;;
    "fish")
        PROFILE_FILE=~/.config/fish/config.fish
        ;;
    *)
        echo "Unknown shell: $SHELL_TYPE"
        echo "Please manually add this alias to your shell profile:"
        echo "alias siso-claude='~/.claude/scripts/siso-claude-launcher.sh'"
        exit 1
        ;;
esac

echo "🚀 Setting up SISO Claude Code launcher..."
echo "Shell detected: $SHELL_TYPE"
echo "Profile file: $PROFILE_FILE"

# Add alias to profile if it doesn't exist
if ! grep -q "alias siso=" "$PROFILE_FILE" 2>/dev/null; then
    echo "" >> "$PROFILE_FILE"
    echo "# SISO Claude Code Launcher" >> "$PROFILE_FILE"
    echo "alias siso='~/.claude/scripts/siso-claude-launcher.sh'" >> "$PROFILE_FILE"
    echo "" >> "$PROFILE_FILE"
    
    echo "✅ SISO Claude Code alias added to $PROFILE_FILE"
    echo ""
    echo "Available commands:"
    echo "  siso    - Launch Claude Code with SISO welcome screen + original Claude welcome"
    echo "  claude  - Original Claude Code with default welcome (unchanged)"
    echo ""
    echo "To use immediately, run:"
    echo "  source $PROFILE_FILE"
    echo ""
    echo "Or restart your terminal."
else
    echo "⚠️  SISO Claude Code alias already exists in $PROFILE_FILE"
fi