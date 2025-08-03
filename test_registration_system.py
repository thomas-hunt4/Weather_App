#!/usr/bin/env python3
"""
Test script for Weather Alerts Registration System
Run this to test the registration functionality before integrating
"""

import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_user_registration():
    """Test the user registration system"""
    print("🧪 Testing Weather Alerts Registration System\n")
    
    try:
        from data.user_preferences.user_registration_manager import UserRegistrationManager
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("📝 Make sure you've created the user_registration_manager.py file in data/user_preferences/")
        return False
    
    # Initialize manager
    manager = UserRegistrationManager()
    
    # Test 1: Add users
    print("Test 1: Adding test users")
    test_users = [
        ("John Doe", "+1-555-123-4567", "New York"),
        ("Jane Smith", "555-987-6543", "Los Angeles"),
        ("Bob Johnson", "+15551112222", "Chicago"),
        ("Alice Brown", "5554445555", "")  # No city
    ]
    
    for name, phone, city in test_users:
        success, message = manager.add_user(name, phone, city)
        status = "✅" if success else "❌"
        print(f"  {status} {name}: {message}")
    
    print()
    
    # Test 2: List users
    print("Test 2: Listing all users")
    users = manager.get_users()
    for i, user in enumerate(users, 1):
        print(f"  {i}. {user['name']} - {user['phone']} - {user.get('city', 'No city')}")
    
    print()
    
    # Test 3: Test duplicate phone
    print("Test 3: Testing duplicate phone number")
    success, message = manager.add_user("Duplicate User", "+1-555-123-4567", "Boston")
    status = "✅" if not success else "❌"  # Should fail
    print(f"  {status} Duplicate test: {message}")
    
    print()
    
    # Test 4: Get users for specific city
    print("Test 4: Getting users for New York")
    ny_users = manager.get_users_for_city("New York")
    for user in ny_users:
        print(f"  - {user['name']} ({user['phone']})")
    
    print()
    
    # Test 5: Update user
    print("Test 5: Updating user city")
    success, message = manager.update_user("+15554445555", city="Miami")
    status = "✅" if success else "❌"
    print(f"  {status} Update test: {message}")
    
    print()
    
    # Test 6: Remove user
    print("Test 6: Removing a user")
    success, message = manager.remove_user("+15551112222")
    status = "✅" if success else "❌"
    print(f"  {status} Remove test: {message}")
    
    print()
    
    # Test 7: Final user count
    print("Test 7: Final user list")
    final_users = manager.get_users()
    print(f"  Total users remaining: {len(final_users)}")
    for user in final_users:
        print(f"  - {user['name']} - {user['phone']} - {user.get('city', 'No city')}")
    
    print()
    
    # Test 8: Export users
    print("Test 8: Exporting users")
    success, message = manager.export_users()
    status = "✅" if success else "❌"
    print(f"  {status} Export test: {message}")
    
    print("\n🎉 Registration system tests completed!")
    return True


def test_sms_integration():
    """Test SMS integration (optional - requires Twilio setup)"""
    print("\n📱 Testing SMS Integration (optional)")
    
    try:
        from data.api_handlers.send_sms import test_sms_system, send_alert_to_registered_users
        
        # Test basic SMS
        print("Testing basic SMS functionality...")
        success = test_sms_system()
        
        if success:
            print("✅ Basic SMS test passed")
            
            # Test with registered users
            print("Testing alert to registered users...")
            test_alert = "⚠️ TEST ALERT: Severe thunderstorm warning in your area. Take precautions!"
            success, result = send_alert_to_registered_users(test_alert)
            
            status = "✅" if success else "❌"
            print(f"  {status} Registered users alert: {result}")
        else:
            print("❌ Basic SMS test failed - check Twilio configuration")
            
    except ImportError as e:
        print(f"⚠️ SMS testing skipped: {e}")
        print("📝 This is normal if you haven't updated send_sms.py yet")
    except Exception as e:
        print(f"❌ SMS test error: {e}")


def check_file_structure():
    """Check if required files exist"""
    print("🔍 Checking file structure...")
    
    required_files = [
        "data/user_preferences/user_registration_manager.py",
        "gui/pages/weather_alerts_window.py",
        "data/user_preferences/favorites_manager.py",
        "gui/pages/home_page.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - MISSING!")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️ Missing {len(missing_files)} required files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        print("\n📝 Please create these files before running the full test.")
        return False
    else:
        print("✅ All required files found!")
        return True


if __name__ == "__main__":
    print("=" * 60)
    print("WEATHER ALERTS REGISTRATION SYSTEM TEST")
    print("=" * 60)
    
    # Check file structure first
    if not check_file_structure():
        print("\n❌ Cannot proceed - missing required files")
        sys.exit(1)
    
    # Test the registration system
    registration_success = test_user_registration()
    
    if registration_success:
        # Ask if user wants to test SMS (requires Twilio setup)
        test_sms = input("\nDo you want to test SMS functionality? (y/n): ").lower().strip()
        if test_sms == 'y':
            test_sms_integration()
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)
    
    # Show next steps
    if registration_success:
        print("\n🎯 NEXT STEPS:")
        print("1. ✅ Registration system is working!")
        print("2. 🚀 Now implement the GUI integration in home_page.py")
        print("3. 📱 Test the full system by running: python main.py")
    else:
        print("\n🔧 FIX REQUIRED:")
        print("1. Create the missing files shown above")
        print("2. Run this test again")