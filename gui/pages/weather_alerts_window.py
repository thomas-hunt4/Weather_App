import customtkinter as ctk
import tkinter as tk
from data.user_preferences.user_registration_manager import UserRegistrationManager


class WeatherAlertsWindow(ctk.CTkToplevel):
    """Weather Alerts Registration Window for SMS notifications"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Weather Alerts Registration")
        self.geometry("500x600")
        self.attributes("-topmost", True)
        self.resizable(False, False)
        
        # Initialize user manager
        self.user_manager = UserRegistrationManager()
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Create main components
        self._create_header()
        self._create_main_content()
        self._create_buttons()
        
        # Load existing users
        self._refresh_user_list()
    
    def _create_header(self):
        """Create header with title and description"""
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame, 
            text="⚠️ Weather Alerts Registration",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(10, 5))
        
        # Description
        desc_label = ctk.CTkLabel(
            header_frame,
            text="Register to receive SMS alerts for severe weather conditions",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        desc_label.grid(row=1, column=0, pady=(0, 10))
    
    def _create_main_content(self):
        """Create main content area with tabs"""
        # Create tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        # Add tabs
        self.register_tab = self.tabview.add("Register")
        self.manage_tab = self.tabview.add("Manage Users")
        
        # Configure tab grids
        self.register_tab.grid_columnconfigure(1, weight=1)
        self.manage_tab.grid_columnconfigure(0, weight=1)
        self.manage_tab.grid_rowconfigure(1, weight=1)
        
        self._create_register_tab()
        self._create_manage_tab()
    
    def _create_register_tab(self):
        """Create registration form"""
        # Registration form
        form_frame = ctk.CTkFrame(self.register_tab)
        form_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Form title
        form_title = ctk.CTkLabel(
            form_frame,
            text="📝 Register for Alerts",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        form_title.grid(row=0, column=0, columnspan=2, pady=(10, 20))
        
        # Name field
        name_label = ctk.CTkLabel(form_frame, text="Full Name:")
        name_label.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="w")
        
        self.name_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Enter your full name",
            width=300
        )
        self.name_entry.grid(row=1, column=1, padx=(5, 10), pady=5, sticky="ew")
        
        # Phone field
        phone_label = ctk.CTkLabel(form_frame, text="Phone Number:")
        phone_label.grid(row=2, column=0, padx=(10, 5), pady=5, sticky="w")
        
        self.phone_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="e.g., +1-555-123-4567",
            width=300
        )
        self.phone_entry.grid(row=2, column=1, padx=(5, 10), pady=5, sticky="ew")
        
        # City field (optional)
        city_label = ctk.CTkLabel(form_frame, text="City (Optional):")
        city_label.grid(row=3, column=0, padx=(10, 5), pady=5, sticky="w")
        
        self.city_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Your city for location-specific alerts",
            width=300
        )
        self.city_entry.grid(row=3, column=1, padx=(5, 10), pady=5, sticky="ew")
        
        # Register button
        register_btn = ctk.CTkButton(
            form_frame,
            text="📱 Register for Alerts",
            command=self._register_user,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        register_btn.grid(row=4, column=0, columnspan=2, pady=(20, 10), padx=10, sticky="ew")
        
        # Status message
        self.status_label = ctk.CTkLabel(
            form_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=5, column=0, columnspan=2, pady=(0, 10))
        
        # Info section
        info_frame = ctk.CTkFrame(self.register_tab)
        info_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
        
        info_title = ctk.CTkLabel(
            info_frame,
            text="ℹ️ Alert Information",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        info_title.grid(row=0, column=0, pady=(10, 5), padx=10)
        
        info_text = ctk.CTkLabel(
            info_frame,
            text="• You'll receive SMS alerts for severe weather conditions\n"
                 "• Alerts include: thunderstorms, heavy rain/snow, extreme conditions\n"
                 "• Your phone number is stored securely and never shared\n"
                 "• You can unregister anytime using the 'Manage Users' tab",
            font=ctk.CTkFont(size=11),
            justify="left"
        )
        info_text.grid(row=1, column=0, pady=(0, 10), padx=10, sticky="w")
    
    def _create_manage_tab(self):
        """Create user management interface"""
        # Users list
        list_frame = ctk.CTkFrame(self.manage_tab)
        list_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        list_frame.grid_columnconfigure(0, weight=1)
        
        list_title = ctk.CTkLabel(
            list_frame,
            text="👥 Registered Users",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        list_title.grid(row=0, column=0, pady=(10, 10))
        
        # Scrollable frame for users
        self.users_scroll = ctk.CTkScrollableFrame(self.manage_tab, height=300)
        self.users_scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.users_scroll.grid_columnconfigure(0, weight=1)
        
        # Management buttons
        mgmt_frame = ctk.CTkFrame(self.manage_tab)
        mgmt_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        mgmt_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        refresh_btn = ctk.CTkButton(
            mgmt_frame,
            text="🔄 Refresh",
            command=self._refresh_user_list,
            width=120
        )
        refresh_btn.grid(row=0, column=0, padx=5, pady=10)
        
        export_btn = ctk.CTkButton(
            mgmt_frame,
            text="💾 Export Users",
            command=self._export_users,
            width=120
        )
        export_btn.grid(row=0, column=1, padx=5, pady=10)
        
        test_btn = ctk.CTkButton(
            mgmt_frame,
            text="🧪 Test SMS",
            command=self._test_sms,
            width=120
        )
        test_btn.grid(row=0, column=2, padx=5, pady=10)
    
    def _create_buttons(self):
        """Create bottom buttons"""
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        button_frame.grid_columnconfigure(1, weight=1)
        
        close_btn = ctk.CTkButton(
            button_frame,
            text="Close",
            command=self.destroy,
            width=100
        )
        close_btn.grid(row=0, column=2, padx=10, pady=10)
    
    def _register_user(self):
        """Handle user registration"""
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        city = self.city_entry.get().strip()
        
        if not name or not phone:
            self._show_status("Please fill in name and phone number", "error")
            return
        
        success, message = self.user_manager.add_user(name, phone, city)
        
        if success:
            self._show_status(message, "success")
            # Clear form
            self.name_entry.delete(0, 'end')
            self.phone_entry.delete(0, 'end')
            self.city_entry.delete(0, 'end')
            # Refresh user list
            self._refresh_user_list()
        else:
            self._show_status(message, "error")
    
    def _refresh_user_list(self):
        """Refresh the user list display"""
        # Clear existing widgets
        for widget in self.users_scroll.winfo_children():
            widget.destroy()
        
        users = self.user_manager.get_users()
        
        if not users:
            no_users_label = ctk.CTkLabel(
                self.users_scroll,
                text="No users registered yet",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
            no_users_label.grid(row=0, column=0, pady=20)
            return
        
        # Display users
        for i, user in enumerate(users):
            user_frame = ctk.CTkFrame(self.users_scroll)
            user_frame.grid(row=i, column=0, sticky="ew", padx=5, pady=2)
            user_frame.grid_columnconfigure(1, weight=1)
            
            # User info
            name_text = f"👤 {user.get('name', 'N/A')}"
            phone_text = f"📱 {user.get('phone', 'N/A')}"
            city_text = f"📍 {user.get('city', 'No city specified')}"
            status_text = "✅ Active" if user.get('active', True) else "❌ Inactive"
            
            info_text = f"{name_text}\n{phone_text}\n{city_text}\n{status_text}"
            
            user_label = ctk.CTkLabel(
                user_frame,
                text=info_text,
                font=ctk.CTkFont(size=11),
                justify="left"
            )
            user_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
            
            # Remove button
            remove_btn = ctk.CTkButton(
                user_frame,
                text="Remove",
                command=lambda p=user.get('phone'): self._remove_user(p),
                width=80,
                height=30,
                fg_color="red",
                hover_color="darkred"
            )
            remove_btn.grid(row=0, column=1, padx=10, pady=5)
    
    def _remove_user(self, phone):
        """Remove a user"""
        success, message = self.user_manager.remove_user(phone)
        
        if success:
            self._show_status(message, "success")
            self._refresh_user_list()
        else:
            self._show_status(message, "error")
    
    def _export_users(self):
        """Export users to backup file"""
        success, message = self.user_manager.export_users()
        self._show_status(message, "success" if success else "error")
    
    def _test_sms(self):
        """Test SMS functionality with registered users"""
        users = self.user_manager.get_active_users()
        
        if not users:
            self._show_status("No registered users to test SMS", "error")
            return
        
        # Here you would integrate with your existing SMS system
        # For now, just show a confirmation
        test_message = f"Found {len(users)} registered user(s) for SMS testing."
        self._show_status(test_message, "success")
        
        # Optional: Actually send test SMS using your existing twilio_sms function
        # from data.api_handlers.send_sms import twilio_sms
        # for user in users:
        #     test_msg = f"Test weather alert for {user['name']} - system working correctly!"
        #     twilio_sms(test_msg)  # Note: this sends to hardcoded number in your current setup
    
    def _show_status(self, message, status_type="info"):
        """Display status message"""
        colors = {
            "success": "green",
            "error": "red",
            "info": "blue"
        }
        
        self.status_label.configure(
            text=message,
            text_color=colors.get(status_type, "blue")
        )
        
        # Clear message after 5 seconds
        self.after(5000, lambda: self.status_label.configure(text=""))