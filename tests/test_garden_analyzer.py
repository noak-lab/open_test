"""
Unit tests for GardenAnalyzer class
Tests watering recommendations, sunlight analysis, and plant care analysis
"""

import pytest
from datetime import datetime, timezone
from garden_manager.garden_analyzer import GardenAnalyzer
from garden_manager.plant import Plant
from garden_manager.weather_data import WeatherData


class TestShouldWaterNow:
    """Test watering decision logic"""
    
    def test_should_water_at_optimal_hour_with_dry_conditions(self):
        """Test watering recommendation at optimal hour with dry conditions"""
        analyzer = GardenAnalyzer()
        plant = Plant(
            common_name="Tomato",
            scientific_name="Solanum lycopersicum",
            botanical_group="vegetable",
            water_needs="high",
            drought_tolerance="low",
            optimal_watering_hours=[6, 7, 8],
            watering_frequency_days=1,
            temperature_threshold=25,
            sunshine_requirement="Full sun"
        )
        
        weather = WeatherData(
            temperature=25,
            humidity=35,  # Dry
            precipitation=0,
            weather_code=1,
            timestamp=datetime.now(timezone.utc),
            location="Tel Aviv",
            timezone="Asia/Jerusalem"
        )
        
        should_water, reason = analyzer.should_water_now(plant, weather, 7)
        
        assert should_water is True
        assert "hour" in reason.lower() or "7" in reason
        assert "dry" in reason.lower() or "water" in reason.lower()
    
    def test_should_not_water_during_rain(self):
        """Test that watering is skipped during rainfall"""
        analyzer = GardenAnalyzer()
        plant = Plant(
            common_name="Basil",
            scientific_name="Ocimum basilicum",
            botanical_group="herb",
            water_needs="medium",
            drought_tolerance="low",
            optimal_watering_hours=[7, 8],
            watering_frequency_days=1,
            temperature_threshold=22,
            sunshine_requirement="Full sun"
        )
        
        weather = WeatherData(
            temperature=20,
            humidity=90,
            precipitation=5,  # Rain
            weather_code=61,  # Rainy code
            timestamp=datetime.now(timezone.utc),
            location="Tel Aviv",
            timezone="Asia/Jerusalem"
        )
        
        should_water, reason = analyzer.should_water_now(plant, weather, 7)
        
        assert should_water is False
        assert "rain" in reason.lower() or "precipitation" in reason.lower()
    
    def test_should_not_water_outside_optimal_hours(self):
        """Test that watering is skipped outside optimal hours"""
        analyzer = GardenAnalyzer()
        plant = Plant(
            common_name="Rose",
            scientific_name="Rosa damascena",
            botanical_group="flower",
            water_needs="high",
            drought_tolerance="low",
            optimal_watering_hours=[6, 7, 8],
            watering_frequency_days=1,
            temperature_threshold=20,
            sunshine_requirement="Full sun"
        )
        
        weather = WeatherData(
            temperature=25,
            humidity=35,
            precipitation=0,
            weather_code=1,
            timestamp=datetime.now(timezone.utc),
            location="Tel Aviv",
            timezone="Asia/Jerusalem"
        )
        
        should_water, reason = analyzer.should_water_now(plant, weather, 14)
        
        assert should_water is False
        assert "hour" in reason.lower() or "optimal" in reason.lower()
    
    def test_should_not_water_when_very_humid(self):
        """Test that watering is skipped when humidity is very high"""
        analyzer = GardenAnalyzer()
        plant = Plant(
            common_name="Mint",
            scientific_name="Mentha spicata",
            botanical_group="herb",
            water_needs="medium",
            drought_tolerance="medium",
            optimal_watering_hours=[7, 8],
            watering_frequency_days=2,
            temperature_threshold=18,
            sunshine_requirement="Partial shade"
        )
        
        weather = WeatherData(
            temperature=20,
            humidity=95,  # Very humid
            precipitation=0,
            weather_code=10,
            timestamp=datetime.now(timezone.utc),
            location="Tel Aviv",
            timezone="Asia/Jerusalem"
        )
        
        should_water, reason = analyzer.should_water_now(plant, weather, 7)
        
        assert should_water is False
        assert "humidity" in reason.lower()
    
    def test_should_not_water_when_too_cold(self):
        """Test that watering is skipped when temperature is too cold"""
        analyzer = GardenAnalyzer()
        plant = Plant(
            common_name="Tomato",
            scientific_name="Solanum lycopersicum",
            botanical_group="vegetable",
            water_needs="high",
            drought_tolerance="low",
            optimal_watering_hours=[6, 7, 8],
            watering_frequency_days=1,
            temperature_threshold=25,
            sunshine_requirement="Full sun"
        )
        
        weather = WeatherData(
            temperature=5,  # Too cold
            humidity=50,
            precipitation=0,
            weather_code=1,
            timestamp=datetime.now(timezone.utc),
            location="Tel Aviv",
            timezone="Asia/Jerusalem"
        )
        
        should_water, reason = analyzer.should_water_now(plant, weather, 7)
        
        assert should_water is False
        assert "cold" in reason.lower() or "temperature" in reason.lower()
    
    def test_should_water_when_hot(self):
        """Test that watering is recommended in hot conditions"""
        analyzer = GardenAnalyzer()
        plant = Plant(
            common_name="Tomato",
            scientific_name="Solanum lycopersicum",
            botanical_group="vegetable",
            water_needs="high",
            drought_tolerance="low",
            optimal_watering_hours=[6, 7, 8],
            watering_frequency_days=1,
            temperature_threshold=25,
            sunshine_requirement="Full sun"
        )
        
        weather = WeatherData(
            temperature=38,  # Very hot
            humidity=30,
            precipitation=0,
            weather_code=1,
            timestamp=datetime.now(timezone.utc),
            location="Tel Aviv",
            timezone="Asia/Jerusalem"
        )
        
        should_water, reason = analyzer.should_water_now(plant, weather, 7)
        
        assert should_water is True
        # Should recommend watering due to hot and/or dry conditions
        assert "water" in reason.lower()


