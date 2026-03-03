"""
Plant data model representing a plant with its characteristics and care requirements
"""

from dataclasses import dataclass
from typing import List, Optional
from .constants import HOURS_PER_DAY, TEMP_MIN_VALID, TEMP_MAX_VALID


@dataclass
class Plant:
    """
    Represents a plant with comprehensive care information.
    
    Attributes:
        common_name: Common name of the plant (e.g., "Tomato")
        scientific_name: Scientific/botanical name (e.g., "Solanum lycopersicum")
        botanical_group: Plant category (flower, cacti, vegetable, herb, tree, shrub, grass)
        water_needs: Water requirement level (very_low, low, medium, high, very_high)
        drought_tolerance: Drought resistance level (very_low, low, medium, high, very_high)
        optimal_watering_hours: List of hours (0-23) when watering is optimal
        watering_frequency_days: How often to water in days
        temperature_threshold: Temperature above which plant needs more water (°C)
        sunshine_requirement: Description of light needs (e.g., "full sun", "partial shade")
        found_in_cache: Whether this plant was found in local cache
    """
    
    common_name: str
    scientific_name: str
    botanical_group: str
    water_needs: str
    drought_tolerance: str
    optimal_watering_hours: List[int]
    watering_frequency_days: int
    temperature_threshold: float
    sunshine_requirement: str
    found_in_cache: bool = False
    
    def __post_init__(self):
        """Validate plant data after initialization"""
        if not self.common_name or not self.common_name.strip():
            raise ValueError("common_name cannot be empty")
        
        if not self.scientific_name or not self.scientific_name.strip():
            raise ValueError("scientific_name cannot be empty")
        
        valid_botanical_groups = {
            "flower", "cacti", "vegetable", "herb", "tree", 
            "shrub", "grass", "succulent", "fern", "moss"
        }
        if self.botanical_group.lower() not in valid_botanical_groups:
            raise ValueError(f"botanical_group must be one of {valid_botanical_groups}")
        
        valid_water_levels = {"very_low", "low", "medium", "high", "very_high"}
        if self.water_needs.lower() not in valid_water_levels:
            raise ValueError(f"water_needs must be one of {valid_water_levels}")
        
        if self.drought_tolerance.lower() not in valid_water_levels:
            raise ValueError(f"drought_tolerance must be one of {valid_water_levels}")
        
        if not all(0 <= hour < HOURS_PER_DAY for hour in self.optimal_watering_hours):
            raise ValueError(f"All hours must be between 0 and {HOURS_PER_DAY - 1}")
        
        if self.watering_frequency_days < 1:
            raise ValueError("watering_frequency_days must be at least 1")
        
        if self.temperature_threshold < TEMP_MIN_VALID or self.temperature_threshold > TEMP_MAX_VALID:
            raise ValueError(f"temperature_threshold must be between {TEMP_MIN_VALID} and {TEMP_MAX_VALID}")
    
    def __str__(self) -> str:
        """Return formatted string representation of the plant"""
        return (f"{self.common_name} ({self.scientific_name}) - {self.botanical_group}")
    
    def __repr__(self) -> str:
        """Return detailed string representation of the plant"""
        return (f"Plant(common='{self.common_name}', scientific='{self.scientific_name}', "
                f"group='{self.botanical_group}', water_needs='{self.water_needs}')")
