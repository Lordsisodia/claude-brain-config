#!/usr/bin/env python3
"""
Migrate Claude shell snapshots to searchable command history database
Solves: "What was that command I used before?" queries
"""

import sqlite3
import os
import re
from pathlib import Path
from datetime import datetime
import hashlib

# Configuration
CLAUDE_HOME = Path.home() / ".claude"
SNAPSHOTS_DIR = CLAUDE_HOME / "shell-snapshots"
DB_PATH = CLAUDE_HOME / "databases" / "commands.db"

def create_database():
    """Create command history database with full-text search"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Main commands table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS commands (
            id TEXT PRIMARY KEY,
            timestamp DATETIME,
            command TEXT,
            working_directory TEXT,
            shell_type TEXT,
            session_id TEXT,
            snapshot_file TEXT,
            line_number INTEGER,
            function_name TEXT,
            alias_name TEXT,
            is_function BOOLEAN DEFAULT 0,
            is_alias BOOLEAN DEFAULT 0
        )
    """)
    
    # Indexes for fast queries
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cmd_timestamp ON commands(timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cmd_session ON commands(session_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cmd_shell ON commands(shell_type)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cmd_function ON commands(is_function)")
    
    # Full-text search virtual table
    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS commands_fts 
        USING fts5(
            command,
            function_name,
            content=commands,
            content_rowid=rowid
        )
    """)
    
    # Trigger to keep FTS index updated
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS commands_fts_insert 
        AFTER INSERT ON commands
        BEGIN
            INSERT INTO commands_fts(rowid, command, function_name)
            VALUES (new.rowid, new.command, new.function_name);
        END
    """)
    
    conn.commit()
    return conn

def extract_timestamp_from_filename(filename):
    """Extract timestamp from snapshot filename"""
    # Format: snapshot-zsh-1752712838457-pzuqjh.sh
    match = re.search(r'snapshot-(\w+)-(\d+)-', filename)
    if match:
        shell_type = match.group(1)
        timestamp_ms = int(match.group(2))
        # Convert from milliseconds to datetime
        timestamp = datetime.fromtimestamp(timestamp_ms / 1000)
        return timestamp, shell_type
    return None, "unknown"

def parse_shell_snapshot(snapshot_path):
    """Parse shell snapshot file and extract commands, functions, aliases"""
    commands = []
    functions = []
    aliases = []
    
    current_function = None
    function_content = []
    in_function = False
    
    try:
        with open(snapshot_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {snapshot_path}: {e}")
        return [], [], []
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        
        # Skip comments and empty lines
        if not line or line.startswith('#'):
            continue
        
        # Detect function definitions
        if re.match(r'^\w+\s*\(\)\s*{?$', line) or re.match(r'^function\s+\w+', line):
            # Function start
            func_name = re.sub(r'[(){}\s]|function', '', line.split()[0])
            current_function = func_name
            function_content = [line]
            in_function = True
            continue
        
        # Detect function end
        if in_function and line == '}':
            function_content.append(line)
            functions.append({
                'name': current_function,
                'content': '\n'.join(function_content),
                'line_number': line_num
            })
            in_function = False
            current_function = None
            function_content = []
            continue
        
        # Inside function
        if in_function:
            function_content.append(line)
            continue
        
        # Detect aliases
        if line.startswith('alias '):
            alias_match = re.match(r'alias\s+([^=]+)=(.+)', line)
            if alias_match:
                aliases.append({
                    'name': alias_match.group(1).strip(),
                    'command': alias_match.group(2).strip().strip('"\''),
                    'line_number': line_num
                })
            continue
        
        # Regular commands (exported functions, variable assignments, etc.)
        if ('export' in line or '=' in line or 
            line.startswith('unset') or line.startswith('source') or 
            'PATH=' in line or 'command -v' in line):
            commands.append({
                'command': line,
                'line_number': line_num,
                'type': 'command'
            })
    
    return commands, functions, aliases

def process_snapshot_file(cursor, snapshot_path):
    """Process a single snapshot file"""
    filename = snapshot_path.name
    timestamp, shell_type = extract_timestamp_from_filename(filename)
    
    # Extract session ID from filename
    session_match = re.search(r'-([a-z0-9]+)\.sh$', filename)
    session_id = session_match.group(1) if session_match else 'unknown'
    
    commands, functions, aliases = parse_shell_snapshot(snapshot_path)
    
    processed = 0
    
    # Insert regular commands
    for cmd_data in commands:
        record_id = hashlib.md5(f"{filename}_{cmd_data['line_number']}_{cmd_data['command']}".encode()).hexdigest()
        
        cursor.execute("""
            INSERT OR REPLACE INTO commands 
            (id, timestamp, command, shell_type, session_id, snapshot_file, 
             line_number, is_function, is_alias)
            VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0)
        """, (
            record_id,
            timestamp,
            cmd_data['command'],
            shell_type,
            session_id,
            filename,
            cmd_data['line_number']
        ))
        processed += 1
    
    # Insert functions
    for func_data in functions:
        record_id = hashlib.md5(f"{filename}_{func_data['line_number']}_func_{func_data['name']}".encode()).hexdigest()
        
        cursor.execute("""
            INSERT OR REPLACE INTO commands 
            (id, timestamp, command, shell_type, session_id, snapshot_file, 
             line_number, function_name, is_function, is_alias)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, 0)
        """, (
            record_id,
            timestamp,
            func_data['content'],
            shell_type,
            session_id,
            filename,
            func_data['line_number'],
            func_data['name']
        ))
        processed += 1
    
    # Insert aliases
    for alias_data in aliases:
        record_id = hashlib.md5(f"{filename}_{alias_data['line_number']}_alias_{alias_data['name']}".encode()).hexdigest()
        
        cursor.execute("""
            INSERT OR REPLACE INTO commands 
            (id, timestamp, command, shell_type, session_id, snapshot_file, 
             line_number, alias_name, is_function, is_alias)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, 1)
        """, (
            record_id,
            timestamp,
            f"alias {alias_data['name']}={alias_data['command']}",
            shell_type,
            session_id,
            filename,
            alias_data['line_number'],
            alias_data['name']
        ))
        processed += 1
    
    return processed

def migrate_commands(conn):
    """Migrate all shell snapshot files"""
    cursor = conn.cursor()
    
    # Find all snapshot files
    snapshot_files = list(SNAPSHOTS_DIR.glob("snapshot-*.sh"))
    total_files = len(snapshot_files)
    
    print(f"Found {total_files} shell snapshot files to migrate")
    
    total_processed = 0
    errors = 0
    
    for idx, snapshot_path in enumerate(snapshot_files, 1):
        try:
            if idx % 25 == 0:
                print(f"Processing {idx}/{total_files} files...")
                conn.commit()
            
            processed = process_snapshot_file(cursor, snapshot_path)
            total_processed += processed
            
        except Exception as e:
            errors += 1
            if errors <= 5:  # Show first 5 errors
                print(f"  Error processing {snapshot_path.name}: {e}")
    
    conn.commit()
    
    print(f"\n✅ Migration complete!")
    print(f"  Processed: {total_processed} commands/functions/aliases")
    print(f"  From: {total_files} snapshot files")
    print(f"  Errors: {errors}")
    
    return total_processed

def search_commands(conn, query, limit=10):
    """Example search function"""
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT c.*, highlight(commands_fts, 0, '**', '**') as highlighted
        FROM commands c
        JOIN commands_fts ON c.rowid = commands_fts.rowid
        WHERE commands_fts MATCH ?
        ORDER BY c.timestamp DESC
        LIMIT ?
    """, (query, limit))
    
    return cursor.fetchall()

def get_statistics(conn):
    """Get database statistics"""
    cursor = conn.cursor()
    
    stats = {}
    
    cursor.execute("SELECT COUNT(*) FROM commands")
    stats['total_commands'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM commands WHERE is_function = 1")
    stats['functions'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM commands WHERE is_alias = 1")
    stats['aliases'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT session_id) FROM commands")
    stats['unique_sessions'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT shell_type, COUNT(*) FROM commands GROUP BY shell_type")
    stats['by_shell'] = cursor.fetchall()
    
    cursor.execute("""
        SELECT function_name, COUNT(*) as usage_count
        FROM commands 
        WHERE is_function = 1 AND function_name IS NOT NULL
        GROUP BY function_name 
        ORDER BY usage_count DESC 
        LIMIT 10
    """)
    stats['top_functions'] = cursor.fetchall()
    
    return stats

def main():
    """Main migration function"""
    print("=== Claude Command History Migration ===")
    print(f"Source: {SNAPSHOTS_DIR}")
    print(f"Destination: {DB_PATH}")
    
    if not SNAPSHOTS_DIR.exists():
        print("❌ Shell snapshots directory not found")
        return 1
    
    # Create database
    print("\nCreating database...")
    conn = create_database()
    
    try:
        # Perform migration
        print("\nMigrating shell snapshots...")
        migrate_commands(conn)
        
        # Show statistics
        print("\n📊 Database Statistics:")
        stats = get_statistics(conn)
        print(f"  Total commands/functions/aliases: {stats['total_commands']:,}")
        print(f"  Functions: {stats['functions']}")
        print(f"  Aliases: {stats['aliases']}")
        print(f"  Unique sessions: {stats['unique_sessions']}")
        
        if stats['by_shell']:
            print("\n  By shell type:")
            for shell, count in stats['by_shell']:
                print(f"    - {shell}: {count:,}")
        
        if stats['top_functions']:
            print("\n  Top functions:")
            for func_name, count in stats['top_functions'][:5]:
                print(f"    - {func_name}: {count} instances")
        
        # Test search
        print("\n🔍 Testing search functionality...")
        test_results = search_commands(conn, "export", limit=3)
        print(f"  Found {len(test_results)} results for 'export'")
        
        print(f"\n✅ Database created at: {DB_PATH}")
        print("\n💡 Example searches you can now do:")
        print("  - 'docker build'")
        print("  - 'git rebase'")
        print("  - 'npm install'")
        print("  - 'python -m'")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        return 1
    finally:
        conn.close()

if __name__ == "__main__":
    exit(main())