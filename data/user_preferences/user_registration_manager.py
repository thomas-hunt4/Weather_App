import json
import os
from datetime import datetime


class UserRegistrationManager:
    """Manages user registration data for weather alerts SMS notifications"""
    
    def __init__(self, users_file="data/user_preferences/alert_users.json"):
        self.users_file = users_file
        os.makedirs(os.path.dirname(users_file), exist_ok=True)
        
        # Initialize file if it doesn't exist
        if not os.path.exists(users_file):
            with open(users_file, 'w') as f:
                json.dump([], f)
    
    def get_users(self):
        """Load all registered users"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading users: {e}")
            return []
    
    def add_user(self, name, phone, city=""):
        """Add a new user registration"""
        users = self.get_users()
        
        # Clean and format input
        name = name.strip().title()
        phone = self._format_phone(phone.strip())
        city = city.strip().title() if city else ""
        
        # Validate input
        if not name or not phone:
            return False, "Name and phone are required"
        
        if not self._validate_phone(phone):
            return False, "Invalid phone number format"
        
        # Check if phone already exists
        for user in users:
            if user.get('phone') == phone:
                return False, f"Phone number {phone} already registered"
        
        # Create new user entry
        new_user = {
            "name": name,
            "phone": phone,
            "city": city,
            "registered_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "active": True
        }
        
        users.append(new_user)
        
        try:
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=2)
            return True, f"User {name} registered successfully!"
        except Exception as e:
            return False, f"Error saving user: {e}"
    
    def remove_user(self, phone):
        """Remove user by phone number"""
        users = self.get_users()
        phone = self._format_phone(phone.strip())
        
        for i, user in enumerate(users):
            if user.get('phone') == phone:
                removed_user = users.pop(i)
                try:
                    with open(self.users_file, 'w') as f:
                        json.dump(users, f, indent=2)
                    return True, f"User {removed_user.get('name', 'Unknown')} removed"
                except Exception as e:
                    return False, f"Error removing user: {e}"
        
        return False, f"Phone number {phone} not found"
    
    def update_user(self, phone, **kwargs):
        """Update user information"""
        users = self.get_users()
        phone = self._format_phone(phone.strip())
        
        for user in users:
            if user.get('phone') == phone:
                # Update allowed fields
                for key, value in kwargs.items():
                    if key in ['name', 'city', 'active']:
                        if key == 'name':
                            user[key] = value.strip().title()
                        elif key == 'city':
                            user[key] = value.strip().title()
                        else:
                            user[key] = value
                
                try:
                    with open(self.users_file, 'w') as f:
                        json.dump(users, f, indent=2)
                    return True, f"User updated successfully"
                except Exception as e:
                    return False, f"Error updating user: {e}"
        
        return False, f"Phone number {phone} not found"
    
    def get_active_users(self):
        """Get list of active users for SMS notifications"""
        users = self.get_users()
        return [user for user in users if user.get('active', True)]
    
    def get_users_for_city(self, city):
        """Get users registered for alerts in a specific city"""
        users = self.get_active_users()
        city = city.strip().title()
        return [user for user in users if user.get('city', '').lower() == city.lower()]
    
    def _format_phone(self, phone):
        """Format phone number to consistent format"""
        # Remove all non-digit characters
        digits = ''.join(filter(str.isdigit, phone))
        
        # Add country code if missing (assume US)
        if len(digits) == 10:
            digits = '1' + digits
        
        # Format as +1XXXXXXXXXX
        if len(digits) == 11 and digits.startswith('1'):
            return f"+{digits}"
        
        return phone  # Return original if format unclear
    
    def _validate_phone(self, phone):
        """Basic phone number validation"""
        # Check if it matches +1XXXXXXXXXX format
        if phone.startswith('+1') and len(phone) == 12:
            return phone[2:].isdigit()
        return False
    
    def export_users(self, filepath=None):
        """Export users to a backup file"""
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"data/user_preferences/users_backup_{timestamp}.json"
        
        users = self.get_users()
        try:
            with open(filepath, 'w') as f:
                json.dump(users, f, indent=2)
            return True, f"Users exported to {filepath}"
        except Exception as e:
            return False, f"Error exporting users: {e}"