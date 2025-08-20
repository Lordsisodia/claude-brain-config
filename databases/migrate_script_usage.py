#!/usr/bin/env python3
"""
Script Usage Tracking Database - Monitor which claude-brain-config scripts are actually used
Solves: "Which scripts are unused?" and "What's the usage pattern of my automation?"
"""

import sqlite3
import os
import hashlib
from pathlib import Path
from datetime import datetime
import json
import re

# Configuration
CLAUDE_HOME = Path.home() / ".claude"
BRAIN_CONFIG_DIR = Path.home() / "DEV" / "claude-brain-config"
DB_PATH = CLAUDE_HOME / "databases" / "script_usage.db"

def create_database():
    """Create script usage tracking database"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Script registry table - all discovered scripts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scripts (
            id TEXT PRIMARY KEY,
            script_path TEXT UNIQUE NOT NULL,
            script_name TEXT NOT NULL,
            script_type TEXT,
            language TEXT,
            size_bytes INTEGER,
            permissions TEXT,
            last_modified DATETIME,
            discovered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            category TEXT,
            description TEXT
        )
    """)
    
    # Script usage tracking table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS script_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            script_id TEXT NOT NULL,
            execution_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            exit_code INTEGER,
            runtime_seconds REAL,
            arguments TEXT,
            working_directory TEXT,
            user TEXT,
            session_info TEXT,
            FOREIGN KEY (script_id) REFERENCES scripts (id)
        )
    """)
    
    # Usage analytics view
    cursor.execute("""
        CREATE VIEW IF NOT EXISTS script_analytics AS
        SELECT 
            s.script_name,
            s.script_path,
            s.category,
            s.script_type,
            COUNT(u.id) as total_executions,
            MAX(u.execution_time) as last_used,
            MIN(u.execution_time) as first_used,
            AVG(u.runtime_seconds) as avg_runtime_seconds,
            SUM(CASE WHEN u.exit_code = 0 THEN 1 ELSE 0 END) as successful_runs,
            SUM(CASE WHEN u.exit_code != 0 THEN 1 ELSE 0 END) as failed_runs,
            ROUND(
                (SUM(CASE WHEN u.exit_code = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(u.id)), 2
            ) as success_rate,
            julianday('now') - julianday(MAX(u.execution_time)) as days_since_last_use
        FROM scripts s
        LEFT JOIN script_usage u ON s.id = u.script_id
        GROUP BY s.id, s.script_name, s.script_path, s.category, s.script_type
    """)
    
    # Unused scripts view
    cursor.execute("""
        CREATE VIEW IF NOT EXISTS unused_scripts AS
        SELECT 
            script_name,
            script_path,
            category,
            script_type,
            size_bytes,
            last_modified,
            discovered_at,
            julianday('now') - julianday(discovered_at) as days_discovered
        FROM scripts
        WHERE id NOT IN (SELECT DISTINCT script_id FROM script_usage WHERE script_id IS NOT NULL)
        ORDER BY size_bytes DESC
    """)
    
    # Indexes for performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_script_usage_script_id ON script_usage(script_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_script_usage_time ON script_usage(execution_time)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_scripts_category ON scripts(category)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_scripts_type ON scripts(script_type)")
    
    conn.commit()
    return conn

def categorize_script(script_path):
    """Categorize scripts based on path and name patterns"""
    path_str = str(script_path).lower()
    name = script_path.name.lower()
    
    if '/scripts/' in path_str:
        if 'test' in name:
            return 'testing'
        elif 'deploy' in name or 'build' in name:
            return 'deployment'
        elif 'monitor' in name or 'track' in name:
            return 'monitoring'
        elif 'auto' in name or 'intelligent' in name:
            return 'automation'
        elif 'telegram' in name or 'notif' in name:
            return 'notifications'
        else:
            return 'scripts'
    elif '/infrastructure/' in path_str:
        return 'infrastructure'
    elif '/agents/' in path_str:
        return 'agents'
    elif '/testing/' in path_str:
        return 'testing'
    elif '/tmux' in path_str:
        return 'orchestration'
    elif '/coordination/' in path_str:
        return 'coordination'
    elif 'setup' in name or 'install' in name:
        return 'setup'
    else:
        return 'other'

def detect_language(script_path):
    """Detect script language from extension and shebang"""
    ext = script_path.suffix.lower()
    
    if ext == '.py':
        return 'python'
    elif ext == '.sh':
        return 'bash'
    elif ext == '.js':
        return 'javascript'
    elif ext == '.md':
        return 'markdown'
    elif ext == '.yml' or ext == '.yaml':
        return 'yaml'
    elif ext == '.json':
        return 'json'
    else:
        # Check shebang
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                if first_line.startswith('#!'):
                    if 'python' in first_line:
                        return 'python'
                    elif 'bash' in first_line or 'sh' in first_line:
                        return 'bash'
                    elif 'node' in first_line:
                        return 'javascript'
        except:
            pass
        
        return 'unknown'

def discover_scripts(cursor):
    """Discover all scripts in claude-brain-config directory"""
    script_patterns = [
        '**/*.py',
        '**/*.sh', 
        '**/*.js',
        '**/*.md',  # Some .md files are executable
    ]
    
    discovered = 0
    
    for pattern in script_patterns:
        for script_path in BRAIN_CONFIG_DIR.glob(pattern):
            # Skip if not a file
            if not script_path.is_file():
                continue
                
            # Skip certain directories/files
            if any(skip in str(script_path) for skip in ['.git', '__pycache__', '.DS_Store', 'node_modules']):
                continue
            
            # Generate script ID
            script_id = hashlib.md5(str(script_path).encode()).hexdigest()
            
            # Get file info
            stat_info = script_path.stat()
            size_bytes = stat_info.st_size
            last_modified = datetime.fromtimestamp(stat_info.st_mtime)
            permissions = oct(stat_info.st_mode)[-3:]
            
            # Determine script type
            if script_path.is_file() and os.access(script_path, os.X_OK):
                script_type = 'executable'
            elif script_path.suffix.lower() in ['.py', '.sh', '.js']:
                script_type = 'script'
            elif script_path.suffix.lower() == '.md':
                script_type = 'documentation'
            else:
                script_type = 'other'
            
            # Get category and language
            category = categorize_script(script_path)
            language = detect_language(script_path)
            
            # Extract description from first line/comment
            description = None
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[:5]  # Check first 5 lines
                    for line in lines:
                        line = line.strip()
                        # Look for description patterns
                        if line.startswith('"""') or line.startswith("'''"):
                            # Python docstring
                            desc_line = line[3:].strip()
                            if desc_line:
                                description = desc_line
                                break
                        elif line.startswith('# ') and not line.startswith('#!/'):
                            # Comment description
                            description = line[2:].strip()
                            break
                        elif line.startswith('//'):
                            # JS comment
                            description = line[2:].strip()
                            break
            except:
                pass
            
            # Insert or update script record
            cursor.execute("""
                INSERT OR REPLACE INTO scripts 
                (id, script_path, script_name, script_type, language, size_bytes, 
                 permissions, last_modified, category, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                script_id,
                str(script_path),
                script_path.name,
                script_type,
                language,
                size_bytes,
                permissions,
                last_modified,
                category,
                description
            ))
            
            discovered += 1
    
    return discovered

def log_script_execution(script_path, exit_code=0, runtime_seconds=None, arguments=None):
    """Log a script execution (to be called by wrapper scripts)"""
    if not DB_PATH.exists():
        print(f"Script usage database not found at {DB_PATH}")
        return
    
    script_id = hashlib.md5(str(script_path).encode()).hexdigest()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if script exists in registry
    cursor.execute("SELECT id FROM scripts WHERE id = ?", (script_id,))
    if not cursor.fetchone():
        print(f"Script {script_path} not found in registry. Run discovery first.")
        return
    
    # Log the execution
    cursor.execute("""
        INSERT INTO script_usage 
        (script_id, exit_code, runtime_seconds, arguments, working_directory, user)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        script_id,
        exit_code,
        runtime_seconds,
        arguments,
        os.getcwd(),
        os.getenv('USER', 'unknown')
    ))
    
    conn.commit()
    conn.close()

