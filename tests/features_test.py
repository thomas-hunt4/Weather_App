from features.weather_extract import parse_json
import unittest
from unittest.mock import patch, Mock
from data.api_handlers.open_weather_api import OpenWeatherAPI

class TestOpenWeatherAPI(unittest.TestCase):

    @patch("weather.open_weather_api.requests.get")
    def test_fetch_open_weather_success(self, mock_get):
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"weather": [{"main": "Clear"}]}
        mock_get.return_value = mock_response

        data, error = OpenWeatherAPI.fetch_open_weather("London")

        self.assertIsNone(error)
        self.assertIsInstance(data, dict)
        self.assertIn("weather", data)

    @patch("weather.open_weather_api.requests.get")
    def test_fetch_open_weather_city_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        data, error = OpenWeatherAPI.fetch_open_weather("InvalidCity")

        self.assertIsNone(data)
        self.assertIsNotNone(error)
        self.assertIn("City InvalidCity not found", error)

    @patch("weather.open_weather_api.requests.get")
    def test_fetch_open_weather_exception(self, mock_get):
        mock_get.side_effect = Exception("Network error")

        data, error = OpenWeatherAPI.fetch_open_weather("Paris")

        self.assertIsNone(data)
        self.assertEqual(error, "Network error")

    @patch("weather.open_weather_api.requests.get")
    def test_fetch_open_geo_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"name": "London", "lat": 51.51, "lon": -0.13}]
        mock_get.return_value = mock_response

        # patching select_city and api key logic internally would be needed to make this method work properly
        data, error = OpenWeatherAPI.fetch_open_geo()

        self.assertIsNone(error)
        self.assertIsInstance(data, list)
        self.assertEqual(data[0]["name"], "London")

    @patch("weather.open_weather_api.requests.get")
    def test_fetch_open_geo_exception(self, mock_get):
        mock_get.side_effect = Exception("Geo lookup failed")

        data, error = OpenWeatherAPI.fetch_open_geo()

        self.assertIsNone(data)
        self.assertEqual(error, "Geo lookup failed")

if __name__ == "__main__":
    unittest.main()



