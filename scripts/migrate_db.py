#!/usr/bin/env python3
"""
Database migration script for Mock Cloud API
Automatically runs Alembic migrations
"""

import os
import sys
import time
import subprocess
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_migrations():
    """Run database migrations using Alembic"""
    try:
        print("🔄 Running database migrations...")
        
        # Run alembic upgrade head
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        if result.returncode == 0:
            print("✅ Database migrations completed successfully")
            return True
        else:
            print(f"❌ Migration failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running migrations: {e}")
        return False

def wait_for_database():
    """Wait for database to be ready"""
    print("⏳ Waiting for database to be ready...")
    max_attempts = 30
    
    for attempt in range(max_attempts):
        try:
            # Try to import and test database connection
            from app.database import engine
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            print("✅ Database is ready!")
            return True
        except Exception:
            if attempt < max_attempts - 1:
                print(f"   Attempt {attempt + 1}/{max_attempts}...")
                time.sleep(2)
            else:
                print("❌ Database is not responding")
                return False
    
    return False

def main():
    """Main migration function"""
    print("🗄️  Database Migration Script")
    print("=" * 40)
    
    # Wait for database
    if not wait_for_database():
        sys.exit(1)
    
    # Run migrations
    if not run_migrations():
        sys.exit(1)
    
    print("🎉 Database setup complete!")

if __name__ == "__main__":
    main()