def get_statistics(conn):
    """Get script usage statistics"""
    cursor = conn.cursor()
    
    stats = {}
    
    # Total scripts
    cursor.execute("SELECT COUNT(*) FROM scripts")
    stats['total_scripts'] = cursor.fetchone()[0]
    
    # Used vs unused
    cursor.execute("SELECT COUNT(DISTINCT script_id) FROM script_usage WHERE script_id IS NOT NULL")
    stats['used_scripts'] = cursor.fetchone()[0]
    stats['unused_scripts'] = stats['total_scripts'] - stats['used_scripts']
    
    # By category
    cursor.execute("""
        SELECT category, COUNT(*) as count
        FROM scripts 
        GROUP BY category 
        ORDER BY count DESC
    """)
    stats['by_category'] = cursor.fetchall()
    
    # By language
    cursor.execute("""
        SELECT language, COUNT(*) as count
        FROM scripts 
        GROUP BY language 
        ORDER BY count DESC
    """)
    stats['by_language'] = cursor.fetchall()
    
    # Most used scripts
    cursor.execute("""
        SELECT script_name, total_executions, success_rate, last_used
        FROM script_analytics 
        WHERE total_executions > 0
        ORDER BY total_executions DESC 
        LIMIT 10
    """)
    stats['most_used'] = cursor.fetchall()
    
    # Largest unused scripts
    cursor.execute("""
        SELECT script_name, script_path, size_bytes, days_discovered
        FROM unused_scripts 
        ORDER BY size_bytes DESC 
        LIMIT 10
    """)
    stats['largest_unused'] = cursor.fetchall()
    
    # Recent executions
    cursor.execute("""
        SELECT s.script_name, u.execution_time, u.exit_code
        FROM script_usage u
        JOIN scripts s ON u.script_id = s.id
        ORDER BY u.execution_time DESC
        LIMIT 10
    """)
    stats['recent_executions'] = cursor.fetchall()
    
    return stats

