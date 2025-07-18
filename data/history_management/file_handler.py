import csv
import os
from datetime import datetime

""" TODO As this file progresses, consider Class designation for organization, dependencies and reusability. """

""" Save weather default and search results for later access """

def save_weather(weather_data, filepath="data/history_management/weather_history.csv"):
    """ weather_data from Features.WeatherProcessor """
     # Flatten coordinates
    coordinates = weather_data.pop('coordinates', {})
    weather_data['latitude'] = coordinates.get('lat')
    weather_data['longitude'] = coordinates.get('lon')

    # Add timestamp
    weather_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    file_exist = os.path.isfile(filepath)
    file_empty = not file_exist or os.path.getsize(filepath) == 0

    headers = ["timestamp", "date", "city", "humidity", "temperature", "description", "latitude", "longitude"]

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
                "humidity": weather_data.get('humidity', 'N/A'),
                "temperature": weather_data.get('temperature', 'N/A'),
                "description": weather_data.get('description', 'N/A'),
                "latitude": weather_data.get('latitude', 'N/A'),
                "longitude": weather_data.get('longitude', 'N/A'),
            }

        # Write weather data row
            writer.writerow(row)
            """ debug print """
        # print("Received data to save:", weather_data)
    except Exception as e:
        print(f"Error saving weather_data: {e}")


