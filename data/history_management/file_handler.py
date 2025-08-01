import csv
import os
from datetime import datetime

""" TODO As this file progresses, consider Class designation for organization, dependencies and reusability. """

""" Save weather default and search results for later access """

def save_weather(weather_data, filepath="data/history_management/weather_history.csv"):
    """ weather_data from Features.WeatherProcessor """
    
    # Handle coordinates - check if already flattened or needs flattening
    if 'coordinates' in weather_data:
        # Original format from WeatherProcessor
        coordinates = weather_data.pop('coordinates', {})
        weather_data['latitude'] = coordinates.get('lat')
        weather_data['longitude'] = coordinates.get('lon')
    # If latitude/longitude already exist as flat keys, leave them as-is

    # Add timestamp
    weather_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    file_exist = os.path.isfile(filepath)
    file_empty = not file_exist or os.path.getsize(filepath) == 0

    headers = ["timestamp", "date", "city", "temp_min", "temp_max", "temp_mean", "latitude", "longitude"]

    try:
        with open(filepath, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            
            # write header
            if file_empty:
                writer.writeheader()
            
            row = {
                "timestamp": weather_data.get('timestamp'),
                "date": weather_data.get('date', 'N/A'),
                "city": weather_data.get('city', 'Unknown'),
                "temp_min": round(weather_data.get('temp_min', 0), 2) if weather_data.get           ('temp_min') not in [None, 'N/A'] else 'N/A',
                "temp_max": round(weather_data.get('temp_max', 0), 2) if weather_data.get           ('temp_max') not in [None, 'N/A'] else 'N/A',
                "temp_mean": round(weather_data.get('temp_mean', 0), 2) if weather_data.get         ('temp_mean') not in [None, 'N/A'] else 'N/A',
                "latitude": round(weather_data.get('latitude', 0), 4) if weather_data.get           ('latitude') not in [None, 'N/A'] else 'N/A',
                "longitude": round(weather_data.get('longitude', 0), 4) if weather_data.get         ('longitude') not in [None, 'N/A'] else 'N/A',
            }

            # Write weather data row
            writer.writerow(row)
    except Exception as e:
        print(f"Error saving weather_data: {e}")


