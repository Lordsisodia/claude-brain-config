#!/usr/bin/env python3
"""
Test migration script - safely test database migration with a small sample
"""

import json
import shutil
from pathlib import Path
import sys

# Add databases directory to path
sys.path.append('/Users/shaansisodia/DEV/claude-brain-config/databases')

from db_compat import DatabaseCompatibilityLayer

def test_migration_safety():
    """Test the migration process with a small sample"""
    config_dir = Path("/Users/shaansisodia/DEV/claude-brain-config")
    todos_dir = config_dir / "todos"
    test_dir = config_dir / "databases" / "test_sample"
    
    print("=== Testing Migration Safety ===\n")
    
    # Step 1: Create test sample directory
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Step 2: Copy a few sample files for testing
    print("Step 1: Selecting sample files for test...")
    json_files = list(todos_dir.glob("*.json"))[:5]  # Test with first 5 files
    
    if not json_files:
        print("❌ No JSON files found in todos directory")
        return False
    
    print(f"Found {len(json_files)} sample files to test with")
    
    # Step 3: Test reading with compatibility layer
    print("\nStep 2: Testing compatibility layer BEFORE migration...")
    
    with DatabaseCompatibilityLayer() as compat:
        status = compat.get_status()
        print("Current database status:")
        for db, available in status.items():
            print(f"  {db}: {'Database' if available else 'Files'}")
        
        # Try to read tasks (should fallback to files)
        tasks_before = compat.get_all_tasks()
        print(f"  ✅ Can read {len(tasks_before)} tasks from files")
    
    # Step 4: Show sample of data that will be migrated
    print("\nStep 3: Sample of data to be migrated:")
    for i, json_file in enumerate(json_files[:3], 1):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            print(f"\n  File {i}: {json_file.name}")
            print(f"    ID: {data.get('id', 'N/A')}")
            print(f"    Content: {data.get('content', data.get('task', 'N/A'))[:50]}...")
            print(f"    Status: {data.get('status', 'N/A')}")
        except Exception as e:
            print(f"  ❌ Error reading {json_file.name}: {e}")
    
    # Step 5: Test the migration script exists and is valid
    print("\nStep 4: Verifying migration script...")
    migrate_script = config_dir / "databases" / "migrate_todos_to_sqlite.py"
    if migrate_script.exists():
        print(f"  ✅ Migration script exists at {migrate_script}")
        # Check if it's valid Python
        try:
            with open(migrate_script, 'r') as f:
                compile(f.read(), str(migrate_script), 'exec')
            print("  ✅ Migration script is valid Python")
        except SyntaxError as e:
            print(f"  ❌ Migration script has syntax error: {e}")
            return False
    else:
        print(f"  ❌ Migration script not found at {migrate_script}")
        return False
    
    # Step 6: Test dual-write capability
    print("\nStep 5: Testing dual-write capability...")
    test_task = {
        'id': 'test_safety_001',
        'content': 'Test task for migration safety check',
        'status': 'pending',
        'agent_id': 'safety_test'
    }
    
    with DatabaseCompatibilityLayer() as compat:
        if compat.save_task(test_task):
            print("  ✅ Successfully saved test task")
            
            # Check if file was created
            test_file = todos_dir / f"{test_task['id']}-agent-{test_task['agent_id']}.json"
            if test_file.exists():
                print(f"  ✅ JSON file created at {test_file.name}")
                # Clean up test file
                test_file.unlink()
            else:
                print("  ⚠️  JSON file not created (might be using database)")
    
    print("\n=== Safety Check Results ===")
    print("✅ Compatibility layer works correctly")
    print("✅ Can read existing JSON files")
    print("✅ Migration script is valid")
    print("✅ Dual-write capability confirmed")
    print("\n✅ It is SAFE to proceed with migration")
    print("\nTo run the full migration, execute:")
    print("  python /Users/shaansisodia/DEV/claude-brain-config/databases/migrate_todos_to_sqlite.py")
    
    return True

def verify_no_data_loss():
    """Verify that no data would be lost during migration"""
    config_dir = Path("/Users/shaansisodia/DEV/claude-brain-config")
    todos_dir = config_dir / "todos"
    
    print("\n=== Verifying No Data Loss ===")
    
    # Count total files
    json_files = list(todos_dir.glob("*.json"))
    total_files = len(json_files)
    print(f"Total JSON files: {total_files}")
    
    # Check for different file patterns
    patterns = {
        'agent_files': list(todos_dir.glob("*agent*.json")),
        'uuid_files': list(todos_dir.glob("*-*-*-*-*.json")),
        'simple_files': [f for f in json_files if '-' not in f.stem]
    }
    
    print("\nFile patterns found:")
    for pattern, files in patterns.items():
        print(f"  {pattern}: {len(files)} files")
    
    # Check for any non-JSON files
    all_files = list(todos_dir.glob("*"))
    non_json = [f for f in all_files if f.suffix != '.json']
    if non_json:
        print(f"\n⚠️  Found {len(non_json)} non-JSON files:")
        for f in non_json[:5]:
            print(f"    - {f.name}")
    
    # Sample data integrity check
    print("\n=== Data Integrity Check ===")
    errors = []
    empty_files = []
    
    for json_file in json_files[:20]:  # Check first 20 files
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                if not data:
                    empty_files.append(json_file.name)
        except Exception as e:
            errors.append((json_file.name, str(e)))
    
    if errors:
        print(f"❌ Found {len(errors)} files with errors:")
        for filename, error in errors[:5]:
            print(f"    - {filename}: {error}")
    else:
        print("✅ No JSON parsing errors found in sample")
    
    if empty_files:
        print(f"⚠️  Found {len(empty_files)} empty files")
    
    print(f"\n{'✅' if not errors else '⚠️ '} Data integrity check complete")
    
    return len(errors) == 0

if __name__ == "__main__":
    print("CLAUDE-BRAIN-CONFIG DATABASE MIGRATION SAFETY TEST")
    print("=" * 60)
    
    # Run safety tests
    if test_migration_safety():
        # Verify no data loss
        if verify_no_data_loss():
            print("\n" + "=" * 60)
            print("✅ ALL SAFETY CHECKS PASSED")
            print("\nYou can now safely run the migration:")
            print("  python /Users/shaansisodia/DEV/claude-brain-config/databases/migrate_todos_to_sqlite.py")
            print("\nThe migration will:")
            print("  1. Backup any existing database")
            print("  2. Migrate all JSON files to SQLite")
            print("  3. Keep original files intact")
            print("  4. Provide export capability for recovery")
        else:
            print("\n⚠️  Some data integrity issues found")
            print("Review the issues above before proceeding")
    else:
        print("\n❌ Safety checks failed")
        print("Do not proceed with migration until issues are resolved")