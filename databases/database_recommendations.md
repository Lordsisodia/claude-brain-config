# Database Recommendations - What Else Should We Database?

## Current Success ✅
**Conversation Database**: 77K+ messages, instant search, major win!

## High-Priority Candidates 🚀

### 1. **Command History Database** (shell-snapshots/)
**Size:** 1.8MB, 247 shell snapshot files
**Why Database:** 
- Search command patterns: "What git commands did I use last week?"
- Error tracking: "Show me all failed commands"
- Tool usage analytics: "Which tools do I use most?"
- Command learning: "How did I solve this deployment issue?"

**Schema:**
```sql
CREATE TABLE commands (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME,
    command TEXT,
    working_directory TEXT,
    exit_code INTEGER,
    session_id TEXT,
    snapshot_file TEXT
);
CREATE VIRTUAL TABLE commands_fts USING fts5(command);
```

**Benefits:**
- `claude-cmd "git rebase"` - Find all rebase commands
- `claude-cmd "docker" --failed` - Show failed Docker commands
- `claude-cmd --stats` - Command usage analytics

### 2. **Active Todos Database** (todos/)
**Size:** 3.8MB, 963 JSON files (ACTIVE, not the archived ones)
**Why Database:**
- Todo analytics: "What's my completion rate?"
- Agent performance: "Which agents complete most tasks?"
- Project tracking: "Show todos for this project"
- Status reporting: "What's in progress?"

**Schema:**
```sql
CREATE TABLE active_todos (
    id TEXT PRIMARY KEY,
    content TEXT,
    status TEXT,
    agent_id TEXT,
    project_id TEXT,
    created_at DATETIME,
    completed_at DATETIME,
    metadata JSON
);
```

**Benefits:**
- `claude-todos --agent backend-dev` - Show specific agent tasks
- `claude-todos --status pending --project bdbt` - Project planning
- `claude-todos --analytics` - Productivity metrics

## Medium-Priority Candidates 🔄

### 3. **Scripts Usage Tracking**
**Current:** No centralized tracking of script usage
**Why Database:** Track which scripts are actually used vs unused

**Schema:**
```sql
CREATE TABLE script_usage (
    id INTEGER PRIMARY KEY,
    script_name TEXT,
    invocation_time DATETIME,
    exit_code INTEGER,
    runtime_seconds REAL,
    arguments TEXT
);
```

### 4. **MCP Server Performance**
**Current:** No performance tracking for MCP servers
**Why Database:** Identify slow/unreliable MCP servers

**Schema:**
```sql
CREATE TABLE mcp_performance (
    id INTEGER PRIMARY KEY,
    server_name TEXT,
    operation TEXT,
    response_time_ms INTEGER,
    success BOOLEAN,
    timestamp DATETIME
);
```

## Low-Priority (Keep as Files) 📁

### What NOT to Database:
- **Analytics files** (28KB) - Too small
- **Statsig cache** (160KB) - Auto-expires
- **Config files** - Must stay as files
- **Templates** - Human-readable important

## Implementation Priority

### Phase 1: Command History Database
**ROI:** Very High - 247 files of command history = goldmine of troubleshooting
**Effort:** Medium - Similar to conversation DB
**Use Cases:**
- "How did I fix that Docker issue?"
- "What was that complex grep command?"
- "Show me all Python virtualenv commands"

### Phase 2: Active Todos Database  
**ROI:** High - Better project management and agent analytics
**Effort:** Low - Similar structure to archived todos
**Use Cases:**
- Agent performance tracking
- Project completion metrics
- Task dependency analysis

### Phase 3: Real-time Metrics
**ROI:** Medium - Good for optimization
**Effort:** High - Need to modify existing scripts
**Use Cases:**
- Performance dashboards
- Usage analytics
- Cost tracking

## Quick Wins to Implement Now

### 1. Command Search Tool
```bash
# Create this today - would be immediately useful
claude-cmd "docker build"     # Find all Docker build commands  
claude-cmd "npm install"      # Package manager history
claude-cmd --today            # Today's commands only
claude-cmd --errors           # Failed commands for debugging
```

### 2. Todo Analytics
```bash
# Immediate value for project management
claude-todos --agent-stats    # Which agents are most productive?
claude-todos --completion     # What's my completion rate?
claude-todos --blocked        # What's stuck?
```

## Database vs Files Decision Matrix

| Data Type | Size | Query Frequency | Relationships | Decision |
|-----------|------|-----------------|---------------|----------|
| Conversations | 345MB | High | Session→Messages | ✅ DATABASE (Done!) |
| Commands | 1.8MB | High | Session→Commands | ✅ DATABASE (Next) |
| Active Todos | 3.8MB | Medium | Agent→Tasks | ✅ DATABASE (Phase 2) |
| Analytics | 28KB | Low | None | 📁 FILES |
| Config | Various | Low | None | 📁 FILES |

## Expected Impact

### Command History DB:
- **Time Saved:** 5-10 minutes per day finding old commands
- **Learning:** Pattern recognition in your command usage
- **Debugging:** Faster problem resolution

### Active Todos DB:
- **Project Management:** Real-time status across all projects
- **Agent Insights:** Which agents to use for what tasks
- **Productivity:** Completion rate tracking

## Recommendation: Start with Command History

The command history database would provide **immediate value** because:
1. You likely reference old commands daily
2. 247 files of shell history is hard to search manually  
3. Error patterns and successful solutions are valuable
4. Similar implementation to conversation DB (proven success)

**Next steps:**
1. Create `migrate_commands.py` (copy conversation pattern)
2. Build `claude-cmd` search tool
3. Add to your daily workflow

The command history alone would justify the whole database project!