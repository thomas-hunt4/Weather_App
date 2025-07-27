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
    
