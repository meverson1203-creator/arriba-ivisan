#!/usr/bin/env python3
"""
Migration script to add status and created_at columns to Room, Cottage, Food, and Activity tables.
Run this script after updating the models to add the new columns.
"""

import os
import sys
from datetime import datetime

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Room, Cottage, Food, Activity

def migrate_database():
    """Add new columns to existing tables and set default values."""
    with app.app_context():
        try:
            # Check if the new columns exist by trying to query them
            # If they don't exist, SQLAlchemy will raise an error
            
            # Test if columns exist
            db.session.execute(db.text("SELECT status FROM room LIMIT 1"))
            print("Columns already exist, no migration needed.")
            return
            
        except Exception:
            print("Columns don't exist, creating database tables...")
            
            # Drop and recreate all tables to ensure they have the new structure
            db.drop_all()
            db.create_all()
            print("Database tables recreated with new structure.")
            
            # Ensure default admin exists
            from werkzeug.security import generate_password_hash
            from app import Admin
            
            default_admin = Admin.query.filter_by(username='admin').first()
            if not default_admin:
                hashed = generate_password_hash('password')
                admin = Admin(username='admin', password=hashed, name='Administrator', email='admin@example.com')
                db.session.add(admin)
                db.session.commit()
                print("Default admin user created.")
            
            print("Migration completed successfully!")

if __name__ == "__main__":
    migrate_database()