#!/usr/bin/env python3
"""
Database Compatibility Layer
Provides seamless transition between JSON files and SQLite databases
Automatically falls back to files if database is not available
"""

import json
import sqlite3
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import glob

class DatabaseCompatibilityLayer:
    """Compatibility layer for gradual migration from files to databases"""
    
    def __init__(self, config_dir: str = "/Users/shaansisodia/DEV/claude-brain-config"):
        self.config_dir = Path(config_dir)
        self.databases_dir = self.config_dir / "databases"
        self.databases = {}
        self._init_connections()
    
    def _init_connections(self):
        """Initialize database connections if databases exist"""
        db_configs = {
            'tasks': {
                'path': self.databases_dir / 'tasks.db',
                'fallback': self.config_dir / 'todos'
            },
            'analytics': {
                'path': self.databases_dir / 'analytics.db',
                'fallback': self.config_dir / 'analytics'
            },
            'sessions': {
                'path': self.databases_dir / 'sessions.db',
                'fallback': self.config_dir / 'statsig'
            }
        }
        
        for db_name, config in db_configs.items():
            if config['path'].exists():
                try:
                    self.databases[db_name] = {
                        'conn': sqlite3.connect(config['path'], check_same_thread=False),
                        'path': config['path'],
                        'fallback': config['fallback']
                    }
                    # Enable JSON support
                    self.databases[db_name]['conn'].row_factory = sqlite3.Row
                except Exception as e:
                    print(f"Warning: Could not connect to {db_name} database: {e}")
                    self.databases[db_name] = {'fallback': config['fallback']}
            else:
                self.databases[db_name] = {'fallback': config['fallback']}
    
    # ========== TASKS/TODOS OPERATIONS ==========
    
    def get_all_tasks(self) -> List[Dict]:
        """Get all tasks from database or JSON files"""
        if 'conn' in self.databases.get('tasks', {}):
            # Use database
            cursor = self.databases['tasks']['conn'].cursor()
            cursor.execute("SELECT * FROM tasks")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        else:
            # Fallback to JSON files
            tasks = []
            todos_dir = self.databases['tasks']['fallback']
            if todos_dir.exists():
                for json_file in todos_dir.glob("*.json"):
                    try:
                        with open(json_file, 'r') as f:
                            data = json.load(f)
                            
                            # Handle different JSON structures
                            if isinstance(data, list):
                                # If it's an array, treat each item as a task
                                for item in data:
                                    if isinstance(item, dict):
                                        if 'id' not in item:
                                            item['id'] = f"{json_file.stem}_{data.index(item)}"
                                        tasks.append(item)
                            elif isinstance(data, dict):
                                # Normal dict structure
                                if 'id' not in data:
                                    data['id'] = json_file.stem
                                tasks.append(data)
                    except Exception as e:
                        print(f"Error reading {json_file}: {e}")
            return tasks
    
    def get_task(self, task_id: str) -> Optional[Dict]:
        """Get a specific task by ID"""
        if 'conn' in self.databases.get('tasks', {}):
            cursor = self.databases['tasks']['conn'].cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        else:
            # Try to find JSON file
            todos_dir = self.databases['tasks']['fallback']
            # Try different filename patterns
            patterns = [
                f"{task_id}.json",
                f"{task_id}-*.json",
                f"*{task_id}*.json"
            ]
            for pattern in patterns:
                matches = list(todos_dir.glob(pattern))
                if matches:
                    try:
                        with open(matches[0], 'r') as f:
                            return json.load(f)
                    except Exception as e:
                        print(f"Error reading task file: {e}")
            return None
    
    def save_task(self, task: Dict) -> bool:
        """Save or update a task (dual-write to both DB and JSON during transition)"""
        task_id = task.get('id')
        if not task_id:
            task_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            task['id'] = task_id
        
        success = True
        
        # Try database first
        if 'conn' in self.databases.get('tasks', {}):
            try:
                conn = self.databases['tasks']['conn']
                cursor = conn.cursor()
                
                # Check if exists
                cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
                exists = cursor.fetchone() is not None
                
                if exists:
                    # Update existing
                    cursor.execute("""
                        UPDATE tasks 
                        SET content = ?, status = ?, agent_id = ?, metadata = ?
                        WHERE id = ?
                    """, (
                        task.get('content', ''),
                        task.get('status', 'pending'),
                        task.get('agent_id'),
                        json.dumps({k: v for k, v in task.items() 
                                   if k not in ['id', 'content', 'status', 'agent_id']}),
                        task_id
                    ))
                else:
                    # Insert new
                    cursor.execute("""
                        INSERT INTO tasks (id, content, status, agent_id, metadata)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        task_id,
                        task.get('content', ''),
                        task.get('status', 'pending'),
                        task.get('agent_id'),
                        json.dumps({k: v for k, v in task.items() 
                                   if k not in ['id', 'content', 'status', 'agent_id']})
                    ))
                
                conn.commit()
            except Exception as e:
                print(f"Error saving to database: {e}")
                success = False
        
        # Also write to JSON for compatibility (dual-write period)
        todos_dir = self.databases['tasks']['fallback']
        if todos_dir.exists():
            try:
                filename = f"{task_id}.json"
                if task.get('agent_id'):
                    filename = f"{task_id}-agent-{task['agent_id']}.json"
                
                with open(todos_dir / filename, 'w') as f:
                    json.dump(task, f, indent=2, default=str)
            except Exception as e:
                print(f"Error saving to JSON: {e}")
                success = False
        
        return success
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task from both database and files"""
        success = True
        
        # Delete from database
        if 'conn' in self.databases.get('tasks', {}):
            try:
                cursor = self.databases['tasks']['conn'].cursor()
                cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
                self.databases['tasks']['conn'].commit()
            except Exception as e:
                print(f"Error deleting from database: {e}")
                success = False
        
        # Delete JSON files
        todos_dir = self.databases['tasks']['fallback']
        if todos_dir.exists():
            for json_file in todos_dir.glob(f"*{task_id}*.json"):
                try:
                    json_file.unlink()
                except Exception as e:
                    print(f"Error deleting file {json_file}: {e}")
                    success = False
        
        return success
    
    # ========== ANALYTICS OPERATIONS ==========
    
    def log_analytics(self, event_type: str, data: Dict) -> bool:
        """Log an analytics event"""
        if 'conn' in self.databases.get('analytics', {}):
            try:
                cursor = self.databases['analytics']['conn'].cursor()
                cursor.execute("""
                    INSERT INTO usage_patterns (pattern_type, pattern_data)
                    VALUES (?, ?)
                """, (event_type, json.dumps(data)))
                self.databases['analytics']['conn'].commit()
                return True
            except Exception as e:
                print(f"Error logging to analytics database: {e}")
        
        # Fallback to JSON file
        analytics_dir = self.databases['analytics']['fallback']
        if analytics_dir.exists():
            try:
                filename = analytics_dir / f"{event_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(filename, 'w') as f:
                    json.dump({'type': event_type, 'data': data, 'timestamp': datetime.now().isoformat()}, f)
                return True
            except Exception as e:
                print(f"Error logging to analytics file: {e}")
        
        return False
    
    def get_analytics(self, event_type: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """Get analytics events"""
        if 'conn' in self.databases.get('analytics', {}):
            cursor = self.databases['analytics']['conn'].cursor()
            if event_type:
                cursor.execute("""
                    SELECT * FROM usage_patterns 
                    WHERE pattern_type = ? 
                    ORDER BY timestamp DESC LIMIT ?
                """, (event_type, limit))
            else:
                cursor.execute("""
                    SELECT * FROM usage_patterns 
                    ORDER BY timestamp DESC LIMIT ?
                """, (limit,))
            return [dict(row) for row in cursor.fetchall()]
        else:
            # Fallback to reading JSON files
            events = []
            analytics_dir = self.databases['analytics']['fallback']
            if analytics_dir.exists():
                for json_file in sorted(analytics_dir.glob("*.json"), reverse=True)[:limit]:
                    try:
                        with open(json_file, 'r') as f:
                            event = json.load(f)
                            if not event_type or event.get('type') == event_type:
                                events.append(event)
                    except Exception as e:
                        print(f"Error reading {json_file}: {e}")
            return events
    
    # ========== SESSION OPERATIONS ==========
    
    def get_or_create_session(self, session_id: str) -> Dict:
        """Get or create a session"""
        if 'conn' in self.databases.get('sessions', {}):
            cursor = self.databases['sessions']['conn'].cursor()
            cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            else:
                # Create new session
                cursor.execute("""
                    INSERT INTO sessions (session_id, stable_id)
                    VALUES (?, ?)
                """, (session_id, session_id))
                self.databases['sessions']['conn'].commit()
                return {'session_id': session_id, 'stable_id': session_id}
        else:
            # Fallback to file
            session_file = self.databases['sessions']['fallback'] / f"statsig.session_id.{session_id}"
            if session_file.exists():
                with open(session_file, 'r') as f:
                    return {'session_id': session_id, 'data': f.read()}
            else:
                # Create new session file
                with open(session_file, 'w') as f:
                    f.write(session_id)
                return {'session_id': session_id}
    
    # ========== UTILITY METHODS ==========
    
    def close(self):
        """Close all database connections"""
        for db_name, db_info in self.databases.items():
            if 'conn' in db_info:
                try:
                    db_info['conn'].close()
                except:
                    pass
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def is_database_available(self, db_name: str) -> bool:
        """Check if a specific database is available"""
        return 'conn' in self.databases.get(db_name, {})
    
    def get_status(self) -> Dict[str, bool]:
        """Get status of all databases"""
        return {
            db_name: self.is_database_available(db_name)
            for db_name in ['tasks', 'analytics', 'sessions']
        }
    
    def export_database(self, db_name: str, output_dir: Path) -> int:
        """Export a database back to JSON files"""
        if not self.is_database_available(db_name):
            print(f"Database {db_name} not available")
            return 0
        
        output_dir.mkdir(parents=True, exist_ok=True)
        exported = 0
        
        if db_name == 'tasks':
            tasks = self.get_all_tasks()
            for task in tasks:
                filename = f"{task['id']}.json"
                with open(output_dir / filename, 'w') as f:
                    json.dump(task, f, indent=2, default=str)
                exported += 1
        
        # Add other database exports as needed
        
        return exported


# ========== CONVENIENCE FUNCTIONS ==========

_compat_layer = None

def get_compat_layer() -> DatabaseCompatibilityLayer:
    """Get or create the global compatibility layer instance"""
    global _compat_layer
    if _compat_layer is None:
        _compat_layer = DatabaseCompatibilityLayer()
    return _compat_layer

def save_task(task: Dict) -> bool:
    """Convenience function to save a task"""
    return get_compat_layer().save_task(task)

def get_task(task_id: str) -> Optional[Dict]:
    """Convenience function to get a task"""
    return get_compat_layer().get_task(task_id)

def get_all_tasks() -> List[Dict]:
    """Convenience function to get all tasks"""
    return get_compat_layer().get_all_tasks()

def log_analytics(event_type: str, data: Dict) -> bool:
    """Convenience function to log analytics"""
    return get_compat_layer().log_analytics(event_type, data)

def get_database_status() -> Dict[str, bool]:
    """Get status of all databases"""
    return get_compat_layer().get_status()


if __name__ == "__main__":
    # Test the compatibility layer
    print("Testing Database Compatibility Layer")
    print("=" * 50)
    
    with DatabaseCompatibilityLayer() as compat:
        # Check status
        status = compat.get_status()
        print("Database Status:")
        for db, available in status.items():
            print(f"  {db}: {'✅ Available' if available else '❌ Using files'}")
        
        print("\nTesting task operations...")
        
        # Test saving a task
        test_task = {
            'id': 'test_task_001',
            'content': 'Test task from compatibility layer',
            'status': 'pending',
            'agent_id': 'test_agent'
        }
        
        if compat.save_task(test_task):
            print("✅ Task saved successfully")
        
        # Test retrieving the task
        retrieved = compat.get_task('test_task_001')
        if retrieved:
            print(f"✅ Task retrieved: {retrieved.get('content')}")
        
        # Test getting all tasks
        all_tasks = compat.get_all_tasks()
        print(f"\n📊 Total tasks: {len(all_tasks)}")
        
        # Test analytics
        print("\nTesting analytics operations...")
        if compat.log_analytics('test_event', {'action': 'compatibility_test'}):
            print("✅ Analytics logged successfully")
        
        events = compat.get_analytics('test_event', limit=5)
        print(f"📊 Retrieved {len(events)} analytics events")
        
        print("\n✅ Compatibility layer test complete!")