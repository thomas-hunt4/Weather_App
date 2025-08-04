# API Handlers Documentation

This directory contains all API integration modules for the Weather Application. Each file handles specific external service interactions with comprehensive error handling and fallback mechanisms.

## File Overview

### `open_weather_api.py`
**Primary weather data provider using OpenWeatherMap API**

**Key Features:**
- Current weather conditions by city name
- Geographic coordinate lookup for cities
- IP-based location detection
- Dual API key support for reliability
- Multi-language weather descriptions

**Main Methods:**
```python
fetch_open_weather(select_city, language="en")
# Returns: (weather_data, error) tuple
# Fetches current weather with fallback to alternate API key

fetch_open_geo(select_city) 
# Returns: (geo_data, error) tuple
# Gets latitude/longitude coordinates for mapping

get_location_by_ip()
# Returns: (city_name, error) tuple  
# Detects user location via IP geolocation

alternate_fetch_open_weather(select_city, language="en")
# Backup method using secondary API key
```

**Error Handling:**
- HTTP status code validation
- API key rotation on 401 errors
- Network timeout handling
- Invalid city name detection
- Rate limit management

**Configuration Required:**
```env
open_weather_key=your_primary_api_key
alternate_open_weather_api_key=your_backup_api_key
open_weather_url=https://api.openweathermap.org/data/2.5/weather
open_weather_geo_url=https://api.openweathermap.org/geo/1.0/direct
```

---

### `open_meteo_api.py`
**Historical weather data and extended forecasting using Open-Meteo API**

**Key Features:**
- Historical weather data retrieval
- 7-day weather forecasting
- Coordinate-based weather lookups
- Built-in caching and retry logic
- No API key required (free service)

**Main Methods:**
```python
fetch_historical_weather(select_city, target_date)
# Returns: (historical_data, error) tuple
# Gets weather data for specific past dates

meteo_forecast_and_trend(city_name)
# Returns: (pandas_dataframe, error) tuple
# Provides 7-day forecast with temperature trends

_get_coordinates(city_name)
# Internal method for city coordinate lookup
# Returns: (latitude, longitude) tuple
```

**Error Handling:**
- Automatic retry with exponential backoff
- Response caching to reduce API calls
- Date validation (historical vs. future)
- City name geocoding validation
- Network connectivity checks

**Data Format:**
Returns pandas DataFrames with columns:
- `date`: Date of forecast/historical data
- `temperature_2m_max`: Maximum temperature (°C)
- `temperature_2m_min`: Minimum temperature (°C)
- Additional meteorological parameters

---

### `send_sms.py`
**SMS notification system using Twilio API**

**Key Features:**
- Weather alert SMS notifications
- User registration system integration
- Message formatting and templating
- Delivery status tracking
- Error logging and monitoring

**Main Methods:**
```python
twilio_sms(alert_message)
# Sends SMS to all registered users
# Returns: (success_boolean, delivery_info)

send_alert_to_registered_users(alert_data)
# Processes weather alerts and sends notifications
# Handles user preference filtering

validate_phone_number(phone_number)
# Validates phone number format
# Returns: (is_valid, formatted_number)
```

**Error Handling:**
- Phone number format validation
- Twilio service availability checks
- Message delivery failure handling
- Rate limiting and quota management
- Invalid recipient handling

**Configuration Required:**
```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_number
```

**Message Format:**
```
🌦️ WEATHER ALERT 🌦️
Location: [City Name]
Alert: [Alert Type]
Description: [Detailed Information]
Time: [Timestamp]
Stay safe!
```

## API Integration Patterns

### Error Handling Strategy
All API handlers follow a consistent error handling pattern:

```python
def api_method(parameters):
    try:
        # Primary API call
        response = make_api_request(parameters)
        if response.status_code == 200:
            return process_response(response), None
        elif response.status_code == 401:
            # Try alternate API key/service
            return fallback_method(parameters)
        else:
            return None, f"API Error: {response.status_code}"
    except Exception as e:
        return None, str(e)
```

