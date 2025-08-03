import os
import schedule 
from schedule import every, repeat, run_pending
import time
import pandas as pd 
from datetime import datetime, timedelta
# Link Data and Feature files for interactions
from ..api_handlers.open_weather_api import OpenWeatherAPI
from ..api_handlers.open_meteo_api import OpenMeteoAPI
from features.weather_extract import WeatherProcessor
from data.history_management.file_handler import save_weather


""" Function to call Openweather_api to populate data as backup for when API is down for locations that are frequently searched or from a list of user favorites """

""" TODO save and sort top searched cities to df """
""" TODO pass the top 5 from df to list """
""" TODO allow user to add favorites and .append() list for api calls """



""" favorite cities import from user input in gui.v2gui.py """  




class ForecastArchiveAutomation:
    def __init__(self, search_log_path='data/history_management/weather_history.csv', history_path='data/history_management/historical_search.csv', limit=10):

        self.search_log_path = search_log_path
        self.history_path = history_path
        self.limit = limit
        self.weather_api = OpenWeatherAPI()  # Keep for current weather
        self.historical_api = OpenMeteoAPI()  # Add for historical data
        self.processor = WeatherProcessor()

    
    """ TODO check user entered search for top 10 locations searched by count """
    def get_top_searched(self):
        
        if os.path.exists(self.search_log_path):
            df = pd.read_csv(self.search_log_path)
            if not df.empty and 'city' in df.columns:
                return df['city'].value_counts().head(self.limit).index.tolist()
        return []
    
    """ TODO + GUI element that appends and returns list(limit=10) """
    def get_user_favorites(self):
        try:
            from data.user_preferences.favorites_manager import FavoritesManager
            favorites_manager = FavoritesManager()
            return favorites_manager.get_favorites()
        except:
            return []
    
    """ Combine list """
    def get_cities_list(self):
        top_searched = self.get_top_searched()
        user_favorites = self.get_user_favorites()

        all_cities = list(set(top_searched + user_favorites))
        return all_cities 
    
    """ update historical_search.csv to maintain a min 7 days of data available for comparison """
    def get_last_recorded_date(self):
        if os.path.exists(self.history_path):
            try:
                # Check if file is empty
                if os.path.getsize(self.history_path) == 0:
                    return datetime.today().date() - timedelta(days=7)
                
                df = pd.read_csv(self.history_path)
                if not df.empty and 'date' in df.columns:
                    try:
                        return pd.to_datetime(df['date']).max().date()
                    except Exception:
                        pass
            except Exception:
                pass

        return datetime.today().date() - timedelta(days=7)
    
    def _extract_minimal_weather_info(self, weather_json):
        """Extract only the fields we want for historical CSV"""
        if not weather_json:
            return None
    
        # Get temperature values and handle None values
        temp_max = weather_json['main'].get('temp_max')
        temp_min = weather_json['main'].get('temp_min') 
        temp_mean = weather_json['main'].get('temp_mean')
    
        return {
            'city': weather_json['name'],
            'temp_max': round(temp_max, 2) if temp_max is not None else None,
            'temp_min': round(temp_min, 2) if temp_min is not None else None,
            'temp_mean': round(temp_mean, 2) if temp_mean is not None else None,
            'latitude': round(weather_json['coord']['lat'], 4),
            'longitude': round(weather_json['coord']['lon'], 4)
        }

    def populate_history(self):
        today = datetime.today().date()
        last_date = self.get_last_recorded_date()
        cities = self.get_cities_list()

        print(f"Today: {today}")
        print(f"Last recorded date: {last_date}")
        print(f"Cities to process: {cities}")

        if not cities:
            print("No cities to process")
            return
        
        days_diff = (today - last_date).days
        if days_diff <= 0:
            print("History is up to date")
            return
        
        date_range = [last_date + timedelta(days=i) for i in range(1, days_diff + 1)]
        print(f"DEBUG - Date range to process: {date_range}")

        for city in cities:
            for target_date in date_range:
                try:
                    # Use different APIs based on date
                    if target_date < datetime.today().date():
                        # Use Open-Meteo for historical data
                        weather_response, error = self.historical_api.fetch_historical_weather(city, target_date)
                        if not weather_response or error:
                            print(f"Failed to get weather data for {city} on {target_date}. Error: {error}")
                            continue
                
                        # Use custom extraction for historical data
                        processed = self._extract_minimal_weather_info(weather_response)
                
                    else:
                        # Use OpenWeather for current data
                        weather_response, error = self.weather_api.fetch_open_weather(city)
                        if not weather_response or error:
                            print(f"Failed to get weather data for {city} on {target_date}. Error: {error}")
                            continue
                
                        # Use WeatherProcessor extraction for current data
                        processed = self.processor.extract_minimal_weather_info(weather_response)
            
                    if not processed:
                        print(f"Failed to process weather data for {city} on {target_date}")
                        continue

                    # Add the date
                    processed['date'] = target_date.strftime("%Y-%m-%d")
            
                    # Save to historical file
                    save_weather(processed, filepath=self.history_path)

                    print(f"Successfully saved weather data for {city} on {target_date}")

                    # Add small delay to avoid hitting API rate limits
                    # time.sleep(0.1)

                except Exception as e:
                    print(f"Error processing {city} on {target_date}: {e}")
                    continue

    """ Run daily or on start-up to keep baseline data available for fallback, processing and GUI """
    def run_daily(self):
        schedule.every().day.at("01:00").do(self.populate_history)

    def run_once(self):
        self.populate_history()


def main():
    scheduler = ForecastArchiveAutomation()

    scheduler.run_once()

    scheduler.run_daily()

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()