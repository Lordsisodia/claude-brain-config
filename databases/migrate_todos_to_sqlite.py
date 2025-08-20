#!/usr/bin/env python3
"""
Migrate todos JSON files to SQLite database
Safe migration that preserves original files
"""

import json
import sqlite3
import os
from pathlib import Path
from datetime import datetime
import shutil

# Configuration
CLAUDE_BRAIN_CONFIG = Path("/Users/shaansisodia/DEV/claude-brain-config")
TODOS_DIR = CLAUDE_BRAIN_CONFIG / "todos"
DATABASES_DIR = CLAUDE_BRAIN_CONFIG / "databases"
BACKUP_DIR = DATABASES_DIR / "backups"
DB_PATH = DATABASES_DIR / "tasks.db"

def create_database():
    """Create the tasks database with proper schema"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create main tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            agent_id TEXT,
            content TEXT NOT NULL,
            status TEXT CHECK(status IN ('pending', 'in_progress', 'completed')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            original_filename TEXT,
            metadata JSON
        )
    """)
    
    # Create indexes for performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_agent ON tasks(agent_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_created ON tasks(created_at)")
    
    # Create trigger to update the updated_at timestamp
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS update_tasks_timestamp
        AFTER UPDATE ON tasks
        FOR EACH ROW
        BEGIN
            UPDATE tasks SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
        END
    """)
    
    conn.commit()
    return conn

def backup_existing_database():
    """Backup existing database if it exists"""
    if DB_PATH.exists():
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = BACKUP_DIR / f"tasks_backup_{timestamp}.db"
        shutil.copy2(DB_PATH, backup_path)
        print(f"Backed up existing database to {backup_path}")

def migrate_json_files(conn):
    """Migrate all JSON files from todos directory"""
    cursor = conn.cursor()
    
    # Get all JSON files
    json_files = list(TODOS_DIR.glob("*.json"))
    total_files = len(json_files)
    
    print(f"Found {total_files} JSON files to migrate")
    
    migrated = 0
    skipped = 0
    errors = []
    
    for json_file in json_files:
        try:
            # Read JSON file
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, list):
                # If it's an empty array, skip it
                if not data:
                    skipped += 1
                    continue
                    
                # If it's an array with items, process each item
                for idx, item in enumerate(data):
                    if isinstance(item, dict):
                        process_task_item(cursor, item, json_file, f"{json_file.stem}_{idx}")
                        migrated += 1
                    
            elif isinstance(data, dict):
                # Process single dict
                process_task_item(cursor, data, json_file, json_file.stem)
                migrated += 1
            else:
                # Unknown structure, skip
                skipped += 1
                
            if migrated % 50 == 0 and migrated > 0:
                print(f"Migrated {migrated} tasks...")
                conn.commit()
                
        except Exception as e:
            errors.append((json_file.name, str(e)))
            print(f"Error migrating {json_file.name}: {e}")
    
    conn.commit()
    
    print(f"\nMigration complete!")
    print(f"Successfully migrated: {migrated} tasks from {total_files} files")
    if skipped > 0:
        print(f"Skipped {skipped} empty/invalid files")
    
    if errors:
        print(f"\nErrors encountered ({len(errors)} files):")
        for filename, error in errors[:5]:  # Show first 5 errors
            print(f"  - {filename}: {error}")
        if len(errors) > 5:
            print(f"  ... and {len(errors) - 5} more errors")
    
    return migrated, errors

def process_task_item(cursor, data, json_file, default_id):
    """Process a single task item and insert into database"""
    # Extract fields with defaults
    task_id = data.get('id', default_id)
    
    # Handle different possible field names
    content = data.get('content') or data.get('task') or data.get('description', '')
    status = data.get('status', 'pending')
    
    # Normalize status values
    if status.lower() in ['done', 'complete', 'finished']:
        status = 'completed'
    elif status.lower() in ['doing', 'active', 'working']:
        status = 'in_progress'
    elif status not in ['pending', 'in_progress', 'completed']:
        status = 'pending'
    
    # Extract agent_id from filename or data
    filename = json_file.name
    agent_id = None
    if 'agent-' in filename:
        parts = filename.split('agent-')
        if len(parts) > 1:
            agent_id = parts[1].replace('.json', '')
    if not agent_id:
        agent_id = data.get('agent_id') or data.get('agentId')
    
    # Store remaining data as metadata
    metadata = {k: v for k, v in data.items() 
               if k not in ['id', 'content', 'task', 'description', 'status', 'agent_id', 'agentId']}
    
    # Insert into database
    cursor.execute("""
        INSERT OR REPLACE INTO tasks 
        (id, agent_id, content, status, original_filename, metadata)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        task_id,
        agent_id,
        content,
        status,
        filename,
        json.dumps(metadata) if metadata else None
    ))

