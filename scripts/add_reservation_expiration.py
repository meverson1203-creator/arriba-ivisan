"""
Migration script to add expires_at column to Reservation table
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from sqlalchemy import text
from datetime import datetime, timedelta

def add_expiration_column():
    with app.app_context():
        try:
            # Check if column already exists
            result = db.session.execute(text("PRAGMA table_info(reservation)"))
            columns = [row[1] for row in result]
            
            if 'expires_at' not in columns:
                print("Adding expires_at column to reservation table...")
                db.session.execute(text(
                    "ALTER TABLE reservation ADD COLUMN expires_at DATETIME"
                ))
                db.session.commit()
                print("✓ expires_at column added successfully")
                
                # Set expires_at for existing pending reservations (24 hours from creation)
                print("Updating existing pending reservations...")
                from app import Reservation
                pending_reservations = Reservation.query.filter_by(status='pending').all()
                for res in pending_reservations:
                    res.expires_at = res.created_at + timedelta(hours=24)
                db.session.commit()
                print(f"✓ Updated {len(pending_reservations)} pending reservations")
            else:
                print("expires_at column already exists")
                
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()

if __name__ == '__main__':
    add_expiration_column()
