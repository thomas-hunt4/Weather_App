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
alternate_api_key = os.getenv("alternate_open_weather_api_key")

# Open Weather Geo URL
ow_geo_url = os.getenv("open_weather_geo_url")

""" Handling Open Weather API for weather, geo, and associated """
class OpenWeatherAPI:
    def fetch_open_weather(self,select_city, language="en"):
        try: 
            params = {
                "q": select_city,
                "appid": weather_api_key, 
                "units": "metric",
                "lang": language 
            } 
            """ TODO temp_unit_select  #create function in logic to handle and attach to button selector """
            """ 
    Revisit for other response codes/developer tab relay/API call counter function 
            """
            
            response = requests.get(weather_url, params=params)
            if response.status_code == 200:
                weather_json_data = response.json()
                # print(weather_json_data)
                return weather_json_data, None
            elif response.status_code == 401: 
                return self.alternate_fetch_open_weather(select_city)
                """ 401 API related/Handle through retry and alternate API """
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

        
    def alternate_fetch_open_weather(self, select_city, language="en"):
        try: 
            params = {
                "q": select_city,
                "appid": alternate_api_key, 
                "units": "metric",
                "lang": language 
            } 
            """ This is primarily to handle bad/expired API key and will have nominal error handling before kicking to tertiary """
            
            response = requests.get(weather_url, params=params)
            
            if response.status_code == 200:
                weather_json_data = response.json()
                return weather_json_data, None
            # elif response.status_code == 401: 
                
               
                """ 401 API related/Handle through retry and alternate API """
            else:
                return None, f"City {select_city} not found."
        except Exception as e:
            return None, str(e)

