import tkinter as tk
from tkinter import ttk 
import customtkinter as ctk
from PIL import ImageTk


# Link Data and Feature files for interactions
from data.api_handlers.open_weather_api import OpenWeatherAPI
from features.weather_extract import WeatherProcessor

""" TODO See data.file_handler for addition notes. If additional file and db processes developed into Class, edit imports to reflect this change. """
# weather file saving and db update. 
from data.history_management.file_handler import save_weather
""" language dictionary files """
from features.language_select import set_language, get_language



""" default to dark mode but add variable and button """
ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue")

""" import weather alert sms system """
from features.alerts import SMS_Alerts
from data.api_handlers.send_sms import twilio_sms

""" TODO some comments are placed above or before the proceeding function that they reference. Explore a way to make that system still collapsible but so that comments are not missed. For now, TODO open the above function to double check for comments. """

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x800")
        self.title("Weather Wonderland")
        self.resizable(True, True)

        """ Track theme state """
        self.theme_mode = "Dark"
        self.theme_buttons = []

        """ main frame for widgets using grid geometry """
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.frames = {}
        '''ForecastPage, TrendPage, HistoricalPage, FirePage'''
        for pages in (HomePage, ForecastPage, TrendPage, HistoricalPage, FirePage):
            frame = pages(parent=main_frame, controller=self)
            self.frames[pages] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()

    """ toggle them parent """
    def toggle_theme(self):
        # Toggle theme mode
        if self.theme_mode == "Dark":
            ctk.set_appearance_mode("Light")
            self.theme_mode = "Light"
        else:
            ctk.set_appearance_mode("Dark")
            self.theme_mode = "Dark"

        # Update all theme toggle buttons' text
        for button in self.theme_buttons:
            button.configure(text="Dark Mode" if self.theme_mode == "Light" else "Light Mode")

    def update_language(self, selected_lang):
        print(f"Language changed to {selected_lang}")
        from features.language_select import set_language
        set_language(selected_lang)

        # Optional: refresh weather if HomePage has it
        home_page = self.frames.get(HomePage)
        if home_page and hasattr(home_page, 'current_weather') and home_page.current_weather:
            city = home_page.current_weather.get('city')
            if city:
                home_page.update_weather(city)    

class ToplevelWindow(ctk.CTkToplevel):
        def __init__(self, parent):
            super().__init__(parent)
            self.geometry("600x600")
            self.title()
            self.attributes("-topmost", True) # makes window stick to front

            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            label = ctk.CTkLabel(self, text="ALERT!!")
            label.grid(row=0, column=0, pady=(5,5), padx=10)

            self.content_frame = ctk.CTkFrame(self)
            self.content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
            
            
        """ landing/main page for app with buttons to navigate to other features. Base weather stats, map inserts """
