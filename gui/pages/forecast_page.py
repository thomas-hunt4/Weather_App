import customtkinter as ctk
import threading
from datetime import datetime, timedelta


class ForecastPage(ctk.CTkFrame):
    """7-day weather forecast page with city selection and threading for data loading"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Data loading state
        self.loading = False
        self.forecast_data = None
        self.current_city = None
        
        # City management
        self.cities_list = []
        
        # Call builders
        self._configure_grid()
        self._build_header()
        self._build_city_selection()
        self._build_forecast_display()
        
        # Load initial data
        self.load_city_list()
        self.load_default_forecast()

    def _configure_grid(self):
        """Configure the main grid layout for forecast page"""
        for row in range(6):
            self.grid_rowconfigure(row, weight=1)
        for column in range(8):
            self.grid_columnconfigure(column, weight=1)

    def _build_header(self):
        """Build the header with back button and theme toggle"""
        header_frame = ctk.CTkFrame(self, height=40)
        header_frame.grid(row=0, column=0, columnspan=8, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=1)

        # Import here to avoid circular imports
        from .home_page import HomePage

        # Back button
        menu_button = ctk.CTkButton(
            header_frame, 
            text="<- Back", 
            width=120, 
            height=28, 
            command=lambda: self.controller.show_frame(HomePage)
        )
        menu_button.grid(row=0, column=0, padx=10, sticky="w")

        # Theme toggle button
        self.theme_button = ctk.CTkButton(
            header_frame,
            text="Dark Mode",
            command=self.controller.toggle_theme
        )
        self.theme_button.grid(row=0, column=1, sticky="e", padx=10)

        # Set correct theme button text
        current_mode = ctk.get_appearance_mode()
        self.theme_button.configure(text="Dark Mode" if current_mode == "Light" else "Light Mode")

        # Register button with App for syncing text
        self.controller.theme_buttons.append(self.theme_button)

    def _build_city_selection(self):
        """Build city selection dropdown and manual entry"""
        city_frame = ctk.CTkFrame(self, corner_radius=15)
        city_frame.grid(row=1, column=0, columnspan=6, padx=20, pady=10, sticky="ew")
        city_frame.grid_columnconfigure(1, weight=1)  # Dropdown
        city_frame.grid_columnconfigure(3, weight=1)  # Entry field

        # City selection label
        city_label = ctk.CTkLabel(
            city_frame, 
            text="Select City:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        city_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # City dropdown (favorites + top searched)
        self.city_var = ctk.StringVar(value="Loading cities...")
        self.city_dropdown = ctk.CTkOptionMenu(
            city_frame,
            variable=self.city_var,
            values=["Loading cities..."],
            command=self._on_city_selected,
            width=200
        )
        self.city_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # "OR" separator
        or_label = ctk.CTkLabel(
            city_frame,
            text="OR",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        or_label.grid(row=0, column=2, padx=10, pady=5)

        # Manual city entry
        self.city_entry = ctk.CTkEntry(
            city_frame, 
            placeholder_text="Enter city name...", 
            corner_radius=15
        )
        self.city_entry.grid(row=0, column=3, padx=10, pady=5, sticky="ew")
        self.city_entry.bind("<Return>", self._on_city_entry)

        # Search button
        search_button = ctk.CTkButton(
            city_frame,
            text="Search",
            width=80,
            command=self._on_search_button_click
        )
        search_button.grid(row=0, column=4, padx=5, pady=5)

        # Loading/Status indicator
        self.status_label = ctk.CTkLabel(
            city_frame, 
            text="", 
            font=ctk.CTkFont(size=11)
        )
        self.status_label.grid(row=1, column=0, columnspan=5, padx=10, pady=(0, 5))

    def _build_forecast_display(self):
        """Build the forecast display with dynamic widget creation"""
        # Main forecast container
        self.forecast_container = ctk.CTkFrame(self, corner_radius=15)
        self.forecast_container.grid(row=2, column=0, columnspan=8, rowspan=4, padx=20, pady=20, sticky="nsew")
        
        # Configure main container grid to expand properly
        for col in range(8):
            self.forecast_container.grid_columnconfigure(col, weight=1)
        self.forecast_container.grid_rowconfigure(0, weight=0)  # Title
        self.forecast_container.grid_rowconfigure(1, weight=1)  # Day widgets
        self.forecast_container.grid_rowconfigure(2, weight=0)  # Info section

        # Title
        self.forecast_title = ctk.CTkLabel(
            self.forecast_container, 
            text="Weather Forecast", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.forecast_title.grid(row=0, column=0, columnspan=8, pady=(10, 20), sticky="ew")

        # Day widgets will be created dynamically when data loads
        self.day_widgets = []
        self.days_frame = None

        # Additional info section
        self._build_forecast_info()

    def _create_day_widget(self, parent, day_index):
        """Create a single day forecast widget with parent/child structure"""
        # Parent frame for the day - ensure it expands to fill available space
        day_frame = ctk.CTkFrame(parent, corner_radius=10)
        day_frame.grid_rowconfigure(0, weight=0)  # Date
        day_frame.grid_rowconfigure(1, weight=1)  # Icon/weather
        day_frame.grid_rowconfigure(2, weight=0)  # Max temp
        day_frame.grid_rowconfigure(3, weight=0)  # Min temp
        day_frame.grid_rowconfigure(4, weight=0)  # Description
        day_frame.grid_columnconfigure(0, weight=1)

        # Date label (child widget)
        date_label = ctk.CTkLabel(
            day_frame, 
            text="Loading...", 
            font=ctk.CTkFont(size=12, weight="bold")
        )
        date_label.grid(row=0, column=0, pady=(10, 5), padx=5, sticky="ew")

        # Weather icon/emoji (child widget)
        weather_icon = ctk.CTkLabel(
            day_frame, 
            text="🌤️", 
            font=ctk.CTkFont(size=24)
        )
        weather_icon.grid(row=1, column=0, pady=5, padx=5, sticky="ew")

        # Max temperature (child widget)
        max_temp_label = ctk.CTkLabel(
            day_frame, 
            text="--°C", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("#d73027", "#fc8d59")  # Red-orange for max
        )
        max_temp_label.grid(row=2, column=0, pady=2, padx=5, sticky="ew")

        # Min temperature (child widget)
        min_temp_label = ctk.CTkLabel(
            day_frame, 
            text="--°C", 
            font=ctk.CTkFont(size=12),
            text_color=("#4575b4", "#91bfdb")  # Blue for min
        )
        min_temp_label.grid(row=3, column=0, pady=2, padx=5, sticky="ew")

        # Weather description (child widget)
        desc_label = ctk.CTkLabel(
            day_frame, 
            text="Loading...", 
            font=ctk.CTkFont(size=10),
            wraplength=100
        )
        desc_label.grid(row=4, column=0, pady=(2, 10), padx=5, sticky="ew")

        # Store references to child widgets for updates
        day_frame.date_label = date_label
        day_frame.weather_icon = weather_icon
        day_frame.max_temp_label = max_temp_label
        day_frame.min_temp_label = min_temp_label
        day_frame.desc_label = desc_label

        return day_frame

    def _build_forecast_info(self):
        """Build additional forecast information section"""
        self.info_frame = ctk.CTkFrame(self.forecast_container, corner_radius=10)
        self.info_frame.grid(row=2, column=0, columnspan=8, padx=10, pady=(10, 20), sticky="ew")
        self.info_frame.grid_columnconfigure(0, weight=1)
        self.info_frame.grid_columnconfigure(1, weight=1)

        # Summary info (child widgets)
        self.forecast_summary = ctk.CTkLabel(
            self.info_frame, 
            text="Select a city to view forecast", 
            font=ctk.CTkFont(size=12)
        )
        self.forecast_summary.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Last updated (child widget)
        self.last_updated = ctk.CTkLabel(
            self.info_frame, 
            text="", 
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        self.last_updated.grid(row=0, column=1, padx=10, pady=10, sticky="e")

    def load_city_list(self):
        """Load city list using ForecastArchiveAutomation in background thread"""
        def _load_cities():
            try:
                from data.history_management.auto_api_history_builder import ForecastArchiveAutomation
                automation = ForecastArchiveAutomation()
                cities = automation.get_cities_list()
                
                # Update UI on main thread
                self.after(0, self._update_city_dropdown, cities)
                
            except Exception as e:
                print(f"Error loading cities: {e}")
                # Fallback cities
                fallback_cities = ["Madrid", "New York", "London", "Tokyo", "Sydney"]
                self.after(0, self._update_city_dropdown, fallback_cities)

        # Start loading in background
        threading.Thread(target=_load_cities, daemon=True).start()

    def _update_city_dropdown(self, cities):
        """Update city dropdown with loaded cities (runs on main thread)"""
        self.cities_list = cities
        if cities:
            # Update dropdown values
            self.city_dropdown.configure(values=cities)
            self.city_var.set(cities[0])  # Set first city as default
            self.current_city = cities[0]
        else:
            self.city_dropdown.configure(values=["No cities available"])
            self.city_var.set("No cities available")

    def _on_city_entry(self, event):
        """Handle Enter key press in city entry field"""
        city_name = self.city_entry.get().strip()
        if city_name:
            self._search_city(city_name)

    def _on_search_button_click(self):
        """Handle search button click"""
        city_name = self.city_entry.get().strip()
        if city_name:
            self._search_city(city_name)
        else:
            self._show_status("Please enter a city name", "error")

    def _search_city(self, city_name):
        """Search for city with error handling and validation"""
        if not city_name or len(city_name.strip()) < 2:
            self._show_status("City name too short", "error")
            return

        # Validate city name (basic checks)
        if not self._validate_city_name(city_name):
            self._show_status("Invalid city name format", "error")
            return

        # Clear any previous status
        self._show_status("Searching...", "info")
        
        # Start search in background thread
        threading.Thread(target=self._validate_and_load_city, args=(city_name,), daemon=True).start()

    def _validate_city_name(self, city_name):
        """Basic validation for city name input"""
        city_name = city_name.strip()
        
        # Check length
        if len(city_name) < 2 or len(city_name) > 50:
            return False
        
        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        import re
        if not re.match(r"^[a-zA-Z\s\-'\.]+$", city_name):
            return False
            
        # Check for repeated characters (basic spam detection)
        if any(char * 4 in city_name.lower() for char in 'abcdefghijklmnopqrstuvwxyz'):
            return False
            
        return True

    def _validate_and_load_city(self, city_name):
        """Validate city exists and load forecast data in background thread"""
        try:
            # First, try to validate the city using the API to get coordinates
            from data.api_handlers.open_meteo_api import OpenMeteoAPI
            api = OpenMeteoAPI()
            lat, lon = api._get_coordinates(city_name)
            
            if not lat or not lon:
                # City not found
                self.after(0, self._show_status, f"City '{city_name}' not found. Please check spelling.", "error")
                return
            
            # City found, update UI and load forecast
            self.after(0, self._on_valid_city_found, city_name)
            
        except Exception as e:
            print(f"Error validating city: {e}")
            self.after(0, self._show_status, "Error searching for city. Please try again.", "error")

    def _on_valid_city_found(self, city_name):
        """Handle when a valid city is found (runs on main thread)"""
        # Clear the entry field
        self.city_entry.delete(0, 'end')
        
        # Update dropdown to show the found city
        self.city_var.set(city_name)
        
        # Add to dropdown if not already there
        current_values = list(self.city_dropdown.cget("values"))
        if city_name not in current_values and "Loading cities..." not in current_values:
            current_values.append(city_name)
            self.city_dropdown.configure(values=current_values)
        
        # Load forecast for this city
        self.current_city = city_name
        self._show_status(f"Loading forecast for {city_name}...", "info")
        self.load_forecast_data(city_name)

    def _on_city_selected(self, selected_city):
        """Handle city selection from dropdown"""
        if selected_city and selected_city != "Loading cities..." and selected_city != "No cities available":
            self.current_city = selected_city
            self._show_status(f"Loading forecast for {selected_city}...", "info")
            self.load_forecast_data(selected_city)

    def _show_status(self, message, status_type="info"):
        """Show status message with appropriate color"""
        colors = {
            "info": ("gray", "lightgray"),
            "success": ("green", "lightgreen"), 
            "error": ("red", "lightcoral")
        }
        
        color = colors.get(status_type, colors["info"])
        self.status_label.configure(text=message, text_color=color)
        
        # Clear status message after 5 seconds for non-error messages
        if status_type != "error":
            self.after(5000, lambda: self.status_label.configure(text=""))
        """Show status message with appropriate color"""
        colors = {
            "info": ("gray", "lightgray"),
            "success": ("green", "lightgreen"), 
            "error": ("red", "lightcoral")
        }
        
        color = colors.get(status_type, colors["info"])
        self.status_label.configure(text=message, text_color=color)
        
        # Clear status message after 5 seconds for non-error messages
        if status_type != "error":
            self.after(5000, lambda: self.status_label.configure(text=""))

    def load_default_forecast(self):
        """Load default forecast (from HomePage city or fallback)"""
        try:
            # Try to get city from HomePage
            from .home_page import HomePage
            home_page = self.controller.frames.get(HomePage)
            
            if home_page and hasattr(home_page, 'current_weather') and home_page.current_weather:
                city = home_page.current_weather.get('city', 'Madrid')
            else:
                city = 'Madrid'  # Fallback city
                
            self.current_city = city
            # Wait a bit for city dropdown to load, then set the city
            self.after(1000, lambda: self._set_default_city(city))
            
        except Exception as e:
            print(f"Error loading default forecast: {e}")
            self.current_city = 'Madrid'

    def _set_default_city(self, city):
        """Set default city in dropdown if available"""
        if city in self.cities_list:
            self.city_var.set(city)
            self.load_forecast_data(city)
        elif self.cities_list:
            # Use first available city
            self.city_var.set(self.cities_list[0])
            self.load_forecast_data(self.cities_list[0])

    def load_forecast_data(self, city):
        """Load forecast data for selected city using threading"""
        if self.loading:
            return  # Already loading
        
        self.loading = True
        self.status_label.configure(text="Loading forecast data...")
        
        # Show loading state in widgets
        self._show_loading_state()
        
        def _fetch_data():
            try:
                # Use existing TrendandGraphProcessor to get all 13-day data
                from features.trend_and_graph import TrendandGraphProcessor
                processor = TrendandGraphProcessor()
                
                # Get the full dataset (5 past + current + 7 future)
                full_data, error = processor.prepare_trend_display_data(city)
                
                if error or not full_data:
                    print(f"Error loading forecast data: {error}")
                    # Use fallback data
                    display_data = self._get_fallback_data(city)
                else:
                    # Extract only current day + future days from the full dataset
                    display_data = self._extract_forecast_data(full_data)
                    
                    # If extraction failed, use fallback
                    if not display_data:
                        print("No valid forecast data found, using fallback")
                        display_data = self._get_fallback_data(city)
                
                # Update UI on main thread
                self.after(0, self._update_forecast_display, display_data, city)
                
            except Exception as e:
                print(f"Exception loading forecast: {e}")
                fallback_data = self._get_fallback_data(city)
                self.after(0, self._update_forecast_display, fallback_data, city)
            
            finally:
                self.after(0, self._finish_loading)

        # Start loading in background thread
        threading.Thread(target=_fetch_data, daemon=True).start()

    def _create_dynamic_widgets(self, num_days):
        """Create day widgets dynamically based on available data"""
        # Clear existing widgets
        self._clear_day_widgets()
        
        # Create frame for day widgets that spans the full width
        self.days_frame = ctk.CTkFrame(self.forecast_container, fg_color="transparent")
        self.days_frame.grid(row=1, column=0, columnspan=8, padx=10, pady=10, sticky="nsew")
        
        # Configure grid for the number of days we have - make sure all columns expand
        for col in range(num_days):
            self.days_frame.grid_columnconfigure(col, weight=1)
        self.days_frame.grid_rowconfigure(0, weight=1)
        
        # Create widgets for each day with proper sticky to fill the space
        self.day_widgets = []
        for i in range(num_days):
            day_widget = self._create_day_widget(self.days_frame, i)
            day_widget.grid(row=0, column=i, padx=5, pady=10, sticky="nsew")
            self.day_widgets.append(day_widget)
        
        # Update title to reflect actual number of days
        if num_days == 1:
            self.forecast_title.configure(text="Today's Weather")
        else:
            self.forecast_title.configure(text=f"{num_days}-Day Weather Forecast")

    def _clear_day_widgets(self):
        """Clear existing day widgets"""
        if hasattr(self, 'days_frame') and self.days_frame:
            self.days_frame.destroy()
        self.day_widgets = []

    def _show_loading_state(self):
        """Show loading state - create temporary widgets if needed"""
        # Clear any existing widgets
        self._clear_day_widgets()
        
        # Create a temporary loading display that spans full width
        self.days_frame = ctk.CTkFrame(self.forecast_container, fg_color="transparent")
        self.days_frame.grid(row=1, column=0, columnspan=8, padx=10, pady=10, sticky="nsew")
        self.days_frame.grid_columnconfigure(0, weight=1)
        self.days_frame.grid_rowconfigure(0, weight=1)
        
        loading_label = ctk.CTkLabel(
            self.days_frame,
            text="Loading forecast data...",
            font=ctk.CTkFont(size=16)
        )
        loading_label.grid(row=0, column=0, pady=50, sticky="ew")

    def _update_forecast_display(self, display_data, city):
        """Update forecast widgets with loaded data (runs on main thread)"""
        try:
            if not display_data or len(display_data.get('dates', [])) == 0:
                self._show_error_state("No forecast data available")
                return

            num_days = len(display_data['dates'])
            
            # Create widgets dynamically based on available data
            self._create_dynamic_widgets(num_days)

            # Update each day widget with data
            for i in range(num_days):
                day_widget = self.day_widgets[i]
                
                # Update date
                date_str = display_data['dates'][i]
                day_widget.date_label.configure(text=date_str)
                
                # Update temperatures
                max_temp = display_data['max_temps'][i]
                min_temp = display_data['min_temps'][i]
                
                day_widget.max_temp_label.configure(text=f"{max_temp:.1f}°C")
                day_widget.min_temp_label.configure(text=f"{min_temp:.1f}°C")
                
                # Update weather icon based on temperature
                weather_icon = self._get_weather_icon(max_temp, min_temp)
                day_widget.weather_icon.configure(text=weather_icon)
                
                # Update description
                desc = self._get_weather_description(max_temp, min_temp)
                day_widget.desc_label.configure(text=desc)
                
                # Highlight today (now at index 0 for forecast)
                if i == 0:  # Today is always the first day in forecast
                    day_widget.configure(fg_color=("#3B8ED0", "#1F6AA5"))  # Highlight today
                else:
                    day_widget.configure(fg_color=("gray75", "gray25"))  # Normal color

            # Update summary
            self.forecast_summary.configure(text=f"{num_days}-day forecast for {city}")
            
            # Update last updated
            current_time = datetime.now().strftime("%H:%M")
            self.last_updated.configure(text=f"Updated: {current_time}")
            
        except Exception as e:
            print(f"Error updating forecast display: {e}")
            self._show_error_state("Error displaying data")

    def _get_weather_icon(self, max_temp, min_temp):
        """Get weather icon emoji based on temperature"""
        if max_temp is None or min_temp is None:
            return "❓"
        
        avg_temp = (max_temp + min_temp) / 2
        
        if avg_temp >= 30:
            return "☀️"  # Hot/sunny
        elif avg_temp >= 20:
            return "🌤️"  # Partly cloudy
        elif avg_temp >= 10:
            return "⛅"  # Cloudy
        elif avg_temp >= 0:
            return "🌧️"  # Rainy/cool
        else:
            return "❄️"  # Cold/snow

    def _get_weather_description(self, max_temp, min_temp):
        """Get weather description based on temperature"""
        if max_temp is None or min_temp is None:
            return "No data"
        
        avg_temp = (max_temp + min_temp) / 2
        temp_range = max_temp - min_temp
        
        # Base description on average temperature
        if avg_temp >= 30:
            base = "Hot"
        elif avg_temp >= 25:
            base = "Warm"
        elif avg_temp >= 15:
            base = "Mild"
        elif avg_temp >= 5:
            base = "Cool"
        else:
            base = "Cold"
        
        # Add variation indicator
        if temp_range > 15:
            return f"{base} day"
        elif temp_range > 10:
            return f"{base}"
        else:
            return f"{base} steady"

    def _extract_forecast_data(self, full_data):
        """Extract only current and future days from the full 13-day dataset"""
        try:
            # The full dataset has 7 days with today at index 3 (3 past + today + 3 future)
            # We want current day + future days, so we take from today_index onwards
            today_index = full_data.get('today_index', 3)
            
            # Get all data from today onwards (should give us current + future days)
            max_temps_raw = full_data['max_temps'][today_index:]
            min_temps_raw = full_data['min_temps'][today_index:]
            dates_raw = full_data['dates'][today_index:]
            
            # Filter out any None or N/A data - only keep valid entries
            max_temps = []
            min_temps = []
            dates = []
            
            for i, (max_temp, min_temp, date_str) in enumerate(zip(max_temps_raw, min_temps_raw, dates_raw)):
                # Only include entries with valid temperature data
                if max_temp is not None and min_temp is not None and date_str != "N/A":
                    max_temps.append(max_temp)
                    min_temps.append(min_temp)
                    
                    # Format dates for forecast display
                    if i == 0:
                        dates.append("Today")
                    elif i == 1:
                        dates.append("Tomorrow")
                    else:
                        dates.append(date_str)
            
            # Only return data if we have at least 1 valid day
            if len(max_temps) == 0:
                return None
            
            return {
                'dates': dates,
                'max_temps': max_temps,
                'min_temps': min_temps,
                'today_index': 0,  # Today is now at index 0 in our forecast array
                'city': full_data.get('city', 'Unknown')
            }
            
        except Exception as e:
            print(f"Error extracting forecast data: {e}")
            return None

    def _get_fallback_data(self, city):
        """Generate fallback forecast data for current + future days"""
        from datetime import datetime, timedelta
        
        # Generate 7 days of sample forecast data starting from today
        base_date = datetime.now().date()
        dates = []
        max_temps = []
        min_temps = []
        
        for i in range(7):
            date = base_date + timedelta(days=i)  # Today + future days
            
            # Format dates for forecast display
            if i == 0:
                dates.append("Today")
            elif i == 1:
                dates.append("Tomorrow")
            else:
                dates.append(date.strftime('%a %m/%d'))
            
            # Generate realistic temperature ranges
            base_max = 20 + (i * 1.5)  # Gradually changing over the week
            base_min = base_max - 10   # Typical day/night difference
            
            max_temps.append(base_max)
            min_temps.append(base_min)
        
        return {
            'dates': dates,
            'max_temps': max_temps,
            'min_temps': min_temps,
            'today_index': 0,  # Today is at index 0
            'city': city
        }

    def _show_error_state(self, error_msg):
        """Show error state in forecast display"""
        # Clear existing widgets
        self._clear_day_widgets()
        
        # Create error display that spans full width
        self.days_frame = ctk.CTkFrame(self.forecast_container, fg_color="transparent")
        self.days_frame.grid(row=1, column=0, columnspan=8, padx=10, pady=10, sticky="nsew")
        self.days_frame.grid_columnconfigure(0, weight=1)
        self.days_frame.grid_rowconfigure(0, weight=1)
        
        error_label = ctk.CTkLabel(
            self.days_frame,
            text=f"❌ {error_msg}",
            font=ctk.CTkFont(size=16),
            text_color="red"
        )
        error_label.grid(row=0, column=0, pady=50, sticky="ew")
        
        self.forecast_summary.configure(text=f"Error: {error_msg}")
        self.forecast_title.configure(text="Weather Forecast")

    def _finish_loading(self):
        """Clean up loading state"""
        self.loading = False
        self.status_label.configure(text="")