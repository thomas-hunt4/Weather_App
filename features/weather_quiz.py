import pandas as pd
import random
import os

class WeatherQuiz:
    def __init__(self):
        self.merged_data = None
        self.current_question = None
        self.score = 0
        self.total_questions = 0
        self.quiz_data_path = "features/group_feature/merged_weather_data.csv"
        
        # Pre-generated questions based on data analysis
        # Track used questions to avoid repeats
        # Question set tracking - cycle through sets of 5
        self.questions_per_set = 5
        self.set_completed = False
        self.current_question_set = 0  # 0, 1, or 2
        self.current_question_index = 0  # 0-4 within current set
        
        # Column mapping for different naming conventions
        self.column_mappings = {
            'temperature_max': [
                'temperature_2m_max (°F)', 
                'temperature_2m_max (°C)',
                'temperature_2m (°F)',
                'temperature_2m (°C)'
            ],
            'temperature_min': [
                'temperature_2m_min (°F)', 
                'temperature_2m_min (°C)'
            ],
            'temperature_mean': [
                'temperature_2m_mean (°F)', 
                'temperature_2m_mean (°C)'
            ],
            'rain': [
                'rain_sum (inch)', 
                'rain_sum (mm)',
                'precipitation (mm)'
            ],
            'wind_speed': [
                'wind_speed_10m_max (mp/h)',
                'wind_speed_10m_max (km/h)',
                'wind_speed_10m (km/h)'
            ],
            'humidity': [
                'relative_humidity_2m_mean (%)',
                'relative_humidity_2m (%)'
            ]
        }
        
        # Load data and generate questions once
        self.load_and_merge_data()
        self.generate_predefined_questions()
    
    def find_column(self, column_type):
        """Find the actual column name for a given type in the merged data"""
        if self.merged_data is None:
            return None
        
        possible_names = self.column_mappings.get(column_type, [])
        for col_name in possible_names:
            if col_name in self.merged_data.columns:
                return col_name
        return None
    
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
                    if 'city' in df.columns:
                        dataframes.append(df)
                    else:
                        print(f"Warning: {file} missing 'city' column")
                except Exception as e:
                    print(f"Error reading {file}: {e}")
        
        if dataframes:
            self.merged_data = pd.concat(dataframes, ignore_index=True, sort=False)
            self.clean_data()
            self.save_merged_data()

        else:
            print("No valid CSV files found!")
    
    def clean_data(self):
        """Clean and standardize the merged data"""
        if self.merged_data is None:
            return
        
        # Convert numeric columns
        for column_type, possible_names in self.column_mappings.items():
            actual_column = self.find_column(column_type)
            if actual_column:
                self.merged_data[actual_column] = pd.to_numeric(
                    self.merged_data[actual_column], errors='coerce'
                )
        
        # Remove rows with missing city names
        self.merged_data = self.merged_data.dropna(subset=['city'])
    
    def save_merged_data(self):
        """Save merged data to CSV for future reference"""
        if self.merged_data is not None:
            try:
                os.makedirs(os.path.dirname(self.quiz_data_path), exist_ok=True)
                self.merged_data.to_csv(self.quiz_data_path, index=False)
            except Exception as e:
                print(f"Error saving merged data: {e}")
    
    def analyze_data_for_questions(self):
        """Analyze the data to find interesting facts for questions"""
        if self.merged_data is None:
            return {}
        
        analysis = {}
        
        # Temperature analysis
        temp_col = self.find_column('temperature_max')
        if temp_col:
            temp_data = self.merged_data.dropna(subset=[temp_col])
            if len(temp_data) > 0:
                # Hottest city
                max_temp_row = temp_data.loc[temp_data[temp_col].idxmax()]
                analysis['hottest_city'] = {
                    'city': max_temp_row['city'],
                    'temperature': max_temp_row[temp_col],
                    'column': temp_col
                }
                
                # Coldest city
                min_temp_row = temp_data.loc[temp_data[temp_col].idxmin()]
                analysis['coldest_city'] = {
                    'city': min_temp_row['city'],
                    'temperature': min_temp_row[temp_col],
                    'column': temp_col
                }
        
        # Rain analysis
        rain_col = self.find_column('rain')
        if rain_col:
            rain_data = self.merged_data.dropna(subset=[rain_col])
            rain_data = rain_data[rain_data[rain_col] > 0]  # Only rows with actual rain
            if len(rain_data) > 0:
                max_rain_row = rain_data.loc[rain_data[rain_col].idxmax()]
                analysis['rainiest_city'] = {
                    'city': max_rain_row['city'],
                    'rainfall': max_rain_row[rain_col],
                    'column': rain_col
                }
        
        # Wind analysis
        wind_col = self.find_column('wind_speed')
        if wind_col:
            wind_data = self.merged_data.dropna(subset=[wind_col])
            if len(wind_data) > 0:
                max_wind_row = wind_data.loc[wind_data[wind_col].idxmax()]
                analysis['windiest_city'] = {
                    'city': max_wind_row['city'],
                    'wind_speed': max_wind_row[wind_col],
                    'column': wind_col
                }
        
        # Humidity analysis
        humidity_col = self.find_column('humidity')
        if humidity_col:
            humidity_data = self.merged_data.dropna(subset=[humidity_col])
            if len(humidity_data) > 0:
                max_humidity_row = humidity_data.loc[humidity_data[humidity_col].idxmax()]
                analysis['most_humid_city'] = {
                    'city': max_humidity_row['city'],
                    'humidity': max_humidity_row[humidity_col],
                    'column': humidity_col
                }
        
        return analysis
    
    def generate_predefined_questions(self):
        """Generate 15 questions in 3 organized sets of 5 each"""
        if self.merged_data is None:

            # Create fallback questions if no data
            self.questions = self._create_fallback_questions()
            return
        
        analysis = self.analyze_data_for_questions()
        cities = list(self.merged_data['city'].unique())
        
        self.questions = []
        
        # SET 1: Temperature-based questions (Questions 1-5)
        
        # Question 1
        if 'hottest_city' in analysis:
            data = analysis['hottest_city']
            units = "°F" if "°F" in data['column'] else "°C"
            other_cities = [city for city in cities if city != data['city']]
            self.questions.append({
                'question': f"Which city recorded the highest temperature of {data['temperature']:.1f}{units}?",
                'correct_answer': data['city'],
                'wrong_answers': other_cities[:3],
                'type': 'multiple_choice'
            })
        else:
            self.questions.append({
                'question': "Which city is known for extreme desert heat?",
                'correct_answer': "Phoenix",
                'wrong_answers': ["Denver", "Columbus", "Lebrija"],
                'type': 'multiple_choice'
            })
        
        # Question 2
        if 'coldest_city' in analysis:
            data = analysis['coldest_city']
            units = "°F" if "°F" in data['column'] else "°C"
            other_cities = [city for city in cities if city != data['city']]
            self.questions.append({
                'question': f"Which city recorded the lowest temperature of {data['temperature']:.1f}{units}?",
                'correct_answer': data['city'],
                'wrong_answers': other_cities[:3],
                'type': 'multiple_choice'
            })
        else:
            self.questions.append({
                'question': "Which city has the coldest winters?",
                'correct_answer': "Denver",
                'wrong_answers': ["Phoenix", "Ahmedabad", "Lebrija"],
                'type': 'multiple_choice'
            })
        
        # Questions 3-5 for Set 1
        self.questions.extend([
            {
                'question': "Which city experiences the most temperature variation?",
                'correct_answer': "Denver",
                'wrong_answers': ["Phoenix", "Lebrija", "Ahmedabad"],
                'type': 'multiple_choice'
            },
            {
                'question': "Which city has consistently hot temperatures year-round?",
                'correct_answer': "Phoenix",
                'wrong_answers': ["Denver", "Columbus", "Lebrija"],
                'type': 'multiple_choice'
            },
            {
                'question': "Which city has moderate temperatures due to its location?",
                'correct_answer': "Lebrija",
                'wrong_answers': ["Phoenix", "Denver", "Ahmedabad"],
                'type': 'multiple_choice'
            }
        ])
        
        # SET 2: Weather pattern questions (Questions 6-10)
        
        
        # Question 6
        if 'rainiest_city' in analysis:
            data = analysis['rainiest_city']
            units = "inches" if "inch" in data['column'] else "mm"
            other_cities = [city for city in cities if city != data['city']]
            self.questions.append({
                'question': f"Which city received the most rainfall with {data['rainfall']:.2f} {units}?",
                'correct_answer': data['city'],
                'wrong_answers': other_cities[:3],
                'type': 'multiple_choice'
            })
        else:
            self.questions.append({
                'question': "Which city experiences monsoon weather patterns?",
                'correct_answer': "Ahmedabad",
                'wrong_answers': ["Phoenix", "Denver", "Columbus"],
                'type': 'multiple_choice'
            })
        
        # Questions 7-10 for Set 2
        remaining_set2 = [
            {
                'question': "Which city has the most arid climate?",
                'correct_answer': "Phoenix",
                'wrong_answers': ["Columbus", "Ahmedabad", "Lebrija"],
                'type': 'multiple_choice'
            },
            {
                'question': "Which city typically has the highest humidity?",
                'correct_answer': "Columbus",
                'wrong_answers': ["Phoenix", "Denver", "Lebrija"],
                'type': 'multiple_choice'
            },
            {
                'question': "Which city experiences the strongest winds?",
                'correct_answer': "Denver",
                'wrong_answers': ["Lebrija", "Columbus", "Ahmedabad"],
                'type': 'multiple_choice'
            },
            {
                'question': "Which city has Mediterranean climate characteristics?",
                'correct_answer': "Lebrija",
                'wrong_answers': ["Phoenix", "Denver", "Columbus"],
                'type': 'multiple_choice'
            }
        ]
        
        self.questions.extend(remaining_set2)
        
        # SET 3: Geographic questions (Questions 11-15)
        
        set3_questions = [
            {
                'question': "Which city is located in Spain?",
                'correct_answer': "Lebrija",
                'wrong_answers': ["Columbus", "Denver", "Phoenix"],
                'type': 'multiple_choice'
            },
            {
                'question': "Which city is the capital of Colorado?",
                'correct_answer': "Denver",
                'wrong_answers': ["Phoenix", "Columbus", "Ahmedabad"],
                'type': 'multiple_choice'
            },
            {
                'question': "Which city is located in Gujarat, India?",
                'correct_answer': "Ahmedabad",
                'wrong_answers': ["Lebrija", "Phoenix", "Denver"],
                'type': 'multiple_choice'
            },
            {
                'question': "Which city is in the Sonoran Desert?",
                'correct_answer': "Phoenix",
                'wrong_answers': ["Ahmedabad", "Columbus", "Denver"],
                'type': 'multiple_choice'
            },
            {
                'question': "Which city is in Ohio, USA?",
                'correct_answer': "Columbus",
                'wrong_answers': ["Phoenix", "Lebrija", "Ahmedabad"],
                'type': 'multiple_choice'
            }
        ]
        
        self.questions.extend(set3_questions)
        

    def _create_fallback_questions(self):
        """Create fallback questions if data loading fails"""
        return [
            # Set 1: Temperature
            {"question": "Which city is known for extreme desert heat?", "correct_answer": "Phoenix", "wrong_answers": ["Denver", "Columbus", "Lebrija"], "type": "multiple_choice"},
            {"question": "Which city has the coldest winters?", "correct_answer": "Denver", "wrong_answers": ["Phoenix", "Ahmedabad", "Lebrija"], "type": "multiple_choice"},
            {"question": "Which city experiences the most temperature variation?", "correct_answer": "Denver", "wrong_answers": ["Phoenix", "Lebrija", "Ahmedabad"], "type": "multiple_choice"},
            {"question": "Which city has consistently hot temperatures year-round?", "correct_answer": "Phoenix", "wrong_answers": ["Denver", "Columbus", "Lebrija"], "type": "multiple_choice"},
            {"question": "Which city has moderate temperatures due to its location?", "correct_answer": "Lebrija", "wrong_answers": ["Phoenix", "Denver", "Ahmedabad"], "type": "multiple_choice"},
            
            # Set 2: Weather patterns
            {"question": "Which city experiences monsoon weather patterns?", "correct_answer": "Ahmedabad", "wrong_answers": ["Phoenix", "Denver", "Columbus"], "type": "multiple_choice"},
            {"question": "Which city has the most arid climate?", "correct_answer": "Phoenix", "wrong_answers": ["Columbus", "Ahmedabad", "Lebrija"], "type": "multiple_choice"},
            {"question": "Which city typically has the highest humidity?", "correct_answer": "Columbus", "wrong_answers": ["Phoenix", "Denver", "Lebrija"], "type": "multiple_choice"},
            {"question": "Which city experiences the strongest winds?", "correct_answer": "Denver", "wrong_answers": ["Lebrija", "Columbus", "Ahmedabad"], "type": "multiple_choice"},
            {"question": "Which city has Mediterranean climate characteristics?", "correct_answer": "Lebrija", "wrong_answers": ["Phoenix", "Denver", "Columbus"], "type": "multiple_choice"},
            
            # Set 3: Geographic
            {"question": "Which city is located in Spain?", "correct_answer": "Lebrija", "wrong_answers": ["Columbus", "Denver", "Phoenix"], "type": "multiple_choice"},
            {"question": "Which city is the capital of Colorado?", "correct_answer": "Denver", "wrong_answers": ["Phoenix", "Columbus", "Ahmedabad"], "type": "multiple_choice"},
            {"question": "Which city is located in Gujarat, India?", "correct_answer": "Ahmedabad", "wrong_answers": ["Lebrija", "Phoenix", "Denver"], "type": "multiple_choice"},
            {"question": "Which city is in the Sonoran Desert?", "correct_answer": "Phoenix", "wrong_answers": ["Ahmedabad", "Columbus", "Denver"], "type": "multiple_choice"},
            {"question": "Which city is in Ohio, USA?", "correct_answer": "Columbus", "wrong_answers": ["Phoenix", "Lebrija", "Ahmedabad"], "type": "multiple_choice"}
        ]
    
    def generate_question(self):
        """Get the next question in current set, end after 5 questions"""
        if not self.questions:
            print("No questions available")
            return None
        
        # Check if current set is completed
        if self.current_question_index >= self.questions_per_set:
            self.set_completed = True
            return None
        
        # Calculate which question to show
        question_index = (self.current_question_set * 5) + self.current_question_index
        
        # Make sure we don't go out of bounds
        if question_index >= len(self.questions):
            self.set_completed = True
            return None
        
        # Get the current question
        self.current_question = self.questions[question_index]
        
        
        # ADVANCE POSITION FOR NEXT TIME
        self.current_question_index += 1
        
        return self.current_question

    def start_next_set(self):
        """Start the next set of 5 questions"""
        # Move to next set
        self.current_question_set = (self.current_question_set + 1) % 3
        self.current_question_index = 0
        self.set_completed = False
        
        return self.current_question_set + 1

    def get_current_set_info(self):
        """Get information about the current set"""
        set_names = ["Temperature Questions", "Weather Pattern Questions", "Geographic Questions"]
        current_set_name = set_names[self.current_question_set]
        return {
            'set_number': self.current_question_set + 1,
            'set_name': current_set_name,
            'questions_answered': self.current_question_index,
            'total_in_set': self.questions_per_set
        }
    
    def check_answer(self, user_answer):
        """Check if the user's answer is correct"""
        if not self.current_question:
            return False
        
        is_correct = user_answer.strip().lower() == self.current_question['correct_answer'].strip().lower()
        
        self.total_questions += 1
        if is_correct:
            self.score += 1
        
        return is_correct
    
    def get_score(self):
        """Get current score and percentage"""
        if self.total_questions == 0:
            return 0, 0
        
        percentage = (self.score / self.total_questions) * 100
        return self.score, percentage
    
    def get_score_percentage(self):
        """Get the current score as a percentage"""
        if self.total_questions == 0:
            return 0
        return (self.score / self.total_questions) * 100
    
    def reset_quiz(self):
        """Reset the quiz score and question tracking"""
        self.score = 0
        self.total_questions = 0
        self.current_question = None
        self.current_question_set = 0
        self.current_question_index = 0
        self.set_completed = False
        
    
    def get_quiz_stats(self):
        """Get current quiz statistics"""
        return {
            'score': self.score,
            'total_questions': self.total_questions,
            'percentage': self.get_score_percentage(),
            'cities_available': list(self.merged_data['city'].unique()) if self.merged_data is not None else [],
            'data_loaded': self.merged_data is not None,
            'questions_available': len(self.questions)
        }
    
    