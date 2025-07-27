from data.api_handlers.open_meteo_api import OpenMeteoAPI
import pandas as pd


class TrendandGraphProcessor:
    def __init__(self):
        self.api = OpenMeteoAPI()
        

    def process_city_trend(self, city_name):
        """ Open-Meteo returns pandas dataframe when using their API call builder """
        trend_df, error = self.api.meteo_forecast_and_trend(city_name)

        if error:
            return None, error
        
        trend_df = trend_df.set_index('date')
        trend_df = trend_df.sort_index()
        trend_df = trend_df.dropna()

        """ round to nearest decimal, Open-Meteo returns 6 places """
        trend_df['temperature_2m_max'] = trend_df['temperature_2m_max'].round(2)
        trend_df['temperature_2m_min'] = trend_df['temperature_2m_min'].round(2)
        
        """ TODO cleaning data here/could be another function. Let's see if we pull in more Open-Meteo calls and need a seperate process and cleaning function """
        
        return trend_df 
    


    def test_data_retrieval(self, city="Madrid"):
        """Quick test to see what processed data looks like"""
        print(f"=== Testing process_city_trend for {city} ===")
    
        processed_df = self.process_city_trend(city)
    
    # Check if we got an error
        if processed_df is None:
            print(f"Error retrieving data for {city}")
            return
    
        print(f"DataFrame Shape: {processed_df.shape}")
        print(f"Columns: {processed_df.columns.tolist()}")
        print(f"Date range: {processed_df.index.min()} to {processed_df.index.max()}")
        print(f"\nFirst few rows (formatted):")
    
    # Format the display to 2 decimal places
        with pd.option_context('display.float_format', '{:.2f}'.format):
            print(processed_df.head())
    
        print(f"\nData types:")
        print(processed_df.dtypes)
    
        print(f"\nActual values (should be clean 2 decimals):")
        for i in range(3):
            max_temp = processed_df.iloc[i]['temperature_2m_max']
            min_temp = processed_df.iloc[i]['temperature_2m_min']
            date = processed_df.index[i].strftime('%Y-%m-%d')
            print(f"{date}: Max={max_temp:.2f}°C, Min={min_temp:.2f}°C")

    def get_seven_day_data(self, city):
        """Get 7 days of temperature data centered on today"""
        try:
            trend_df = self.process_city_trend(city)
            if trend_df is None:
                return None, "Failed to get weather data"
            
            # Get today's date and find it in the data
            from datetime import datetime, timedelta
            today = datetime.now().date()
            
            # Convert DataFrame index to date for comparison
            df_dates = [date.date() for date in trend_df.index]
            
            # Find today's position in the data
            if today in df_dates:
                today_index = df_dates.index(today)
            else:
                # If today not found, use middle of available data
                today_index = len(df_dates) // 2
            
            # Calculate start and end indices for 7-day window (3 before, today, 3 after)
            start_index = max(0, today_index - 3)
            end_index = min(len(trend_df), today_index + 4)
            
            # Extract 7 days of data
            seven_day_data = trend_df.iloc[start_index:end_index]
            
            # Ensure we have exactly 7 days (pad with None if needed)
            max_temps = []
            min_temps = []
            dates = []
            
            for i in range(7):
                if i < len(seven_day_data):
                    max_temps.append(seven_day_data.iloc[i]['temperature_2m_max'])
                    min_temps.append(seven_day_data.iloc[i]['temperature_2m_min'])
                    # Format as "Day MM/DD" (e.g., "Mon 12/30")
                    date_str = seven_day_data.index[i].strftime('%a %m/%d')
                    dates.append(date_str)
                else:
                    max_temps.append(None)
                    min_temps.append(None)
                    dates.append("N/A")
            
            return {
                'max_temps': max_temps,
                'min_temps': min_temps,
                'dates': dates,
                'today_index': 3  # Day 4 is always today in our 7-day window
            }, None
            
        except Exception as e:
            return None, str(e)

    def calculate_trend_values(self, temp_list):
        """Calculate 3-day rolling average trend values for temperature list"""
        trends = []
        
        for i in range(len(temp_list)):
            if i < 2:  # First 2 days: can't calculate full 3-day average
                if temp_list[i] is not None and temp_list[i+1] is not None:
                    # Simple day-to-day change for first 2 days
                    trend = temp_list[i+1] - temp_list[i] if i < len(temp_list)-1 else 0
                else:
                    trend = 0
            else:  # Days 3-7: use 3-day rolling average
                # Calculate trend based on 3-day rolling average
                current_3day = [temp_list[i-2], temp_list[i-1], temp_list[i]]
                prev_3day = [temp_list[i-3], temp_list[i-2], temp_list[i-1]] if i > 2 else current_3day
                
                # Remove None values and calculate averages
                current_valid = [t for t in current_3day if t is not None]
                prev_valid = [t for t in prev_3day if t is not None]
                
                if len(current_valid) > 0 and len(prev_valid) > 0:
                    current_avg = sum(current_valid) / len(current_valid)
                    prev_avg = sum(prev_valid) / len(prev_valid)
                    trend = current_avg - prev_avg
                else:
                    trend = 0
            
            trends.append(trend)
        
        return trends

    def prepare_trend_display_data(self, city):
        """Prepare all data needed for TrendPage display"""
        try:
            # Get 7-day temperature data
            seven_day_data, error = self.get_seven_day_data(city)
            if error:
                return None, error
            
            max_temps = seven_day_data['max_temps']
            min_temps = seven_day_data['min_temps']
            dates = seven_day_data['dates']
            
            # Calculate trend values for arrows
            max_trends = self.calculate_trend_values(max_temps)
            min_trends = self.calculate_trend_values(min_temps)
            
            return {
                'max_temps': max_temps,
                'min_temps': min_temps,
                'max_trends': max_trends,
                'min_trends': min_trends,
                'dates': dates,
                'today_index': seven_day_data['today_index'],
                'city': city
            }, None
            
        except Exception as e:
            return None, str(e)
    
