import tkinter as tk
from tkinter import ttk 
import customtkinter as ctk

# Link Data and Feature files for interactions
from data.open_weather_api import OpenWeatherAPI
from features.weather_extract import WeatherProcessor


""" default to dark mode but add variable and button """
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x800")
        self.title("Weather Wonderland")
        self.resizable(True, True)

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

  
        """ landing/main page for app with buttons to navigate to other features. Base weather stats, map inserts """
class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # API and Default weather display
        self.weather_api = OpenWeatherAPI()
        self.update_weather("New Haven")

        self._configure_grid()
        self._build_header()
        self._build_weather_frame()
        self._build_features_frame()
        self._build_map_frame()
        self._build_sun_frame()
        self._build_panic_button_frame()
        self._build_weather_control_frame()


    def _configure_grid(self):
        for row in range(5):
            self.grid_rowconfigure(row, weight=1)
        for column in range(7):
            self.grid_columnconfigure(column, weight=1)
        """ current grid page/grid dimensions
          0_1_2_   3_4_   5_6_7_
        0___H__e__a__d__e__r____
        
        1_______   ____   ______
        2_Temp__   _Nav   __Map_
        3_______   ____   ______
        
        4_Sun___   Butt   _Cont_
        5_______   ____   ______
        """


        # Top Menu and controls frame * pages
    def _build_header(self):
        header_frame = ctk.CTkFrame(self, height=40)
        header_frame.grid(row=0, column=0, columnspan=8, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1) # Menu Button
        header_frame.grid_columnconfigure(1, weight=1) # Light/Dark toggle, other settings?

        menu_button = ctk.CTkButton(header_frame, text="Menu", width=80, height=28) # left aligned 
        menu_button.grid(row=0, column=0, padx=10, sticky="w")

        self.theme_switch = ctk.CTkSwitch(header_frame, text="Light Mode",)# command=self.-> add set_appearance_mode function to toggle variable
        self.theme_switch.grid(row=0, column=1, padx=10, sticky="e")


        #  Parent Frame for Temp, Humidity, Wind, Precip, description
    def _build_weather_frame(self):
        weather_frame = ctk.CTkFrame(self,corner_radius=15)
        weather_frame.grid(row=1, column=0, columnspan=3, rowspan=3, padx=20, pady=20, sticky="nsew")
        
        for row in range(4):
            weather_frame.grid_rowconfigure(row, weight=1)

        for column in range(2):
            weather_frame.grid_columnconfigure(column, weight=1)


        # Temperature Frame -> Child of weather_frame
        temp_frame = ctk.CTkFrame(weather_frame)
        temp_frame.grid(row=0, column=0, columnspan=2, pady=(10,5), sticky="nsew")
        temp_frame.grid_columnconfigure(0, weight=1)
        self.temp_label = ctk.CTkLabel(temp_frame, text="Temperature:") #font?
        self.temp_label.grid(row=0, column=0, padx=10, pady=5)
        self.temp_value = ctk.CTkLabel(temp_frame, text="{weather['temperature']} ℃") #font?
        self.temp_value.grid(row=1, column=0, sticky="n")


        # Description Frame -> Child of weather_frame
        desc_frame = ctk.CTkFrame(weather_frame)
        desc_frame.grid(row=1, column=0, columnspan=2, pady=(0,10), sticky="nsew")
        desc_frame.grid_columnconfigure(0, weight=1)
        self.desc_label = ctk.CTkLabel(desc_frame, text="Condition Description") #font?
        self.desc_label.grid(row=3, column=0, padx=10, pady=5)
        self.desc_value = ctk.CTkLabel(desc_frame, text="Rainy") #font?
        self.desc_value.grid(row=1, column=0, sticky="n")


        # Wind Frame -> Child of weather_frame
        wind_frame = ctk.CTkFrame(weather_frame)
        wind_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        wind_frame.grid_columnconfigure(0, weight=1)
        self.wind_label = ctk.CTkLabel(wind_frame, text="Wind") #font?
        self.wind_label.grid(row=1, column=0, padx=10, pady=5)
        self.wind_value = ctk.CTkLabel(wind_frame, text="7 km/h") #font/direction symbols?
        self.wind_value.grid(row=1, column=0, sticky="n")

        # Humidity Frame -> Child of weather_frame
        humidity_frame = ctk.CTkFrame(weather_frame)
        humidity_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        humidity_frame.grid_columnconfigure(0, weight=1)
        self.humidity_label = ctk.CTkLabel(humidity_frame, text="Humidity") #font?
        self.humidity_label.grid(row=2, column=0, padx=10, pady=5)
        self.humidity_value = ctk.CTkLabel(humidity_frame, text="66%") #font/direction symbols?
        self.humidity_value.grid(row=1, column=0, sticky="n")
        
        # Precipitation Frame -? Child of weather_frame
        precip_frame = ctk.CTkFrame(weather_frame)
        precip_frame.grid(row=3, column=0, columnspan=2, pady=(10,20), sticky="nsew")
        precip_frame.grid_columnconfigure(0, weight=1)
        self.precip_label = ctk.CTkLabel(precip_frame, text="Chance of Precipitation:") #font?
        self.precip_label.grid(row=0, column=0, padx=10, pady=5)
        self.precip_value = ctk.CTkLabel(precip_frame, text="4%") #font/direction symbols?
        self.precip_value.grid(row=1, column=0, sticky="n")

        """ Connect to Features """
    def update_weather(self, city):
        data, error = self.weather_api.fetch_open_weather(city)
        if error:
            print("Error:", error)
            return
        weather = WeatherProcessor.extract_weather_info(data)
        """ Follow Up on this Comment dude """ 
        # self.display_weather(weather)
        # Features Frame -> Search bar and buttons to activate Features
    def _build_features_frame(self):
        features_frame = ctk.CTkFrame(self,corner_radius=15)
        features_frame.grid(row=1, column=3, columnspan=2, rowspan=3, padx=20, pady=20, sticky="nsew")

        for row in range(5):
            features_frame.grid_rowconfigure(row, weight=1)
        features_frame.grid_columnconfigure(0, weight=1)
        """ collect desire city from user-> TODO: pass to API/Data for retrieval. Set a default or us IP on start up to display current location at WeatherApp load time """
        # select_city
        city_entry = ctk.CTkEntry(features_frame, placeholder_text="Select City", corner_radius=15,)
        city_entry.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

        city_entry.bind("<Key>", lambda event: self.update_weather(city_entry.get()))

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
        weather_alerts_button = ctk.CTkButton(features_frame, text="Weather Alerts!!", corner_radius=15, command=lambda: self.controller.show_frame())
        weather_alerts_button.grid(row=4, padx=5, pady=10, sticky="ew")

    def _build_map_frame(self):
        map_frame = ctk.CTkFrame(self,corner_radius=15)
        map_frame.grid(row=1, column=5, columnspan=3, rowspan=3, padx=20, pady=20, sticky="nsew")

        for row in range(5):
            map_frame.grid_rowconfigure(row, weight=1)

    def _build_sun_frame(self):
        sun_frame = ctk.CTkFrame(self,corner_radius=15)
        sun_frame.grid(row=4, column=0, columnspan=3, rowspan=2, padx=20, pady=20, sticky="nsew")

        for row in range(2):
            sun_frame.grid_rowconfigure(row, weight=1)

    def _build_panic_button_frame(self):
        panic_frame = ctk.CTkFrame(self,corner_radius=15)
        panic_frame.grid(row=4, column=3, columnspan=2, rowspan=2, padx=20, pady=20, sticky="nsew")

        for row in range(2):
            panic_frame.grid_rowconfigure(row, weight=1)



    def _build_weather_control_frame(self):
        weather_control_frame = ctk.CTkFrame(self,corner_radius=15)
        weather_control_frame.grid(row=4, column=5, columnspan=3, rowspan=2, padx=20, pady=20, sticky="nsew")

        for row in range(2):
            weather_control_frame.grid_rowconfigure(row, weight=1)
    
       
        pass
        

        """ connected to HomePage via button-> plt graphs or other graphics? """
class ForecastPage(ctk.CTkFrame):
    def __init__(self,parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Forecast Page")
        label.grid(row=0, column=0)

        pass
        

        """ connected to HomePage via button-> This is for advanced feature and may be removed. Check on feature timeline. If required features not completed, remove TrendPage by 15/7/25 """
class TrendPage(ctk.CTkFrame):
    def __init__(self,parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Trend Page")
        label.grid(row=0, column=0)
    
        pass
        

        """ connected to Homepage via button-> prepare db/API calls/test by 10/7/25 """
class HistoricalPage(ctk.CTkFrame):
    def __init__(self,parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Historical Page")
        label.grid(row=0, column=0)
   
        pass
        

        """ Optional Fire information button-> Remove if not implemented by 10/7/25 """
class FirePage(ctk.CTkFrame):
    def __init__(self,parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Fire Page")
        label.grid(row=0, column=0)

        pass



""" For testing layout """
# if __name__ == "__main__":
    
#     app = App()
#     app.mainloop()