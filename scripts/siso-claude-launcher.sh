#!/bin/bash

# SISO Claude Code Launcher with custom welcome screen
# This script shows the SISO welcome screen before launching Claude Code

clear

# Display SISO welcome screen
cat << 'EOF'
╭─────────────────────────────────────────────────────────────╮
│                                                             │
│   ███████╗██╗███████╗ ██████╗                              │
│   ██╔════╝██║██╔════╝██╔═══██╗                             │
│   ███████╗██║███████╗██║   ██║                             │
│   ╚════██║██║╚════██║██║   ██║                             │
│   ███████║██║███████║╚██████╔╝                             │
│   ╚══════╝╚═╝╚══════╝ ╚═════╝                              │
│                                                             │
│  🚀 SuperClaude Enhanced Development Environment           │
│  ⚡ AUTONOMOUS CODING AGENT | 10X INTELLIGENCE ACTIVATED    │
│                                                             │
│     🧠 Ultra Think Mode Ready                               │
│     🎯 MUSK Algorithm Engaged                               │
│     🔧 Multi-Agent Teams Available                          │
│     💎 First Principles Thinking Active                     │
│                                                             │
│  /help for help, /status for your current setup            │
│                                                             │
EOF

# Show current project info
CURRENT_DIR=$(basename "$PWD")
PROJECT_TYPE="Development"

# Detect project type
if [[ -f "package.json" ]]; then
    if grep -q "react" package.json 2>/dev/null; then
        PROJECT_TYPE="React/TypeScript"
    elif grep -q "next" package.json 2>/dev/null; then
        PROJECT_TYPE="Next.js"
    else
        PROJECT_TYPE="Node.js"
    fi
elif [[ -f "requirements.txt" ]] || [[ -f "pyproject.toml" ]]; then
    PROJECT_TYPE="Python"
elif [[ -f "Cargo.toml" ]]; then
    PROJECT_TYPE="Rust"
elif [[ -f "go.mod" ]]; then
    PROJECT_TYPE="Go"
fi

# Special detection for SISO projects
if [[ "$CURRENT_DIR" == *"SISO"* ]] || [[ "$PWD" == *"SISO"* ]]; then
    PROJECT_TYPE="🌟 SISO $PROJECT_TYPE"
fi

# Show project info
printf "│  🎯 Project: %-44s │\n" "$CURRENT_DIR"
printf "│  🔧 Type: %-47s │\n" "$PROJECT_TYPE"
printf "│  📍 cwd: %-48s │\n" "$PWD"

cat << 'EOF'
│                                                             │
│  💡 Ready to revolutionize your development workflow!       │
│                                                             │
╰─────────────────────────────────────────────────────────────╯

🔥 SISO Enhanced Claude Code is now starting...

EOF

# Give user a moment to see the welcome screen
sleep 1

# Launch Claude Code with all arguments passed through
# The regular claude welcome will show after our SISO screen
exec claude "$@"