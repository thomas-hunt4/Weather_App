import pandas as pd
import random
import os
from datetime import datetime

class WeatherQuiz:
    def __init__(self):
        self.merged_data = None
        self.current_question = None
        self.score = 0
        self.total_questions = 0
        self.quiz_data_path = "features/group_feature/merged_weather_data.csv"
        
        # Load and merge data on initialization
        self.load_and_merge_data()
    
    def load_and_merge_data(self):
        """Load and merge all CSV files into one dataset"""
        csv_files = [
            "features/group_feature/columbus.csv",
            "features/group_feature/Denver.csv", 
            "features/group_feature/phoenix2024.csv",
            "features/group_feature/Ahmedabad.csv",
            "features/group_feature/Lebrija.csv"
        ]
        
        dataframes = []
        
        for file in csv_files:
            if os.path.exists(file):
                try:
                    df = pd.read_csv(file)
                    # Standardize column names and ensure city column exists
                    if 'city' in df.columns:
                        dataframes.append(df)
                    else:
                        print(f"Warning: {file} missing 'city' column")
                except Exception as e:
                    print(f"Error reading {file}: {e}")
        
        if dataframes:
            # Merge all dataframes
            self.merged_data = pd.concat(dataframes, ignore_index=True, sort=False)
            
            # Clean and standardize data
            self.clean_data()
            
            # Save merged data for future use
            self.save_merged_data()
            print(f"Loaded data for {len(self.merged_data['city'].unique())} cities")
        else:
            print("No valid CSV files found!")
    
    def clean_data(self):
        """Clean and standardize the merged data"""
        if self.merged_data is None:
            return
        
        # Convert temperature columns to numeric, handling different naming conventions
        temp_columns = ['temperature_2m_max (°F)', 'temperature_2m_min (°F)', 'temperature_2m_mean (°F)']
        for col in temp_columns:
            if col in self.merged_data.columns:
                self.merged_data[col] = pd.to_numeric(self.merged_data[col], errors='coerce')
        
        # Convert other numeric columns
        numeric_cols = ['rain_sum (inch)', 'snowfall_sum (inch)', 'wind_speed_10m_max (mp/h)', 
                       'relative_humidity_2m_mean (%)', 'cloud_cover_mean (%)']
        
        for col in numeric_cols:
            if col in self.merged_data.columns:
                self.merged_data[col] = pd.to_numeric(self.merged_data[col], errors='coerce')
        
        # Remove rows with all NaN values in key columns
        self.merged_data = self.merged_data.dropna(subset=['city'])
    
    def save_merged_data(self):
        """Save merged data to CSV for future reference"""
        if self.merged_data is not None:
            os.makedirs(os.path.dirname(self.quiz_data_path), exist_ok=True)
            self.merged_data.to_csv(self.quiz_data_path, index=False)
    
    def generate_temperature_question(self):
        """Generate a question about temperature comparisons"""
        if self.merged_data is None:
            return None
        
        # Get cities with valid temperature data
        temp_col = 'temperature_2m_max (°F)'
        if temp_col not in self.merged_data.columns:
            return None
        
        valid_data = self.merged_data.dropna(subset=[temp_col])
        if len(valid_data) < 2:
            return None
        
        # Get random sample of cities
        cities = valid_data['city'].unique()
        if len(cities) < 2:
            return None
        
        # Random question types
        question_types = ['hottest_city', 'coldest_city', 'temperature_range']
        question_type = random.choice(question_types)
        
        if question_type == 'hottest_city':
            # Find the city with highest max temperature
            max_temp_row = valid_data.loc[valid_data[temp_col].idxmax()]
            correct_city = max_temp_row['city']
            max_temp = max_temp_row[temp_col]
            
            # Get other cities for wrong answers
            other_cities = [city for city in cities if city != correct_city]
            wrong_answers = random.sample(other_cities, min(3, len(other_cities)))
            
            return {
                'question': f"Which city recorded the highest temperature of {max_temp:.1f}°F?",
                'correct_answer': correct_city,
                'wrong_answers': wrong_answers,
                'type': 'multiple_choice'
            }
        
        elif question_type == 'coldest_city':
            temp_min_col = 'temperature_2m_min (°F)'
            if temp_min_col in valid_data.columns:
                min_temp_row = valid_data.loc[valid_data[temp_min_col].idxmin()]
                correct_city = min_temp_row['city']
                min_temp = min_temp_row[temp_min_col]
                
                other_cities = [city for city in cities if city != correct_city]
                wrong_answers = random.sample(other_cities, min(3, len(other_cities)))
                
                return {
                    'question': f"Which city recorded the lowest temperature of {min_temp:.1f}°F?",
                    'correct_answer': correct_city,
                    'wrong_answers': wrong_answers,
                    'type': 'multiple_choice'
                }
        
        return None
    
    def generate_weather_pattern_question(self):
        """Generate questions about weather patterns"""
        if self.merged_data is None:
            return None
        
        rain_col = 'rain_sum (inch)'
        if rain_col not in self.merged_data.columns:
            return None
        
        valid_data = self.merged_data.dropna(subset=[rain_col])
        if len(valid_data) < 2:
            return None
        
        # Find city with most rainfall
        max_rain_row = valid_data.loc[valid_data[rain_col].idxmax()]
        if max_rain_row[rain_col] == 0:
            return None  # Skip if no rain data
        
        correct_city = max_rain_row['city']
        max_rain = max_rain_row[rain_col]
        
        cities = valid_data['city'].unique()
        other_cities = [city for city in cities if city != correct_city]
        wrong_answers = random.sample(other_cities, min(3, len(other_cities)))
        
        return {
            'question': f"Which city received the most rainfall with {max_rain:.3f} inches?",
            'correct_answer': correct_city,
            'wrong_answers': wrong_answers,
            'type': 'multiple_choice'
        }
    
    def generate_humidity_question(self):
        """Generate questions about humidity"""
        if self.merged_data is None:
            return None
        
        humidity_col = 'relative_humidity_2m_mean (%)'
        if humidity_col not in self.merged_data.columns:
            return None
        
        valid_data = self.merged_data.dropna(subset=[humidity_col])
        if len(valid_data) < 2:
            return None
        
        # Find city with highest humidity
        max_humidity_row = valid_data.loc[valid_data[humidity_col].idxmax()]
        correct_city = max_humidity_row['city']
        max_humidity = max_humidity_row[humidity_col]
        
        cities = valid_data['city'].unique()
        other_cities = [city for city in cities if city != correct_city]
        wrong_answers = random.sample(other_cities, min(3, len(other_cities)))
        
        return {
            'question': f"Which city had the highest humidity of {max_humidity:.0f}%?",
            'correct_answer': correct_city,
            'wrong_answers': wrong_answers,
            'type': 'multiple_choice'
        }
    
    def generate_question(self):
        """Generate a random weather question"""
        question_generators = [
            self.generate_temperature_question,
            self.generate_weather_pattern_question, 
            self.generate_humidity_question
        ]
        
        # Try different question types until we get a valid question
        random.shuffle(question_generators)
        
        for generator in question_generators:
            question = generator()
            if question:
                self.current_question = question
                return question
        
        return None
    
    def check_answer(self, user_answer):
        """Check if the user's answer is correct"""
        if not self.current_question:
            return False
        
        is_correct = user_answer.strip().lower() == self.current_question['correct_answer'].strip().lower()
        
        if is_correct:
            self.score += 1
        
        self.total_questions += 1
        return is_correct
    
    def get_score(self):
        """Get current score and percentage"""
        if self.total_questions == 0:
            return 0, 0
        
        percentage = (self.score / self.total_questions) * 100
        return self.score, percentage
    
    def reset_quiz(self):
        """Reset quiz statistics"""
        self.score = 0
        self.total_questions = 0
        self.current_question = None