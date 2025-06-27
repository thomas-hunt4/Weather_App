import requests
import os
from dotenv import load_dotenv
from gui.gui_main import select_city

# import API Keys and URLs from .env
load_dotenv()

# Open Weather API and URL
weather_api_key = os.getenv("open_weather_key")
weather_url = os.getenv("open_weather_url")

# Open Weather Geo URL
ow_geo_url = os.getenv("open_weather_geo_url")

""" Handling Open Weather API as stand alone """
class OpenWeatherAPI:
    def fetch_open_weather(select_city):
        try: 
            params = {
                "?q=": select_city,
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
    def fetch_open_geo():
        try:
            params = {
                "?q=": {select_city},
                "&limit=": "5",
                "&appid=": {weather_api_key}
            }

            response = requests.get(ow_geo_url, params=params)
            if response.status_code == 200:
                return response.json(), None
            else:
                return None, f"***PLACE**HOLDER**OPEN_WEATHER_API.PY***"
        except Exception as e:
            return None, str(e)
    
