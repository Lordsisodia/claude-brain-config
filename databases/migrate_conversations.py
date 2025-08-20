#!/usr/bin/env python3
"""
Migrate Claude conversation history to searchable SQLite database
Solves: "How did I solve this problem before?" queries
"""

import json
import sqlite3
import os
from pathlib import Path
from datetime import datetime
import hashlib

# Configuration
CLAUDE_HOME = Path.home() / ".claude"
PROJECTS_DIR = CLAUDE_HOME / "projects"
DB_PATH = CLAUDE_HOME / "databases" / "conversations.db"

def create_database():
    """Create conversation database with full-text search"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Main conversations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            session_id TEXT,
            project_path TEXT,
            timestamp DATETIME,
            uuid TEXT,
            parent_uuid TEXT,
            message_role TEXT,
            message_content TEXT,
            model TEXT,
            tokens_input INTEGER,
            tokens_output INTEGER,
            metadata JSON
        )
    """)
    
    # Indexes for fast queries
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_conv_session ON conversations(session_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_conv_project ON conversations(project_path)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_conv_timestamp ON conversations(timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_conv_role ON conversations(message_role)")
    
    # Full-text search virtual table
    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS conversations_fts 
        USING fts5(
            message_content,
            content=conversations,
            content_rowid=rowid
        )
    """)
    
    # Trigger to keep FTS index updated
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS conversations_fts_insert 
        AFTER INSERT ON conversations
        BEGIN
            INSERT INTO conversations_fts(rowid, message_content)
            VALUES (new.rowid, new.message_content);
        END
    """)
    
    conn.commit()
    return conn

def process_jsonl_file(cursor, jsonl_path, project_name):
    """Process a single JSONL conversation file"""
    processed = 0
    errors = 0
    
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line.strip())
                
                # Extract message content based on structure
                message_content = ""
                message_role = data.get('type', '')
                
                if 'message' in data:
                    msg = data['message']
                    if isinstance(msg, dict):
                        message_role = msg.get('role', message_role)
                        
                        # Handle different content structures
                        content = msg.get('content')
                        if isinstance(content, str):
                            message_content = content
                        elif isinstance(content, list):
                            # Extract text from content array
                            text_parts = []
                            for item in content:
                                if isinstance(item, dict):
                                    if item.get('type') == 'text':
                                        text_parts.append(item.get('text', ''))
                                    elif item.get('type') == 'thinking':
                                        text_parts.append(f"[THINKING] {item.get('thinking', '')}")
                            message_content = "\n".join(text_parts)
                        elif isinstance(content, dict):
                            message_content = str(content)
                
                # Generate unique ID
                unique_string = f"{jsonl_path.name}_{line_num}_{data.get('uuid', '')}"
                record_id = hashlib.md5(unique_string.encode()).hexdigest()
                
                # Extract token usage
                tokens_input = 0
                tokens_output = 0
                if 'usage' in msg:
                    usage = msg['usage']
                    tokens_input = usage.get('input_tokens', 0) + usage.get('cache_read_input_tokens', 0)
                    tokens_output = usage.get('output_tokens', 0)
                
                # Insert into database
                cursor.execute("""
                    INSERT OR REPLACE INTO conversations 
                    (id, session_id, project_path, timestamp, uuid, parent_uuid,
                     message_role, message_content, model, tokens_input, tokens_output, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    record_id,
                    data.get('sessionId', ''),
                    project_name,
                    data.get('timestamp', ''),
                    data.get('uuid', ''),
                    data.get('parentUuid', ''),
                    message_role,
                    message_content[:10000],  # Limit content length
                    msg.get('model', '') if isinstance(msg, dict) else '',
                    tokens_input,
                    tokens_output,
                    json.dumps({k: v for k, v in data.items() 
                               if k not in ['message', 'uuid', 'sessionId', 'timestamp']})
                ))
                
                processed += 1
                
            except Exception as e:
                errors += 1
                if errors <= 5:  # Show first 5 errors
                    print(f"  Error in {jsonl_path.name} line {line_num}: {e}")
    
    return processed, errors

def migrate_conversations(conn):
    """Migrate all conversation JSONL files"""
    cursor = conn.cursor()
    
    # Find all JSONL files
    jsonl_files = list(PROJECTS_DIR.rglob("*.jsonl"))
    total_files = len(jsonl_files)
    
    print(f"Found {total_files} conversation files to migrate")
    
    total_processed = 0
    total_errors = 0
    
    for idx, jsonl_path in enumerate(jsonl_files, 1):
        # Extract project name from path
        project_name = jsonl_path.parent.name
        
        if idx % 10 == 0:
            print(f"Processing {idx}/{total_files} files...")
            conn.commit()
        
        processed, errors = process_jsonl_file(cursor, jsonl_path, project_name)
        total_processed += processed
        total_errors += errors
    
    conn.commit()
    
    print(f"\n✅ Migration complete!")
    print(f"  Processed: {total_processed} messages")
    print(f"  Errors: {total_errors}")
    
    return total_processed

def search_conversations(conn, query, limit=10):
    """Example search function"""
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT c.*, highlight(conversations_fts, 0, '**', '**') as highlighted
        FROM conversations c
        JOIN conversations_fts ON c.rowid = conversations_fts.rowid
        WHERE conversations_fts MATCH ?
        ORDER BY rank
        LIMIT ?
    """, (query, limit))
    
    return cursor.fetchall()

def get_statistics(conn):
    """Get database statistics"""
    cursor = conn.cursor()
    
    stats = {}
    
    cursor.execute("SELECT COUNT(*) FROM conversations")
    stats['total_messages'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT session_id) FROM conversations")
    stats['unique_sessions'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT project_path) FROM conversations")
    stats['unique_projects'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(tokens_input) + SUM(tokens_output) FROM conversations")
    stats['total_tokens'] = cursor.fetchone()[0] or 0
    
    cursor.execute("""
        SELECT project_path, COUNT(*) as msg_count 
        FROM conversations 
        GROUP BY project_path 
        ORDER BY msg_count DESC 
        LIMIT 5
    """)
    stats['top_projects'] = cursor.fetchall()
    
    return stats

def main():
    """Main migration function"""
    print("=== Claude Conversation History Migration ===")
    print(f"Source: {PROJECTS_DIR}")
    print(f"Destination: {DB_PATH}")
    
    if not PROJECTS_DIR.exists():
        print("❌ Projects directory not found")
        return 1
    
    # Create database
    print("\nCreating database...")
    conn = create_database()
    
    try:
        # Perform migration
        print("\nMigrating conversations...")
        migrate_conversations(conn)
        
        # Show statistics
        print("\n📊 Database Statistics:")
        stats = get_statistics(conn)
        print(f"  Total messages: {stats['total_messages']:,}")
        print(f"  Unique sessions: {stats['unique_sessions']}")
        print(f"  Unique projects: {stats['unique_projects']}")
        print(f"  Total tokens used: {stats['total_tokens']:,}")
        
        if stats['top_projects']:
            print("\n  Top 5 projects by message count:")
            for project, count in stats['top_projects']:
                print(f"    - {project}: {count:,} messages")
        
        # Test search
        print("\n🔍 Testing search functionality...")
        test_results = search_conversations(conn, "python function", limit=3)
        print(f"  Found {len(test_results)} results for 'python function'")
        
        print(f"\n✅ Database created at: {DB_PATH}")
        print("\n💡 Example searches you can now do:")
        print("  - 'React component useState'")
        print("  - 'database migration'")
        print("  - 'error handling'")
        print("  - 'TODO FIXME'")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        return 1
    finally:
        conn.close()

if __name__ == "__main__":
    exit(main())