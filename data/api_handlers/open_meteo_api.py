import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from datetime import datetime, timedelta

class OpenMeteoAPI:
    def __init__(self):
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        self.openmeteo = openmeteo_requests.Client(session = retry_session)
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

    def fetch_historical_weather(self, select_city, target_date):
        """
        Fetch historical weather data for a specific date using official client
        """
        try:
            # First get coordinates for the city
            lat, lon = self._get_coordinates(select_city)
            if not lat or not lon:
                return None, f"City {select_city} not found."
            
            # Only fetch historical data (past dates)
            if target_date >= datetime.today().date():
                return None, "Use OpenWeatherAPI for current/future dates"
                
            return self._fetch_historical_data(lat, lon, select_city, target_date)
                
        except Exception as e:
            return None, str(e)

    def _get_coordinates(self, city_name):
        """Get lat/lon coordinates for a city using requests"""
        import requests
        
        try:
            params = {
                "name": city_name,
                "count": 1,
                "language": "en",
                "format": "json"
            }
            
            response = requests.get(self.geocoding_url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get('results') and len(data['results']) > 0:
                    result = data['results'][0]
                    return result['latitude'], result['longitude']
            return None, None
        except Exception:
            return None, None

    def _fetch_historical_data(self, lat, lon, city_name, target_date):
        """Fetch historical weather data using official Open-Meteo client"""
        try:
            date_str = target_date.strftime("%Y-%m-%d")
            
            url = "https://archive-api.open-meteo.com/v1/archive"
            params = {
                "latitude": lat,
                "longitude": lon,
                "start_date": date_str,
                "end_date": date_str,
                "daily": ["temperature_2m_max", "temperature_2m_min", "temperature_2m_mean"]
            }
            
            responses = self.openmeteo.weather_api(url, params=params)
            response = responses[0]
            
            # Process daily data
            daily = response.Daily()
            daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
            daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
            daily_temperature_2m_mean = daily.Variables(2).ValuesAsNumpy()
            
            # Get the values for the single day (first and only entry)
            temp_max = float(daily_temperature_2m_max[0]) if len(daily_temperature_2m_max) > 0 else None
            temp_min = float(daily_temperature_2m_min[0]) if len(daily_temperature_2m_min) > 0 else None
            temp_mean = float(daily_temperature_2m_mean[0]) if len(daily_temperature_2m_mean) > 0 else None
            
            # Return in a format compatible with existing processing
            weather_data = {
                'name': city_name,
                'main': {
                    'temp_max': temp_max,
                    'temp_min': temp_min,
                    'temp_mean': temp_mean
                },
                'coord': {'lat': lat, 'lon': lon}
            }
            
            return weather_data, None
                
        except Exception as e:
            return None, str(e)