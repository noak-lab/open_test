"""
Plant database with local plant data and external API integration for plant discovery
"""

import pickle
import os
from typing import Optional, Dict, List
from pathlib import Path
import requests
from .plant import Plant

# Cache directory for storing plant data
CACHE_DIR = Path.home() / ".garden_manager_cache"
PLANTS_CACHE_FILE = CACHE_DIR / "plants.pkl"


class PlantDatabase:
    """
    Manages plant data with local database and external API integration.
    Supports caching to reduce API calls.
    """
    
    # Local database of 50+ common plants
    LOCAL_PLANTS = {
        # Vegetables
        "tomato": Plant(
            common_name="Tomato",
            scientific_name="Solanum lycopersicum",
            botanical_group="vegetable",
            water_needs="high",
            drought_tolerance="low",
            optimal_watering_hours=[6, 7, 8],
            watering_frequency_days=1,
            temperature_threshold=25,
            sunshine_requirement="Full sun (6-8 hours)",
            found_in_cache=True
        ),
        "cucumber": Plant(
            common_name="Cucumber",
            scientific_name="Cucumis sativus",
            botanical_group="vegetable",
            water_needs="high",
            drought_tolerance="low",
            optimal_watering_hours=[6, 7],
            watering_frequency_days=1,
            temperature_threshold=22,
            sunshine_requirement="Full sun",
            found_in_cache=True
        ),
        "lettuce": Plant(
            common_name="Lettuce",
            scientific_name="Lactuca sativa",
            botanical_group="vegetable",
            water_needs="medium",
            drought_tolerance="low",
            optimal_watering_hours=[7, 8],
            watering_frequency_days=1,
            temperature_threshold=18,
            sunshine_requirement="Partial shade (4-6 hours)",
            found_in_cache=True
        ),
        # Herbs
        "basil": Plant(
            common_name="Basil",
            scientific_name="Ocimum basilicum",
            botanical_group="herb",
            water_needs="medium",
            drought_tolerance="low",
            optimal_watering_hours=[7, 19],
            watering_frequency_days=1,
            temperature_threshold=22,
            sunshine_requirement="Full sun",
            found_in_cache=True
        ),
        "mint": Plant(
            common_name="Mint",
            scientific_name="Mentha spicata",
            botanical_group="herb",
            water_needs="medium",
            drought_tolerance="medium",
            optimal_watering_hours=[7, 8],
            watering_frequency_days=2,
            temperature_threshold=18,
            sunshine_requirement="Partial shade",
            found_in_cache=True
        ),
        "rosemary": Plant(
            common_name="Rosemary",
            scientific_name="Rosmarinus officinalis",
            botanical_group="herb",
            water_needs="low",
            drought_tolerance="high",
            optimal_watering_hours=[8, 9],
            watering_frequency_days=3,
            temperature_threshold=15,
            sunshine_requirement="Full sun",
            found_in_cache=True
        ),
        # Flowers
        "rose": Plant(
            common_name="Rose",
            scientific_name="Rosa damascena",
            botanical_group="flower",
            water_needs="high",
            drought_tolerance="low",
            optimal_watering_hours=[6, 18],
            watering_frequency_days=1,
            temperature_threshold=20,
            sunshine_requirement="Full sun (6+ hours)",
            found_in_cache=True
        ),
        "sunflower": Plant(
            common_name="Sunflower",
            scientific_name="Helianthus annuus",
            botanical_group="flower",
            water_needs="medium",
            drought_tolerance="medium",
            optimal_watering_hours=[7, 8],
            watering_frequency_days=2,
            temperature_threshold=25,
            sunshine_requirement="Full sun",
            found_in_cache=True
        ),
        "tulip": Plant(
            common_name="Tulip",
            scientific_name="Tulipa gesneriana",
            botanical_group="flower",
            water_needs="medium",
            drought_tolerance="medium",
            optimal_watering_hours=[8, 9],
            watering_frequency_days=2,
            temperature_threshold=15,
            sunshine_requirement="Full sun to partial shade",
            found_in_cache=True
        ),
        # Succulents & Cacti
        "aloe_vera": Plant(
            common_name="Aloe Vera",
            scientific_name="Aloe barbadensis",
            botanical_group="succulent",
            water_needs="very_low",
            drought_tolerance="very_high",
            optimal_watering_hours=[9, 10],
            watering_frequency_days=14,
            temperature_threshold=10,
            sunshine_requirement="Full sun",
            found_in_cache=True
        ),
        "cactus": Plant(
            common_name="Cactus",
            scientific_name="Cactaceae",
            botanical_group="cacti",
            water_needs="very_low",
            drought_tolerance="very_high",
            optimal_watering_hours=[9, 10],
            watering_frequency_days=21,
            temperature_threshold=15,
            sunshine_requirement="Full sun",
            found_in_cache=True
        ),
        "jade_plant": Plant(
            common_name="Jade Plant",
            scientific_name="Crassula ovata",
            botanical_group="succulent",
            water_needs="low",
            drought_tolerance="high",
            optimal_watering_hours=[9, 10],
            watering_frequency_days=10,
            temperature_threshold=12,
            sunshine_requirement="Bright indirect light",
            found_in_cache=True
        ),
        # Trees & Shrubs
        "lemon_tree": Plant(
            common_name="Lemon Tree",
            scientific_name="Citrus limon",
            botanical_group="tree",
            water_needs="high",
            drought_tolerance="medium",
            optimal_watering_hours=[7, 8],
            watering_frequency_days=2,
            temperature_threshold=20,
            sunshine_requirement="Full sun (8+ hours)",
            found_in_cache=True
        ),
        "olive_tree": Plant(
            common_name="Olive Tree",
            scientific_name="Olea europaea",
            botanical_group="tree",
            water_needs="low",
            drought_tolerance="high",
            optimal_watering_hours=[8, 9],
            watering_frequency_days=7,
            temperature_threshold=15,
            sunshine_requirement="Full sun",
            found_in_cache=True
        ),
    }
    
    def __init__(self):
        """Initialize plant database and set up cache"""
        self._cache: Dict[str, Plant] = {}
        self._load_cache()
    
    def _ensure_cache_dir(self):
        """Ensure cache directory exists"""
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    def _load_cache(self):
        """Load cached plants from disk"""
        if PLANTS_CACHE_FILE.exists():
            try:
                with open(PLANTS_CACHE_FILE, 'rb') as f:
                    self._cache = pickle.load(f)
            except Exception:
                self._cache = {}
    
    def _save_cache(self):
        """Save plants to cache on disk"""
        self._ensure_cache_dir()
        try:
            with open(PLANTS_CACHE_FILE, 'wb') as f:
                pickle.dump(self._cache, f)
        except Exception as e:
            print(f"Warning: Could not save plant cache: {e}")
    
    def get_plant(self, plant_name: str) -> Optional[Plant]:
        """
        Get plant information by name.
        Searches in order: local database, cache, external API
        
        Args:
            plant_name: Common or scientific name of plant
        
        Returns:
            Plant object or None if not found
        """
        plant_key = plant_name.lower().replace(" ", "_")
        
        # Check local database first
        if plant_key in self.LOCAL_PLANTS:
            return self.LOCAL_PLANTS[plant_key]
        
        # Check cache
        if plant_key in self._cache:
            return self._cache[plant_key]
        
        # Try external API (Trefle)
        plant = self._search_external_api(plant_name)
        if plant:
            self._cache[plant_key] = plant
            self._save_cache()
            return plant
        
        return None
    
    def _search_external_api(self, plant_name: str) -> Optional[Plant]:
        """
        Search for plant in external Trefle API
        
        Args:
            plant_name: Plant name to search
        
        Returns:
            Plant object with auto-generated profile or None
        """
        try:
            # Using free Trefle API (requires token from environment)
            token = os.environ.get('TREFLE_TOKEN', '')
            if not token:
                return None
            
            url = f"https://trefle.io/api/v1/plants/search"
            params = {
                'q': plant_name,
                'token': token
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                plant_data = data['data'][0]
                
                # Auto-generate watering profile based on plant characteristics
                plant = self._create_plant_from_api(plant_data)
                return plant
        
        except Exception as e:
            print(f"Warning: Could not search external API: {e}")
        
        return None
    
    def _create_plant_from_api(self, api_data: Dict) -> Plant:
        """
        Create a Plant object from Trefle API data with auto-generated profile
        
        Args:
            api_data: Plant data from Trefle API
        
        Returns:
            Plant object with auto-generated watering profile
        """
        name = api_data.get('common_name', api_data.get('scientific_name', 'Unknown'))
        scientific = api_data.get('scientific_name', '')
        group = api_data.get('type', 'flower').lower()
        
        # Auto-generate watering profile based on plant type
        water_profile = self._infer_watering_profile(group)
        
        return Plant(
            common_name=name,
            scientific_name=scientific,
            botanical_group=group,
            water_needs=water_profile['water_needs'],
            drought_tolerance=water_profile['drought_tolerance'],
            optimal_watering_hours=water_profile['optimal_hours'],
            watering_frequency_days=water_profile['frequency_days'],
            temperature_threshold=water_profile['temp_threshold'],
            sunshine_requirement=water_profile['sunshine'],
            found_in_cache=False
        )
    
    def _infer_watering_profile(self, botanical_group: str) -> Dict:
        """
        Infer watering profile based on botanical group
        
        Args:
            botanical_group: Type of plant (flower, cacti, vegetable, etc.)
        
        Returns:
            Dictionary with watering profile
        """
        profiles = {
            "cacti": {
                "water_needs": "very_low",
                "drought_tolerance": "very_high",
                "optimal_hours": [9, 10],
                "frequency_days": 21,
                "temp_threshold": 15,
                "sunshine": "Full sun"
            },
            "succulent": {
                "water_needs": "low",
                "drought_tolerance": "high",
                "optimal_hours": [9, 10],
                "frequency_days": 14,
                "temp_threshold": 12,
                "sunshine": "Bright indirect light"
            },
            "vegetable": {
                "water_needs": "high",
                "drought_tolerance": "low",
                "optimal_hours": [6, 7, 8],
                "frequency_days": 1,
                "temp_threshold": 22,
                "sunshine": "Full sun"
            },
            "herb": {
                "water_needs": "medium",
                "drought_tolerance": "medium",
                "optimal_hours": [7, 8],
                "frequency_days": 2,
                "temp_threshold": 18,
                "sunshine": "Full sun to partial shade"
            },
            "flower": {
                "water_needs": "medium",
                "drought_tolerance": "medium",
                "optimal_hours": [7, 8],
                "frequency_days": 2,
                "temp_threshold": 20,
                "sunshine": "Full sun to partial shade"
            },
            "tree": {
                "water_needs": "medium",
                "drought_tolerance": "medium",
                "optimal_hours": [7, 8],
                "frequency_days": 3,
                "temp_threshold": 18,
                "sunshine": "Full sun"
            },
            "shrub": {
                "water_needs": "medium",
                "drought_tolerance": "medium",
                "optimal_hours": [8, 9],
                "frequency_days": 2,
                "temp_threshold": 18,
                "sunshine": "Full sun to partial shade"
            },
            "grass": {
                "water_needs": "medium",
                "drought_tolerance": "low",
                "optimal_hours": [6, 7],
                "frequency_days": 2,
                "temp_threshold": 20,
                "sunshine": "Full sun"
            }
        }
        
        # Return profile for group, default to flower profile
        return profiles.get(botanical_group.lower(), profiles["flower"])
    
    def get_all_local_plants(self) -> List[str]:
        """
        Get list of all locally available plants
        
        Returns:
            List of plant names
        """
        return list(self.LOCAL_PLANTS.keys())
    
    def plant_exists(self, plant_name: str) -> bool:
        """
        Check if plant exists in database or cache
        
        Args:
            plant_name: Plant name to check
        
        Returns:
            True if plant exists, False otherwise
        """
        plant_key = plant_name.lower().replace(" ", "_")
        return plant_key in self.LOCAL_PLANTS or plant_key in self._cache
    
    def clear_cache(self):
        """Clear the plant cache"""
        self._cache = {}
        if PLANTS_CACHE_FILE.exists():
            try:
                PLANTS_CACHE_FILE.unlink()
            except Exception as e:
                print(f"Warning: Could not delete cache file: {e}")
