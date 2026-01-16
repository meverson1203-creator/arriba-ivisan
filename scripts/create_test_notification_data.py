"""
Script to create test notification data for testing the notification system.
This will create notifications for both users and owners.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, User, Owner, Notification, Reservation, Room, Cottage
from datetime import datetime

def create_test_notifications():
    with app.app_context():
        print("Creating test notifications...")
        
        # Get the first user and owner
        user = User.query.first()
        owner = Owner.query.first()
        
        if not user:
            print("No users found in database. Please create a user first.")
            return
        
        if not owner:
            print("No owners found in database. Please create an owner first.")
            return
        
        print(f"Found user: {user.name or user.username}")
        print(f"Found owner: {owner.name or owner.username}")
        
        # Delete existing test notifications to avoid duplicates
        Notification.query.filter_by(notification_type='reservation_confirmed').delete()
        Notification.query.filter_by(notification_type='offer_approved').delete()
        db.session.commit()
        
        # Create a reservation confirmed notification for the user
        reservation = Reservation.query.filter_by(user_id=user.id).first()
        
        if reservation:
            resource_name = ''
            if reservation.resource_type == 'room':
                room = db.session.get(Room, reservation.resource_id)
                resource_name = room.name if room else 'Room'
            else:
                cottage = db.session.get(Cottage, reservation.resource_id)
                resource_name = cottage.name if cottage else 'Cottage'
            
            resort_name = owner.resort_name if owner else 'Resort'
            
            notif1 = Notification(
                notification_type='reservation_confirmed',
                title='Reservation Confirmed',
                message=f'Your reservation for {resource_name} at {resort_name} has been confirmed!',
                related_user_id=user.id,
                related_reservation_id=reservation.id,
                is_read=False,
                created_at=datetime.utcnow()
            )
            db.session.add(notif1)
            print(f"✓ Created reservation confirmed notification for user {user.name or user.username}")
        else:
            print("⚠ No reservations found. Creating generic notification...")
            notif1 = Notification(
                notification_type='reservation_confirmed',
                title='Test Reservation Confirmed',
                message=f'Your test reservation has been confirmed!',
                related_user_id=user.id,
                is_read=False,
                created_at=datetime.utcnow()
            )
            db.session.add(notif1)
            print(f"✓ Created test notification for user {user.name or user.username}")
        
        # Create an offer approved notification for the owner
        room = Room.query.filter_by(owner_id=owner.id, status='approved').first()
        
        if room:
            notif2 = Notification(
                notification_type='offer_approved',
                title='Room Approved',
                message=f'Your room "{room.name}" has been approved and is now visible to customers!',
                related_owner_id=owner.id,
                is_read=False,
                created_at=datetime.utcnow()
            )
            db.session.add(notif2)
            print(f"✓ Created offer approved notification for owner {owner.name or owner.username}")
        else:
            print("⚠ No approved rooms found. Creating generic notification...")
            notif2 = Notification(
                notification_type='offer_approved',
                title='Test Offer Approved',
                message=f'Your test offer has been approved and is now visible to customers!',
                related_owner_id=owner.id,
                is_read=False,
                created_at=datetime.utcnow()
            )
            db.session.add(notif2)
            print(f"✓ Created test notification for owner {owner.name or owner.username}")
        
        # Create another notification for variety
        notif3 = Notification(
            notification_type='offer_approved',
            title='Cottage Approved',
            message=f'Your cottage "Beachside Cottage" has been approved!',
            related_owner_id=owner.id,
            is_read=False,
            created_at=datetime.utcnow()
        )
        db.session.add(notif3)
        print(f"✓ Created another notification for owner {owner.name or owner.username}")
        
        db.session.commit()
        
        print("\n✅ Test notifications created successfully!")
        print("\nTo test:")
        print("1. Login as a user to see reservation confirmed notifications")
        print("2. Login as an owner to see offer approved notifications")
        print("3. Click the bell icon in the navbar to view notifications")
        print("4. Click on a notification to mark it as read")

if __name__ == '__main__':
    create_test_notifications()
