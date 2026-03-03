"""
Unit tests for WeatherFetcher service
"""

import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from garden_manager.weather_fetcher import WeatherFetcher


class TestWeatherFetcher:
    """Test suite for WeatherFetcher class"""
    
    def test_default_location_constants(self):
        """Test that default location constants are correct"""
        assert WeatherFetcher.DEFAULT_LAT == 32.0853
        assert WeatherFetcher.DEFAULT_LON == 34.7818
        assert WeatherFetcher.DEFAULT_LOCATION == "Tel Aviv, Israel"
        assert WeatherFetcher.DEFAULT_TIMEZONE == "Asia/Jerusalem"
    
    @patch('garden_manager.weather_fetcher.requests.get')
    def test_get_current_weather_success(self, mock_get):
        """Test successful weather fetch"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "current": {
                "temperature_2m": 25.0,
                "relative_humidity_2m": 50,
                "precipitation": 0.0,
                "weather_code": 0
            },
            "timezone": "Asia/Jerusalem"
        }
        mock_get.return_value = mock_response
        
        weather = WeatherFetcher.get_current_weather()
        
        assert weather is not None
        assert weather.temperature == 25.0
        assert weather.humidity == 50
        assert weather.precipitation == 0.0
        assert weather.location == "Tel Aviv, Israel"
    
    @patch('garden_manager.weather_fetcher.requests.get')
    def test_get_current_weather_with_custom_location(self, mock_get):
        """Test weather fetch with custom location"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "current": {
                "temperature_2m": 20.0,
                "relative_humidity_2m": 60,
                "precipitation": 2.0,
                "weather_code": 51
            },
            "timezone": "Europe/Paris"
        }
        mock_get.return_value = mock_response
        
        weather = WeatherFetcher.get_current_weather(
            latitude=48.8566,
            longitude=2.3522,
            location="Paris, France",
            timezone="Europe/Paris"
        )
        
        assert weather is not None
        assert weather.temperature == 20.0
        assert weather.location == "Paris, France"
        assert weather.timezone == "Europe/Paris"
    
    @patch('garden_manager.weather_fetcher.requests.get')
    def test_get_current_weather_request_exception(self, mock_get, capsys):
        """Test handling of network errors"""
        import requests
        mock_get.side_effect = requests.RequestException("Network error")
        
        weather = WeatherFetcher.get_current_weather()
        
        assert weather is None
        captured = capsys.readouterr()
        assert "Error fetching weather" in captured.out
    
    @patch('garden_manager.weather_fetcher.requests.get')
    def test_get_current_weather_invalid_response(self, mock_get, capsys):
        """Test handling of invalid API response"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"invalid": "data"}
        mock_get.return_value = mock_response
        
        weather = WeatherFetcher.get_current_weather()
        
        assert weather is None
        captured = capsys.readouterr()
        assert "Error parsing weather data" in captured.out
