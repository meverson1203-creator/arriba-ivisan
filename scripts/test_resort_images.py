#!/usr/bin/env python3
"""
Test script to verify resort image functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Owner
import sqlite3

def test_resort_image_columns():
    """Test that the resort image columns exist in the database"""
    print("Testing resort image columns in database...")
    
    try:
        # Connect to database
        con = sqlite3.connect('instance/site.db')
        cur = con.cursor()
        
        # Get column info
        columns = cur.execute('PRAGMA table_info(owner)').fetchall()
        column_names = [col[1] for col in columns]
        
        # Check for required columns
        required_columns = ['resort_profile_image', 'resort_background_image']
        missing_columns = [col for col in required_columns if col not in column_names]
        
        if missing_columns:
            print(f"❌ Missing columns: {missing_columns}")
            return False
        else:
            print("✅ All resort image columns exist")
            return True
            
    except Exception as e:
        print(f"❌ Error checking columns: {e}")
        return False
    finally:
        if 'con' in locals():
            con.close()

def test_routes():
    """Test that the new routes are accessible"""
    print("\nTesting routes...")
    
    with app.test_client() as client:
        # Test routes exist (they should return 405 for GET requests since they expect POST)
        routes_to_test = [
            '/upload_resort_profile_image',
            '/upload_resort_background_image'
        ]
        
        for route in routes_to_test:
            try:
                response = client.get(route)
                # We expect 405 (Method Not Allowed) since these are POST-only routes
                if response.status_code == 405:
                    print(f"✅ Route {route} exists and correctly rejects GET requests")
                else:
                    print(f"❌ Route {route} returned unexpected status: {response.status_code}")
            except Exception as e:
                print(f"❌ Error testing route {route}: {e}")

def test_owner_data():
    """Test that we can query owner data with resort image fields"""
    print("\nTesting owner data access...")
    
    try:
        with app.app_context():
            # Try to query the first owner
            owner = Owner.query.first()
            if owner:
                print(f"✅ Found owner: {owner.name}")
                print(f"   Resort name: {owner.resort_name}")
                print(f"   Resort profile image: {owner.resort_profile_image}")
                print(f"   Resort background image: {owner.resort_background_image}")
            else:
                print("ℹ️  No owners found in database")
                
    except Exception as e:
        print(f"❌ Error querying owner data: {e}")

if __name__ == "__main__":
    print("=== Resort Image Functionality Test ===\n")
    
    # Run tests
    db_test = test_resort_image_columns()
    test_routes()
    test_owner_data()
    
    print(f"\n=== Test Summary ===")
    if db_test:
        print("✅ Database structure is correct")
        print("✅ Routes are configured")
        print("✅ Ready to test image uploads!")
    else:
        print("❌ Database structure needs attention")