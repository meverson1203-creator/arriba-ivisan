"""
Test script to verify reservation expiration functionality
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Reservation, User, Owner
from datetime import datetime, timedelta

def test_expiration():
    with app.app_context():
        print("Testing Reservation Expiration Functionality")
        print("=" * 50)
        
        # Check pending reservations
        pending = Reservation.query.filter_by(status='pending').all()
        print(f"\nFound {len(pending)} pending reservations:")
        
        for r in pending:
            user = db.session.get(User, r.user_id)
            owner = db.session.get(Owner, r.owner_id)
            
            print(f"\n  Reservation #{r.id}")
            print(f"  - User: {user.username if user else 'Unknown'}")
            print(f"  - Owner: {owner.resort_name if owner else 'Unknown'}")
            print(f"  - Resource: {r.resource_type} #{r.resource_id}")
            print(f"  - Created: {r.created_at}")
            print(f"  - Expires: {r.expires_at}")
            
            if r.expires_at:
                time_left = r.expires_at - datetime.utcnow()
                if time_left.total_seconds() > 0:
                    hours = int(time_left.total_seconds() // 3600)
                    minutes = int((time_left.total_seconds() % 3600) // 60)
                    print(f"  - Time remaining: {hours}h {minutes}m")
                else:
                    print(f"  - Status: EXPIRED (should auto-update)")
        
        # Check expired reservations
        expired = Reservation.query.filter_by(status='expired').all()
        print(f"\n\nFound {len(expired)} expired reservations:")
        for r in expired:
            print(f"  - Reservation #{r.id} (expired at {r.expires_at})")
        
        # Check confirmed reservations (should have no expiration)
        confirmed = Reservation.query.filter_by(status='confirmed').all()
        print(f"\n\nFound {len(confirmed)} confirmed reservations:")
        for r in confirmed:
            print(f"  - Reservation #{r.id} - expires_at: {r.expires_at}")
        
        print("\n" + "=" * 50)
        print("Test completed successfully!")

if __name__ == '__main__':
    test_expiration()
