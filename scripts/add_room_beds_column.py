#!/usr/bin/env python3
"""
Add 'beds' column to Room table if it doesn't exist.
This is a lightweight SQLite migration to avoid dropping data.
Usage: python scripts/add_room_beds_column.py
"""
import os
import sys
import sqlite3

# Add parent directory to path to import app config (for DB path convention)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, 'instance', 'site.db')


def add_beds_column():
    if not os.path.exists(DB_FILE):
        print(f"Database not found at {DB_FILE}. Nothing to migrate.")
        return
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        # Inspect room table columns
        cur.execute("PRAGMA table_info(room)")
        columns = [row[1] for row in cur.fetchall()]
        if 'beds' in columns:
            print("✓ 'beds' column already exists on room table.")
            return
        print("Adding 'beds' column to room table...")
        cur.execute("ALTER TABLE room ADD COLUMN beds VARCHAR(20)")
        conn.commit()
        print("✓ 'beds' column added successfully.")


if __name__ == '__main__':
    add_beds_column()
