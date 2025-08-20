# Claude Brain Config - Database Migration Plan

## Executive Summary
Migrating from 200+ JSON files to 4 SQLite databases for better performance and organization.
**All original files will be preserved - this is a safe, reversible migration.**

## What Gets Migrated to SQLite

### 1. **tasks.db** - Todo/Task Management
- **Source:** `todos/` folder (200+ JSON files)
- **Target:** `databases/tasks.db`
- **Benefits:** 
  - Fast queries and filtering
  - Status tracking
  - Agent performance metrics
  - 90% reduction in file count

### 2. **analytics.db** - Metrics & Benchmarks  
- **Source:** `analytics/` folder (JSON/CSV files)
- **Target:** `databases/analytics.db`
- **Benefits:**
  - Time-series queries
  - Performance tracking
  - Trend analysis
  - Aggregations

### 3. **sessions.db** - Session Management
- **Source:** `statsig/` folder (cache files)
- **Target:** `databases/sessions.db`
- **Benefits:**
  - Session tracking
  - Cache management
  - Metrics collection

### 4. **agent_economy.db** - Token Economics
- **Source:** `agent_economy/` Python files with data
- **Target:** `databases/agent_economy.db`
- **Benefits:**
  - Transaction tracking
  - Balance management
  - Economic metrics

## What Stays as Files (DO NOT MIGRATE)

### Documentation (35+ files)
- All `.md` files - Human-readable documentation
- README files
- Guides and reports
- Setup instructions

### Code & Scripts
- All `.py` files - Python scripts
- All `.sh` files - Shell scripts  
- All `.yml` files - Configuration templates
- `deploy.py` and other executables

### Configuration
- `settings.hooks.json` and variants - Critical system config
- `shared/` folder - YAML configuration templates
- `commands/` folder - Command definitions
- `agents/` folder - Agent configurations
- `output-styles/` folder - Style templates
- `templates/` folder - System templates

### Infrastructure
- `scripts/` folder - Automation scripts
- `tmux-brain-scripts/` folder - Orchestration scripts
- `infrastructure/` folder - System components

## Migration Safety Features

1. **Non-Destructive**: Original files are preserved
2. **Reversible**: Can export databases back to JSON
3. **Dual-Write Period**: Writes to both DB and files during transition
4. **Compatibility Layer**: Auto-fallback to files if DB unavailable
5. **Backup System**: Automatic backups before migration

## How to Run Migration

### Step 1: Test Migration (Safe)
```bash
cd /Users/shaansisodia/DEV/claude-brain-config/databases
python3 test_migration.py
```

### Step 2: Run Actual Migration
```bash
python3 migrate_todos_to_sqlite.py
```

### Step 3: Verify Success
```bash
python3 -c "from db_compat import get_database_status; print(get_database_status())"
```

## Emergency Recovery

If anything goes wrong, you can restore from:
1. Original files (still intact in their folders)
2. Database backups in `databases/backups/`
3. Export databases back to JSON:
```python
from db_compat import DatabaseCompatibilityLayer
with DatabaseCompatibilityLayer() as compat:
    compat.export_database('tasks', Path('./json_export'))
```

## Expected Results

- **Before Migration:** 200+ individual JSON files
- **After Migration:** 4 optimized SQLite databases
- **Performance Gain:** 10-100x faster queries
- **Storage Efficiency:** 50-70% less disk space
- **Maintenance:** Much easier to backup and manage

## Current Status

✅ Migration infrastructure created
✅ Compatibility layer implemented  
✅ Backup/restore utilities ready
✅ Todos migration script ready
⏳ Analytics migration script pending
⏳ Sessions migration script pending
⏳ Agent economy migration pending

## Questions?

The migration is designed to be completely safe. Your original files remain untouched, and everything is reversible. The system will continue to work during and after migration with automatic fallbacks.