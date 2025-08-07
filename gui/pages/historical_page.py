import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import os
from datetime import datetime, timedelta
import queue
import tkinter as tk

# Link Data and Feature files for interactions
from features.trend_and_graph import TrendandGraphProcessor
from data.history_management.file_handler import save_weather


class HistoricalPage(ctk.CTkFrame):
    """Historical weather data page with threading and CSV data foundation"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Threading and data management
        self.data_queue = queue.Queue()
        self.is_loading = False
        self.cached_data = {}  # Cache for city data
        self._destroyed = False  # Track if widget is destroyed
        
        # Data sources
        self.weather_history_path = 'data/history_management/weather_history.csv'
        self.trend_processor = TrendandGraphProcessor()
        
        # Current city tracking
        self.current_city = None
        self.current_data = None
        
        # UI elements
        self.loading_label = None
        self.city_selector = None
        self.chart_frame = None
        self.stats_frame = None
        self.canvas = None
        self.figure = None
        
        """ Call builders """
        self._configure_grid()
        self._build_header()
        self._build_city_selector()
        self._build_loading_indicator()
        self._build_chart_area()
        self._build_stats_area()
        
        self.after(500, self._initialize_data) 

    def destroy(self):
        """Override destroy to clean up background tasks"""
        self._destroyed = True
        super().destroy()

    def _configure_grid(self):
        """Configure grid layout for the historical page"""
        for row in range(6):
            self.grid_rowconfigure(row, weight=1)
        for column in range(7):
            self.grid_columnconfigure(column, weight=1)

    def _build_header(self):
        """Build header with navigation and theme toggle"""
        header_frame = ctk.CTkFrame(self, height=40)
        header_frame.grid(row=0, column=0, columnspan=7, sticky="ew", padx=10, pady=5)
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_columnconfigure(2, weight=1)

        # Import here to avoid circular imports
        from .home_page import HomePage

        # Back button
        menu_button = ctk.CTkButton(
            header_frame, 
            text="← Back", 
            width=120, 
            height=28, 
            command=lambda: self.controller.show_frame(HomePage)
        )
        menu_button.grid(row=0, column=0, padx=10, sticky="w")
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame, 
            text="Historical Weather Data", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.grid(row=0, column=1)

        # Theme toggle
        self.theme_button = ctk.CTkButton(
            header_frame,
            text="Dark Mode",
            width=120,
            height=28,
            command=self.controller.toggle_theme
        )
        self.theme_button.grid(row=0, column=2, sticky="e", padx=10)

        current_mode = ctk.get_appearance_mode()
        self.theme_button.configure(text="Dark Mode" if current_mode == "Light" else "Light Mode")
        self.controller.theme_buttons.append(self.theme_button)

    def _build_city_selector(self):
        """Build city selection controls"""
        selector_frame = ctk.CTkFrame(self)
        selector_frame.grid(row=1, column=0, columnspan=7, sticky="ew", padx=10, pady=5)
        selector_frame.grid_columnconfigure(0, weight=1)
        selector_frame.grid_columnconfigure(1, weight=2)
       
        
        # City selection label
        city_label = ctk.CTkLabel(selector_frame, text="Select City:")
        city_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        
        # City dropdown (will be populated with available cities)
        self.city_selector = ctk.CTkComboBox(
            selector_frame,
            values=["Loading..."],
            command=self._on_city_selected,
            state="disabled"
        )
        self.city_selector.grid(row=0, column=1, padx=10, pady=10, sticky="ew", columnspan=2)
        
        

    def _build_loading_indicator(self):
        """Build loading indicator"""
        self.loading_label = ctk.CTkLabel(
            self, 
            text="", 
            font=ctk.CTkFont(size=14)
        )
        self.loading_label.grid(row=2, column=0, columnspan=7, pady=10)

    def _build_chart_area(self):
        """Build the main chart display area"""
        self.chart_frame = ctk.CTkFrame(self)
        self.chart_frame.grid(row=3, column=0, columnspan=5, sticky="nsew", padx=10, pady=5)
        self.chart_frame.grid_rowconfigure(0, weight=1)
        self.chart_frame.grid_columnconfigure(0, weight=1)
        
        # Placeholder label
        placeholder_label = ctk.CTkLabel(
            self.chart_frame, 
            text="Select a city to view historical temperature data",
            font=ctk.CTkFont(size=16)
        )
        placeholder_label.grid(row=0, column=0, padx=20, pady=20)

    def _build_stats_area(self):
        """Build statistics display area"""
        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.grid(row=3, column=5, columnspan=2, sticky="nsew", padx=10, pady=5)
        self.stats_frame.grid_rowconfigure(0, weight=1)
        self.stats_frame.grid_columnconfigure(0, weight=1)
        
        # Stats title
        stats_title = ctk.CTkLabel(
            self.stats_frame, 
            text="Statistics", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        stats_title.grid(row=0, column=0, pady=(10, 5), sticky="n")

    def _initialize_data(self):
        """Initialize data loading on startup"""
        self._show_loading("Loading available cities...")
        threading.Thread(target=self._load_available_cities, daemon=True).start()
        
        # Start checking for data updates
        self.after(100, self._check_data_queue)

    def _load_available_cities(self):
        """Load available cities using get_cities_list from auto_api_history_builder (threaded)"""
        try:
            # Import and use the ForecastArchiveAutomation class to get cities
            from data.history_management.auto_api_history_builder import ForecastArchiveAutomation
            
            # Create automation instance with limit=10 for each category
            automation = ForecastArchiveAutomation(limit=10)
            
            # Get the curated list of cities (top 10 most searched + up to 10 favorites)
            cities = automation.get_cities_list()
            
    
            
            # Add current city from HomePage if not already included
            try:
                from .home_page import HomePage
                home_page = self.controller.frames.get(HomePage)
                if home_page and hasattr(home_page, 'current_weather') and home_page.current_weather:
                    current_city = home_page.current_weather.get('city')
                    if current_city and current_city not in cities:
                        cities.append(current_city)
            except Exception as e:
                print(f"Error getting current city: {e}")
            
            # If still no cities, add a few defaults (limited set)
            if not cities:
                cities = ["Madrid", "New York", "London"]
                print("Using default cities as fallback")
            
            # Limit total cities to max 25 (safety check)
            if len(cities) > 25:
                cities = cities[:25]
                print(f"WARNING: Too many cities ({len(cities)}), limiting to 25")
            
            # Sort alphabetically for better UX
            city_list = sorted(cities)
            
    
            
            # Queue the result
            self.data_queue.put(('cities_loaded', city_list))
            
        except Exception as e:
            print(f"Error in _load_available_cities: {e}")
            self.data_queue.put(('error', f"Error loading cities: {str(e)}"))

    def _on_city_selected(self, city_name):
        """Handle city selection"""
        if city_name and city_name != "Loading..." and not self.is_loading:
            self.current_city = city_name
            self._show_loading(f"Loading data for {city_name}...")
            threading.Thread(target=self._load_city_data, args=(city_name,), daemon=True).start()

    def _load_city_data(self, city_name):
        """Load historical and current data for a city (threaded)"""
        try:
            data_sources = {
                'csv_data': None,
                'api_data': None,
                'trend_data': None
            }
            
            # 1. Load CSV data first (fastest)
            if os.path.exists(self.weather_history_path):
                try:
                    df = pd.read_csv(self.weather_history_path)
                    city_data = df[df['city'].str.contains(city_name, case=False, na=False)]
                    if not city_data.empty:
                        data_sources['csv_data'] = city_data
                except Exception as e:
                    print(f"Error loading CSV data: {e}")
            
            # 2. Get Open-Meteo 13-day data (5 past + current + 7 forecast)
            try:
                trend_data, error = self.trend_processor.prepare_trend_display_data(city_name)
                if not error and trend_data:
                    data_sources['trend_data'] = trend_data
            except Exception as e:
                print(f"Error loading trend data: {e}")
            
            # Queue the combined data
            self.data_queue.put(('city_data_loaded', city_name, data_sources))
            
        except Exception as e:
            self.data_queue.put(('error', f"Error loading data for {city_name}: {str(e)}"))

    def _check_data_queue(self):
        """Check for data updates from background threads"""
        # Check if widget still exists
        if not self.winfo_exists():
            return
            
        try:
            while not self.data_queue.empty():
                message = self.data_queue.get_nowait()
                
                if message[0] == 'cities_loaded':
                    self._update_city_selector(message[1])
                elif message[0] == 'city_data_loaded':
                    city_name, data = message[1], message[2]
                    self._update_display(city_name, data)
                elif message[0] == 'error':
                    self._show_error(message[1])
                    
        except queue.Empty:
            pass
        except tk.TclError:
            return  # Widget destroyed
        except Exception as e:
            print(f"Error in _check_data_queue: {e}")
            return
        
        # Schedule next check more carefully
        try:
            if self.winfo_exists():
                self.after(100, self._check_data_queue)
        except (tk.TclError, AttributeError):
            pass  # Widget destroyed or doesn't exist

    def _update_city_selector(self, cities):
        """Update city selector with available cities"""
        self.city_selector.configure(values=cities, state="normal")
        
        # Set default selection
        if cities:
            # Try to select current city from HomePage first
            default_city = None
            try:
                from .home_page import HomePage
                home_page = self.controller.frames.get(HomePage)
                if home_page and hasattr(home_page, 'current_weather') and home_page.current_weather:
                    current_city = home_page.current_weather.get('city')
                    if current_city in cities:
                        default_city = current_city
            except:
                pass
            
            if not default_city:
                default_city = cities[0]
                
            self.city_selector.set(default_city)
            
        self._hide_loading()

    def _update_display(self, city_name, data_sources):
        """Update the chart and statistics display"""
        try:
            # Clear existing display
            for widget in self.chart_frame.winfo_children():
                widget.destroy()
            for widget in self.stats_frame.winfo_children():
                widget.destroy()
                
            # Rebuild stats title
            stats_title = ctk.CTkLabel(
                self.stats_frame, 
                text="Statistics", 
                font=ctk.CTkFont(size=16, weight="bold")
            )
            stats_title.grid(row=0, column=0, pady=(10, 5), sticky="n")
            
            # Process and combine data
            chart_data = self._process_chart_data(data_sources)
            
            if chart_data and len(chart_data['dates']) > 0:
                # Create matplotlib chart
                self._create_temperature_chart(chart_data)
                self._create_statistics_display(chart_data)
            else:
                # Show no data message
                no_data_label = ctk.CTkLabel(
                    self.chart_frame,
                    text=f"No historical data available for {city_name}",
                    font=ctk.CTkFont(size=14)
                )
                no_data_label.grid(row=0, column=0, padx=20, pady=20)
                
        except Exception as e:
            self._show_error(f"Error updating display: {str(e)}")
        finally:
            self._hide_loading()

    def _process_chart_data(self, data_sources):
        """Process and combine data from different sources"""
        chart_data = {
            'dates': [],
            'max_temps': [],
            'min_temps': [],
            'data_sources': []
        }
        
        # Add Open-Meteo 13-day data (primary source)
        trend_data = data_sources.get('trend_data')
        if trend_data:
            # Get the data arrays
            dates = trend_data.get('dates', [])
            max_temps = trend_data.get('max_temps', [])
            min_temps = trend_data.get('min_temps', [])
            
            for i, date in enumerate(dates):
                if i < len(max_temps) and i < len(min_temps):
                    chart_data['dates'].append(date)
                    chart_data['max_temps'].append(max_temps[i])
                    chart_data['min_temps'].append(min_temps[i])
                    chart_data['data_sources'].append('Open-Meteo API')
        
        # Add CSV historical data (supplementary)
        csv_data = data_sources.get('csv_data')
        if csv_data is not None and not csv_data.empty:
            # Limit to recent CSV data to avoid overwhelming the chart
            csv_recent = csv_data.tail(20)  # Last 20 entries
            
            for _, row in csv_recent.iterrows():
                try:
                    if 'date' in row and pd.notna(row['date']):
                        date_val = pd.to_datetime(row['date']).date()
                        
                        # Avoid duplicates with API data
                        if date_val not in [d.date() if hasattr(d, 'date') else d for d in chart_data['dates']]:
                            chart_data['dates'].append(date_val)
                            chart_data['max_temps'].append(row.get('temp_max', None))
                            chart_data['min_temps'].append(row.get('temp_min', None))
                            chart_data['data_sources'].append('Historical CSV')
                except Exception as e:
                    print(f"Error processing CSV row: {e}")
                    continue
        
        # Sort by date
        if chart_data['dates']:
            combined = list(zip(chart_data['dates'], chart_data['max_temps'], 
                              chart_data['min_temps'], chart_data['data_sources']))
            combined.sort(key=lambda x: x[0])
            
            chart_data['dates'] = [x[0] for x in combined]
            chart_data['max_temps'] = [x[1] for x in combined]
            chart_data['min_temps'] = [x[2] for x in combined]
            chart_data['data_sources'] = [x[3] for x in combined]
        
        return chart_data

    def _create_temperature_chart(self, chart_data):
        """Create matplotlib temperature chart"""
        try:
            # Create figure
            self.figure, ax = plt.subplots(figsize=(10, 6))
            
            # Prepare data for plotting
            dates = chart_data['dates']
            max_temps = [t if t is not None else None for t in chart_data['max_temps']]
            min_temps = [t if t is not None else None for t in chart_data['min_temps']]
            
            # Plot temperature lines
            ax.plot(dates, max_temps, 'r--', marker='o', label='Max Temperature', linewidth=2, markersize=4)
            ax.plot(dates, min_temps, 'b--', marker='s', label='Min Temperature', linewidth=2, markersize=4)
            
            # Formatting
            ax.set_title(f'Temperature History - {self.current_city}', fontsize=14, fontweight='bold')
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('Temperature (°C)', fontsize=12)
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Format x-axis
            if len(dates) > 10:
                ax.tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            
            # Embed in tkinter
            self.canvas = FigureCanvasTkAgg(self.figure, self.chart_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            
        except Exception as e:
            print(f"Error creating chart: {e}")
            error_label = ctk.CTkLabel(
                self.chart_frame,
                text="Error creating temperature chart",
                font=ctk.CTkFont(size=14)
            )
            error_label.grid(row=0, column=0, padx=20, pady=20)

    def _create_statistics_display(self, chart_data):
        """Create statistics display"""
        try:
            # Calculate statistics
            max_temps = [t for t in chart_data['max_temps'] if t is not None]
            min_temps = [t for t in chart_data['min_temps'] if t is not None]
            
            if max_temps and min_temps:
                stats = {
                    'Max Temperature': f"{max(max_temps):.1f}°C",
                    'Min Temperature': f"{min(min_temps):.1f}°C",
                    'Avg Max': f"{sum(max_temps)/len(max_temps):.1f}°C",
                    'Avg Min': f"{sum(min_temps)/len(min_temps):.1f}°C",
                    'Data Points': str(len(chart_data['dates'])),
                    'Date Range': f"{len(chart_data['dates'])} days"
                }
                
                # Display statistics
                row = 1
                for key, value in stats.items():
                    stat_frame = ctk.CTkFrame(self.stats_frame)
                    stat_frame.grid(row=row, column=0, sticky="ew", padx=10, pady=2)
                    stat_frame.grid_columnconfigure(0, weight=1)
                    
                    key_label = ctk.CTkLabel(stat_frame, text=key, font=ctk.CTkFont(size=12, weight="bold"))
                    key_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
                    
                    value_label = ctk.CTkLabel(stat_frame, text=value, font=ctk.CTkFont(size=12))
                    value_label.grid(row=1, column=0, sticky="w", padx=5, pady=2)
                    
                    row += 1
                    
        except Exception as e:
            print(f"Error creating statistics: {e}")

    def _refresh_data(self):
        """Refresh all data"""
        if not self.is_loading:
            self.cached_data.clear()
            self._initialize_data()

    def _show_loading(self, message):
        """Show loading indicator"""
        self.is_loading = True
        self.loading_label.configure(text=message)

    def _hide_loading(self):
        """Hide loading indicator"""
        self.is_loading = False
        self.loading_label.configure(text="")

    def _show_error(self, message):
        """Show error message"""
        self.is_loading = False
        self.loading_label.configure(text=f"Error: {message}")
        print(f"Historical Page Error: {message}")