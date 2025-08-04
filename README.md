# Weather App - Advanced Weather Information System

A comprehensive weather application built with Python and CustomTkinter, featuring real-time weather data, forecasting, weather alerts with SMS notifications, and interactive visualizations.

## Features

### Core Features
- **Real-time Weather Data**: Current weather conditions using OpenWeatherMap API
- **4-Day Forecast**: Accurate extended weather forecasting with Open-Meteo API
- **Location Detection**: Automatic location detection via IP geolocation
- **Historical Weather Data**: Access to past weather information
- **Theme Switching**: Light/Dark mode toggle for better user experience

### Advanced Features
- **Weather Alerts & SMS**: Severe weather notifications with Twilio SMS integration
- **Temperature Trends**: Visual graphs and trend analysis
- **Weather Quiz**: Interactive weather knowledge quiz
- **User Registration**: Personal weather alert preferences
- **Favorites System**: Save frequently searched locations
- **Multi-language Support**: English, Hindi, and Spanish (planned)

### Custom Enhancements
- **Trend Detection**: Intelligent weather pattern recognition
- **Auto History Building**: Automated data collection for popular cities
- **Advanced Error Handling**: Comprehensive error management with fallback APIs
- **Data Persistence**: CSV-based storage for weather history and user preferences

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd weather-project
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory with the following variables:

```env
# OpenWeatherMap API Keys
open_weather_key=your_primary_openweather_api_key
alternate_open_weather_api_key=your_backup_openweather_api_key
open_weather_url=https://api.openweathermap.org/data/2.5/weather
open_weather_geo_url=https://api.openweathermap.org/geo/1.0/direct

# Twilio Configuration (for SMS alerts)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token  
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# Optional: Additional API configurations
# Add other API keys as needed
```

### 4. API Key Setup

#### OpenWeatherMap API
1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Generate your API key
4. Add the key to your `.env` file

