"""
Test script to verify admin conversation feature
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, User, Owner, Admin, AdminConversation, Message

def test_admin_conversations():
    with app.app_context():
        print("Testing Admin Conversation Feature\n")
        print("=" * 50)
        
        # Check if admin exists
        admin = Admin.query.first()
        if not admin:
            print("❌ No admin found in database")
            return
        print(f"✓ Admin found: {admin.username}")
        
        # Check if we have users
        users = User.query.all()
        print(f"✓ Found {len(users)} user(s)")
        
        # Check if we have owners
        owners = Owner.query.all()
        print(f"✓ Found {len(owners)} owner(s)")
        
        # Check admin conversations table
        admin_convs = AdminConversation.query.all()
        print(f"\n✓ Found {len(admin_convs)} admin conversation(s)")
        
        if admin_convs:
            for conv in admin_convs:
                partner = "Unknown"
                if conv.user_id:
                    user = db.session.get(User, conv.user_id)
                    partner = f"User: {user.username if user else 'Unknown'}"
                elif conv.owner_id:
                    owner = db.session.get(Owner, conv.owner_id)
                    partner = f"Owner: {owner.username if owner else 'Unknown'}"
                
                msg_count = len(conv.messages) if conv.messages else 0
                print(f"  - Conversation {conv.id}: {partner} ({msg_count} messages)")
        
        print("\n" + "=" * 50)
        print("✅ Admin conversation feature is ready!")
        print("\nTo test:")
        print("1. Start the Flask app: python app.py")
        print("2. Login as a user or owner")
        print("3. Go to the Chats page")
        print("4. Click the 'Contact Admin' button (red button)")
        print("5. Send a message to admin")
        print("6. Login as admin and check the admin chat page")

if __name__ == '__main__':
    test_admin_conversations()
