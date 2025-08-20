#!/usr/bin/env python3
"""
Migrate active Claude todos to database for analytics and management
Solves: "What's my todo completion rate?" and agent performance tracking
"""

import json
import sqlite3
import os
from pathlib import Path
from datetime import datetime
import hashlib
import re

# Configuration  
CLAUDE_HOME = Path.home() / ".claude"
TODOS_DIR = CLAUDE_HOME / "todos"
DB_PATH = CLAUDE_HOME / "databases" / "todos.db"

def create_database():
    """Create todos database with analytics capabilities"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Main todos table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id TEXT PRIMARY KEY,
            agent_id TEXT,
            content TEXT NOT NULL,
            status TEXT CHECK(status IN ('pending', 'in_progress', 'completed')),
            priority TEXT CHECK(priority IN ('low', 'medium', 'high')),
            created_at TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            project_id TEXT,
            tags TEXT,
            original_filename TEXT,
            metadata JSON
        )
    """)
    
    # Indexes for fast queries
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_todos_agent ON todos(agent_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_todos_status ON todos(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_todos_created ON todos(created_at)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_todos_project ON todos(project_id)")
    
    # Full-text search virtual table
    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS todos_fts 
        USING fts5(
            content,
            tags,
            content=todos,
            content_rowid=rowid
        )
    """)
    
    # Trigger to keep FTS index updated
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS todos_fts_insert 
        AFTER INSERT ON todos
        BEGIN
            INSERT INTO todos_fts(rowid, content, tags)
            VALUES (new.rowid, new.content, new.tags);
        END
    """)
    
    # Trigger to update completed_at timestamp
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS todos_completion_timestamp
        AFTER UPDATE OF status ON todos
        FOR EACH ROW
        WHEN NEW.status = 'completed' AND OLD.status != 'completed'
        BEGIN
            UPDATE todos SET completed_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
        END
    """)
    
    # Analytics view for completion rates
    cursor.execute("""
        CREATE VIEW IF NOT EXISTS todo_analytics AS
        SELECT 
            agent_id,
            COUNT(*) as total_tasks,
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_tasks,
            SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress_tasks,
            SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending_tasks,
            ROUND(
                (SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
            ) as completion_rate,
            AVG(
                CASE WHEN completed_at IS NOT NULL AND created_at IS NOT NULL 
                THEN (julianday(completed_at) - julianday(created_at)) * 24 
                ELSE NULL END
            ) as avg_completion_time_hours
        FROM todos 
        WHERE agent_id IS NOT NULL
        GROUP BY agent_id
    """)
    
    conn.commit()
    return conn

def extract_project_from_filename(filename):
    """Extract project info from filename patterns"""
    # Pattern: uuid-agent-uuid.json or project-specific patterns
    if '-agent-' in filename:
        parts = filename.split('-agent-')
        return parts[0] if len(parts) > 1 else None
    return None

def process_todo_file(cursor, todo_file):
    """Process a single todo JSON file"""
    try:
        with open(todo_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle different JSON structures
        if isinstance(data, list):
            # Array of todos
            processed = 0
            for idx, item in enumerate(data):
                if isinstance(item, dict):
                    processed += process_single_todo(cursor, item, todo_file, f"{todo_file.stem}_{idx}")
            return processed
        elif isinstance(data, dict):
            # Single todo
            return process_single_todo(cursor, data, todo_file, todo_file.stem)
        else:
            return 0
            
    except Exception as e:
        print(f"  Error processing {todo_file.name}: {e}")
        return 0

def process_single_todo(cursor, data, todo_file, default_id):
    """Process a single todo item"""
    # Generate unique ID
    todo_id = data.get('id', default_id)
    if not todo_id:
        todo_id = hashlib.md5(f"{todo_file.name}_{data.get('content', '')}".encode()).hexdigest()
    
    # Extract basic fields
    content = data.get('content') or data.get('task') or data.get('description', '')
    if not content:
        return 0  # Skip empty todos
    
    status = data.get('status', 'pending')
    # Normalize status values
    if status.lower() in ['done', 'complete', 'finished']:
        status = 'completed'
    elif status.lower() in ['doing', 'active', 'working']:
        status = 'in_progress'
    elif status not in ['pending', 'in_progress', 'completed']:
        status = 'pending'
    
    priority = data.get('priority', 'medium')
    if priority not in ['low', 'medium', 'high']:
        priority = 'medium'
    
    # Extract agent_id from filename or data
    agent_id = data.get('agent_id') or data.get('agentId')
    if not agent_id:
        filename = todo_file.name
        if '-agent-' in filename:
            parts = filename.split('-agent-')
            if len(parts) > 1:
                agent_id = parts[1].replace('.json', '')
    
    # Extract timestamps
    created_at = data.get('created_at') or data.get('createdAt') or data.get('timestamp')
    updated_at = data.get('updated_at') or data.get('updatedAt')
    completed_at = data.get('completed_at') or data.get('completedAt')
    
    # If status is completed but no completed_at, use updated_at or current time
    if status == 'completed' and not completed_at:
        completed_at = updated_at or datetime.now().isoformat()
    
    # Extract project info
    project_id = data.get('project_id') or data.get('projectId') or extract_project_from_filename(todo_file.name)
    
    # Extract tags from content (look for #hashtags)
    tags = []
    if content:
        hashtags = re.findall(r'#(\w+)', content)
        tags.extend(hashtags)
    
    # Add tags from data
    if 'tags' in data:
        if isinstance(data['tags'], list):
            tags.extend(data['tags'])
        elif isinstance(data['tags'], str):
            tags.append(data['tags'])
    
    tags_str = ','.join(tags) if tags else None
    
    # Store remaining data as metadata
    metadata = {k: v for k, v in data.items() 
                if k not in ['id', 'content', 'task', 'description', 'status', 'priority',
                            'agent_id', 'agentId', 'created_at', 'createdAt', 'updated_at', 
                            'updatedAt', 'completed_at', 'completedAt', 'project_id', 
                            'projectId', 'tags', 'timestamp']}
    
    # Insert into database
    cursor.execute("""
        INSERT OR REPLACE INTO todos 
        (id, agent_id, content, status, priority, created_at, updated_at, 
         completed_at, project_id, tags, original_filename, metadata)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        todo_id,
        agent_id,
        content,
        status,
        priority,
        created_at,
        updated_at,
        completed_at,
        project_id,
        tags_str,
        todo_file.name,
        json.dumps(metadata) if metadata else None
    ))
    
    return 1

