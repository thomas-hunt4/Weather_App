import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk
import tkintermapview
import requests
import io
import random
import re

# Link Data and Feature files for interactions
from data.api_handlers.open_weather_api import OpenWeatherAPI
from features.weather_extract import WeatherProcessor
from data.history_management.file_handler import save_weather
from features.language_select import set_language, get_language, language_selector as t
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

        """ API/On load/Default weather display """
        self.weather_api = OpenWeatherAPI()
        self.current_weather = None

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
        try:
            from features.trend_and_graph import TrendandGraphProcessor
            processor = TrendandGraphProcessor()
            processor.test_data_retrieval("Madrid")
        except Exception as e:
            print(f"Error testing trend processor: {e}")

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

    # ==================== ERROR HANDLING & VALIDATION FUNCTIONS ====================
    
    def show_error_toplevel(self, title_key, message_key, **format_vars):
        """Show error in CustomTkinter toplevel window"""
        try:
            title = t(title_key, **format_vars)
            message = t(message_key, **format_vars)
            self._create_message_toplevel(title, message, "error")
        except Exception as e:
            self._create_message_toplevel("Error", f"An error occurred: {message_key}", "error")
            print(f"Translation error: {e}")
    
    def show_info_toplevel(self, title_key, message_key, **format_vars):
        """Show info in CustomTkinter toplevel window"""
        try:
            title = t(title_key, **format_vars)
            message = t(message_key, **format_vars)
            self._create_message_toplevel(title, message, "info")
        except Exception as e:
            self._create_message_toplevel("Information", f"Info: {message_key}", "info")
            print(f"Translation error: {e}")

    def show_warning_toplevel(self, title_key, message_key, **format_vars):
        """Show warning in CustomTkinter toplevel window"""
        try:
            title = t(title_key, **format_vars)
            message = t(message_key, **format_vars)
            self._create_message_toplevel(title, message, "warning")
        except Exception as e:
            self._create_message_toplevel("Warning", f"Warning: {message_key}", "warning")
            print(f"Translation error: {e}")

    def _create_message_toplevel(self, title, message, msg_type="info"):
        """Enhanced message toplevel with better styling and window management"""
        try:
            # Prevent multiple windows of the same type
            window_attr = f"_{msg_type}_window"
            if hasattr(self, window_attr) and getattr(self, window_attr) and getattr(self, window_attr).winfo_exists():
                getattr(self, window_attr).focus()
                return

            msg_window = ctk.CTkToplevel(self)
            setattr(self, window_attr, msg_window)
            
            msg_window.title(title)
            msg_window.geometry("400x250")
            msg_window.transient(self.winfo_toplevel())
            msg_window.grab_set()
            
            # Center the window
            msg_window.update_idletasks()
            x = (msg_window.winfo_screenwidth() // 2) - (400 // 2)
            y = (msg_window.winfo_screenheight() // 2) - (250 // 2)
            msg_window.geometry(f"400x250+{x}+{y}")
            
            # Configure colors based on message type
            colors = {
                "error": {"bg": "#ff4444", "text": "#ffffff", "button": "#cc3333"},
                "warning": {"bg": "#ffaa00", "text": "#ffffff", "button": "#cc8800"},
                "info": {"bg": "#4488ff", "text": "#ffffff", "button": "#3366cc"},
                "success": {"bg": "#44ff44", "text": "#ffffff", "button": "#33cc33"}
            }
            
            color_scheme = colors.get(msg_type, colors["info"])
            
            # Configure window layout
            msg_window.grid_columnconfigure(0, weight=1)
            msg_window.grid_rowconfigure(0, weight=0)  # Header
            msg_window.grid_rowconfigure(1, weight=1)  # Content
            msg_window.grid_rowconfigure(2, weight=0)  # Button
            
            # Create header frame with colored background
            header_frame = ctk.CTkFrame(msg_window, fg_color=color_scheme["bg"])
            header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
            
            # Title label
            title_label = ctk.CTkLabel(
                header_frame,
                text=title,
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=color_scheme["text"]
            )
            title_label.pack(pady=10)
            
            # Message frame
            text_frame = ctk.CTkFrame(msg_window)
            text_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
            text_frame.grid_columnconfigure(0, weight=1)
            text_frame.grid_rowconfigure(0, weight=1)
            
            message_label = ctk.CTkLabel(
                text_frame,
                text=message,
                font=ctk.CTkFont(size=14),
                wraplength=350,
                justify="center"
            )
            message_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            
            # Button frame
            button_frame = ctk.CTkFrame(msg_window)
            button_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))
            
            ok_button = ctk.CTkButton(
                button_frame,
                text=t("ok_button"),
                command=lambda: self._close_message_window(msg_window, window_attr),
                fg_color=color_scheme["button"],
                hover_color=color_scheme["button"],
                width=100,
                height=32
            )
            ok_button.pack(pady=10)
            
            # Auto-close for non-error messages after 8 seconds
            if msg_type in ["info", "success"]:
                msg_window.after(8000, lambda: self._auto_close_window(msg_window, window_attr))
            
            # Handle window close event
            msg_window.protocol("WM_DELETE_WINDOW", lambda: self._close_message_window(msg_window, window_attr))
            
        except Exception as e:
            print(f"Error creating {msg_type} toplevel: {e}")
            print(f"{msg_type.upper()}: {title} - {message}")

    def validate_city_input(self, city_name):
        """Validate city name input with comprehensive checks"""
        if not city_name:
            return False, "empty_city_name"
        
        city_name = city_name.strip()
        
        if len(city_name) < 2:
            return False, "city_name_too_short"
        if len(city_name) > 50:
            return False, "city_name_too_long"
        if not re.match(r"^[a-zA-ZÀ-ÿ\s\-'\.]+$", city_name):
            return False, "invalid_city_characters"
        if not re.search(r"[a-zA-ZÀ-ÿ]", city_name):
            return False, "city_name_no_letters"
            
        return True, city_name.strip()

    def handle_api_error(self, error_type, city_name=None, exception=None):
        """Handle different types of API errors - log only, no popups to user"""
        print(f"API Error ({error_type}): {city_name} - {exception}")
        # Don't show popups to user for API errors

    def update_ui_text(self, widget, text_key, **format_vars):
        """Update widget text with translation support"""
        try:
            translated_text = t(text_key, **format_vars)
            widget.configure(text=translated_text)
        except Exception as e:
            print(f"Error updating UI text for {text_key}: {e}")

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

        # Menu dropdown - Enhanced with translation support
        self.menu_dropdown = ctk.CTkOptionMenu(
            header_frame, 
            values=[t("manage_favorites"), t("settings"), t("help")],
            width=120,
            height=28,
            command=self._handle_menu_selection
        )
        self.menu_dropdown.set(t("menu_button"))
        self.menu_dropdown.grid(row=0, column=0, padx=10, sticky="w")

        """ language selection dropdown """
        lang_display = {"en": "English", "es": "Español", "hi": "हिन्दी"}
        self.language_var = tk.StringVar(value=lang_display.get(get_language(), "English"))
        language_menu = ctk.CTkOptionMenu(header_frame, values=["English", "Español", "हिन्दी"],variable=self.language_var, command=self.on_language_change)
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
        self.city_label = ctk.CTkLabel(city_frame, text=t("select_city_prompt"), font=ctk.CTkFont(size=16, weight="bold"))
        self.city_label.grid(row=0, column=0, padx=10, pady=5)

        # Temperature Frame -> Child of weather_frame
        temp_frame = ctk.CTkFrame(weather_frame)
        temp_frame.grid(row=1, column=0, columnspan=2, pady=(0,5), sticky="nsew")
        temp_frame.grid_columnconfigure(0, weight=1)
        self.temp_label = ctk.CTkLabel(temp_frame, text=t("temperature_label"))
        self.temp_label.grid(row=0, column=0, padx=10, pady=5)
        self.temp_value = ctk.CTkLabel(temp_frame, text="--°C")
        self.temp_value.grid(row=1, column=0, sticky="n")

        # Description Frame -> Child of weather_frame
        desc_frame = ctk.CTkFrame(weather_frame)
        desc_frame.grid(row=2, column=0, columnspan=2, pady=(0,10), sticky="nsew")
        desc_frame.grid_columnconfigure(0, weight=1)
        self.desc_label = ctk.CTkLabel(desc_frame, text=t("description_label"))
        self.desc_label.grid(row=0, column=0, padx=10, pady=5)
        self.desc_value = ctk.CTkLabel(desc_frame, text="--")
        self.desc_value.grid(row=1, column=0, sticky="n")

        # Wind Frame -> Child of weather_frame
        wind_frame = ctk.CTkFrame(weather_frame)
        wind_frame.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
        wind_frame.grid_columnconfigure(0, weight=1)
        self.wind_label = ctk.CTkLabel(wind_frame, text=t("wind_label"))
        self.wind_label.grid(row=0, column=0, padx=10, pady=5)
        self.wind_value = ctk.CTkLabel(wind_frame, text="-- m/s")
        self.wind_value.grid(row=1, column=0, sticky="n")

        # Humidity Frame -> Child of weather_frame
        humidity_frame = ctk.CTkFrame(weather_frame)
        humidity_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        humidity_frame.grid_columnconfigure(0, weight=1)
        self.humidity_label = ctk.CTkLabel(humidity_frame, text=t("humidity_label"))
        self.humidity_label.grid(row=0, column=0, padx=10, pady=5)
        self.humidity_value = ctk.CTkLabel(humidity_frame, text="--%")
        self.humidity_value.grid(row=1, column=0, sticky="n")
        
        # Precipitation Frame -> Child of weather_frame
        precip_frame = ctk.CTkFrame(weather_frame)
        precip_frame.grid(row=4, column=0, columnspan=2, pady=(10,20), sticky="nsew")
        precip_frame.grid_columnconfigure(0, weight=1)
        self.precip_label = ctk.CTkLabel(precip_frame, text=t("precipitation_label"))
        self.precip_label.grid(row=0, column=0, padx=10, pady=5)
        self.precip_value = ctk.CTkLabel(precip_frame, text="--%")
        self.precip_value.grid(row=1, column=0, sticky="n")

    # Features Frame -> Search bar and buttons to activate Features
    def _build_features_frame(self):
        """Weather search, navigation, and control buttons"""
        features_frame = ctk.CTkFrame(self, corner_radius=15)
        features_frame.grid(row=1, column=3, columnspan=1, rowspan=3, padx=20, pady=20, sticky="nsew")
        
        for row in range(7):  
            features_frame.grid_rowconfigure(row, weight=1)
        features_frame.grid_columnconfigure(0, weight=1)

        # Favorites dropdown 
        try:
            self.favorites_manager = FavoritesManager()
            self.favorites_var = ctk.StringVar(value=t("select_favorite"))
            self.favorites_dropdown = ctk.CTkOptionMenu(
                features_frame,
                variable=self.favorites_var,
                values=[t("select_favorite")] + self.favorites_manager.get_favorites(),
                command=self._on_favorite_selected,
                width=200
            )
            self.favorites_dropdown.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        except Exception as e:
            print(f"Error setting up favorites: {e}")

        # City entry - Enhanced with validation
        self.city_entry = ctk.CTkEntry(features_frame, placeholder_text=t("select_city_placeholder"), corner_radius=15)
        self.city_entry.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
        self.city_entry.bind("<Return>", lambda event: self.search_weather(self.city_entry.get()))

        """TODO Import here to avoid circular imports"""
        from .forecast_page import ForecastPage
        from .trend_page import TrendPage
        from .historical_page import HistoricalPage

        # Nav to forecast page
        forecast_button = ctk.CTkButton(features_frame, text=t("forecast_button"), corner_radius=15, 
                                        command=lambda: self.controller.show_frame(ForecastPage))
        forecast_button.grid(row=2, column=0, padx=5, pady=10, sticky="ew")

        # Nav to Trend page
        trend_button = ctk.CTkButton(features_frame, text=t("trend_button"), corner_radius=15, 
                                     command=lambda: self.controller.show_frame(TrendPage))
        trend_button.grid(row=3, column=0, padx=5, pady=10, sticky="ew")

        # Nav to Historical page
        historical_button = ctk.CTkButton(features_frame, text=t("historical_button"), corner_radius=15,
                                         command=lambda: self.controller.show_frame(HistoricalPage))
        historical_button.grid(row=4, column=0, padx=5, pady=10, sticky="ew")

        # Weather Alerts button - Keep original functionality
        weather_alerts_button = ctk.CTkButton(features_frame, text="Weather Alerts", corner_radius=15,
                                             command=self._open_weather_alerts_window)
        weather_alerts_button.grid(row=5, column=0, padx=5, pady=10, sticky="ew")

        

    # Default weather loading 
    def load_default_weather(self):
        """Load to populate display at start up by IP look up"""
        try:
            location, error = self.weather_api.get_location_by_ip()
            if location:
                self.update_weather(location)
            else:
                print(f"Could not detect {error}")
                self.update_weather("Lebrija")
        except Exception as e:
            print(f"Error loading default weather: {e}")
            # Final fallback
            try:
                self.update_weather("New Haven")
            except:
                print("Failed to load any default weather")

    # Search Entry bar handling 
    def search_weather(self, city_input):
        """Enhanced weather search with validation and error handling"""
        # Validate input
        is_valid, result = self.validate_city_input(city_input)
        
        if not is_valid:
            self.show_error_toplevel("invalid_input_title", result)
            return False
        
        # If validation passed, result contains the cleaned city name
        cleaned_city = result
        
        # Update weather for validated city
        success = self.update_weather(cleaned_city)
        if success:
            self.city_entry.delete(0, 'end')
        return success
    
    def top_level_weather_alert(self, alert):
        """Enhanced weather alert with error handling"""
        try:
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
        except Exception as e:
            print(f"Error showing weather alert: {e}")
            self.show_warning_toplevel("weather_alert_title", "weather_alert_message", alert=alert)
            
    def update_weather(self, city):
        if not city:
            self.show_error_toplevel("error_title", "empty_city_name")
            return False

        try:
            current_language = get_language()
            data, error = self.weather_api.fetch_open_weather(city, current_language)

            if error:
                print("Error:", error)
                if "not found" in error.lower():
                    self.handle_api_error("city_not_found", city)
                else:
                    self.handle_api_error("general_api_error", city, error)
                return False
                
            processor = WeatherProcessor()
            weather = processor.extract_weather_info(data)  
            
            if weather:
                self.current_weather = weather
                self.display_weather(weather)
                
                # save weather data to csv
                try:
                    save_weather(weather)
                except Exception as save_error:
                    print(f"Warning: Could not save weather data: {save_error}")

                # Check for weather alerts
                try:
                    alertsms = SMS_Alerts()
                    alert = alertsms.weather_alerts(data)
                    if alert:
                        # Send SMS to registered users instead of hardcoded number
                        self._send_alert_to_registered_users(alert)
                        self.top_level_weather_alert(alert)
                except Exception as alert_error:
                    print(f"Warning: Could not process weather alerts: {alert_error}")
                    
                return True
            else:
                    self.handle_api_error("general_api_error", city, "Could not process weather data")
                    return False
                
        except requests.exceptions.Timeout:
            self.handle_api_error("timeout_error", city)
            return False
        except requests.exceptions.ConnectionError:
            self.handle_api_error("network_error", city)
            return False
        except requests.exceptions.RequestException as req_error:
            self.handle_api_error("general_api_error", city, req_error)
            return False
        except Exception as e:
            self.handle_api_error("general_api_error", city, e)
            return False

    def display_weather(self, weather):
        """Enhanced weather display with error handling and language support"""
        if not weather:
            self.show_error_toplevel("error_title", "no_weather_data")
            return

        try:
            # Update city name frame with translation support
            city_text = t("city_display", city=weather['city'], country=weather['country'])
            self.city_label.configure(text=city_text)

            # Update temperature frame
            temp_text = t("temperature_display", temp=f"{weather['temperature']:.1f}")
            self.temp_value.configure(text=temp_text)

            # Update description frame
            desc_text = weather['description'].title()
            self.desc_value.configure(text=desc_text)

            # Update humidity and wind frames
            humidity_text = t("humidity_display", humidity=weather['humidity'])
            self.humidity_value.configure(text=humidity_text)
            
            wind_text = t("wind_display", speed=weather['wind_speed'])
            self.wind_value.configure(text=wind_text)

            # Update sunrise and sunset times (if sun frame exists)
            if hasattr(self, 'sunrise_time'):
                sunrise_text = t("sunrise_display", time=weather['sunrise'])
                self.sunrise_time.configure(text=sunrise_text)
            
            if hasattr(self, 'sunset_time'):
                sunset_text = t("sunset_display", time=weather['sunset'])
                self.sunset_time.configure(text=sunset_text)

            # Update weather icon background
            self.update_sun_widget_background(weather.get('weather_icon', '01d'))

            # Update weather map
            self.update_weather_map()
            
        except Exception as e:
            print(f"Error displaying weather: {e}")
            self.show_error_toplevel("error_title", "display_weather_error")

    def update_weather_map(self):
        """Update map position based on current weather location with error handling"""
        if not self.current_weather:
            return
        
        try:
            # Get coordinates from current weather
            coords = self.current_weather.get('coordinates', {})
            lat = coords.get('lat')
            lon = coords.get('lon')
            
            if lat and lon and hasattr(self, 'map_widget'):
                # Set map position to the weather location
                self.map_widget.set_position(lat, lon)
                self.map_widget.set_zoom(12)
                
                # Add a marker for the city
                city_name = self.current_weather.get('city', t('current_location'))
                self.map_widget.delete_all_marker()  # Clear previous markers
                self.map_widget.set_marker(lat, lon, text=city_name)
                
        except Exception as e:
            print(f"Error updating map: {e}")

    def on_language_change(self, selected_lang):
        """Handle language change with UI updates"""
        try:
            # Convert display language to internal language code
            lang_map = {"English": "en", "Español": "es", "हिन्दी": "hi"}
            lang_code = lang_map.get(selected_lang, "en")
            
            self.controller.update_language(lang_code)
            self._update_all_ui_text()
        except Exception as e:
            print(f"Error changing language: {e}")

    def _update_all_ui_text(self):
        """Update all UI text elements with current language"""
        try:
            # Update weather frame labels
            self.update_ui_text(self.temp_label, "temperature_label")
            self.update_ui_text(self.desc_label, "description_label")
            self.update_ui_text(self.wind_label, "wind_label")
            self.update_ui_text(self.humidity_label, "humidity_label")
            self.update_ui_text(self.precip_label, "precipitation_label")
            
            # Update placeholders and dropdowns
            self.city_entry.configure(placeholder_text=t("select_city_placeholder"))
            self.favorites_var.set(t("select_favorite"))
            self.menu_dropdown.set(t("menu_button"))
            
            # Update dropdown values
            self.menu_dropdown.configure(values=[t("menu_button"), t("manage_favorites"), 
                                                t("settings"), t("help")])
                
        except Exception as e:
            print(f"Error updating UI text: {e}")

    def _handle_menu_selection(self, choice):
        """Handle menu dropdown selection - Enhanced with error handling"""
        try:
            if choice == t("manage_favorites") or choice == "Manage Favorites":
                self._open_favorites_dialog()
            elif choice == t("settings") or choice == "Settings":
                self.show_info_toplevel("info_title", "settings_coming_soon")
            elif choice == t("help") or choice == "Help":
                self.show_info_toplevel("help_title", "help_information")
            
            # Reset dropdown to show "Menu"
            self.menu_dropdown.set(t("menu_button"))
        except Exception as e:
            print(f"Error handling menu selection: {e}")
            self.show_error_toplevel("error_title", "menu_selection_error")
            
    def _open_favorites_dialog(self):
        """Open the favorites management dialog with enhanced error handling"""
        try:
            # Close menu first
            if hasattr(self, 'menu_window'):
                self.menu_window.destroy()
            
            # Open favorites dialog
            if hasattr(self, 'fav_window') and self.fav_window.winfo_exists():
                return
            
            self.fav_window = ctk.CTkToplevel(self)
            self.fav_window.title(t("manage_favorites_title"))
            self.fav_window.geometry("300x200")
            
            # Make it stay on top and grab focus
            self.fav_window.transient(self)
            self.fav_window.lift()
            self.fav_window.focus_force()
            self.fav_window.grab_set()
            
            self.favorites_manager = FavoritesManager()
            
            # Add city entry
            ctk.CTkLabel(self.fav_window, text=t("add_city_label")).pack(pady=5)
            self.fav_entry = ctk.CTkEntry(self.fav_window, width=200)
            self.fav_entry.pack(pady=5)
            
            ctk.CTkButton(self.fav_window, text=t("add_button"), command=self._add_favorite).pack(pady=5)
            
            # Show current favorites
            ctk.CTkLabel(self.fav_window, text=t("current_favorites_label")).pack(pady=(10,5))
            self.fav_list_frame = ctk.CTkFrame(self.fav_window)
            self.fav_list_frame.pack(pady=5, padx=20, fill="x")
            
            self._refresh_favorites()
        except Exception as e:
            print(f"Error opening favorites dialog: {e}")
            self.show_error_toplevel("error_title", "favorites_dialog_error")

    def _add_favorite(self):
        """Add favorite with validation and error handling"""
        try:
            city = self.fav_entry.get()
            
            # Validate city input  
            is_valid, result = self.validate_city_input(city)
            if not is_valid:
                self.show_error_toplevel("invalid_input_title", result)
                return
            
            success, msg = self.favorites_manager.add_favorite(result)
            if success:
                self.show_info_toplevel("success_title", "favorite_added", city=result)
                self.fav_entry.delete(0, 'end')
                self._refresh_favorites()
                # Update dropdown
                self._update_favorites_dropdown()
            else:
                self.show_error_toplevel("error_title", "favorite_add_failed", error=msg)
        except Exception as e:
            print(f"Error adding favorite: {e}")
            self.show_error_toplevel("error_title", "favorite_add_error")

    def _refresh_favorites(self):
        """Refresh favorites list with error handling"""
        try:
            # Clear existing favorites display
            for widget in self.fav_list_frame.winfo_children():
                widget.destroy()
            
            favorites = self.favorites_manager.get_favorites()
            for fav in favorites:
                fav_frame = ctk.CTkFrame(self.fav_list_frame)
                fav_frame.pack(fill="x", pady=2)
                
                ctk.CTkLabel(fav_frame, text=fav).pack(side="left", padx=5)
                ctk.CTkButton(fav_frame, text=t("remove_button"), width=60,
                             command=lambda f=fav: self._remove_favorite(f)).pack(side="right", padx=5)
        except Exception as e:
            print(f"Error refreshing favorites: {e}")

    def _remove_favorite(self, favorite):
        """Remove favorite with error handling"""
        try:
            success, msg = self.favorites_manager.remove_favorite(favorite)
            if success:
                self.show_info_toplevel("success_title", "favorite_removed", city=favorite)
                self._refresh_favorites()
                self._update_favorites_dropdown()
            else:
                self.show_error_toplevel("error_title", "favorite_remove_failed", error=msg)
        except Exception as e:
            print(f"Error removing favorite: {e}")
            self.show_error_toplevel("error_title", "favorite_remove_error")

    def _update_favorites_dropdown(self):
        """Update favorites dropdown with current favorites"""
        try:
            favorites = self.favorites_manager.get_favorites()
            new_values = [t("select_favorite")] + favorites
            self.favorites_dropdown.configure(values=new_values)
        except Exception as e:
            print(f"Error updating favorites dropdown: {e}")

    def _on_favorite_selected(self, selection):
        """Handle favorite city selection - Enhanced with error handling"""
        try:
            if selection != t("select_favorite") and selection != "Select Favorite":
                success = self.update_weather(selection)
                # Update the city entry to show selected favorite
                if success and hasattr(self, 'city_entry'):
                    self.city_entry.delete(0, 'end')
                    self.city_entry.insert(0, selection)
        except Exception as e:
            print(f"Error selecting favorite: {e}")
            self.show_error_toplevel("error_title", "favorite_selection_error")

    # Weather Alerts methods 
    def _open_weather_alerts_window(self):
        """Open the Weather Alerts registration window - Original functionality"""
        if hasattr(self, 'alerts_window') and self.alerts_window.winfo_exists():
            self.alerts_window.focus()
        else:
            self.alerts_window = WeatherAlertsWindow(self)
            self.alerts_window.focus()

    def _send_alert_to_registered_users(self, alert):
        """Send weather alerts to all registered users - Enhanced with error handling"""
        try:
            from data.user_preferences.user_registration_manager import UserRegistrationManager
            
            manager = UserRegistrationManager()
            users = manager.get_users()
            
            if not users:
                print("No registered users to send alerts to")
                # Try alternative method for active users
                try:
                    active_users = manager.get_active_users()
                    if active_users:
                        success = twilio_sms(alert)
                        if success:
                            print(f"Weather alert sent to {len(active_users)} registered user(s)")
                except:
                    pass
                return
                
            # Send to all registered users
            success_count = 0
            for user in users:
                try:
                    phone = user.get('phone', '')
                    if phone:
                        # Send SMS alert
                        success = twilio_sms(phone, f"Weather Alert: {alert}")
                        if success:
                            success_count += 1
                            print(f"Alert sent to {user.get('name', 'Unknown')}: {phone}")
                        else:
                            print(f"Failed to send alert to {phone}")
                except Exception as user_error:
                    print(f"Error sending alert to user {user.get('name', 'Unknown')}: {user_error}")
            
            if success_count > 0:
                print(f"Successfully sent alerts to {success_count}/{len(users)} users")
                    
        except Exception as e:
            print(f"Error sending alerts to registered users: {e}")

    

    def _build_map_frame(self):
        """Build map frame with error handling"""
        try:
            map_frame = ctk.CTkFrame(self, corner_radius=15)
            map_frame.grid(row=1, column=4, columnspan=3, rowspan=3, padx=20, pady=20, sticky="nsew")
            map_frame.grid_rowconfigure(0, weight=1)
            map_frame.grid_columnconfigure(0, weight=1)

            # Map widget with error handling
            try:
                self.map_widget = tkintermapview.TkinterMapView(map_frame,corner_radius=10)
                self.map_widget.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
                self.map_widget.set_position(41.3, -72.9)  # Default to New Haven
                self.map_widget.set_zoom(10)
            except Exception as map_error:
                print(f"Error creating map widget: {map_error}")
                # Create fallback label instead of map
                fallback_label = ctk.CTkLabel(map_frame, text=t("map_unavailable"))
                fallback_label.grid(row=0, column=0, padx=20, pady=20)
                
        except Exception as e:
            print(f"Error building map frame: {e}")

    def _build_sun_frame(self):
        """Build sun/moon phase frame with language support"""
        try:
            sun_frame = ctk.CTkFrame(self, corner_radius=15)
            sun_frame.grid(row=4, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")
            sun_frame.grid_rowconfigure(0, weight=1)
            sun_frame.grid_columnconfigure(0, weight=1)
            sun_frame.grid_columnconfigure(1, weight=1)

            # Sunrise frame
            sunrise_frame = ctk.CTkFrame(sun_frame)
            sunrise_frame.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")
            sunrise_frame.grid_columnconfigure(0, weight=1)

            self.sunrise_label = ctk.CTkLabel(sunrise_frame, text=t("sunrise_label"))
            self.sunrise_label.grid(row=0, column=0, padx=10, pady=5)
            self.sunrise_time = ctk.CTkLabel(sunrise_frame, text="--:--")
            self.sunrise_time.grid(row=1, column=0, sticky="n")

            # Sunset frame
            sunset_frame = ctk.CTkFrame(sun_frame)
            sunset_frame.grid(row=0, column=1, padx=10, pady=20, sticky="nsew")
            sunset_frame.grid_columnconfigure(0, weight=1)

            self.sunset_label = ctk.CTkLabel(sunset_frame, text=t("sunset_label"))
            self.sunset_label.grid(row=0, column=0, padx=10, pady=5)
            self.sunset_time = ctk.CTkLabel(sunset_frame, text="--:--")
            self.sunset_time.grid(row=1, column=0, sticky="n")
            
        except Exception as e:
            print(f"Error building sun frame: {e}")

    def _build_panic_button_frame(self):
        """Build panic/emergency button frame - REMOVED as requested"""
        # This frame has been removed per user request
        pass

    def _build_weather_control_frame(self):
        """Build weather control frame (quiz) with language support"""
        try:
            weather_control_frame = ctk.CTkFrame(self, corner_radius=15)
            weather_control_frame.grid(row=4, column=4, columnspan=3, padx=20, pady=20, sticky="nsew")
            weather_control_frame.grid_rowconfigure(1, weight=1)
            weather_control_frame.grid_columnconfigure(0, weight=1)

            # Quiz title
            self.quiz_title = ctk.CTkLabel(weather_control_frame, text=t("weather_quiz_title"), 
                                          font=ctk.CTkFont(size=16, weight="bold"))
            self.quiz_title.grid(row=0, column=0, pady=(10, 5))

            # Question frame  
            question_frame = ctk.CTkFrame(weather_control_frame)
            question_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
            question_frame.grid_rowconfigure(1, weight=1)
            question_frame.grid_columnconfigure(0, weight=1)

            # Question label
            self.question_label = ctk.CTkLabel(
                question_frame, 
                text=t("quiz_loading"), 
                font=ctk.CTkFont(size=12),
                wraplength=250
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

            self.new_question_btn = ctk.CTkButton(button_frame, text=t("new_question_button"), 
                                                 command=self.load_new_question)
            self.new_question_btn.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="ew")

            self.reset_quiz_btn = ctk.CTkButton(button_frame, text=t("reset_quiz_button"), 
                                               command=self.reset_quiz)
            self.reset_quiz_btn.grid(row=0, column=1, padx=(5, 10), pady=5, sticky="ew")

            # Score display
            self.score_label = ctk.CTkLabel(weather_control_frame, text=t("quiz_score", score=0, total=0, percent=0), 
                                           font=ctk.CTkFont(size=12))
            self.score_label.grid(row=3, column=0, pady=(5, 10))

            # Store answer buttons for later reference
            self.answer_buttons = []

            # Initialize quiz
            self.weather_quiz = None
            self.load_new_question()
            
        except Exception as e:
            print(f"Error building weather control frame: {e}")

    # ==================== QUIZ METHODS WITH ERROR HANDLING ====================

    def load_new_question(self):
        """Load a new quiz question with enhanced error handling"""
        try:
            if not self.weather_quiz:
                self.weather_quiz = WeatherQuiz()
            
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
                self.new_question_btn.configure(text=t("new_question_button"))
                
                # Change button text to start next set
                next_set_num = self.weather_quiz.start_next_set()
                if next_set_num <= 3:
                    self.new_question_btn.configure(text=t("start_set", set_num=next_set_num))
                else:
                    # All sets completed
                    self.new_question_btn.configure(text=t("quiz_complete"))
                return
            
            question = self.weather_quiz.generate_question()
            if not question:
                # Set completed during generation
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
                    self.new_question_btn.configure(text=t("start_set", set_num=next_set_num))
                else:
                    self.new_question_btn.configure(text=t("all_sets_complete"))
                return
            
            # Display the question
            self._display_question(question)
            
        except Exception as e:
            print(f"Error loading quiz question: {e}")
            self.question_label.configure(text=t("quiz_error"))

    def reset_quiz(self):
        """Reset quiz with error handling"""
        try:
            if self.weather_quiz:
                self.weather_quiz.reset_quiz()  
                self._update_score_display()
                self.load_new_question()
            else:
                self.weather_quiz = WeatherQuiz()
                self.load_new_question()
        except Exception as e:
            print(f"Error resetting quiz: {e}")
            # Fallback: create new quiz instance
            try:
                self.weather_quiz = WeatherQuiz()
                self.load_new_question()
            except Exception as e2:
                print(f"Error creating new quiz: {e2}")

    def _display_question(self, question_data):
        """Display quiz question with error handling"""
        try:
            # Update question text
            self.question_label.configure(text=question_data['question'])
            
            # Clear existing answer buttons
            for button in self.answer_buttons:
                button.destroy()
            self.answer_buttons.clear()
            
            # Build answer list from correct_answer and wrong_answers
            if 'answers' in question_data:
                # If answers key exists, use it directly
                answers = question_data['answers']
                correct_answer = question_data.get('correct', question_data['answers'][0])
            else:
                # Build answers from correct_answer and wrong_answers
                correct_answer = question_data.get('correct_answer', '')
                wrong_answers = question_data.get('wrong_answers', [])
                
                # Combine and shuffle answers
                answers = [correct_answer] + wrong_answers
                import random
                random.shuffle(answers)
            
            # Create new answer buttons
            for i, answer in enumerate(answers):
                btn = ctk.CTkButton(
                    self.answers_frame,
                    text=answer,
                    command=lambda ans=answer: self._handle_answer(ans, correct_answer)
                )
                btn.grid(row=i, column=0, pady=2, sticky="ew")
                self.answer_buttons.append(btn)
                
        except Exception as e:
            print(f"Error displaying question: {e}")
            print(f"Question data keys: {list(question_data.keys()) if question_data else 'None'}")
            self.question_label.configure(text=t("quiz_display_error"))

    def _handle_answer(self, selected_answer, correct_answer):
        """Handle quiz answer with error handling"""
        try:
            is_correct = (selected_answer == correct_answer)
            
            if self.weather_quiz:
                self.weather_quiz.answer_question(is_correct)
                self._update_score_display()
            
            # Show feedback
            if is_correct:
                self.show_info_toplevel("correct_answer_title", "correct_answer_message")
            else:
                self.show_info_toplevel("incorrect_answer_title", "incorrect_answer_message", 
                                       correct=correct_answer)
                
            # Auto-load next question after a brief delay
            self.after(1500, self.load_new_question)
                
        except Exception as e:
            print(f"Error handling quiz answer: {e}")

    def _update_score_display(self):
        """Update quiz score display with error handling"""
        try:
            if self.weather_quiz:
                score, total = self.weather_quiz.get_score()
                percentage = int((score / total * 100)) if total > 0 else 0
                score_text = t("quiz_score", score=score, total=total, percent=percentage)
                self.score_label.configure(text=score_text)
        except Exception as e:
            print(f"Error updating score display: {e}")

    # ==================== ADDITIONAL METHODS ====================

    def update_sun_widget_background(self, weather_icon):
        """Update sun widget background based on weather icon with error handling"""
        try:
            if not hasattr(self, 'sun_background_label'):
                print("Sun background label not found")
                return
                
            # Load weather icon from OpenWeatherMap
            icon_url = f"https://openweathermap.org/img/wn/{weather_icon}@2x.png"
            
            response = requests.get(icon_url, timeout=5)
            if response.status_code == 200:
                # Load the icon image
                from PIL import Image
                icon_image = Image.open(io.BytesIO(response.content))
                
                # Get the current widget size
                widget_width = self.sun_background_label.winfo_width() or 100
                widget_height = self.sun_background_label.winfo_height() or 100
                
                # Resize to fit the widget
                icon_image = icon_image.resize((widget_width, widget_height), Image.Resampling.LANCZOS)
                
                # Convert to CTkImage
                icon_ctk_image = ctk.CTkImage(
                    light_image=icon_image, 
                    dark_image=icon_image, 
                    size=(widget_width, widget_height)
                )
                
                # Set as background
                self.sun_background_label.configure(image=icon_ctk_image, text="")
                
                # Keep a reference to prevent garbage collection
                self.sun_background_label.image = icon_ctk_image
                
                print(f"Weather icon background updated successfully with icon: {weather_icon}")
            else:
                print(f"Failed to load weather icon: {weather_icon}")
                
        except Exception as e:
            print(f"Error updating sun widget background: {e}")

