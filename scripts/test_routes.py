#!/usr/bin/env python3
"""
Simple test to verify routes are loaded
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

def test_routes_exist():
    """Test that the new routes are registered with Flask"""
    print("Testing route registration...")
    
    # Get all registered routes
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(rule.rule)
    
    # Check for our new routes
    required_routes = [
        '/upload_resort_profile_image',
        '/upload_resort_background_image'
    ]
    
    missing_routes = []
    for route in required_routes:
        if route in routes:
            print(f"✅ Route {route} is registered")
        else:
            print(f"❌ Route {route} is NOT registered")
            missing_routes.append(route)
    
    if not missing_routes:
        print("✅ All resort image upload routes are properly registered!")
        return True
    else:
        print(f"❌ Missing routes: {missing_routes}")
        return False

def test_owner_model():
    """Test that Owner model has resort image fields"""
    print("\nTesting Owner model...")
    
    try:
        from app import Owner
        
        # Check if the model has the required attributes
        required_attrs = ['resort_profile_image', 'resort_background_image']
        missing_attrs = []
        
        for attr in required_attrs:
            if hasattr(Owner, attr):
                print(f"✅ Owner model has {attr} attribute")
            else:
                print(f"❌ Owner model missing {attr} attribute")
                missing_attrs.append(attr)
        
        return len(missing_attrs) == 0
        
    except Exception as e:
        print(f"❌ Error testing Owner model: {e}")
        return False

if __name__ == "__main__":
    print("=== Resort Image Upload Test ===\n")
    
    routes_ok = test_routes_exist()
    model_ok = test_owner_model()
    
    print(f"\n=== Test Summary ===")
    if routes_ok and model_ok:
        print("✅ All tests passed! Resort image upload functionality is ready.")
    else:
        print("❌ Some tests failed. Please check the issues above.")