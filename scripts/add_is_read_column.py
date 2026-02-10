"""
Migration script to add is_read column to message table.
Run this script once to add the column to an existing database.
"""
import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set default database URI if not set
if not os.environ.get('DATABASE_URL'):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.environ['DATABASE_URL'] = f'sqlite:///{os.path.join(base_dir, "instance", "site.db")}'

from app import app, db
from sqlalchemy import text

def add_is_read_column():
    """Add is_read column to message table if it doesn't exist."""
    with app.app_context():
        # Check if column already exists
        try:
            result = db.session.execute(text("SELECT is_read FROM message LIMIT 1"))
            print("Column 'is_read' already exists in message table.")
            return
        except Exception as e:
            if 'no such column' in str(e).lower() or 'does not exist' in str(e).lower() or 'unknown column' in str(e).lower():
                print("Column 'is_read' does not exist. Adding it now...")
            else:
                print(f"Error checking column: {e}")
                # Try to add the column anyway
        
        # Add the column
        try:
            db.session.execute(text("ALTER TABLE message ADD COLUMN is_read BOOLEAN DEFAULT FALSE"))
            db.session.commit()
            print("Successfully added 'is_read' column to message table.")
            
            # Set all existing messages to read (since they're old messages)
            db.session.execute(text("UPDATE message SET is_read = TRUE WHERE is_read IS NULL"))
            db.session.commit()
            print("Set all existing messages as read.")
        except Exception as e:
            print(f"Error adding column: {e}")
            db.session.rollback()

if __name__ == '__main__':
    add_is_read_column()
