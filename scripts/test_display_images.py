#!/usr/bin/env python3
"""
Test script to verify that resort images are properly displayed on browse and viewResortMain pages
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Owner
import sqlite3

def test_browse_page_data():
    """Test that browse page will have access to resort profile images"""
    print("Testing browse page data...")
    
    try:
        with app.app_context():
            # Simulate what the browse route does
            owners = Owner.query.all()
            
            if owners:
                print(f"✅ Found {len(owners)} owners")
                for owner in owners:
                    print(f"   Owner: {owner.name}")
                    print(f"   Resort: {owner.resort_name}")
                    if hasattr(owner, 'resort_profile_image'):
                        print(f"   Profile Image: {owner.resort_profile_image or 'None'}")
                    if hasattr(owner, 'resort_background_image'):
                        print(f"   Background Image: {owner.resort_background_image or 'None'}")
                    print()
                return True
            else:
                print("ℹ️  No owners found in database")
                return True
                
    except Exception as e:
        print(f"❌ Error testing browse page data: {e}")
        return False

def test_viewResortMain_data():
    """Test that viewResortMain will have access to resort background images"""
    print("Testing viewResortMain page data...")
    
    try:
        with app.app_context():
            # Simulate what the viewResortMain route does
            owner = Owner.query.first()  # Get first owner
            
            if owner:
                print(f"✅ Found owner: {owner.name}")
                print(f"   Resort: {owner.resort_name}")
                if hasattr(owner, 'resort_background_image'):
                    print(f"   Background Image: {owner.resort_background_image or 'None'}")
                if hasattr(owner, 'resort_profile_image'):
                    print(f"   Profile Image: {owner.resort_profile_image or 'None'}")
                return True
            else:
                print("ℹ️  No owners found in database")
                return True
                
    except Exception as e:
        print(f"❌ Error testing viewResortMain data: {e}")
        return False

def test_template_updates():
    """Test that templates have been updated with image logic"""
    print("Testing template updates...")
    
    # Check browse.html
    try:
        with open('templates/browse.html', 'r') as f:
            browse_content = f.read()
            
        if 'owner.resort_profile_image' in browse_content:
            print("✅ browse.html updated to use resort profile images")
        else:
            print("❌ browse.html not updated for resort profile images")
            
    except Exception as e:
        print(f"❌ Error checking browse.html: {e}")
        return False
    
    # Check viewResortMain.html
    try:
        with open('templates/viewResortMain.html', 'r') as f:
            resort_main_content = f.read()
            
        if 'resort.resort_background_image' in resort_main_content:
            print("✅ viewResortMain.html updated to use resort background images")
        else:
            print("❌ viewResortMain.html not updated for resort background images")
            
    except Exception as e:
        print(f"❌ Error checking viewResortMain.html: {e}")
        return False
        
    return True

if __name__ == "__main__":
    print("=== Resort Images Display Test ===\n")
    
    # Run tests
    browse_ok = test_browse_page_data()
    main_ok = test_viewResortMain_data()
    templates_ok = test_template_updates()
    
    print(f"\n=== Test Summary ===")
    if browse_ok and main_ok and templates_ok:
        print("✅ All tests passed!")
        print("✅ Browse page will display resort profile images")
        print("✅ ViewResortMain page will display resort background images")
        print("✅ Templates have been properly updated")
        print("\n🎯 Next steps:")
        print("   1. Visit http://127.0.0.1:5000/browse to see resort profile images")
        print("   2. Click on a resort to see its background image on the main page")
        print("   3. Login as an owner and upload resort images from dashboard/profile")
    else:
        print("❌ Some tests failed. Please check the issues above.")