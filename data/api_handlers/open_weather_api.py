import requests
import os
from dotenv import load_dotenv
from features.weather_extract import WeatherProcessor
import math
from PIL import Image
from io import BytesIO
import time


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
    def fetch_open_weather(self, select_city, language="en"):
        # Input validation
        if not select_city or not select_city.strip():
            return None, "City name cannot be empty"
        
        if len(select_city) > 100:
            return None, "City name is too long"
        
        # API key validation
        if not weather_api_key:
            return None, "Weather API key not configured"
        
        # Basic sanitization
        select_city = select_city.strip()
        
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
            
            response = requests.get(weather_url, params=params, timeout=5)
            
            if response.status_code == 200:
                try:
                    weather_json_data = response.json()
                    # Validate essential fields exist
                    if 'main' not in weather_json_data or 'weather' not in weather_json_data:
                        return None, "Invalid weather data format received"
                    return weather_json_data, None
                except ValueError:
                    return None, "Invalid JSON response from weather service"
            elif response.status_code == 401: 
                return self.alternate_fetch_open_weather(select_city, language)
                """ 401 API related/Handle through retry and alternate API """
            elif response.status_code == 404:
                return None, f"City '{select_city}' not found. Please check the spelling or try a nearby major city."
            elif response.status_code == 429:
                return None, "API rate limit exceeded. Please try again later."
            elif response.status_code in [500, 502, 503, 504]:
                # Try alternate API for server errors
                return self.alternate_fetch_open_weather(select_city, language)
            else:
                return None, f"Weather service error (Code: {response.status_code}). Please try again later."
                
        except requests.exceptions.Timeout:
            return None, "Request timed out. Please check your internet connection and try again."
        except requests.exceptions.ConnectionError:
            return None, "Unable to connect to weather service. Please check your internet connection."
        except requests.exceptions.RequestException as e:
            return None, f"Network error occurred: {str(e)}"
        except ValueError as e:
            return None, f"Invalid response format from weather service: {str(e)}"
        except KeyError as e:
            return None, f"Missing expected data in weather response: {str(e)}"
        except Exception as e:
            return None, f"Unexpected error: {str(e)}"
    
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

