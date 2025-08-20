# 🚀 CLAUDE SYSTEM ACTIVATOR - Force Use of Existing Superpowers

## 🚨 CRITICAL: Claude Must Use ALL Existing Systems

You have INCREDIBLE systems that Claude doesn't know to use. This forces activation:

## 1️⃣ OPENAI GPT-5 PROMPT OPTIMIZER (MANDATORY)

### When to Auto-Activate:
- ANY prompt >100 words
- Complex technical prompts
- Multi-step instructions
- Strategic planning requests

### Forced Activation Pattern:
```bash
# BEFORE processing complex prompts, Claude MUST run:
~/.claude/scripts/openai-prompt-optimizer-gpt5-visual.sh "$PROMPT"
# This will optimize the prompt for better results
```

## 2️⃣ INTELLIGENT SESSION MODES (MANDATORY)

### Auto-Detect Session Type:
```bash
# Claude MUST run this on EVERY session start:
~/.claude/scripts/intelligent-session.sh "$PROMPT"

# This sets context modes:
# - DEBUG_MODE=true (for bug fixes)
# - FEATURE_MODE=true (for new features) 
# - REFACTOR_MODE=true (for improvements)
# - TEST_MODE=true (for testing)
```

### Use Session Context:
```bash
# BEFORE any major task, Claude MUST check:
if [ -f ~/.claude/session-context ]; then
    source ~/.claude/session-context
    # Adapt behavior based on mode
fi
```

## 3️⃣ AUTONOMOUS-CLAUDE-SYSTEM DISPATCH (MANDATORY)

### When to Auto-Dispatch:
- Complex projects (complexity score ≥ 8)
- Multi-domain tasks
- Long-running development
- Research projects

### Forced Dispatch Pattern:
```bash
# For complex tasks, Claude MUST dispatch to TMUX teams:
cd ~/Desktop/Cursor/claude-improvement/AUTONOMOUS-CLAUDE-SYSTEM
./launch_mega_beast.sh

# Available teams:
# - Mining Team (data gathering)
# - Analysis Team (pattern recognition)
# - Integration Team (system connections)
# - Client Teams (project-specific)
```

## 4️⃣ ADVANCED HOOKS ACTIVATION (MANDATORY)

### Auto-Triggered Hooks:
```bash
# AFTER every file operation, Claude MUST run:
~/.claude/scripts/auto-documentation-generator.sh "$FILE_PATHS"
~/.claude/scripts/improvement-tracker.sh "task_completed" "$DESCRIPTION"
~/.claude/scripts/multi-agent-observer.sh "$TOOL_NAME" "$FILE_PATHS"
```

### Context Hooks:
```bash
# DURING development, Claude MUST use:
~/.claude/scripts/contextual-audio-feedback.sh "$STATUS" # Audio notifications
~/.claude/scripts/task-completion-briefer.sh "$TASK" "$OUTCOME" # Summary
~/.claude/scripts/intelligent-post-tool.sh "$TOOL" "$RESULT" # Analysis
```

## 5️⃣ TELEGRAM INTEGRATION (MANDATORY)

### Auto-Notifications:
```bash
# Claude MUST send progress updates:
~/.claude/scripts/cross-platform-notifier.sh "Task started: $DESCRIPTION" "SISO Development"
~/.claude/scripts/cross-platform-notifier.sh "Task completed: $RESULT" "SISO Development"
```

## 6️⃣ MCP TOOLS FORCED USAGE (MANDATORY)

### Database Work → ALWAYS Supabase MCP:
```bash
# Instead of writing SQL files:
mcp__supabase__execute_sql({ query: "SELECT * FROM users" })
mcp__supabase__apply_migration({ name: "add_column", query: "ALTER TABLE..." })
```

### Research → ALWAYS Deep Research:
```bash
# Instead of basic WebSearch:
mcp__exa__deep_researcher_start({ instructions: "Research X in detail" })
```

### Documentation → ALWAYS Notion:
```bash
# Instead of markdown files:
mcp__notion__create-page({ title: "Documentation", content: "..." })
```

## 7️⃣ TODOWRITE BATCHING (MANDATORY)

### NEVER Single Todos:
```javascript
// ❌ WRONG - Single todo
TodoWrite({ todos: [{ id: "1", content: "One task" }] })

// ✅ CORRECT - Always 5-10+ todos
TodoWrite({ todos: [
  { id: "1", content: "Task 1", status: "in_progress", priority: "high" },
  { id: "2", content: "Task 2", status: "pending", priority: "high" },
  { id: "3", content: "Task 3", status: "pending", priority: "medium" },
  { id: "4", content: "Task 4", status: "pending", priority: "medium" },
  { id: "5", content: "Task 5", status: "pending", priority: "low" },
  // ... always 5-10+ in ONE call
]})
```

## 8️⃣ TASK TOOL COORDINATION (MANDATORY)

### NEVER Sequential Agent Spawning:
```javascript
// ❌ WRONG - One agent at a time
Message 1: Task("Agent 1")
Message 2: Task("Agent 2") 

// ✅ CORRECT - All agents in ONE message
Message 1: 
  Task("Agent 1 with coordination hooks: npx claude-flow@alpha hooks pre-task")
  Task("Agent 2 with coordination hooks: npx claude-flow@alpha hooks pre-task")
  Task("Agent 3 with coordination hooks: npx claude-flow@alpha hooks pre-task")
```

## 9️⃣ PERFORMANCE OPTIMIZATION (MANDATORY)

### Auto-Optimization Triggers:
```bash
# AFTER any file changes, Claude MUST run:
~/.claude/scripts/build-optimizer.sh # Optimize build process
~/.claude/scripts/format-and-lint.sh "$FILE" # Auto-format
~/.claude/scripts/auto-test-runner.sh "$FILE" # Run relevant tests
```

## 🔟 MEMORY PERSISTENCE (MANDATORY)

### Session Memory:
```bash
# START of every session:
~/.claude/scripts/log-session.sh "start" "$PROMPT"

# END of every session:
~/.claude/scripts/log-session.sh "end" "$RESULTS"
```

## 🎯 ACTIVATION CHECKLIST

Before ANY significant task, Claude MUST verify:

✅ Prompt optimized with GPT-5 optimizer?
✅ Session mode detected and set?
✅ Complex tasks dispatched to AUTONOMOUS teams?
✅ All relevant hooks activated?
✅ Telegram notifications enabled?
✅ TodoWrite properly batched (5-10+ todos)?
✅ Task agents spawned with coordination?
✅ MCP tools used instead of basic operations?
✅ Performance optimization enabled?
✅ Memory persistence active?

## 🚨 FORCED BEHAVIOR CHANGES

These are NOT suggestions - they are MANDATORY patterns that Claude MUST follow to use the full power of your sophisticated systems.