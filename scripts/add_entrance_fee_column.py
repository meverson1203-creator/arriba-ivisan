"""
Migration script to add entrance_fee column to Owner table
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, Owner

def add_entrance_fee_column():
    with app.app_context():
        try:
            # Check if column already exists by trying to access it
            test_owner = Owner.query.first()
            if test_owner:
                _ = test_owner.entrance_fee
                print("✓ entrance_fee column already exists in Owner table")
                return
        except Exception:
            pass
        
        # Add the column using raw SQL
        with db.engine.connect() as conn:
            try:
                conn.execute(db.text("ALTER TABLE owner ADD COLUMN entrance_fee VARCHAR(200)"))
                conn.commit()
                print("✓ Successfully added entrance_fee column to Owner table")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("✓ entrance_fee column already exists")
                else:
                    print(f"✗ Error adding entrance_fee column: {e}")
                    raise

if __name__ == "__main__":
    add_entrance_fee_column()