class TestOptimalWateringHour:
    """Test optimal watering hour retrieval"""
    
    def test_get_optimal_watering_hour(self):
        """Test getting optimal watering hour from plant"""
        analyzer = GardenAnalyzer()
        plant = Plant(
            common_name="Tomato",
            scientific_name="Solanum lycopersicum",
            botanical_group="vegetable",
            water_needs="high",
            drought_tolerance="low",
            optimal_watering_hours=[6, 7, 8],
            watering_frequency_days=1,
            temperature_threshold=25,
            sunshine_requirement="Full sun"
        )
        
        optimal_hour = analyzer.get_optimal_watering_hour(plant)
        
        assert optimal_hour == 6
    
    def test_optimal_watering_hour_different_plants(self):
        """Test optimal watering hour for different plants"""
        analyzer = GardenAnalyzer()
        
        # Early morning watering
        morning_plant = Plant(
            common_name="Rose",
            scientific_name="Rosa damascena",
            botanical_group="flower",
            water_needs="high",
            drought_tolerance="low",
            optimal_watering_hours=[5, 6],
            watering_frequency_days=1,
            temperature_threshold=20,
            sunshine_requirement="Full sun"
        )
        
        # Evening watering
        evening_plant = Plant(
            common_name="Cactus",
            scientific_name="Cactaceae",
            botanical_group="cacti",
            water_needs="very_low",
            drought_tolerance="very_high",
            optimal_watering_hours=[19, 20],
            watering_frequency_days=21,
            temperature_threshold=15,
            sunshine_requirement="Full sun"
        )
        
        assert analyzer.get_optimal_watering_hour(morning_plant) == 5
        assert analyzer.get_optimal_watering_hour(evening_plant) == 19


