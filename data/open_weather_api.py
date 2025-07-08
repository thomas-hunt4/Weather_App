import requests
import os
from dotenv import load_dotenv
from features.weather_extract import WeatherProcessor
import math
from PIL import Image
from io import BytesIO


city = WeatherProcessor.select_city()

# import API Keys and URLs from .env
load_dotenv()

# Open Weather API and URL
weather_api_key = os.getenv("open_weather_key")
weather_url = os.getenv("open_weather_url")

# Open Weather Geo URL
ow_geo_url = os.getenv("open_weather_geo_url")

""" Handling Open Weather API as stand alone """
class OpenWeatherAPI:
    def fetch_open_weather(self,select_city):
        try: 
            params = {
                "q": select_city,
                "appid": weather_api_key, 
                "units": "metric" #temp_unit_select  #create function in logic to handle and attach to button selector
            }
            """ 
    Revisit for other response codes/developer tab relay/API call counter function 
            """
            response = requests.get(weather_url, params=params)
            if response.status_code == 200:
                weather_json_data = response.json()
                return weather_json_data, None
            else:
                return None, f"City {select_city} not found."
        except Exception as e:
            return None, str(e)
    
    """ fetch lat/lon and location information for maps/other features """
    def fetch_open_geo(select_city):
        try:
            params = {
                "q": select_city,
                "limit": "5",
                "appid": weather_api_key
            }

            response = requests.get(ow_geo_url, params=params)
            if response.status_code == 200:
                return response.json(), None
            else:
                return None, f"***PLACE**HOLDER**GEO***OPEN_WEATHER_API.PY***"
        except Exception as e:
            return None, str(e)

    """ locate by IP for real vs default weather values on load """    
    def get_location_by_ip(self):
        try:
            response = requests.get("http://ip-api.com/json/")
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success':
                    return data['city'], None
                else:
                    return None, "Could not determine location from IP"
            else:
                return None, "IP geolocation service unavailable"
        except Exception as e:
            return None, str(e)


    # """ Convert lat/lon into Tile based format for map display """
    """ TODO make a decision on whether or not to tie user input to fixed list of city options. If using fixed list then perhaps tie this conversion to the lat/lon data stored in that list. """
    def deg2num(self, lat_deg, lon_deg, zoom):
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        x = int((lon_deg + 180.0) / 360.0 * n)
        y = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        return (x, y)

    def fetch_weather_map(self, lat, lon, layer="clouds_new", zoom=4):
        try:
            x, y = self.deg2num(lat, lon, zoom)
            url = f"https://tile.openweathermap.org/map/{layer}/{zoom}/{x}/{y}.png?appid={weather_api_key}"
        
            response = requests.get(url)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                return image, None
            else:
                return None, f"Failed to fetch weather map: {response.status_code}"
        except Exception as e:
            return None, str(e)
        
    def get_available_map_layers(self):
        return {
        "Clouds": "clouds_new",
        "Precipitation": "precipitation_new", 
        "Pressure": "pressure_new",
        "Wind Speed": "wind_new",
        "Temperature": "temp_new"
    }