def verify_migration(conn):
    """Verify the migration was successful"""
    cursor = conn.cursor()
    
    # Get statistics
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cursor.fetchone()[0]
    
    cursor.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status")
    status_counts = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(DISTINCT agent_id) FROM tasks WHERE agent_id IS NOT NULL")
    unique_agents = cursor.fetchone()[0]
    
    print("\n=== Migration Verification ===")
    print(f"Total tasks in database: {total_tasks}")
    print(f"Unique agents: {unique_agents}")
    print("\nTasks by status:")
    for status, count in status_counts:
        print(f"  {status}: {count}")
    
    return total_tasks

def export_to_json(conn, output_dir=None):
    """Export database back to JSON for emergency recovery"""
    if output_dir is None:
        output_dir = DATABASES_DIR / "json_export"
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    
    exported = 0
    for row in cursor.fetchall():
        task_data = {
            'id': row[0],
            'agent_id': row[1],
            'content': row[2],
            'status': row[3],
            'created_at': row[4],
            'updated_at': row[5],
            'original_filename': row[6]
        }
        
        # Add metadata if exists
        if row[7]:
            metadata = json.loads(row[7])
            task_data.update(metadata)
        
        # Write to JSON file
        filename = f"{row[0]}.json"
        if row[1]:  # If agent_id exists
            filename = f"{row[0]}-agent-{row[1]}.json"
        
        with open(output_dir / filename, 'w') as f:
            json.dump(task_data, f, indent=2, default=str)
        
        exported += 1
    
    print(f"\nExported {exported} tasks to {output_dir}")
    return exported

def main():
    """Main migration function"""
    print("=== Todos to SQLite Migration ===")
    print(f"Source: {TODOS_DIR}")
    print(f"Destination: {DB_PATH}")
    
    # Safety checks
    if not TODOS_DIR.exists():
        print(f"Error: Todos directory not found at {TODOS_DIR}")
        return 1
    
    # Create databases directory
    DATABASES_DIR.mkdir(parents=True, exist_ok=True)
    
    # Backup existing database if it exists
    backup_existing_database()
    
    # Create or connect to database
    print("\nCreating database schema...")
    conn = create_database()
    
    try:
        # Perform migration
        print("\nStarting migration...")
        migrated, errors = migrate_json_files(conn)
        
        # Verify migration
        verify_migration(conn)
        
        # Offer to export back to JSON as a test
        print("\n=== Testing JSON Export (Emergency Recovery) ===")
        export_dir = DATABASES_DIR / "test_export"
        export_to_json(conn, export_dir)
        print(f"Test export complete. Check {export_dir} to verify data integrity")
        
        print("\n✅ Migration successful!")
        print(f"Database created at: {DB_PATH}")
        print("\n⚠️  Original JSON files have been preserved in {TODOS_DIR}")
        print("You can safely delete them after verifying the database works correctly")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        return 1
    finally:
        conn.close()

if __name__ == "__main__":
    exit(main())