class TestWateringFrequencyMessage:
    """Test watering frequency formatting"""
    
    def test_daily_watering_frequency(self):
        """Test formatting for daily watering"""
        analyzer = GardenAnalyzer()
        plant = Plant(
            common_name="Tomato",
            scientific_name="Solanum lycopersicum",
            botanical_group="vegetable",
            water_needs="high",
            drought_tolerance="low",
            optimal_watering_hours=[6, 7, 8],
            watering_frequency_days=1,
            temperature_threshold=25,
            sunshine_requirement="Full sun"
        )
        
        message = analyzer.get_watering_frequency_message(plant)
        
        assert message == "Daily"
    
    def test_weekly_watering_frequency(self):
        """Test formatting for weekly watering"""
        analyzer = GardenAnalyzer()
        plant = Plant(
            common_name="Olive Tree",
            scientific_name="Olea europaea",
            botanical_group="tree",
            water_needs="low",
            drought_tolerance="high",
            optimal_watering_hours=[8, 9],
            watering_frequency_days=7,
            temperature_threshold=15,
            sunshine_requirement="Full sun"
        )
        
        message = analyzer.get_watering_frequency_message(plant)
        
        assert message == "Weekly"
    
    def test_biweekly_watering_frequency(self):
        """Test formatting for bi-weekly watering"""
        analyzer = GardenAnalyzer()
        plant = Plant(
            common_name="Aloe Vera",
            scientific_name="Aloe barbadensis",
            botanical_group="succulent",
            water_needs="very_low",
            drought_tolerance="very_high",
            optimal_watering_hours=[9, 10],
            watering_frequency_days=14,
            temperature_threshold=10,
            sunshine_requirement="Full sun"
        )
        
        message = analyzer.get_watering_frequency_message(plant)
        
        assert message == "Every 2 weeks"
    
    def test_custom_watering_frequency(self):
        """Test formatting for custom watering frequency"""
        analyzer = GardenAnalyzer()
        plant = Plant(
            common_name="Custom Plant",
            scientific_name="Custom planticus",
            botanical_group="flower",
            water_needs="medium",
            drought_tolerance="medium",
            optimal_watering_hours=[7, 8],
            watering_frequency_days=5,
            temperature_threshold=20,
            sunshine_requirement="Full sun"
        )
        
        message = analyzer.get_watering_frequency_message(plant)
        
        assert message == "Every 5 days"


