"""
Garden Analyzer - Provides intelligent recommendations for plant care

Analyzes weather conditions and plant requirements to generate:
- Watering recommendations (whether to water now and optimal hour)
- Sunlight recommendations
- Reasoning for recommendations
"""

from datetime import datetime
from typing import Dict, Tuple
from .plant import Plant
from .weather_data import WeatherData


class GardenAnalyzer:
    """
    Analyzes weather conditions and plant requirements to provide care recommendations.
    """
    
    def __init__(self):
        """Initialize the garden analyzer"""
        pass
    
    def should_water_now(self, plant: Plant, weather: WeatherData, current_hour: int) -> Tuple[bool, str]:
        """
        Determine if a plant should be watered now based on weather and plant needs.
        
        Args:
            plant: Plant object with watering requirements
            weather: Current weather data
            current_hour: Current hour (0-23)
        
        Returns:
            Tuple of (should_water: bool, reason: str)
        """
        reason_parts = []
        
        # Check if current hour is within optimal watering hours
        hour_ok = current_hour in plant.optimal_watering_hours
        if not hour_ok:
            next_hour = plant.optimal_watering_hours[0]
            return False, f"Not optimal hour. Next watering hour: {next_hour}:00"
        
        reason_parts.append(f"✓ Current hour ({current_hour}:00) is within optimal watering hours")
        
        # Analyze weather conditions
        recommendations = self._analyze_weather_for_watering(plant, weather)
        
        if recommendations["skip"]:
            return False, recommendations["reason"]
        
        reason_parts.append(recommendations["reason"])
        
        # Plant-specific considerations
        plant_reason = self._plant_specific_considerations(plant, weather)
        if plant_reason:
            reason_parts.append(plant_reason)
        
        return True, " | ".join(reason_parts)
    
    def get_optimal_watering_hour(self, plant: Plant) -> int:
        """
        Get the optimal hour for watering a plant.
        
        Args:
            plant: Plant object
        
        Returns:
            Hour (0-23) for optimal watering
        """
        return plant.optimal_watering_hours[0]
    
    def get_watering_frequency_message(self, plant: Plant) -> str:
        """
        Get human-readable watering frequency message.
        
        Args:
            plant: Plant object
        
        Returns:
            Frequency message (e.g., "Daily", "Every 2 days")
        """
        freq = plant.watering_frequency_days
        
        if freq == 1:
            return "Daily"
        elif freq == 7:
            return "Weekly"
        elif freq == 14:
            return "Every 2 weeks"
        elif freq == 21:
            return "Every 3 weeks"
        else:
            return f"Every {freq} days"
    
    def get_sunshine_recommendation(self, plant: Plant, weather: WeatherData) -> str:
        """
        Get sunshine recommendation based on plant needs and weather conditions.
        
        Args:
            plant: Plant object with sunshine requirements
            weather: Current weather data
        
        Returns:
            Sunshine recommendation message
        """
        plant_needs = plant.sunshine_requirement
        
        # Check cloud cover (weather code)
        is_cloudy = weather.is_cloudy()
        is_rainy = weather.has_precipitation()
        
        if is_rainy:
            return f"Plant needs: {plant_needs} | Current: Rainy (limited sunlight available)"
        elif is_cloudy:
            return f"Plant needs: {plant_needs} | Current: Cloudy (limited sunlight)"
        else:
            return f"Plant needs: {plant_needs} | Current: Clear (good sunlight)"
    
    def _analyze_weather_for_watering(self, plant: Plant, weather: WeatherData) -> Dict[str, any]:
        """
        Analyze weather conditions to determine if watering should happen.
        
        Args:
            plant: Plant object
            weather: Current weather data
        
        Returns:
            Dictionary with 'skip' (bool) and 'reason' (str)
        """
        # Check for recent precipitation
        if weather.has_precipitation():
            return {
                "skip": True,
                "reason": f"Rainfall detected - soil moisture sufficient. Skip watering."
            }
        
        # Check humidity levels
        if weather.is_very_humid():
            return {
                "skip": True,
                "reason": f"Very high humidity ({weather.humidity}%) - soil retains moisture well"
            }
        
        # Check temperature extremes
        if plant.temperature_threshold and weather.temperature < (plant.temperature_threshold - 5):
            return {
                "skip": True,
                "reason": f"Temperature too cold ({weather.temperature}°C) for watering"
            }
        
        # Check for hot conditions (priority over dry)
        if weather.temperature > 35:
            return {
                "skip": False,
                "reason": f"✓ Very hot weather ({weather.temperature}°C) - plant needs water urgently"
            }
        
        if weather.is_hot():
            return {
                "skip": False,
                "reason": f"✓ Hot weather ({weather.temperature}°C) - plant needs water"
            }
        
        # Check if conditions are favorable
        if weather.is_dry() and not weather.is_cold():
            return {
                "skip": False,
                "reason": f"✓ Dry conditions (humidity {weather.humidity}%) - plant needs water"
            }
        
        # Normal conditions - proceed with watering based on plant type
        return {
            "skip": False,
            "reason": f"✓ Normal conditions - proceed with watering"
        }
    
    def _plant_specific_considerations(self, plant: Plant, weather: WeatherData) -> str:
        """
        Get plant-specific watering considerations.
        
        Args:
            plant: Plant object
            weather: Current weather data
        
        Returns:
            Additional recommendation message or empty string
        """
        # Vegetables and herbs need consistent moisture
        if plant.botanical_group in ["vegetable", "herb"]:
            if plant.water_needs == "high":
                return "⚠ High water needs - monitor soil moisture closely"
        
        # Succulents and cacti prefer dry conditions
        if plant.botanical_group in ["succulent", "cacti"]:
            if weather.is_humid():
                return "⚠ High humidity - ensure good drainage to prevent root rot"
        
        # Drought-tolerant plants
        if plant.drought_tolerance in ["high", "very_high"]:
            if not weather.is_dry():
                return "⚠ Plant is drought-tolerant - only water if soil is completely dry"
        
        return ""
    
    def analyze_plant_care(self, plant: Plant, weather: WeatherData, current_hour: int) -> Dict[str, any]:
        """
        Comprehensive analysis of plant care requirements.
        
        Args:
            plant: Plant object
            weather: Current weather data
            current_hour: Current hour (0-23)
        
        Returns:
            Dictionary with complete care analysis
        """
        should_water, water_reason = self.should_water_now(plant, weather, current_hour)
        
        return {
            "plant_name": plant.common_name,
            "scientific_name": plant.scientific_name,
            "botanical_group": plant.botanical_group,
            "should_water_now": should_water,
            "watering_reason": water_reason,
            "optimal_watering_hour": self.get_optimal_watering_hour(plant),
            "watering_frequency": self.get_watering_frequency_message(plant),
            "water_needs": plant.water_needs,
            "drought_tolerance": plant.drought_tolerance,
            "sunshine_recommendation": self.get_sunshine_recommendation(plant, weather),
            "sunshine_requirement": plant.sunshine_requirement
        }