class HomePage(ctk.CTkFrame):
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

    def _configure_grid(self):
        for row in range(6):
            self.grid_rowconfigure(row, weight=1)
        for column in range(7):
            self.grid_columnconfigure(column, weight=1)
        """ current grid page/grid dimensions
        0 _1_2_   3_   4_5_6_7_
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

        menu_button = ctk.CTkButton(header_frame, text="Menu", width=80, height=28) # left aligned 
        menu_button.grid(row=0, column=0, padx=10, sticky="w")

        """ language selection dropdowon """
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

        """ TODO Home for widget construction/placement and loaded with default values for formating. For Feature values please see Class WeatherFrameConfig """ 

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

    #     """ Connect to Features """
    # def update_weather(self, city):
    #     data, error = self.weather_api.fetch_open_weather(city)
    #     if error:
    #         print("Error:", error)
    #         return
    #     weather = WeatherProcessor.extract_weather_info(data)
        """ TODO Put a better comment on your work so you remember what you were reminding yourself of. This is trash. Do better.  Follow Up on this Comment dude """ 
        # self.display_weather(weather)

        # Features Frame -> Search bar and buttons to activate Features
    def _build_features_frame(self):
        features_frame = ctk.CTkFrame(self,corner_radius=15)
        features_frame.grid(row=1, column=3, columnspan=1, rowspan=3, padx=20, pady=20, sticky="nsew")

        for row in range(5):
            features_frame.grid_rowconfigure(row, weight=1)

        features_frame.grid_columnconfigure(0, weight=1)


        """ collect desire city from user-> TODO: pass to API/Data for retrieval. Set a default or us IP on start up to display current location at WeatherApp load time """
        # select_city
        city_entry = ctk.CTkEntry(features_frame, placeholder_text="Select City", corner_radius=15,)
        city_entry.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

        city_entry.bind("<Return>", lambda event: self.update_weather(city_entry.get()))

        # Nav to forecast page
        forecast_button = ctk.CTkButton(features_frame, text="Forecast", corner_radius=15, command=lambda: self.controller.show_frame(ForecastPage))
        forecast_button.grid(row=1, padx=5, pady=10, sticky="ew")

         # Nav to Trend page
        trend_button = ctk.CTkButton(features_frame, text="Trending Temperature", corner_radius=15, command=lambda: self.controller.show_frame(TrendPage))
        trend_button.grid(row=2, padx=5, pady=10, sticky="ew")

        # Nav to Historical page
        historical_button = ctk.CTkButton(features_frame, text="Historical Data", corner_radius=15, command=lambda: self.controller.show_frame(HistoricalPage))
        historical_button.grid(row=3, padx=5, pady=10, sticky="ew")

        # Weather Alerts TODO toplevel-> user phone/email for Alerts
        """ TODO Correct widget is not TopLevel, it is CTkInputDialog """
        weather_alerts_button = ctk.CTkButton(features_frame, text="Weather Alerts!!", corner_radius=15, command=lambda: self.controller.show_frame())
        weather_alerts_button.grid(row=4, padx=5, pady=10, sticky="ew")

    def _build_map_frame(self):
        map_frame = ctk.CTkFrame(self,corner_radius=15)
        map_frame.grid(row=1, column=4, columnspan=4, rowspan=3, padx=20, pady=20, sticky="nsew")

        for row in range(5):
            map_frame.grid_rowconfigure(row, weight=1)

        map_frame.grid_columnconfigure(0, weight=1)

        # Map layer selection
        layer_frame = ctk.CTkFrame(map_frame)
        layer_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
    
        # Get available layers from API
        self.map_layers = self.weather_api.get_available_map_layers()
        self.selected_layer = tk.StringVar(value="Clouds")
    
        layer_label = ctk.CTkLabel(layer_frame, text="Map Layer:")
        layer_label.grid(row=0, column=0, padx=5)
    
        layer_menu = ctk.CTkOptionMenu(layer_frame, 
                                   values=list(self.map_layers.keys()),
                                   variable=self.selected_layer,
                                   command=self.update_weather_map)
        layer_menu.grid(row=0, column=1, padx=5)

        # Map display label
        self.map_label = ctk.CTkLabel(map_frame, text="Weather Map will appear here")
        self.map_label.grid(row=1, column=0, rowspan=3, sticky="nsew", padx=10, pady=10)

        # Refresh button
        refresh_button = ctk.CTkButton(map_frame, text="Refresh Map", command=self.refresh_weather_map)
        refresh_button.grid(row=4, column=0, pady=5)

    def _build_sun_frame(self):
        sun_frame = ctk.CTkFrame(self,corner_radius=15)
        sun_frame.grid(row=4, column=0, columnspan=3, rowspan=2, padx=20, pady=20, sticky="nsew")

        for row in range(2):
            sun_frame.grid_rowconfigure(row, weight=1)

    def _build_panic_button_frame(self):
        panic_frame = ctk.CTkFrame(self,corner_radius=15)
        panic_frame.grid(row=4, column=3, columnspan=1, rowspan=2, padx=20, pady=20, sticky="nsew")

        for row in range(2):
            panic_frame.grid_rowconfigure(row, weight=1)
       
    def _build_weather_control_frame(self):
        weather_control_frame = ctk.CTkFrame(self,corner_radius=15)
        weather_control_frame.grid(row=4, column=4, columnspan=4, rowspan=2, padx=20, pady=20, sticky="nsew")

        for row in range(2):
            weather_control_frame.grid_rowconfigure(row, weight=1)
    
       
        pass
    

        """ Load to populate display at start up by IP look up"""
    def load_default_weather(self):
        location, error = self.weather_api.get_location_by_ip()
        if location:
            print(f"{location} detected")
            self.update_weather(location)
        else:
            print(f"Could not detect {error}")
            self.update_weather("Lebrija")
        """ Search Entry bar handling """
    def search_weather(self):
        city = self.city_entry.get().strip()
        if city:
            self.update_weather(city)
            self.city_entry.delete(0, 'end')
    """ TODO revisit for thorough testing, including special characters and location, regional, or linguistic variance. Follow up with through dependencies in Features Frame -> city_entry """
    
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
            # print("weather data keys", list(weather))
            # print("weather data", weather)
            self.display_weather(weather)
            # save weather data to csv
            save_weather(weather)

            alertsms = SMS_Alerts()
            alert = alertsms.weather_alerts(data)
            if alert:
                twilio_sms(alert)
                self.top_level_weather_alert(alert) # checks alerts.py criteria on all searchs and on load


            
        else:
            print("Failed to fetch weather data")

    """ change this name to better associate with it dependants """
    """ TODO Add function to change metric/imperial string units """
    def display_weather(self, weather):
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

        """ TODO Update sunrise and sunset frame """
        # self.sunrise_label.configure(text=f"Sunrise: {weather['sunrise']}")
        # self.sunset_label.configure(text=f"Sunset: {weather['sunset']}")  

        self.update_weather_map()

    """ TODO troubleshoot this map a little but I think it is not good in tkinter or the map quality is low. replace with other map option or consider overlaying it with a google map or replacing the HomePage map display feature entirely. """
    def update_weather_map(self, layer_name=None):
        if not self.current_weather or 'coordinates' not in self.current_weather:
            self.map_label.configure(image="", text="Loading weather data...")
            return
        try:
                # Get coordinates from current weather
            lat = self.current_weather['coordinates']['lat']
            lon = self.current_weather['coordinates']['lon']
    
            # Get selected layer
            layer_key = self.map_layers[self.selected_layer.get()]
    
            # Fetch map image
            image, error = self.weather_api.fetch_weather_map(lat, lon, layer_key)
    
            if image and not error:
            # Convert PIL image for tkinter
                ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(400, 300))
                self.map_label.configure(image=ctk_image, text="")
            else:
                self.map_label.configure(image="", text=f"Map Error: {error}")
        
        except KeyError as e:
            print(f"KeyError in update_weather_map: {e}")
        except Exception as e:
            print(f"Unexpecteed error in update_weather_map: {e}")
            self.map_label.configure(image="", text="Error loading map")


    def refresh_weather_map(self):
        self.update_weather_map()

    def on_language_change(self, selected_lang):
        self.controller.update_language(selected_lang)
    


        """ connected to HomePage via button-> plt graphs or other graphics? """
class ForecastPage(ctk.CTkFrame):
    def __init__(self,parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Forecast Page")
        label.grid(row=0, column=0)
        
        

        """ Call builders """
        self._configure_grid()
        self._build_header()

    

    """ TODO this is copied grid layout from HomePage and needs to be modified to the desired feature layout per page. Only used as boilerplate FramePage starter code. """
    def _configure_grid(self):
        for row in range(6):
            self.grid_rowconfigure(row, weight=1)
        for column in range(7):
            self.grid_columnconfigure(column, weight=1)
        """ current grid page/grid dimensions
        0 _1_2_   3_4_   5_6_7_
        0___H__e__a__d__e__r____
        
        1_______   ____   ______
        2_Temp__   _Nav   __Map_
        3_______   ____   ______
        
        4_Sun___   Butt   _Cont_
        5_______   ____   ______
        """

    def _build_header(self):
        header_frame = ctk.CTkFrame(self, height=40)
        header_frame.grid(row=0, column=0, columnspan=8, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1) # Menu Button
        header_frame.grid_columnconfigure(1, weight=1) # Light/Dark toggle, other settings?

        menu_button = ctk.CTkButton(header_frame, text="<- Back", width=120, height=28, command=lambda: self.controller.show_frame(HomePage)) # left aligned 
        menu_button.grid(row=0, column=0, padx=10, sticky="w")

        
        self.theme_button = ctk.CTkButton(header_frame,text="Dark Mode",command=self.controller.toggle_theme)
        self.theme_button.grid(row=0, column=1, sticky="e", padx=10)

        current_mode = ctk.get_appearance_mode()
        self.theme_button.configure(text="Dark Mode" if current_mode == "Light" else "Light Mode")

        # Register button with App for syncing text
        self.controller.theme_buttons.append(self.theme_button)

        """ connected to HomePage via button-> This is for advanced feature and may be removed. Check on feature timeline. If required features not completed, remove TrendPage by 15/7/25 """
class TrendPage(ctk.CTkFrame):
    def __init__(self,parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Trend Page")
        label.grid(row=0, column=0)

        """ Call builders """
        self._configure_grid()
        self._build_header()

    """ TODO this is copied grid layout from HomePage and needs to be modified to the desired feature layout per page. Only used as boilerplate FramePage starter code. """
    def _configure_grid(self):
        for row in range(6):
            self.grid_rowconfigure(row, weight=1)
        for column in range(7):
            self.grid_columnconfigure(column, weight=1)
        """ current grid page/grid dimensions
        0 _1_2_   3_4_   5_6_7_
        0___H__e__a__d__e__r____
        
        1_______   ____   ______
        2_Temp__   _Nav   __Map_
        3_______   ____   ______
        
        4_Sun___   Butt   _Cont_
        5_______   ____   ______
        """

    def _build_header(self):
        header_frame = ctk.CTkFrame(self, height=40)
        header_frame.grid(row=0, column=0, columnspan=8, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1) # Menu Button
        header_frame.grid_columnconfigure(1, weight=1) # Light/Dark toggle, other settings?

        menu_button = ctk.CTkButton(header_frame, text="<- Back", width=120, height=28, command=lambda: self.controller.show_frame(HomePage)) # left aligned 
        menu_button.grid(row=0, column=0, padx=10, sticky="w")

        
        self.theme_button = ctk.CTkButton(header_frame,text="Dark Mode",command=self.controller.toggle_theme)
        self.theme_button.grid(row=0, column=1, sticky="e", padx=10)

        current_mode = ctk.get_appearance_mode()
        self.theme_button.configure(text="Dark Mode" if current_mode == "Light" else "Light Mode")

        # Register button with App for syncing text
        self.controller.theme_buttons.append(self.theme_button)
        pass
        

        """ connected to Homepage via button-> prepare db/API calls/test by 10/7/25 """
class HistoricalPage(ctk.CTkFrame):
    def __init__(self,parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Historical Page")
        label.grid(row=0, column=0)

        """ Call builders """
        self._configure_grid()
        self._build_header()

    """ TODO this is copied grid layout from HomePage and needs to be modified to the desired feature layout per page. Only used as boilerplate FramePage starter code. """
    def _configure_grid(self):
        for row in range(6):
            self.grid_rowconfigure(row, weight=1)
        for column in range(7):
            self.grid_columnconfigure(column, weight=1)
        """ current grid page/grid dimensions
        0 _1_2_   3_4_   5_6_7_
        0___H__e__a__d__e__r____
        
        1_______   ____   ______
        2_Temp__   _Nav   __Map_
        3_______   ____   ______
        
        4_Sun___   Butt   _Cont_
        5_______   ____   ______
        """

    def _build_header(self):
        header_frame = ctk.CTkFrame(self, height=40)
        header_frame.grid(row=0, column=0, columnspan=8, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1) # Menu Button
        header_frame.grid_columnconfigure(1, weight=1) # Light/Dark toggle, other settings?

        menu_button = ctk.CTkButton(header_frame, text="<- Back", width=120, height=28, command=lambda: self.controller.show_frame(HomePage)) # left aligned 
        menu_button.grid(row=0, column=0, padx=10, sticky="w")

        
        self.theme_button = ctk.CTkButton(header_frame,text="Dark Mode",command=self.controller.toggle_theme)
        self.theme_button.grid(row=0, column=1, sticky="e", padx=10)

        current_mode = ctk.get_appearance_mode()
        self.theme_button.configure(text="Dark Mode" if current_mode == "Light" else "Light Mode")

        # Register button with App for syncing text
        self.controller.theme_buttons.append(self.theme_button)
        pass
        

        """ Optional Fire information button-> Remove if not implemented by 10/7/25 """
class FirePage(ctk.CTkFrame):
    def __init__(self,parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Fire Page")
        label.grid(row=0, column=0)

        """ Call builders """
        self._configure_grid()
        self._build_header()

    """ TODO this is copied grid layout from HomePage and needs to be modified to the desired feature layout per page. Only used as boilerplate FramePage starter code. """
    def _configure_grid(self):
        for row in range(6):
            self.grid_rowconfigure(row, weight=1)
        for column in range(7):
            self.grid_columnconfigure(column, weight=1)
        """ current grid page/grid dimensions
        0 _1_2_   3_4_   5_6_7_
        0___H__e__a__d__e__r____
        
        1_______   ____   ______
        2_Temp__   _Nav   __Map_
        3_______   ____   ______
        
        4_Sun___   Butt   _Cont_
        5_______   ____   ______
        """

    def _build_header(self):
        header_frame = ctk.CTkFrame(self, height=40)
        header_frame.grid(row=0, column=0, columnspan=8, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1) # Menu Button
        header_frame.grid_columnconfigure(1, weight=1) # Light/Dark toggle, other settings?

        menu_button = ctk.CTkButton(header_frame, text="<- Back", width=120, height=28, command=lambda: self.controller.show_frame(HomePage)) # left aligned 
        menu_button.grid(row=0, column=0, padx=10, sticky="w")

        
        self.theme_button = ctk.CTkButton(header_frame,text="Dark Mode",command=self.controller.toggle_theme)
        self.theme_button.grid(row=0, column=1, sticky="e", padx=10)

        current_mode = ctk.get_appearance_mode()
        self.theme_button.configure(text="Dark Mode" if current_mode == "Light" else "Light Mode")

        # Register button with App for syncing text
        self.controller.theme_buttons.append(self.theme_button)
        pass



""" For testing layout """
# if __name__ == "__main__":
    
#     app = App()
#     app.mainloop()