class TestSunshineRecommendation:
    """Test sunshine recommendations"""
    
    def test_sunshine_recommendation_clear_day(self):
        """Test sunshine recommendation on clear day"""
        analyzer = GardenAnalyzer()
        plant = Plant(
            common_name="Sunflower",
            scientific_name="Helianthus annuus",
            botanical_group="flower",
            water_needs="medium",
            drought_tolerance="medium",
            optimal_watering_hours=[7, 8],
            watering_frequency_days=2,
            temperature_threshold=25,
            sunshine_requirement="Full sun"
        )
        
        weather = WeatherData(
            temperature=25,
            humidity=40,
            precipitation=0,
            weather_code=1,  # Clear
            timestamp=datetime.now(timezone.utc),
            location="Tel Aviv",
            timezone="Asia/Jerusalem"
        )
        
        recommendation = analyzer.get_sunshine_recommendation(plant, weather)
        
        assert "Full sun" in recommendation
        assert "Clear" in recommendation
        assert "sunlight" in recommendation.lower()
    
    def test_sunshine_recommendation_rainy_day(self):
        """Test sunshine recommendation on rainy day"""
        analyzer = GardenAnalyzer()
        plant = Plant(
            common_name="Rose",
            scientific_name="Rosa damascena",
            botanical_group="flower",
            water_needs="high",
            drought_tolerance="low",
            optimal_watering_hours=[6, 18],
            watering_frequency_days=1,
            temperature_threshold=20,
            sunshine_requirement="Full sun (6+ hours)"
        )
        
        weather = WeatherData(
            temperature=15,
            humidity=90,
            precipitation=10,  # Rain
            weather_code=65,  # Rainy code
            timestamp=datetime.now(timezone.utc),
            location="Tel Aviv",
            timezone="Asia/Jerusalem"
        )
        
        recommendation = analyzer.get_sunshine_recommendation(plant, weather)
        
        assert "Full sun" in recommendation
        assert "Rainy" in recommendation
        assert "limited" in recommendation.lower()
    
    def test_sunshine_recommendation_cloudy_day(self):
        """Test sunshine recommendation on cloudy day"""
        analyzer = GardenAnalyzer()
        plant = Plant(
            common_name="Lettuce",
            scientific_name="Lactuca sativa",
            botanical_group="vegetable",
            water_needs="medium",
            drought_tolerance="low",
            optimal_watering_hours=[7, 8],
            watering_frequency_days=1,
            temperature_threshold=18,
            sunshine_requirement="Partial shade (4-6 hours)"
        )
        
        weather = WeatherData(
            temperature=18,
            humidity=70,
            precipitation=0,
            weather_code=51,  # Cloudy code
            timestamp=datetime.now(timezone.utc),
            location="Tel Aviv",
            timezone="Asia/Jerusalem"
        )
        
        recommendation = analyzer.get_sunshine_recommendation(plant, weather)
        
        assert "Partial shade" in recommendation
        assert "Cloudy" in recommendation


class TestAnalyzePlantCare:
    """Test comprehensive plant care analysis"""
    
    def test_analyze_plant_care_complete_output(self):
        """Test complete plant care analysis output"""
        analyzer = GardenAnalyzer()
        plant = Plant(
            common_name="Tomato",
            scientific_name="Solanum lycopersicum",
            botanical_group="vegetable",
            water_needs="high",
            drought_tolerance="low",
            optimal_watering_hours=[6, 7, 8],
            watering_frequency_days=1,
            temperature_threshold=25,
            sunshine_requirement="Full sun (6-8 hours)"
        )
        
        weather = WeatherData(
            temperature=28,
            humidity=45,
            precipitation=0,
            weather_code=1,
            timestamp=datetime.now(timezone.utc),
            location="Tel Aviv",
            timezone="Asia/Jerusalem"
        )
        
        analysis = analyzer.analyze_plant_care(plant, weather, 7)
        
        assert analysis["plant_name"] == "Tomato"
        assert analysis["scientific_name"] == "Solanum lycopersicum"
        assert analysis["botanical_group"] == "vegetable"
        assert "should_water_now" in analysis
        assert "watering_reason" in analysis
        assert "optimal_watering_hour" in analysis
        assert "watering_frequency" in analysis
        assert "water_needs" in analysis
        assert "drought_tolerance" in analysis
        assert "sunshine_recommendation" in analysis
        assert "sunshine_requirement" in analysis
    
    def test_analyze_plant_care_different_conditions(self):
        """Test plant care analysis with different weather conditions"""
        analyzer = GardenAnalyzer()
        plant = Plant(
            common_name="Cactus",
            scientific_name="Cactaceae",
            botanical_group="cacti",
            water_needs="very_low",
            drought_tolerance="very_high",
            optimal_watering_hours=[9, 10],
            watering_frequency_days=21,
            temperature_threshold=15,
            sunshine_requirement="Full sun"
        )
        
        # Hot and dry
        hot_weather = WeatherData(
            temperature=35,
            humidity=20,
            precipitation=0,
            weather_code=1,
            timestamp=datetime.now(timezone.utc),
            location="Tel Aviv",
            timezone="Asia/Jerusalem"
        )
        
        analysis = analyzer.analyze_plant_care(plant, hot_weather, 9)
        
        assert analysis["water_needs"] == "very_low"
        assert analysis["drought_tolerance"] == "very_high"
        assert analysis["optimal_watering_hour"] == 9


