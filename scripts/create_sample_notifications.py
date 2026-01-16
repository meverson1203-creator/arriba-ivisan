"""
Script to create sample notifications for testing
"""
import sys
import os

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Notification, User, Owner, Reservation
from datetime import datetime, timedelta

def create_sample_notifications():
    """Create sample notifications for testing"""
    with app.app_context():
        # Get some existing users, owners, and reservations
        users = User.query.all()
        owners = Owner.query.all()
        reservations = Reservation.query.all()
        
        print(f"Found {len(users)} users, {len(owners)} owners, {len(reservations)} reservations")
        
        # Create notifications for existing users
        for user in users[:3]:  # First 3 users
            notif = Notification(
                notification_type='new_user',
                title='New User Registration',
                message=f'New user {user.name or user.username} has registered.',
                related_user_id=user.id,
                created_at=datetime.utcnow() - timedelta(days=len(users) - users.index(user))
            )
            db.session.add(notif)
            print(f"✓ Created notification for user: {user.name or user.username}")
        
        # Create notifications for existing owners
        for owner in owners[:3]:  # First 3 owners
            notif = Notification(
                notification_type='new_owner',
                title='New Owner Registration',
                message=f'New resort owner {owner.name or owner.username} ({owner.resort_name or "Resort"}) has registered.',
                related_owner_id=owner.id,
                created_at=datetime.utcnow() - timedelta(days=len(owners) - owners.index(owner))
            )
            db.session.add(notif)
            print(f"✓ Created notification for owner: {owner.name or owner.username}")
        
        # Create notifications for existing reservations
        for reservation in reservations[:5]:  # First 5 reservations
            user = db.session.get(User, reservation.user_id)
            owner = db.session.get(Owner, reservation.owner_id)
            
            from app import Room, Cottage
            resource_name = ''
            if reservation.resource_type == 'room':
                room = db.session.get(Room, reservation.resource_id)
                resource_name = room.name if room else 'Room'
            else:
                cottage = db.session.get(Cottage, reservation.resource_id)
                resource_name = cottage.name if cottage else 'Cottage'
            
            notif = Notification(
                notification_type='new_reservation',
                title='New Reservation Request',
                message=f'{user.name or user.username} made a reservation for {resource_name} at {owner.resort_name or "resort"}.',
                related_user_id=user.id,
                related_owner_id=owner.id,
                related_reservation_id=reservation.id,
                created_at=reservation.created_at if reservation.created_at else datetime.utcnow()
            )
            db.session.add(notif)
            print(f"✓ Created notification for reservation: {resource_name}")
        
        db.session.commit()
        
        total = Notification.query.count()
        print(f"\n✓ Successfully created sample notifications!")
        print(f"✓ Total notifications in database: {total}")

if __name__ == '__main__':
    create_sample_notifications()