### Fallback Mechanisms
1. **API Key Rotation**: Automatically switches to backup API keys
2. **Service Switching**: Falls back to alternative weather services
3. **Cached Data**: Returns cached results when APIs are unavailable
4. **Default Values**: Provides sensible defaults for non-critical data

### Rate Limiting
- Built-in request throttling to respect API limits
- Intelligent caching to minimize redundant calls
- Queue management for high-frequency requests
- Usage monitoring and alerting

## Usage Examples

### Basic Weather Lookup
```python
from data.api_handlers.open_weather_api import OpenWeatherAPI

api = OpenWeatherAPI()
weather_data, error = api.fetch_open_weather("London")

if error:
    print(f"Error: {error}")
else:
    print(f"Temperature: {weather_data['main']['temp']}°C")
```

### Historical Data Retrieval
```python
from data.api_handlers.open_meteo_api import OpenMeteoAPI
from datetime import date, timedelta

api = OpenMeteoAPI()
past_date = date.today() - timedelta(days=7)
historical_data, error = api.fetch_historical_weather("Madrid", past_date)

if error:
    print(f"Error: {error}")
else:
    print(f"Historical data: {historical_data}")
```

### SMS Alert Integration
```python
from data.api_handlers.send_sms import send_alert_to_registered_users

alert = {
    'city': 'New York',
    'alert_type': 'Severe Thunderstorm',
    'description': 'Heavy rain and strong winds expected',
    'severity': 'High'
}

success, result = send_alert_to_registered_users(alert)
print(f"Alert sent: {success}, Details: {result}")
```

## Testing

### Unit Tests
Each API handler includes comprehensive unit tests in `tests/features_test.py`:

```python
# Test API response handling
def test_fetch_open_weather_success()
def test_fetch_open_weather_city_not_found()
def test_fetch_open_weather_api_key_failure()

# Test error conditions
def test_network_timeout_handling()
def test_invalid_response_handling()
def test_rate_limit_handling()
```

### Integration Testing
Run integration tests to verify API connectivity:

```bash
python -m tests.test_api_integration
```

## Monitoring and Logging

### API Usage Tracking
- Request count monitoring
- Response time measurement
- Error rate calculation
- API quota usage alerts

### Error Logging
All API errors are logged with:
- Timestamp and request details
- Error type and message
- User context (if applicable)
- Recovery actions taken

### Performance Metrics
- Average response times
- Cache hit rates
- Fallback activation frequency
- User satisfaction scores

## Security Considerations

### API Key Management
- Keys stored in environment variables only
- No hardcoded credentials in source code
- Regular key rotation recommended
- Separate keys for development/production

### Data Privacy
- User phone numbers encrypted in storage
- No personal data sent to weather APIs
- SMS message content is weather-related only
- Compliance with data protection regulations

## Troubleshooting

### Common Issues

1. **"City not found" errors**
   - Try different spelling variations
   - Include country/state for disambiguation
   - Use coordinates instead of city names

2. **API rate limit exceeded**
   - Implement request throttling
   - Use caching more aggressively  
   - Consider upgrading API plan

3. **SMS delivery failures**
   - Verify phone number format
   - Check Twilio account balance
   - Validate recipient numbers

4. **Network connectivity issues**
   - Implement retry logic
   - Use multiple API endpoints
   - Provide offline fallback data

### Debug Mode
Enable debug logging by setting:
```env
DEBUG_API_CALLS=true
```

This will log all API requests/responses for troubleshooting.

---

## Development Guidelines

When modifying API handlers:

1. **Maintain Error Handling**: Always return (data, error) tuples
2. **Add Fallback Logic**: Implement alternate data sources
3. **Update Tests**: Add test cases for new functionality
4. **Document Changes**: Update this README for any new methods
5. **Security Review**: Ensure no credentials are exposed
6. **Performance Impact**: Consider API rate limits and caching

For questions or issues with API integrations, refer to the main project documentation or create an issue in the project repository.