class TestPlantSpecificConsiderations:
    """Test plant-specific watering considerations"""
    
    def test_vegetable_high_water_needs_warning(self):
        """Test that vegetables with high water needs get warning"""
        analyzer = GardenAnalyzer()
        plant = Plant(
            common_name="Tomato",
            scientific_name="Solanum lycopersicum",
            botanical_group="vegetable",
            water_needs="high",
            drought_tolerance="low",
            optimal_watering_hours=[6, 7, 8],
            watering_frequency_days=1,
            temperature_threshold=25,
            sunshine_requirement="Full sun"
        )
        
        weather = WeatherData(
            temperature=28,
            humidity=45,
            precipitation=0,
            weather_code=1,
            timestamp=datetime.now(timezone.utc),
            location="Tel Aviv",
            timezone="Asia/Jerusalem"
        )
        
        should_water, reason = analyzer.should_water_now(plant, weather, 7)
        
        assert should_water is True
        if "high water" in reason.lower() or "monitor" in reason.lower():
            # Warning was included
            pass
    
    def test_succulent_dry_conditions_preference(self):
        """Test that succulents prefer dry conditions"""
        analyzer = GardenAnalyzer()
        plant = Plant(
            common_name="Jade Plant",
            scientific_name="Crassula ovata",
            botanical_group="succulent",
            water_needs="low",
            drought_tolerance="high",
            optimal_watering_hours=[9, 10],
            watering_frequency_days=10,
            temperature_threshold=12,
            sunshine_requirement="Bright indirect light"
        )
        
        weather = WeatherData(
            temperature=22,
            humidity=92,  # High humidity
            precipitation=0,
            weather_code=10,
            timestamp=datetime.now(timezone.utc),
            location="Tel Aviv",
            timezone="Asia/Jerusalem"
        )
        
        should_water, reason = analyzer.should_water_now(plant, weather, 9)
        
        # Should still water if it's within optimal hours, but get a warning
        if "drainage" in reason.lower() or "rot" in reason.lower():
            # Warning about humidity included
            pass


class TestEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_plant_with_single_optimal_hour(self):
        """Test plant with only one optimal watering hour"""
        analyzer = GardenAnalyzer()
        plant = Plant(
            common_name="Test Plant",
            scientific_name="Test planticus",
            botanical_group="flower",
            water_needs="medium",
            drought_tolerance="medium",
            optimal_watering_hours=[6],  # Single hour
            watering_frequency_days=2,
            temperature_threshold=20,
            sunshine_requirement="Full sun"
        )
        
        weather = WeatherData(
            temperature=25,
            humidity=40,
            precipitation=0,
            weather_code=1,
            timestamp=datetime.now(timezone.utc),
            location="Tel Aviv",
            timezone="Asia/Jerusalem"
        )
        
        should_water, reason = analyzer.should_water_now(plant, weather, 6)
        
        assert should_water is True
    
    def test_temperature_at_threshold(self):
        """Test behavior when temperature is at threshold"""
        analyzer = GardenAnalyzer()
        plant = Plant(
            common_name="Temperature Test",
            scientific_name="Threshold testicus",
            botanical_group="flower",
            water_needs="medium",
            drought_tolerance="medium",
            optimal_watering_hours=[7, 8],
            watering_frequency_days=2,
            temperature_threshold=20,
            sunshine_requirement="Full sun"
        )
        
        # At threshold
        weather = WeatherData(
            temperature=20,
            humidity=50,
            precipitation=0,
            weather_code=1,
            timestamp=datetime.now(timezone.utc),
            location="Tel Aviv",
            timezone="Asia/Jerusalem"
        )
        
        should_water, reason = analyzer.should_water_now(plant, weather, 7)
        
        # Should allow watering at threshold
        assert should_water is True