def migrate_todos(conn):
    """Migrate all todo JSON files"""
    cursor = conn.cursor()
    
    # Find all JSON files
    json_files = list(TODOS_DIR.glob("*.json"))
    total_files = len(json_files)
    
    print(f"Found {total_files} todo files to migrate")
    
    total_processed = 0
    errors = 0
    
    for idx, json_file in enumerate(json_files, 1):
        if idx % 50 == 0:
            print(f"Processing {idx}/{total_files} files...")
            conn.commit()
        
        processed = process_todo_file(cursor, json_file)
        total_processed += processed
    
    conn.commit()
    
    print(f"\n✅ Migration complete!")
    print(f"  Processed: {total_processed} todos from {total_files} files")
    
    return total_processed

def get_statistics(conn):
    """Get database statistics"""
    cursor = conn.cursor()
    
    stats = {}
    
    cursor.execute("SELECT COUNT(*) FROM todos")
    stats['total_todos'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT status, COUNT(*) FROM todos GROUP BY status")
    stats['by_status'] = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(DISTINCT agent_id) FROM todos WHERE agent_id IS NOT NULL")
    stats['unique_agents'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT project_id) FROM todos WHERE project_id IS NOT NULL")
    stats['unique_projects'] = cursor.fetchone()[0]
    
    # Agent performance
    cursor.execute("""
        SELECT agent_id, total_tasks, completed_tasks, completion_rate
        FROM todo_analytics
        WHERE total_tasks > 5
        ORDER BY completion_rate DESC
        LIMIT 10
    """)
    stats['top_agents'] = cursor.fetchall()
    
    # Recent activity
    cursor.execute("""
        SELECT DATE(created_at) as date, COUNT(*) as count
        FROM todos 
        WHERE created_at >= date('now', '-30 days')
        GROUP BY DATE(created_at)
        ORDER BY date DESC
        LIMIT 7
    """)
    stats['recent_activity'] = cursor.fetchall()
    
    return stats

def main():
    """Main migration function"""
    print("=== Claude Todos Migration ===")
    print(f"Source: {TODOS_DIR}")
    print(f"Destination: {DB_PATH}")
    
    if not TODOS_DIR.exists():
        print("❌ Todos directory not found")
        return 1
    
    # Create database
    print("\nCreating database...")
    conn = create_database()
    
    try:
        # Perform migration
        print("\nMigrating todos...")
        migrate_todos(conn)
        
        # Show statistics
        print("\n📊 Database Statistics:")
        stats = get_statistics(conn)
        print(f"  Total todos: {stats['total_todos']:,}")
        print(f"  Unique agents: {stats['unique_agents']}")
        print(f"  Unique projects: {stats['unique_projects']}")
        
        if stats['by_status']:
            print("\n  By status:")
            for status, count in stats['by_status']:
                print(f"    - {status}: {count:,}")
        
        if stats['top_agents']:
            print("\n  Top performing agents:")
            for agent_id, total, completed, rate in stats['top_agents'][:5]:
                print(f"    - {agent_id}: {rate}% ({completed}/{total} completed)")
        
        if stats['recent_activity']:
            print(f"\n  Recent activity (last 7 days):")
            for date, count in stats['recent_activity']:
                print(f"    - {date}: {count} todos created")
        
        print(f"\n✅ Database created at: {DB_PATH}")
        print("\n💡 Now you can:")
        print("  - Track agent performance")
        print("  - Analyze completion rates")
        print("  - Search todos by content")
        print("  - Generate productivity reports")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        return 1
    finally:
        conn.close()

if __name__ == "__main__":
    exit(main())