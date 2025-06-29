import json
from datetime import datetime


""" View raw data for key value extractions """
class WeatherProcessor:
    def view_raw_json(data, title="API Response"):
        print(f"\n==={title} ===")
        print(json.dumps(data, indent=2))


    def extract_weather_info(weather_json):
        """Extract key weather information from API response"""
        if not weather_json:
            return None
    
        # Basic weather info
        city = weather_json['name']
        country = weather_json['sys']['country']
        temp = weather_json['main']['temp']
        feels_like = weather_json['main']['feels_like']
        humidity = weather_json['main']['humidity']
        pressure = weather_json['main']['pressure']
    
        # Weather description
        weather_desc = weather_json['weather'][0]['description']
        weather_main = weather_json['weather'][0]['main']
    
        # Wind info
        wind_speed = weather_json['wind']['speed']
        wind_direction = weather_json['wind'].get('deg', 'N/A')
    
        # Other info
        cloudiness = weather_json['clouds']['all']
        visibility = weather_json.get('visibility', 'N/A')
    
        # Coordinates
        lat = weather_json['coord']['lat']
        lon = weather_json['coord']['lon']
    
        # Sunrise/sunset (convert from timestamp)
        sunrise = datetime.fromtimestamp(weather_json['sys']['sunrise']).strftime   ('%H:%M:%S')
        sunset = datetime.fromtimestamp(weather_json['sys']['sunset']).strftime ('%H:%M:%S')
    
        return {
            'city': city,
            'country': country,
            'temperature': temp,
            'feels_like': feels_like,
            'humidity': humidity,
            'pressure': pressure,
            'description': weather_desc,
            'main_weather': weather_main,
            'wind_speed': wind_speed,
            'wind_direction': wind_direction,
            'cloudiness': cloudiness,
            'visibility': visibility,
            'coordinates': {'lat': lat, 'lon': lon},
            'sunrise': sunrise,
            'sunset': sunset
        }
    
    """Extract location information from geo API response"""
    def extract_geo_info(geo_json):
        if not geo_json or not isinstance(geo_json, list):
            return None
    
        locations = []
        for location in geo_json:
            try:
                locations.append({
                    'name': location['name'],
                    'country': location['country'],
                    'state': location.get('state', 'N/A'),
                    'latitude': location['lat'],
                    'longitude': location['lon']
                })
            except KeyError as e:
                print(f"Error extracting geo data: Missing key {e}")
                continue
    
        return locations
    
    """ Select location through user input for Weather and Geo request    """
    # @staticmethod
    def select_city():
        pass 
    
    """ Alter API call for 'units' metric/imperial """
    def temp_unit_converter():
        pass


