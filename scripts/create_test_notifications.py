"""
Script to create comprehensive test data including users, owners, and reservations with notifications
"""
import sys
import os

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, User, Owner, Reservation, Room, Cottage, Notification
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta, date

def create_test_data():
    """Create comprehensive test data"""
    with app.app_context():
        print("Creating test data...\n")
        
        # Create test users
        test_users = [
            {
                'username': 'john_doe',
                'password': generate_password_hash('password'),
                'name': 'John Doe',
                'email': 'john@example.com',
                'contact_number': '09123456789',
                'address': 'Manila, Philippines'
            },
            {
                'username': 'jane_smith',
                'password': generate_password_hash('password'),
                'name': 'Jane Smith',
                'email': 'jane@example.com',
                'contact_number': '09987654321',
                'address': 'Quezon City, Philippines'
            },
            {
                'username': 'bob_wilson',
                'password': generate_password_hash('password'),
                'name': 'Bob Wilson',
                'email': 'bob@example.com',
                'contact_number': '09111222333',
                'address': 'Makati, Philippines'
            }
        ]
        
        created_users = []
        for user_data in test_users:
            # Check if user exists
            existing = User.query.filter_by(username=user_data['username']).first()
            if not existing:
                user = User(**user_data)
                db.session.add(user)
                db.session.flush()  # Get the ID
                created_users.append(user)
                
                # Create notification
                notif = Notification(
                    notification_type='new_user',
                    title='New User Registration',
                    message=f'New user {user.name} has registered.',
                    related_user_id=user.id,
                    created_at=datetime.now() - timedelta(days=len(created_users))
                )
                db.session.add(notif)
                print(f"✓ Created user: {user.name}")
            else:
                created_users.append(existing)
                print(f"  User already exists: {existing.name}")
        
        db.session.commit()
        
        # Get existing owner and their rooms/cottages
        owners = Owner.query.all()
        if not owners:
            print("⚠ No owners found in database. Please create an owner first.")
            return
        
        owner = owners[0]
        print(f"\n✓ Using owner: {owner.name or owner.username}")
        
        # Get available rooms and cottages
        rooms = Room.query.filter_by(owner_id=owner.id).all()
        cottages = Cottage.query.filter_by(owner_id=owner.id).all()
        
        if not rooms and not cottages:
            print("⚠ No rooms or cottages found for this owner. Please create some first.")
            return
        
        # Create test reservations
        print("\nCreating reservations...")
        today = date.today()
        
        reservation_templates = [
            {
                'check_in': today + timedelta(days=7),
                'check_out': today + timedelta(days=10),
                'guests': '2',
                'status': 'pending'
            },
            {
                'check_in': today + timedelta(days=14),
                'check_out': today + timedelta(days=17),
                'guests': '4',
                'status': 'pending'
            },
            {
                'check_in': today + timedelta(days=21),
                'check_out': today + timedelta(days=24),
                'guests': '3',
                'status': 'pending'
            }
        ]
        
        created_reservations = 0
        for i, template in enumerate(reservation_templates):
            if i < len(created_users):
                user = created_users[i]
                
                # Alternate between rooms and cottages
                if rooms and i % 2 == 0:
                    resource = rooms[0]
                    resource_type = 'room'
                elif cottages:
                    resource = cottages[0]
                    resource_type = 'cottage'
                elif rooms:
                    resource = rooms[0]
                    resource_type = 'room'
                else:
                    continue
                
                reservation = Reservation(
                    user_id=user.id,
                    owner_id=owner.id,
                    resource_type=resource_type,
                    resource_id=resource.id,
                    check_in=template['check_in'],
                    check_out=template['check_out'],
                    guests=template['guests'],
                    status=template['status'],
                    created_at=datetime.now() - timedelta(hours=i*2)
                )
                db.session.add(reservation)
                db.session.flush()
                
                # Create notification
                notif = Notification(
                    notification_type='new_reservation',
                    title='New Reservation Request',
                    message=f'{user.name} made a reservation for {resource.name} at {owner.resort_name or "resort"}.',
                    related_user_id=user.id,
                    related_owner_id=owner.id,
                    related_reservation_id=reservation.id,
                    created_at=reservation.created_at
                )
                db.session.add(notif)
                created_reservations += 1
                print(f"✓ Created reservation: {user.name} -> {resource.name}")
        
        db.session.commit()
        
        # Summary
        print("\n" + "="*50)
        print("TEST DATA CREATION SUMMARY")
        print("="*50)
        print(f"Users created: {len(created_users)}")
        print(f"Reservations created: {created_reservations}")
        print(f"Total notifications: {Notification.query.count()}")
        print(f"Unread notifications: {Notification.query.filter_by(is_read=False).count()}")
        print("\n✓ Test data creation complete!")
        print("\nYou can now login as admin (username: admin, password: password)")
        print("and view the notifications page to see the new notifications.")

if __name__ == '__main__':
    create_test_data()
