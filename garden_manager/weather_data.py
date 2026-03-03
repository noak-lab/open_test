"""
WeatherData model for storing current weather information
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .constants import (
    TEMP_MIN_VALID, TEMP_MAX_VALID,
    HUMIDITY_MIN_VALID, HUMIDITY_MAX_VALID,
    HUMIDITY_HUMID_THRESHOLD, HUMIDITY_VERY_HUMID_THRESHOLD, HUMIDITY_DRY_THRESHOLD,
    TEMP_HOT_THRESHOLD, TEMP_COLD_THRESHOLD,
    PRECIPITATION_MIN_VALID, PRECIPITATION_RAIN_THRESHOLD,
    WMO_CLOUDY_THRESHOLD
)


@dataclass
class WeatherData:
    """
    Represents current weather conditions.
    
    Attributes:
        temperature: Current temperature in Celsius
        humidity: Current humidity percentage (0-100)
        precipitation: Current precipitation in mm
        weather_code: WMO weather code for condition classification
        timestamp: When the weather data was fetched
        location: Location description (e.g., "Tel Aviv, Israel")
        timezone: Timezone of the location
    """
    
    temperature: float
    humidity: int
    precipitation: float
    weather_code: int
    timestamp: datetime
    location: str = "Unknown"
    timezone: str = "UTC"
    
    def __post_init__(self):
        """Validate weather data after initialization"""
        if self.temperature < TEMP_MIN_VALID or self.temperature > TEMP_MAX_VALID:
            raise ValueError(f"temperature must be between {TEMP_MIN_VALID} and {TEMP_MAX_VALID} Celsius")
        
        if not (HUMIDITY_MIN_VALID <= self.humidity <= HUMIDITY_MAX_VALID):
            raise ValueError(f"humidity must be between {HUMIDITY_MIN_VALID} and {HUMIDITY_MAX_VALID}")
        
        if self.precipitation < PRECIPITATION_MIN_VALID:
            raise ValueError("precipitation cannot be negative")
        
        if not isinstance(self.timestamp, datetime):
            raise ValueError("timestamp must be a datetime object")
    
    def is_humid(self) -> bool:
        """Check if current humidity is high"""
        return self.humidity > HUMIDITY_HUMID_THRESHOLD
    
    def is_very_humid(self) -> bool:
        """Check if current humidity is very high"""
        return self.humidity > HUMIDITY_VERY_HUMID_THRESHOLD
    
    def is_dry(self) -> bool:
        """Check if current humidity is low"""
        return self.humidity < HUMIDITY_DRY_THRESHOLD
    
    def has_precipitation(self) -> bool:
        """Check if there is recent precipitation"""
        return self.precipitation > PRECIPITATION_RAIN_THRESHOLD
    
    def is_hot(self) -> bool:
        """Check if temperature is hot"""
        return self.temperature > TEMP_HOT_THRESHOLD
    
    def is_cold(self) -> bool:
        """Check if temperature is cold"""
        return self.temperature < TEMP_COLD_THRESHOLD
    
    def is_cloudy(self) -> bool:
        """Check if weather is cloudy (based on weather code)"""
        return self.weather_code > WMO_CLOUDY_THRESHOLD
    
    def __str__(self) -> str:
        """Return formatted string representation of weather"""
        return (f"Weather at {self.location}: {self.temperature}°C, "
                f"Humidity: {self.humidity}%, Precipitation: {self.precipitation}mm")
    
    def __repr__(self) -> str:
        """Return detailed string representation of weather"""
        return (f"WeatherData(temp={self.temperature}, humidity={self.humidity}, "
                f"precip={self.precipitation}, code={self.weather_code})")
