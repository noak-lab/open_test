"""
Unit tests for Plant and WeatherData data models
"""

import pytest
from datetime import datetime
from garden_manager.plant import Plant
from garden_manager.weather_data import WeatherData


class TestPlant:
    """Test suite for Plant class"""
    
    def test_plant_creation_valid(self):
        """Test creating a valid plant"""
        plant = Plant(
            common_name="Tomato",
            scientific_name="Solanum lycopersicum",
            botanical_group="vegetable",
            water_needs="high",
            drought_tolerance="low",
            optimal_watering_hours=[6, 7, 8],
            watering_frequency_days=1,
            temperature_threshold=25,
            sunshine_requirement="full sun"
        )
        
        assert plant.common_name == "Tomato"
        assert plant.scientific_name == "Solanum lycopersicum"
        assert plant.botanical_group == "vegetable"
        assert plant.water_needs == "high"
        assert plant.found_in_cache is False
    
    def test_plant_empty_common_name(self):
        """Test that empty common name raises ValueError"""
        with pytest.raises(ValueError):
            Plant(
                common_name="",
                scientific_name="Solanum lycopersicum",
                botanical_group="vegetable",
                water_needs="high",
                drought_tolerance="low",
                optimal_watering_hours=[6, 7],
                watering_frequency_days=1,
                temperature_threshold=25,
                sunshine_requirement="full sun"
            )
    
    def test_plant_invalid_botanical_group(self):
        """Test that invalid botanical group raises ValueError"""
        with pytest.raises(ValueError):
            Plant(
                common_name="Tomato",
                scientific_name="Solanum lycopersicum",
                botanical_group="invalid_group",
                water_needs="high",
                drought_tolerance="low",
                optimal_watering_hours=[6, 7],
                watering_frequency_days=1,
                temperature_threshold=25,
                sunshine_requirement="full sun"
            )
    
    def test_plant_invalid_water_needs(self):
        """Test that invalid water needs raises ValueError"""
        with pytest.raises(ValueError):
            Plant(
                common_name="Tomato",
                scientific_name="Solanum lycopersicum",
                botanical_group="vegetable",
                water_needs="excessive",
                drought_tolerance="low",
                optimal_watering_hours=[6, 7],
                watering_frequency_days=1,
                temperature_threshold=25,
                sunshine_requirement="full sun"
            )
    
    def test_plant_invalid_watering_hours(self):
        """Test that invalid watering hours raise ValueError"""
        with pytest.raises(ValueError):
            Plant(
                common_name="Tomato",
                scientific_name="Solanum lycopersicum",
                botanical_group="vegetable",
                water_needs="high",
                drought_tolerance="low",
                optimal_watering_hours=[6, 25, 8],  # 25 is invalid
                watering_frequency_days=1,
                temperature_threshold=25,
                sunshine_requirement="full sun"
            )
    
    def test_plant_invalid_frequency(self):
        """Test that invalid frequency raises ValueError"""
        with pytest.raises(ValueError):
            Plant(
                common_name="Tomato",
                scientific_name="Solanum lycopersicum",
                botanical_group="vegetable",
                water_needs="high",
                drought_tolerance="low",
                optimal_watering_hours=[6, 7],
                watering_frequency_days=0,  # Must be at least 1
                temperature_threshold=25,
                sunshine_requirement="full sun"
            )
    
    def test_plant_str_representation(self):
        """Test string representation of plant"""
        plant = Plant(
            common_name="Rose",
            scientific_name="Rosa damascena",
            botanical_group="flower",
            water_needs="medium",
            drought_tolerance="medium",
            optimal_watering_hours=[6, 18],
            watering_frequency_days=2,
            temperature_threshold=20,
            sunshine_requirement="full sun"
        )
        
        assert "Rose" in str(plant)
        assert "Rosa damascena" in str(plant)
        assert "flower" in str(plant)
    
    def test_plant_found_in_cache_flag(self):
        """Test found_in_cache flag"""
        plant = Plant(
            common_name="Basil",
            scientific_name="Ocimum basilicum",
            botanical_group="herb",
            water_needs="medium",
            drought_tolerance="low",
            optimal_watering_hours=[7, 19],
            watering_frequency_days=1,
            temperature_threshold=22,
            sunshine_requirement="full sun",
            found_in_cache=True
        )
        
        assert plant.found_in_cache is True


