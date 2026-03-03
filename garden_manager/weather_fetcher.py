"""
WeatherFetcher service for fetching real-time weather data from Open-Meteo API
"""

import requests
from datetime import datetime
from typing import Optional
from .weather_data import WeatherData

# Open-Meteo API endpoint (free, no API key required)
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherFetcher:
    """
    Fetches real-time weather data for specified locations.
    Uses Open-Meteo free API with no authentication required.
    """
    
    # Default location: Tel Aviv, Israel
    DEFAULT_LAT = 32.0853
    DEFAULT_LON = 34.7818
    DEFAULT_LOCATION = "Tel Aviv, Israel"
    DEFAULT_TIMEZONE = "Asia/Jerusalem"
    
    def __init__(
        self,
        latitude: float = DEFAULT_LAT,
        longitude: float = DEFAULT_LON,
        location: str = DEFAULT_LOCATION,
        timezone: str = DEFAULT_TIMEZONE
    ):
        """Initialize WeatherFetcher with location details"""
        self.latitude = latitude
        self.longitude = longitude
        self.location = location
        self.timezone = timezone
    
    def fetch_weather(self) -> Optional[WeatherData]:
        """
        Fetch current weather data for the configured location.
        
        Returns:
            WeatherData object with current conditions, or None if fetch fails
        """
        return self.get_current_weather(
            latitude=self.latitude,
            longitude=self.longitude,
            location=self.location,
            timezone=self.timezone
        )
    
    @staticmethod
    def get_current_weather(
        latitude: float = DEFAULT_LAT,
        longitude: float = DEFAULT_LON,
        location: str = DEFAULT_LOCATION,
        timezone: str = DEFAULT_TIMEZONE
    ) -> Optional[WeatherData]:
        """
        Fetch current weather data for a specific location.
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            location: Location description
            timezone: Location timezone
        
        Returns:
            WeatherData object with current conditions, or None if fetch fails
        """
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,precipitation,weather_code",
                "timezone": timezone
            }
            
            response = requests.get(WEATHER_API_URL, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Validate response structure
            if "current" not in data:
                raise ValueError("Invalid API response: missing 'current' field")
            
            current = data["current"]
            
            # Check for required fields
            required_fields = ["temperature_2m", "relative_humidity_2m", "precipitation", "weather_code"]
            if not all(field in current for field in required_fields):
                raise ValueError("Invalid API response: missing required weather fields")
            
            weather = WeatherData(
                temperature=current["temperature_2m"],
                humidity=current["relative_humidity_2m"],
                precipitation=current["precipitation"],
                weather_code=current["weather_code"],
                timestamp=datetime.now(),
                location=location,
                timezone=timezone
            )
            
            return weather
            
        except requests.RequestException as e:
            print(f"Error fetching weather: {e}")
            return None
        except (KeyError, ValueError) as e:
            print(f"Error parsing weather data: {e}")
            return None
