"""
Script to add Notification table to the database
"""
import sys
import os

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Notification

def add_notifications_table():
    """Add notifications table to database"""
    with app.app_context():
        # Create all tables (will only create missing ones)
        db.create_all()
        print("✓ Notifications table created successfully!")
        
        # Check if table exists and show count
        count = Notification.query.count()
        print(f"✓ Current notification count: {count}")

if __name__ == '__main__':
    add_notifications_table()
