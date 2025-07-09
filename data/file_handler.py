import csv
import os
from datetime import datetime

""" TODO As this file progresses, consider Class designation for organization, dependencies and reusability. """

""" Save weather default and search results for later access """

def save_weather(weather_data, filepath="data/weather_history.csv"):
    """ weather_data from Features.WeatherProcessor """
    file_exist = os.path.isfile(filepath)

    try:
        with open(filepath, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)

            # write header
            if not file_exist:
                writer.writerow(["timestamp", "city", "temperature", "description"])

        # Write weather data row
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                weather_data.get('city', 'Unknown'),
                weather_data.get('temperature', 'N\A'),
                weather_data.get('description', 'N/A')
        ])
    except Exception as e:
        print(f"Error saving weather_data: {e}")