def main():
    """Main script discovery function"""
    print("=== Claude Script Usage Tracking System ===")
    print(f"Brain Config: {BRAIN_CONFIG_DIR}")
    print(f"Database: {DB_PATH}")
    
    if not BRAIN_CONFIG_DIR.exists():
        print("❌ Brain config directory not found")
        return 1
    
    # Create database
    print("\nCreating database...")
    conn = create_database()
    
    try:
        # Discover scripts
        print("\nDiscovering scripts...")
        cursor = conn.cursor()
        discovered = discover_scripts(cursor)
        conn.commit()
        
        print(f"✅ Discovered {discovered} scripts")
        
        # Show statistics
        print("\n📊 Script Registry Statistics:")
        stats = get_statistics(conn)
        
        print(f"  Total scripts: {stats['total_scripts']:,}")
        print(f"  Used scripts: {stats['used_scripts']}")
        print(f"  Unused scripts: {stats['unused_scripts']}")
        
        if stats['by_category']:
            print(f"\n  By category:")
            for category, count in stats['by_category']:
                print(f"    - {category}: {count}")
        
        if stats['by_language']:
            print(f"\n  By language:")
            for language, count in stats['by_language']:
                print(f"    - {language}: {count}")
        
        if stats['largest_unused']:
            print(f"\n  Largest unused scripts:")
            for name, path, size, days in stats['largest_unused'][:5]:
                size_kb = size / 1024
                print(f"    - {name}: {size_kb:.1f}KB ({days:.0f} days discovered)")
        
        print(f"\n✅ Database created at: {DB_PATH}")
        print("\n💡 Next steps:")
        print("  1. Add script execution logging to your most-used scripts")
        print("  2. Use claude-script-stats to analyze usage patterns")
        print("  3. Consider removing large unused scripts")
        print("  4. Track automation effectiveness over time")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Script discovery failed: {e}")
        return 1
    finally:
        conn.close()

if __name__ == "__main__":
    exit(main())