#### Twilio SMS (Optional - for weather alerts)
1. Sign up at [Twilio](https://www.twilio.com/)
2. Get your Account SID and Auth Token
3. Purchase a Twilio phone number
4. Add credentials to your `.env` file

### 5. Run the Application
```bash
python main.py
```

## Usage Guide

### Basic Weather Lookup
1. **Launch the app**: Run `python main.py`
2. **Enter location**: Type a city name in the search bar
3. **View weather**: Current conditions display automatically
4. **Explore features**: Use the navigation tabs to access different features

### Setting Up Weather Alerts
1. Navigate to the **Weather Alerts** section
2. Register your phone number for SMS notifications
3. Set your alert preferences (severe weather, temperature thresholds)
4. Alerts will be sent automatically when conditions are met

### Using Advanced Features
- **Forecast**: View 4-day weather predictions with temperature trends
- **History**: Access historical weather data for any location
- **Quiz**: Test your weather knowledge with interactive questions
- **Themes**: Toggle between light and dark modes in the settings

### Data Storage
- Weather search history is saved to `data/history_management/weather_history.csv`
- User preferences stored in `data/user_preferences/`
- Favorite locations managed through the favorites system

## Project Structure

```
WEATHER-PROJECT/
├── data/                           # Data management modules
│   ├── api_handlers/              # API integration classes
│   │   ├── open_weather_api.py    # OpenWeatherMap API handler
│   │   ├── open_meteo_api.py      # Open-Meteo API handler
│   │   └── send_sms.py            # Twilio SMS integration
│   ├── history_management/        # Data persistence
│   │   ├── file_handler.py        # File I/O operations
│   │   ├── auto_api_history_builder.py # Automated data collection
│   │   └── weather_history.csv    # Historical weather records
│   └── user_preferences/          # User data management
│       ├── user_registration_manager.py # User registration system
│       └── favorites_manager.py   # Favorite locations handler
│
├── features/                      # Feature modules
│   ├── __init__.py
│   ├── weather_extract.py         # Weather data processing
│   ├── alerts.py                  # Weather alert system
│   ├── trend_and_graph.py         # Trend analysis and graphing
│   └── weather_quiz.py            # Interactive weather quiz
│
├── gui/                           # User interface
│   ├── __init__.py
│   ├── v2gui_main.py             # Main GUI application
│   ├── pages/                     # Individual page components
│   │   ├── home_page.py          # Main weather display
│   │   ├── forecast_page.py      # 7-day forecast
│   │   ├── weather_alerts_window.py # Alert management
│   │   └── quiz_page.py          # Weather quiz interface
│   └── components/               # Reusable UI components
│
├── tests/                        # Unit tests
│   ├── __init__.py
│   └── features_test.py          # Feature testing suite
│
├── docs/                         # Documentation
│   ├── Week11_Reflection.md      # Project planning document
│   └── LICENSE                   # Project license
│
├── screenshots/                  # UI screenshots for documentation
├── .env                         # Environment variables (not in repo)
├── .gitignore                   # Git ignore rules
├── config.py                    # Global configuration settings
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Dependencies

Key Python packages used in this project:

```txt
customtkinter>=5.0.0          # Modern UI framework
requests>=2.28.0              # HTTP requests for APIs
python-dotenv>=0.19.0         # Environment variable management
pandas>=1.5.0                 # Data manipulation and analysis
openmeteo-requests>=1.0.0     # Open-Meteo API client
requests-cache>=0.9.0         # API response caching
retry-requests>=1.0.0         # Request retry logic
twilio>=7.16.0               # SMS notifications
schedule>=1.1.0              # Task scheduling
pillow>=9.0.0                # Image processing
matplotlib>=3.6.0            # Data visualization (if used)
```

## Configuration

### Theme Configuration
The app supports both light and dark themes. Theme preference is saved and restored on app restart.

### Language Support
Currently supports English with planned expansion to Hindi and Spanish. Language setting affects:
- Weather condition descriptions
- UI text elements
- Alert messages

### Data Management
- Automatic cleanup of old weather data
- Configurable data retention periods
- Export capabilities for weather history

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Verify your API keys are correct in the `.env` file
   - Check that your OpenWeatherMap API key is activated
   - Ensure you haven't exceeded your API rate limits

2. **SMS Alerts Not Working**
   - Confirm Twilio credentials are correct
   - Verify your Twilio phone number is SMS-enabled
   - Check that recipient phone numbers are in valid format

3. **Location Not Found**
   - Try different variations of city names
   - Include country code for international cities
   - Check spelling and try major cities nearby

4. **GUI Issues**
   - Ensure CustomTkinter is properly installed
   - Update to latest version: `pip install --upgrade customtkinter`
   - Check Python version compatibility

### Getting Help
- Check the `tests/` directory for usage examples
- Review error messages in the console output
- Ensure all required environment variables are set

## Contributing

When contributing to this project:
1. Follow the existing code structure and naming conventions
2. Add appropriate error handling and logging
3. Update tests for new features
4. Document any new configuration options
5. Test thoroughly with different weather conditions and locations

## License

This project is licensed under the terms specified in the `docs/LICENSE` file.

## Development Status

Current implementation includes:
- ✅ Core weather functionality
- ✅ GUI with multiple pages
- ✅ Weather alerts and SMS integration  
- ✅ Theme switching
- ✅ Basic error handling
- 🔄 Enhanced error handling (in progress)
- 🔄 Temperature graphing (in progress)
- 📋 Language selection (planned)

---

## References

### Graphics and Icons
**MoonPhase graphics**  
https://www.vecteezy.com/vector-art/57967153-moons-set-black-yellow
<a href="https://www.vecteezy.com/free-vector/moon">Moon Vectors by Vecteezy</a>  

**Icons for trend display**  
<a target="_blank" href="https://icons8.com/icon/7zlXzrTyT4H4/right-arrow">Arrow</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>

### Libraries and Dependencies
**`schedule` library** for most searched/favorite cities historical data  
https://schedule.readthedocs.io/en/stable/

**CustomTkinter** for modern GUI components  
https://github.com/TomSchimansky/CustomTkinter

**OpenWeatherMap API** for current weather data  
https://openweathermap.org/api

**Open-Meteo API** for forecasting and historical data  
https://open-meteo.com/

**Twilio** for SMS alert notifications  
https://www.twilio.com/docs/sms

