# ⚡ Claude Brain Quick Reference
*Essential commands and patterns for daily operations*

## 🚀 **Daily Essentials**

### System Sync
```bash
./sync-pull.sh    # Pull latest intelligence updates
./sync-push.sh    # Push your improvements
```

### Quick Status
```bash
tail logs/session-*.log              # Recent activity
ls analytics/*.json                  # Performance data
find todos/ -name "*.json" | wc -l   # Active tasks count
```

## 🔍 **Search Patterns**

### Find Files Fast
```bash
# By category
find shared/ -name "*intelligence*"     # Intelligence modules
find agents/ -name "*enhanced*"        # Enhanced agents  
find scripts/ -name "*auto*"           # Automation scripts
find scripts/ -name "*optimizer*"      # Optimization tools

# By function
find . -name "*README*" -o -name "*GUIDE*"  # Documentation
find . -name "*.yml" | head -10             # YAML configs
find . -executable -name "*.sh" | head      # Runnable scripts
```

### Search Content
```bash
# Core concepts
grep -r "@include" . | head -5          # Template includes
grep -r "AUTO-" . | head -5             # Auto-activation
grep -r "intelligence" shared/ | head   # Intelligence patterns
grep -r "MUST" shared/ | head          # Required patterns

# Functionality
grep -r "keyword" shared/ --include="*.yml"
grep -r "pattern" agents/ --include="*.md"  
grep -r "function" scripts/ --include="*.sh"
```

## 🎯 **Common Operations**

### Intelligence Management
```bash
# View core intelligence
cat shared/superclaude-core.yml | head -20
cat shared/musk-algorithm-core.yml | head -20
cat shared/task-intelligence-system.yml | head -20

# Check intelligence systems
find shared/ -name "*intelligence*.yml" | sort
grep -r "Philosophy:" shared/
grep -r "Performance:" shared/
```

### Agent Operations  
```bash
# List available agents
ls agents/*.md | sed 's/agents\///; s/\.md$//'
cat agents/multi-agent-orchestrator.md | head -20

# Agent testing
python agents/phase1-demo.py
python agents/phase1-integration-test.py
```

### Script Execution
```bash
# Core optimizers
scripts/claude-universal-enhancer.sh    # Universal enhancement
scripts/openai-prompt-optimizer.sh      # Prompt optimization
scripts/system-activator.sh             # System activation

# Automation
scripts/auto-agent-detector.sh          # Auto agent spawning
scripts/intelligent-session.sh          # Smart session mgmt

# Monitoring  
scripts/daily-improvement-report.sh     # Generate daily report
scripts/hooks-effectiveness-analyzer.sh # Hook performance
scripts/improvement-tracker.sh          # Progress tracking
```

## 📊 **Performance Monitoring**

### System Health
```bash
# Check logs
tail -20 logs/hooks.log                 # Hook execution
tail -20 logs/notifications.log         # System notifications
grep "ERROR" logs/*.log                 # Find errors

# Performance data
cat analytics/enhancement-metrics.csv | tail -5
cat analytics/usage_patterns.json | jq '.recent'
cat analytics/activation_patterns.json | jq '.top_patterns'
```

### Resource Usage
```bash
# File counts by type
find . -name "*.yml" | wc -l           # YAML configs
find . -name "*.md" | wc -l            # Documentation  
find . -name "*.sh" | wc -l            # Scripts
find . -name "*.json" | wc -l          # Data files

# Directory sizes
du -sh shared/ agents/ scripts/ todos/ analytics/
```

## 🔧 **Development Shortcuts**

### Editing Intelligence
```bash
# Core files to edit
vim CLAUDE.md                          # Main config
vim shared/superclaude-core.yml        # Core intelligence
vim shared/task-intelligence-system.yml # Task management

# Quick edits
sed -i 's/old/new/g' shared/*.yml      # Bulk replace
grep -l "pattern" shared/*.yml | head  # Find files with pattern
```

