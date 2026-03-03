"""
WeatherData model for storing current weather information
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


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
        if self.temperature < -50 or self.temperature > 60:
            raise ValueError("temperature must be between -50 and 60 Celsius")
        
        if not (0 <= self.humidity <= 100):
            raise ValueError("humidity must be between 0 and 100")
        
        if self.precipitation < 0:
            raise ValueError("precipitation cannot be negative")
        
        if not isinstance(self.timestamp, datetime):
            raise ValueError("timestamp must be a datetime object")
    
    def is_humid(self) -> bool:
        """Check if current humidity is high (>80%)"""
        return self.humidity > 80
    
    def is_very_humid(self) -> bool:
        """Check if current humidity is very high (>90%)"""
        return self.humidity > 90
    
    def is_dry(self) -> bool:
        """Check if current humidity is low (<40%)"""
        return self.humidity < 40
    
    def has_precipitation(self) -> bool:
        """Check if there is recent precipitation (>1mm)"""
        return self.precipitation > 1
    
    def is_hot(self) -> bool:
        """Check if temperature is hot (>30°C)"""
        return self.temperature > 30
    
    def is_cold(self) -> bool:
        """Check if temperature is cold (<10°C)"""
        return self.temperature < 10
    
    def is_cloudy(self) -> bool:
        """Check if weather is cloudy (based on weather code)
        WMO codes: 1-3 are clear/partly cloudy, >50 indicates clouds/rain
        """
        return self.weather_code > 50
    
    def __str__(self) -> str:
        """Return formatted string representation of weather"""
        return (f"Weather at {self.location}: {self.temperature}°C, "
                f"Humidity: {self.humidity}%, Precipitation: {self.precipitation}mm")
    
    def __repr__(self) -> str:
        """Return detailed string representation of weather"""
        return (f"WeatherData(temp={self.temperature}, humidity={self.humidity}, "
                f"precip={self.precipitation}, code={self.weather_code})")
