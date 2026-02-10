"""
Script to add admin_conversation table and update message table
for the admin chat feature.
"""
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from sqlalchemy import text

def add_admin_conversations():
    with app.app_context():
        conn = db.engine.connect()
        trans = conn.begin()
        
        try:
            # Check if admin_conversation table exists
            result = conn.execute(text(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='admin_conversation'"
            ))
            if not result.fetchone():
                print("Creating admin_conversation table...")
                conn.execute(text("""
                    CREATE TABLE admin_conversation (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        owner_id INTEGER,
                        admin_id INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(user_id) REFERENCES user(id),
                        FOREIGN KEY(owner_id) REFERENCES owner(id),
                        FOREIGN KEY(admin_id) REFERENCES admin(id)
                    )
                """))
                print("✓ admin_conversation table created")
            else:
                print("admin_conversation table already exists")
            
            # Check if message table has admin_conversation_id column
            result = conn.execute(text("PRAGMA table_info(message)"))
            columns = [row[1] for row in result.fetchall()]
            
            if 'admin_conversation_id' not in columns:
                print("Adding admin_conversation_id column to message table...")
                # SQLite doesn't support ALTER TABLE to add foreign keys directly
                # We need to recreate the table
                
                # 1. Create new table with updated schema
                conn.execute(text("""
                    CREATE TABLE message_new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        conversation_id INTEGER,
                        admin_conversation_id INTEGER,
                        sender VARCHAR(10) NOT NULL,
                        sender_user_id INTEGER,
                        sender_owner_id INTEGER,
                        sender_admin_id INTEGER,
                        text TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(conversation_id) REFERENCES conversation(id),
                        FOREIGN KEY(admin_conversation_id) REFERENCES admin_conversation(id),
                        FOREIGN KEY(sender_user_id) REFERENCES user(id),
                        FOREIGN KEY(sender_owner_id) REFERENCES owner(id),
                        FOREIGN KEY(sender_admin_id) REFERENCES admin(id)
                    )
                """))
                
                # 2. Copy data from old table to new
                conn.execute(text("""
                    INSERT INTO message_new (id, conversation_id, sender, sender_user_id, sender_owner_id, text, created_at)
                    SELECT id, conversation_id, sender, sender_user_id, sender_owner_id, text, created_at
                    FROM message
                """))
                
                # 3. Drop old table
                conn.execute(text("DROP TABLE message"))
                
                # 4. Rename new table
                conn.execute(text("ALTER TABLE message_new RENAME TO message"))
                
                print("✓ message table updated with admin_conversation_id and sender_admin_id columns")
            else:
                print("message table already has admin_conversation_id column")
            
            trans.commit()
            print("\n✅ Database migration completed successfully!")
            
        except Exception as e:
            trans.rollback()
            print(f"\n❌ Error during migration: {e}")
            raise
        finally:
            conn.close()

if __name__ == '__main__':
    print("Starting database migration for admin conversations...\n")
    add_admin_conversations()