### Script Management
```bash
# Make scripts executable
chmod +x scripts/*.sh

# Find recently modified
find scripts/ -mtime -7 -name "*.sh"   # Modified last week
find shared/ -newer CLAUDE.md          # Newer than main config

# Test scripts
bash -n scripts/script-name.sh         # Syntax check
```

### Template Operations
```bash
# View @include structure
grep -r "@include" . | cut -d: -f1 | sort -u
grep "@include" CLAUDE.md | head -10

# Find template usage
grep -r "yml#" . | head -5              # YAML section references
find . -name "*template*" -o -name "*pattern*"
```

## 📋 **Task Management**

### Todo Operations
```bash
# Recent tasks
ls -lt todos/ | head -10               # Recently modified
find todos/ -mtime -1                  # Tasks from last 24h
find todos/ -name "*agent*" | wc -l    # Agent-related tasks
```

### Analytics Review
```bash
# Performance trends
tail analytics/enhancement-metrics.csv
cat analytics/usage_patterns.json | jq '.performance'

# System effectiveness
scripts/hooks-effectiveness-analyzer.sh
cat analytics/team-spawn-analysis.jsonl | tail -5
```

## 🎛️ **Aliases & Shortcuts**

### Directory Navigation
```bash
# Add to ~/.bashrc or ~/.zshrc
alias brain="cd ~/DEV/claude-brain-config"
alias shared="cd ~/DEV/claude-brain-config/shared"
alias agents="cd ~/DEV/claude-brain-config/agents" 
alias scripts="cd ~/DEV/claude-brain-config/scripts"
alias analytics="cd ~/DEV/claude-brain-config/analytics"
```

### Common Commands
```bash
# Search functions
alias brainfind='find ~/DEV/claude-brain-config -name'
alias braingrep='grep -r --include="*.yml" --include="*.md"'

# Quick status
alias brainstatus='tail ~/DEV/claude-brain-config/logs/session-*.log'
alias brainmetrics='cat ~/DEV/claude-brain-config/analytics/enhancement-metrics.csv | tail -5'

# Sync shortcuts
alias brainpull='cd ~/DEV/claude-brain-config && ./sync-pull.sh'
alias brainpush='cd ~/DEV/claude-brain-config && ./sync-push.sh'
```

## 🆘 **Emergency Patterns**

### System Reset
```bash
# Backup first
cp CLAUDE.md CLAUDE.md.backup
cp -r shared/ shared.backup/

# Reset from template
git checkout HEAD -- CLAUDE.md
git checkout HEAD -- shared/superclaude-core.yml
```

### Quick Fixes
```bash
# Fix permissions
find scripts/ -name "*.sh" -exec chmod +x {} \;

# Clean cache
rm -rf cache/*
rm -f logs/*.log.old

# Restart system
scripts/system-activator.sh
```

### Troubleshooting
```bash
# Check configuration
python -c "import yaml; yaml.safe_load(open('shared/superclaude-core.yml'))"

# Validate JSON files
find analytics/ -name "*.json" -exec python -m json.tool {} \; > /dev/null

# Test core functionality  
python agents/phase1-integration-test.py
```

## 📚 **Key File References**

| Function | File Path | Description |
|----------|-----------|-------------|
| Main Config | `CLAUDE.md` | Entry point with @include directives |
| Core Intelligence | `shared/superclaude-core.yml` | 70% token reduction, core patterns |
| Agent Orchestration | `agents/multi-agent-orchestrator.md` | Team coordination |
| System Sync | `sync-pull.sh` / `sync-push.sh` | Cross-device synchronization |
| Performance Metrics | `analytics/enhancement-metrics.csv` | Measured improvements |
| Daily Operations | `scripts/daily-improvement-report.sh` | Automated reporting |

---
*Quick reference for 3,083 files | Optimized for daily operations*