class TestWeatherData:
    """Test suite for WeatherData class"""
    
    def test_weather_creation_valid(self):
        """Test creating valid weather data"""
        now = datetime.now()
        weather = WeatherData(
            temperature=25.0,
            humidity=50,
            precipitation=0.0,
            weather_code=0,
            timestamp=now,
            location="Tel Aviv, Israel"
        )
        
        assert weather.temperature == 25.0
        assert weather.humidity == 50
        assert weather.precipitation == 0.0
        assert weather.location == "Tel Aviv, Israel"
    
    def test_weather_invalid_temperature(self):
        """Test that invalid temperature raises ValueError"""
        now = datetime.now()
        with pytest.raises(ValueError):
            WeatherData(
                temperature=70.0,  # Too high
                humidity=50,
                precipitation=0.0,
                weather_code=0,
                timestamp=now
            )
    
    def test_weather_invalid_humidity(self):
        """Test that invalid humidity raises ValueError"""
        now = datetime.now()
        with pytest.raises(ValueError):
            WeatherData(
                temperature=25.0,
                humidity=150,  # Invalid
                precipitation=0.0,
                weather_code=0,
                timestamp=now
            )
    
    def test_weather_negative_precipitation(self):
        """Test that negative precipitation raises ValueError"""
        now = datetime.now()
        with pytest.raises(ValueError):
            WeatherData(
                temperature=25.0,
                humidity=50,
                precipitation=-5.0,  # Invalid
                weather_code=0,
                timestamp=now
            )
    
    def test_weather_is_humid(self):
        """Test is_humid method"""
        now = datetime.now()
        
        humid_weather = WeatherData(
            temperature=25.0, humidity=85, precipitation=0.0,
            weather_code=0, timestamp=now
        )
        assert humid_weather.is_humid() is True
        
        dry_weather = WeatherData(
            temperature=25.0, humidity=50, precipitation=0.0,
            weather_code=0, timestamp=now
        )
        assert dry_weather.is_humid() is False
    
    def test_weather_is_dry(self):
        """Test is_dry method"""
        now = datetime.now()
        
        dry_weather = WeatherData(
            temperature=25.0, humidity=30, precipitation=0.0,
            weather_code=0, timestamp=now
        )
        assert dry_weather.is_dry() is True
        
        normal_weather = WeatherData(
            temperature=25.0, humidity=50, precipitation=0.0,
            weather_code=0, timestamp=now
        )
        assert normal_weather.is_dry() is False
    
    def test_weather_has_precipitation(self):
        """Test has_precipitation method"""
        now = datetime.now()
        
        rainy_weather = WeatherData(
            temperature=25.0, humidity=90, precipitation=5.0,
            weather_code=0, timestamp=now
        )
        assert rainy_weather.has_precipitation() is True
        
        dry_weather = WeatherData(
            temperature=25.0, humidity=50, precipitation=0.0,
            weather_code=0, timestamp=now
        )
        assert dry_weather.has_precipitation() is False
    
    def test_weather_is_hot(self):
        """Test is_hot method"""
        now = datetime.now()
        
        hot_weather = WeatherData(
            temperature=35.0, humidity=50, precipitation=0.0,
            weather_code=0, timestamp=now
        )
        assert hot_weather.is_hot() is True
        
        cool_weather = WeatherData(
            temperature=20.0, humidity=50, precipitation=0.0,
            weather_code=0, timestamp=now
        )
        assert cool_weather.is_hot() is False
    
    def test_weather_is_cold(self):
        """Test is_cold method"""
        now = datetime.now()
        
        cold_weather = WeatherData(
            temperature=5.0, humidity=50, precipitation=0.0,
            weather_code=0, timestamp=now
        )
        assert cold_weather.is_cold() is True
        
        warm_weather = WeatherData(
            temperature=20.0, humidity=50, precipitation=0.0,
            weather_code=0, timestamp=now
        )
        assert warm_weather.is_cold() is False
    
    def test_weather_str_representation(self):
        """Test string representation of weather"""
        now = datetime.now()
        weather = WeatherData(
            temperature=25.0, humidity=60, precipitation=2.0,
            weather_code=0, timestamp=now, location="New York"
        )
        
        weather_str = str(weather)
        assert "25.0" in weather_str
        assert "60" in weather_str
        assert "2.0" in weather_str
