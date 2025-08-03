import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk
import tkintermapview
import requests
import io
import random

# Link Data and Feature files for interactions
from data.api_handlers.open_weather_api import OpenWeatherAPI
from features.weather_extract import WeatherProcessor
from data.history_management.file_handler import save_weather
from features.language_select import set_language, get_language
from features.alerts import SMS_Alerts
from data.api_handlers.send_sms import twilio_sms
from .toplevel_window import ToplevelWindow
from data.user_preferences.favorites_manager import FavoritesManager
from .weather_alerts_window import WeatherAlertsWindow
from features.weather_quiz import WeatherQuiz


class HomePage(ctk.CTkFrame):
    """Landing/main page for app with buttons to navigate to other features. Base weather stats, map inserts"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # """ set dark/light mode theme """
        # self.theme_set = ctk.StringVar(value="dark")

        """ API/On load/Default weather display """
        self.weather_api = OpenWeatherAPI()
        self.current_weather = None
        # self.update_weather("New Haven")

        """ GUI elements to update with location selection """
        self.city_entry = None 
        self.toplevel_window = None

        self._configure_grid()        # grid of HomePage cluster of widgets

        """ build all home page widgets """
        self._build_header()          
        self._build_weather_frame()
        self._build_features_frame()
        self._build_map_frame()
        self._build_sun_frame()
        self._build_panic_button_frame()
        self._build_weather_control_frame()

        """ On-Load IP or Default Weather on build """
        self.load_default_weather()

    """ TODO remove processor after Trend, Forecast, History in place """
    def test_trend_processor(self):
        from features.trend_and_graph import TrendandGraphProcessor
        processor = TrendandGraphProcessor()
        processor.test_data_retrieval("Madrid")

    def _configure_grid(self):
        for row in range(6):
            self.grid_rowconfigure(row, weight=1)
        for column in range(7):
            self.grid_columnconfigure(column, weight=1)
        """ current grid page/grid dimensions
          0_1_2_  _3_   4_5_6_7_
        0___H__e__a__d__e__r____
        
        1_______   ___   _______
        2_Temp__   Nav   ___Map_
        3_______   ___   _______
        
        4_Sun___   Butt  _Cont__
        5_______   ____  _______
        """
    
    def toggle_theme(self):
        current_theme = ctk.get_appearance_mode()
        if current_theme == "Dark":
            ctk.set_appearance_mode("Light")
            self.theme_button.configure(text="Dark Mode")
        else:
            ctk.set_appearance_mode("Dark")
            self.theme_button.configure(text="Light Mode")

    # Top Menu and controls frame * pages
    def _build_header(self):
        header_frame = ctk.CTkFrame(self, height=40)
        header_frame.grid(row=0, column=0, columnspan=8, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)  # Left (Menu)
        header_frame.grid_columnconfigure(1, weight=0)  # Language dropdown
        header_frame.grid_columnconfigure(2, weight=0)  # Theme button

        # Menu dropdown - FIXED: removed duplicate
        self.menu_dropdown = ctk.CTkOptionMenu(
            header_frame, 
            values=["Manage Favorites", "Settings", "Help"],
            width=120,
            height=28,
            command=self._handle_menu_selection
        )
        self.menu_dropdown.set("Menu")
        self.menu_dropdown.grid(row=0, column=0, padx=10, sticky="w")

        """ language selection dropdown """
        self.language_var = tk.StringVar(value=get_language())
        language_menu = ctk.CTkOptionMenu(header_frame, values=["en", "es", "hi"],variable=self.language_var, command=self.on_language_change)
        language_menu.grid(row=0, column=1, padx=(10,5), sticky="e")

        self.theme_button = ctk.CTkButton(header_frame, text="Dark Mode", command=self.toggle_theme)
        self.theme_button.grid(row=0, column=2, padx=10, sticky="e")
        current_mode = ctk.get_appearance_mode()
        self.theme_button.configure(text="Dark Mode" if current_mode == "Light" else "Light Mode")
        self.controller.theme_buttons.append(self.theme_button)

    #  Parent Frame for Temp, Humidity, Wind, Precip, Description
    def _build_weather_frame(self):
        weather_frame = ctk.CTkFrame(self,corner_radius=15)
        weather_frame.grid(row=1, column=0, columnspan=3, rowspan=3, padx=20, pady=20, sticky="nsew")
        
        for row in range(5):
            weather_frame.grid_rowconfigure(row, weight=1)

        for column in range(2):
            weather_frame.grid_columnconfigure(column, weight=1)

        """ TODO Home for widget construction/placement and loaded with default values for formatting. For Feature values please see Class WeatherFrameConfig """ 

        # City Name Frame -> Child of weather_frame
        city_frame = ctk.CTkFrame(weather_frame)
        city_frame.grid(row=0, column=0, columnspan=2, pady=(10,5), sticky="nsew")
        city_frame.grid_columnconfigure(0, weight=1)
        self.city_label = ctk.CTkLabel(city_frame, text="City", font=ctk.CTkFont(size=16, weight="bold"))
        self.city_label.grid(row=0, column=0, padx=10, pady=5)

        # Temperature Frame -> Child of weather_frame
        temp_frame = ctk.CTkFrame(weather_frame)
        temp_frame.grid(row=1, column=0, columnspan=2, pady=(0,5), sticky="nsew")
        temp_frame.grid_columnconfigure(0, weight=1)
        self.temp_label = ctk.CTkLabel(temp_frame, text="Temperature:") #font? text=(sl.["Temp"])
        self.temp_label.grid(row=0, column=0, padx=10, pady=5)
        self.temp_value = ctk.CTkLabel(temp_frame, text="{weather['temperature']} ℃") #font?
        self.temp_value.grid(row=1, column=0, sticky="n")

        # Description Frame -> Child of weather_frame
        desc_frame = ctk.CTkFrame(weather_frame)
        desc_frame.grid(row=2, column=0, columnspan=2, pady=(0,10), sticky="nsew")
        desc_frame.grid_columnconfigure(0, weight=1)
        self.desc_label = ctk.CTkLabel(desc_frame, text="Condition Description") #font?
        self.desc_label.grid(row=0, column=0, padx=10, pady=5)
        self.desc_value = ctk.CTkLabel(desc_frame, text="Rainy") #font?
        self.desc_value.grid(row=1, column=0, sticky="n")

        # Wind Frame -> Child of weather_frame
        wind_frame = ctk.CTkFrame(weather_frame)
        wind_frame.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
        wind_frame.grid_columnconfigure(0, weight=1)
        self.wind_label = ctk.CTkLabel(wind_frame, text="Wind") #font?
        self.wind_label.grid(row=1, column=0, padx=10, pady=5)
        self.wind_value = ctk.CTkLabel(wind_frame, text="7 km/h") #font/direction symbols?
        self.wind_value.grid(row=1, column=0, sticky="n")

        # Humidity Frame -> Child of weather_frame
        humidity_frame = ctk.CTkFrame(weather_frame)
        humidity_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        humidity_frame.grid_columnconfigure(0, weight=1)
        self.humidity_label = ctk.CTkLabel(humidity_frame, text="Humidity") #font?
        self.humidity_label.grid(row=2, column=0, padx=10, pady=5)
        self.humidity_value = ctk.CTkLabel(humidity_frame, text="66%") #font/direction symbols?
        self.humidity_value.grid(row=1, column=0, sticky="n")
        
        # Precipitation Frame -> Child of weather_frame
        precip_frame = ctk.CTkFrame(weather_frame)
        precip_frame.grid(row=4, column=0, columnspan=2, pady=(10,20), sticky="nsew")
        precip_frame.grid_columnconfigure(0, weight=1)
        self.precip_label = ctk.CTkLabel(precip_frame, text="Chance of Precipitation:") #font?
        self.precip_label.grid(row=0, column=0, padx=10, pady=5)
        self.precip_value = ctk.CTkLabel(precip_frame, text="4%") #font/direction symbols?
        self.precip_value.grid(row=1, column=0, sticky="n")

    # Features Frame -> Search bar and buttons to activate Features
    def _build_features_frame(self):
        """Weather search, navigation, and control buttons"""
        features_frame = ctk.CTkFrame(self, corner_radius=15)
        features_frame.grid(row=1, column=3, columnspan=1, rowspan=3, padx=20, pady=20, sticky="nsew")
        
        for row in range(7):  # 7 rows for all buttons including test button
            features_frame.grid_rowconfigure(row, weight=1)
        features_frame.grid_columnconfigure(0, weight=1)

        # Favorites dropdown (clean, simple selector)
        self.favorites_manager = FavoritesManager()
        self.favorites_var = ctk.StringVar(value="Select Favorite")
        self.favorites_dropdown = ctk.CTkOptionMenu(
            features_frame,
            variable=self.favorites_var,
            values=["Select Favorite"] + self.favorites_manager.get_favorites(),
            command=self._on_favorite_selected,
            width=200
        )
        self.favorites_dropdown.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

        # City entry
        city_entry = ctk.CTkEntry(features_frame, placeholder_text="Select City", corner_radius=15)
        city_entry.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
        city_entry.bind("<Return>", lambda event: self.update_weather(city_entry.get()))

        # Import here to avoid circular imports
        from .forecast_page import ForecastPage
        from .trend_page import TrendPage
        from .historical_page import HistoricalPage

        # Nav to forecast page
        forecast_button = ctk.CTkButton(features_frame, text="Forecast", corner_radius=15, 
                                        command=lambda: self.controller.show_frame(ForecastPage))
        forecast_button.grid(row=2, column=0, padx=5, pady=10, sticky="ew")

        # Nav to Trend page
        trend_button = ctk.CTkButton(features_frame, text="Trending Temperature", corner_radius=15, 
                                     command=lambda: self.controller.show_frame(TrendPage))
        trend_button.grid(row=3, column=0, padx=5, pady=10, sticky="ew")

        # Nav to Historical page
        historical_button = ctk.CTkButton(features_frame, text="Historical Data", corner_radius=15, 
                                          command=lambda: self.controller.show_frame(HistoricalPage))
        historical_button.grid(row=4, column=0, padx=5, pady=10, sticky="ew")

        # Weather Alerts Registration Button
        weather_alerts_button = ctk.CTkButton(
            features_frame, 
            text="⚠️ Weather Alerts", 
            corner_radius=15,
            command=self._open_weather_alerts_window,
            fg_color="#ff6b6b",
            hover_color="#ff5252"
        )
        weather_alerts_button.grid(row=5, column=0, padx=5, pady=10, sticky="ew")

        # Test button (keep if you want it)
        test_button = ctk.CTkButton(features_frame, text="Test Trend Data", command=self.test_trend_processor)
        test_button.grid(row=6, column=0, padx=5, pady=10, sticky="ew")

        self.city_entry = city_entry

    def _build_map_frame(self):
        map_frame = ctk.CTkFrame(self, corner_radius=15)
        map_frame.grid(row=1, column=4, columnspan=4, rowspan=3, padx=20, pady=20, sticky="nsew")
        
        # Configure grid
        map_frame.grid_rowconfigure(1, weight=1)
        map_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        map_title = ctk.CTkLabel(map_frame, text="Location Map", font=ctk.CTkFont(size=14, weight="bold"))
        map_title.grid(row=0, column=0, pady=(10, 5))
        
        # Create the map widget - no default position, will be set by weather loading
        self.map_widget = tkintermapview.TkinterMapView(
            map_frame, 
            width=400, 
            height=300, 
            corner_radius=10
        )
        self.map_widget.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="nsew")

    def _build_sun_frame(self):
        sun_frame = ctk.CTkFrame(self, corner_radius=15)
        sun_frame.grid(row=4, column=0, columnspan=3, rowspan=2, padx=20, pady=20, sticky="nsew")

        # Configure grid for overlay layout
        sun_frame.grid_rowconfigure(0, weight=1)
        sun_frame.grid_columnconfigure(0, weight=1)

        # Background label for weather icon (will be set when weather loads)
        self.sun_background_label = ctk.CTkLabel(sun_frame, text="")
        self.sun_background_label.grid(row=0, column=0, sticky="nsew")

        # Content frame for text overlay (transparent background)
        content_frame = ctk.CTkFrame(sun_frame, fg_color="transparent")
        content_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Configure content frame grid
        content_frame.grid_rowconfigure(0, weight=0)  # Title
        content_frame.grid_rowconfigure(1, weight=1)  # Sunrise
        content_frame.grid_rowconfigure(2, weight=1)  # Sunset
        content_frame.grid_columnconfigure(0, weight=1)

        # Title with semi-transparent background
        sun_title = ctk.CTkLabel(
            content_frame, 
            text="Sun Times", 
            font=ctk.CTkFont(size=16, weight="bold"),
             fg_color=("white", "gray10"),
            corner_radius=8
        )
        sun_title.grid(row=0, column=0, pady=(5, 10), padx=20, sticky="ew")

        # Sunrise with semi-transparent background
        sunrise_frame = ctk.CTkFrame(content_frame, fg_color=("white", "gray10"), corner_radius=8)
        sunrise_frame.grid(row=1, column=0, pady=5, padx=20, sticky="ew")
        
        sunrise_label = ctk.CTkLabel(sunrise_frame, text="🌅 Sunrise", font=ctk.CTkFont(size=12, weight="bold"))
        sunrise_label.grid(row=0, column=0, pady=(5, 0), padx=10)
        
        self.sunrise_time = ctk.CTkLabel(sunrise_frame, text="--:--", font=ctk.CTkFont(size=16))
        self.sunrise_time.grid(row=1, column=0, pady=(0, 5), padx=10)

        # Sunset with semi-transparent background
        sunset_frame = ctk.CTkFrame(content_frame, fg_color=("white", "gray10"), corner_radius=8)
        sunset_frame.grid(row=2, column=0, pady=5, padx=20, sticky="ew")
        
        sunset_label = ctk.CTkLabel(sunset_frame, text="🌇 Sunset", font=ctk.CTkFont(size=12, weight="bold"))
        sunset_label.grid(row=0, column=0, pady=(5, 0), padx=10)
        
        self.sunset_time = ctk.CTkLabel(sunset_frame, text="--:--", font=ctk.CTkFont(size=16))
        self.sunset_time.grid(row=1, column=0, pady=(0, 5), padx=10)

    def _build_panic_button_frame(self):
        panic_frame = ctk.CTkFrame(self,corner_radius=15)
        panic_frame.grid(row=4, column=3, columnspan=1, rowspan=2, padx=20, pady=20, sticky="nsew")

        for row in range(2):
            panic_frame.grid_rowconfigure(row, weight=1)
       
    def _build_weather_control_frame(self):
        weather_control_frame = ctk.CTkFrame(self, corner_radius=15)
        weather_control_frame.grid(row=4, column=4, columnspan=4, rowspan=2, padx=20, pady=20, sticky="nsew")

        # Configure grid
        weather_control_frame.grid_rowconfigure(0, weight=0)  # Title
        weather_control_frame.grid_rowconfigure(1, weight=1)  # Question area
        weather_control_frame.grid_rowconfigure(2, weight=0)  # Buttons
        weather_control_frame.grid_rowconfigure(3, weight=0)  # Score
        weather_control_frame.grid_columnconfigure(0, weight=1)

        # Initialize quiz with error handling
        try:
            self.weather_quiz = WeatherQuiz()
            print("Weather quiz initialized successfully")
        except Exception as e:
            print(f"Error initializing weather quiz: {e}")
            self.weather_quiz = None

        # Title
        quiz_title = ctk.CTkLabel(weather_control_frame, text="🌤️ Weather Quiz", font=ctk.CTkFont(size=16, weight="bold"))
        quiz_title.grid(row=0, column=0, pady=(10, 5), sticky="ew")

        # Question display area
        question_frame = ctk.CTkFrame(weather_control_frame)
        question_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        question_frame.grid_rowconfigure(0, weight=0)  # Question text
        question_frame.grid_rowconfigure(1, weight=1)  # Answer buttons
        question_frame.grid_columnconfigure(0, weight=1)

        # Question text
        self.question_label = ctk.CTkLabel(
            question_frame, 
            text="Click 'New Question' to start the quiz!", 
            font=ctk.CTkFont(size=12),
            wraplength=350
        )
        self.question_label.grid(row=0, column=0, pady=(10, 5), padx=10, sticky="ew")

        # Answer buttons frame
        self.answers_frame = ctk.CTkFrame(question_frame, fg_color="transparent")
        self.answers_frame.grid(row=1, column=0, pady=(5, 10), padx=10, sticky="nsew")
        self.answers_frame.grid_columnconfigure(0, weight=1)

        # Control buttons
        button_frame = ctk.CTkFrame(weather_control_frame, fg_color="transparent")
        button_frame.grid(row=2, column=0, pady=5, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        self.new_question_btn = ctk.CTkButton(button_frame, text="New Question", command=self.load_new_question)
        self.new_question_btn.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="ew")

        self.reset_quiz_btn = ctk.CTkButton(button_frame, text="Reset Quiz", command=self.reset_quiz)
        self.reset_quiz_btn.grid(row=0, column=1, padx=(5, 10), pady=5, sticky="ew")

        # Score display
        self.score_label = ctk.CTkLabel(weather_control_frame, text="Score: 0/0 (0%)", font=ctk.CTkFont(size=12))
        self.score_label.grid(row=3, column=0, pady=(5, 10))

        # Store answer buttons for later reference
        self.answer_buttons = []

    # Weather Alerts methods
    def _open_weather_alerts_window(self):
        """Open the Weather Alerts registration window"""
        if hasattr(self, 'alerts_window') and self.alerts_window.winfo_exists():
            self.alerts_window.focus()
        else:
            self.alerts_window = WeatherAlertsWindow(self)
            self.alerts_window.focus()

    def _on_favorite_selected(self, selection):
        """Handle favorite city selection"""
        if selection != "Select Favorite":
            self.update_weather(selection)
            # Update the city entry to show selected favorite
            if hasattr(self, 'city_entry'):
                self.city_entry.delete(0, 'end')
                self.city_entry.insert(0, selection)

    def _send_alert_to_registered_users(self, alert):
        """Send weather alerts to all registered users"""
        try:
            from data.user_preferences.user_registration_manager import UserRegistrationManager
            user_manager = UserRegistrationManager()
            active_users = user_manager.get_active_users()
            
            if active_users:
                from data.api_handlers.send_sms import twilio_sms
                twilio_sms(alert)
                print(f"Weather alert sent to {len(active_users)} registered user(s)")
        except Exception as e:
            print(f"Error sending alerts to registered users: {e}")

    # Default weather loading
    def load_default_weather(self):
        """Load to populate display at start up by IP look up"""
        location, error = self.weather_api.get_location_by_ip()
        if location:
            print(f"{location} detected")
            self.update_weather(location)
        else:
            print(f"Could not detect {error}")
            self.update_weather("Lebrija")

    # Search Entry bar handling
    def search_weather(self):
        city = self.city_entry.get().strip()
        if city:
            self.update_weather(city)
            self.city_entry.delete(0, 'end')
    
    def top_level_weather_alert(self, alert):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self) # Creates window if its None or Destroyed
            self.toplevel_window.focus()

            self.toplevel_window.content_frame.grid_rowconfigure(0, weight=1)
            self.toplevel_window.content_frame.grid_columnconfigure(0, weight=1)

            textbox = ctk.CTkTextbox(self.toplevel_window.content_frame, width=450, height=200)
            textbox.grid(row=0, column=0, sticky="nsew")
            textbox.insert("0.0", alert)
            textbox.configure(state="disabled")
        else:
            self.toplevel_window.focus() # If window exist, focus it
            
    def update_weather(self, city):
        print(f"Updating weather for {city}")
        data, error = self.weather_api.fetch_open_weather(city, get_language())

        if error:
            print("Error:", error)
            return 
        processor = WeatherProcessor()
        weather = processor.extract_weather_info(data)
        if weather:
            self.current_weather = weather
            print(f"Language call from api {get_language()}")
            self.display_weather(weather)
            # save weather data to csv
            save_weather(weather)

            alertsms = SMS_Alerts()
            alert = alertsms.weather_alerts(data)
            if alert:
                # Send SMS to registered users instead of hardcoded number
                self._send_alert_to_registered_users(alert)
                self.top_level_weather_alert(alert)
        else:
            print("Failed to fetch weather data")

    def display_weather(self, weather):
        """change this name to better associate with it dependants"""
        if not weather:
            return

        # Update city name frame
        self.city_label.configure(text=f"{weather['city']}, {weather['country']}") 

        # Update temperature frame
        self.temp_value.configure(text=f"{weather['temperature']:.1f}°C")  

        #Update description frame
        self.desc_value.configure(text=weather['description'].title())  

        # Update humidity and wind frames
        self.humidity_value.configure(text=f"{weather['humidity']}%")
        self.wind_value.configure(text=f"{weather['wind_speed']} m/s") 

       # Update sunrise and sunset times
        self.sunrise_time.configure(text=weather['sunrise'])
        self.sunset_time.configure(text=weather['sunset'])

        # Update weather icon background
        self.update_sun_widget_background(weather.get('weather_icon', '01d'))

        self.update_weather_map()

    def update_weather_map(self):
        """Update map position based on current weather location"""
        if not self.current_weather:
            return
        
        try:
            # Get coordinates from current weather
            coords = self.current_weather.get('coordinates', {})
            lat = coords.get('lat')
            lon = coords.get('lon')
            
            if lat and lon:
                # Set map position to the weather location
                self.map_widget.set_position(lat, lon)
                self.map_widget.set_zoom(12)
                
                # Add a marker for the city
                city_name = self.current_weather.get('city', 'Current Location')
                self.map_widget.delete_all_marker()  # Clear previous markers
                self.map_widget.set_marker(lat, lon, text=city_name)
                
        except Exception as e:
            print(f"Error updating map: {e}")

    def on_language_change(self, selected_lang):
        self.controller.update_language(selected_lang)

    def _handle_menu_selection(self, choice):
        """Handle menu dropdown selection"""
        if choice == "Manage Favorites":
            self._open_favorites_dialog()
        elif choice == "Settings":
            print("Settings selected")
        elif choice == "Help":
            print("Help selected")
        
        # Reset dropdown to show "Menu"
        self.menu_dropdown.set("Menu")
            
    def _open_favorites_dialog(self):
        """Open the favorites management dialog"""
        # Close menu first
        if hasattr(self, 'menu_window'):
            self.menu_window.destroy()
        
        # Open favorites dialog
        if hasattr(self, 'fav_window') and self.fav_window.winfo_exists():
            return
        
        self.fav_window = ctk.CTkToplevel(self)
        self.fav_window.title("Manage Favorites")
        self.fav_window.geometry("300x200")
        
        # Make it stay on top and grab focus
        self.fav_window.transient(self)
        self.fav_window.lift()
        self.fav_window.focus_force()
        self.fav_window.grab_set()
        
        self.favorites_manager = FavoritesManager()
        
        # Add city entry
        ctk.CTkLabel(self.fav_window, text="Add City:").pack(pady=5)
        self.fav_entry = ctk.CTkEntry(self.fav_window, width=200)
        self.fav_entry.pack(pady=5)
        
        ctk.CTkButton(self.fav_window, text="Add", command=self._add_favorite).pack(pady=5)
        
        # Show current favorites
        ctk.CTkLabel(self.fav_window, text="Current Favorites:").pack(pady=(10,5))
        self.fav_list_frame = ctk.CTkFrame(self.fav_window)
        self.fav_list_frame.pack(pady=5, padx=20, fill="x")
        
        self._refresh_favorites()

    def _add_favorite(self):
        city = self.fav_entry.get()
        success, msg = self.favorites_manager.add_favorite(city)
        print(msg)  # Simple feedback for now
        if success:
            self.fav_entry.delete(0, 'end')
            self._refresh_favorites()

    def _refresh_favorites(self):
        for widget in self.fav_list_frame.winfo_children():
            widget.destroy()
        
        favorites = self.favorites_manager.get_favorites()
        for city in favorites:
            frame = ctk.CTkFrame(self.fav_list_frame)
            frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(frame, text=city).pack(side="left", padx=10)
            ctk.CTkButton(frame, text="X", width=30, 
                        command=lambda c=city: self._remove_favorite(c)).pack(side="right", padx=5)

    def _remove_favorite(self, city):
        success, msg = self.favorites_manager.remove_favorite(city)
        print(msg)  # Simple feedback for now
        if success:
            self._refresh_favorites()

    def update_sun_widget_background(self, icon_code):
        """Update the weather icon background for the entire sun widget"""
        try:
            # Download weather icon from OpenWeatherMap
            icon_url = f"https://openweathermap.org/img/wn/{icon_code}@4x.png"
            response = requests.get(icon_url)
            
            if response.status_code == 200:
                from PIL import Image
                
                # Open and resize the image to fit the widget
                icon_image = Image.open(io.BytesIO(response.content))
                
                # Get the widget size and resize icon to fill it
                widget_width = 400  # Increased size
                widget_height = 200  # Increased size
                
                # Resize image to cover the widget area
                icon_image = icon_image.resize((widget_width, widget_height), Image.Resampling.LANCZOS)
                
                # Make it more visible by reducing transparency less
                icon_image = icon_image.convert("RGBA")
                # Reduce opacity to 80% instead of 60% for better visibility
                alpha = icon_image.split()[3]
                alpha = alpha.point(lambda p: int(p * 0.8))
                icon_image.putalpha(alpha)
                
                # Convert to CTkImage with the actual size
                icon_ctk_image = ctk.CTkImage(
                    light_image=icon_image, 
                    dark_image=icon_image, 
                    size=(widget_width, widget_height)
                )
                
                # Set as background
                self.sun_background_label.configure(image=icon_ctk_image, text="")
                
                # Keep a reference to prevent garbage collection
                self.sun_background_label.image = icon_ctk_image
                
                print(f"Weather icon background updated successfully with icon: {icon_code}")
                
        except Exception as e:
            print(f"Error loading weather icon background: {e}")

    # Quiz-related methods
    def load_new_question(self):
        """Load a new quiz question"""
        if not self.weather_quiz:
            self.question_label.configure(text="Quiz not available - check CSV files")
            return
        
        # Check if current set is completed
        if hasattr(self.weather_quiz, 'set_completed') and self.weather_quiz.set_completed:
            set_info = self.weather_quiz.get_current_set_info()
            score, percentage = self.weather_quiz.get_score()
            
            # Show set completion message
            completion_text = f"🎉 Set {set_info['set_number']} Complete!\n"
            completion_text += f"({set_info['set_name']})\n"
            completion_text += f"Score: {score}/{self.weather_quiz.total_questions} ({percentage:.1f}%)"
            
            self.question_label.configure(text=completion_text)
            
            # Clear answer buttons
            for button in self.answer_buttons:
                button.destroy()
            self.answer_buttons = []
            
            # Reset button text
            self.new_question_btn.configure(text="New Question")
            
            # Change button text to start next set
            next_set_num = self.weather_quiz.start_next_set()
            if next_set_num <= 3:
                self.new_question_btn.configure(text=f"Start Set {next_set_num}")
            else:
                # All sets completed
                self.new_question_btn.configure(text="Quiz Complete!")
            return
        
        try:
            question = self.weather_quiz.generate_question()
            if not question:
                # Set completed
                set_info = self.weather_quiz.get_current_set_info()
                score, percentage = self.weather_quiz.get_score()
                
                completion_text = f"🎉 Set {set_info['set_number']} Complete!\n"
                completion_text += f"({set_info['set_name']})\n"
                completion_text += f"Score: {score}/{self.weather_quiz.total_questions} ({percentage:.1f}%)"
                
                self.question_label.configure(text=completion_text)
                
                # Clear answer buttons
                for button in self.answer_buttons:
                    button.destroy()
                self.answer_buttons = []
                
                # Prepare for next set
                next_set_num = self.weather_quiz.start_next_set()
                if next_set_num <= 3:
                    self.new_question_btn.configure(text=f"Start Set {next_set_num}")
                else:
                    self.new_question_btn.configure(text="All Sets Complete!")
                return
            
            # Reset button text for normal questions
            self.new_question_btn.configure(text="New Question")
            
            # Update question text
            self.question_label.configure(text=question['question'])
            
            # Clear previous answer buttons
            for button in self.answer_buttons:
                button.destroy()
            self.answer_buttons = []
            
            # Create answer options
            all_answers = [question['correct_answer']] + question['wrong_answers']
            random.shuffle(all_answers)
            
            for i, answer in enumerate(all_answers):
                btn = ctk.CTkButton(
                    self.answers_frame, 
                    text=answer,
                    command=lambda a=answer: self.check_quiz_answer(a)
                )
                btn.grid(row=i, column=0, pady=2, padx=5, sticky="ew")
                self.answer_buttons.append(btn)
                
        except Exception as e:
            print(f"Error loading question: {e}")
            self.question_label.configure(text="Error loading question")

    def check_quiz_answer(self, user_answer):
        """Check the user's answer, show feedback, and automatically advance to next question"""
        if not self.weather_quiz:
            return
            
        try:
            is_correct = self.weather_quiz.check_answer(user_answer)
            
            # Update score display
            score, percentage = self.weather_quiz.get_score()
            self.score_label.configure(text=f"Score: {score}/{self.weather_quiz.total_questions} ({percentage:.1f}%)")
            
            # Provide feedback
            correct_answer = self.weather_quiz.current_question['correct_answer']
            if is_correct:
                feedback = f"✅ Correct! The answer is {correct_answer}"
            else:
                feedback = f"❌ Incorrect. The correct answer is {correct_answer}"
            
            # Show feedback briefly
            self.question_label.configure(text=feedback)
            
            # Disable answer buttons temporarily
            for button in self.answer_buttons:
                button.configure(state="disabled")
            
            # Automatically advance to next question after 2 seconds
            self.after(2000, self._advance_to_next_question)
            
        except Exception as e:
            print(f"Error checking answer: {e}")

    def _advance_to_next_question(self):
        """Automatically advance to the next question after feedback"""
        # Load the next question (this automatically advances the quiz state)
        self.load_new_question()

    def reset_quiz(self):
        """Reset quiz score and stats"""
        if self.weather_quiz:
            self.weather_quiz.reset_quiz()
            self.score_label.configure(text="Score: 0/0 (0%)")
            self.question_label.configure(text="Click 'New Question' to start the quiz!")
            
            # Clear answer buttons
            for button in self.answer_buttons:
                button.destroy()
            self.answer_buttons = []