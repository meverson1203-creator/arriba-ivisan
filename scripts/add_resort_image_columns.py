#!/usr/bin/env python3

"""
Add resort_profile_image and resort_background_image columns to Owner table if they don't exist.
"""

import sqlite3
import os
import sys

# Add parent directory to path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def add_resort_image_columns():
    # Get the database file path
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_FILE = os.path.join(BASE_DIR, 'instance', 'site.db')
    
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        
        # Check if columns exist
        cursor.execute("PRAGMA table_info(owner)")
        columns = [row[1] for row in cursor.fetchall()]
        
        # Add resort_profile_image column if it doesn't exist
        if 'resort_profile_image' not in columns:
            print("Adding resort_profile_image column...")
            cursor.execute("ALTER TABLE owner ADD COLUMN resort_profile_image VARCHAR(300)")
            print("✓ resort_profile_image column added")
        else:
            print("✓ resort_profile_image column already exists")
        
        # Add resort_background_image column if it doesn't exist
        if 'resort_background_image' not in columns:
            print("Adding resort_background_image column...")
            cursor.execute("ALTER TABLE owner ADD COLUMN resort_background_image VARCHAR(300)")
            print("✓ resort_background_image column added")
        else:
            print("✓ resort_background_image column already exists")
        
        conn.commit()
        print("Database migration completed successfully!")

if __name__ == "__main__":
    add_resort_image_columns()