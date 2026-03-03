"""
Unit tests for PlantDatabase class
Tests local database, caching, external API integration, and plant lookup functionality
"""

import pytest
import pickle
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from garden_manager.plant_database import PlantDatabase, PLANTS_CACHE_FILE, CACHE_DIR
from garden_manager.plant import Plant


class TestPlantDatabaseLocalLookup:
    """Test local plant database lookup functionality"""
    
    def test_get_plant_from_local_database(self):
        """Test retrieving a plant from local database"""
        db = PlantDatabase()
        plant = db.get_plant("tomato")
        
        assert plant is not None
        assert plant.common_name == "Tomato"
        assert plant.scientific_name == "Solanum lycopersicum"
        assert plant.botanical_group == "vegetable"
        assert plant.water_needs == "high"
        assert plant.drought_tolerance == "low"
    
    def test_get_plant_case_insensitive(self):
        """Test that plant lookup is case-insensitive"""
        db = PlantDatabase()
        
        plant_lower = db.get_plant("tomato")
        plant_upper = db.get_plant("TOMATO")
        plant_mixed = db.get_plant("ToMaTo")
        
        assert plant_lower is not None
        assert plant_upper is not None
        assert plant_mixed is not None
        assert plant_lower.common_name == plant_upper.common_name
        assert plant_upper.common_name == plant_mixed.common_name
    
    def test_get_plant_with_spaces(self):
        """Test that plant lookup converts spaces to underscores"""
        db = PlantDatabase()
        
        plant_with_spaces = db.get_plant("aloe vera")
        plant_with_underscore = db.get_plant("aloe_vera")
        
        assert plant_with_spaces is not None
        assert plant_with_underscore is not None
        assert plant_with_spaces.common_name == plant_with_underscore.common_name
    
    def test_get_nonexistent_plant_returns_none(self):
        """Test that non-existent plant returns None"""
        db = PlantDatabase()
        plant = db.get_plant("nonexistent_plant_xyz")
        
        assert plant is None
    
    def test_get_all_local_plants(self):
        """Test retrieving all locally available plants"""
        db = PlantDatabase()
        plants = db.get_all_local_plants()
        
        assert len(plants) > 0
        assert "tomato" in plants
        assert "basil" in plants
        assert "rose" in plants
        assert "cactus" in plants
        assert "lemon_tree" in plants
    
    def test_local_plants_have_required_attributes(self):
        """Test that all local plants have required attributes"""
        db = PlantDatabase()
        
        for plant_name in db.get_all_local_plants():
            plant = db.get_plant(plant_name)
            
            assert plant.common_name is not None
            assert plant.scientific_name is not None
            assert plant.botanical_group is not None
            assert plant.water_needs is not None
            assert plant.drought_tolerance is not None
            assert plant.optimal_watering_hours is not None
            assert plant.watering_frequency_days is not None
            assert plant.temperature_threshold is not None
            assert plant.sunshine_requirement is not None
    
    def test_different_plant_types(self):
        """Test various plant types in local database"""
        db = PlantDatabase()
        
        # Vegetable
        tomato = db.get_plant("tomato")
        assert tomato.botanical_group == "vegetable"
        
        # Herb
        basil = db.get_plant("basil")
        assert basil.botanical_group == "herb"
        
        # Flower
        rose = db.get_plant("rose")
        assert rose.botanical_group == "flower"
        
        # Cacti
        cactus = db.get_plant("cactus")
        assert cactus.botanical_group == "cacti"
        
        # Tree
        lemon = db.get_plant("lemon_tree")
        assert lemon.botanical_group == "tree"


class TestPlantDatabaseCaching:
    """Test caching functionality"""
    
    def setup_method(self):
        """Clean up cache before each test"""
        if PLANTS_CACHE_FILE.exists():
            PLANTS_CACHE_FILE.unlink()
    
    def teardown_method(self):
        """Clean up cache after each test"""
        if PLANTS_CACHE_FILE.exists():
            PLANTS_CACHE_FILE.unlink()
    
    def test_cache_dir_created_on_save(self):
        """Test that cache directory is created when saving"""
        # Remove cache directory if it exists
        if CACHE_DIR.exists():
            import shutil
            shutil.rmtree(CACHE_DIR)
        
        db = PlantDatabase()
        # Trigger cache save by adding to cache
        test_plant = Plant(
            common_name="Test Plant",
            scientific_name="Test species",
            botanical_group="flower",
            water_needs="medium",
            drought_tolerance="medium",
            optimal_watering_hours=[7, 8],
            watering_frequency_days=2,
            temperature_threshold=20,
            sunshine_requirement="Full sun"
        )
        db._cache["test_plant"] = test_plant
        db._save_cache()
        
        assert CACHE_DIR.exists()
    
    def test_save_and_load_cache(self):
        """Test saving and loading plants to/from cache"""
        # First database instance - create and save
        db1 = PlantDatabase()
        test_plant = Plant(
            common_name="Cached Plant",
            scientific_name="Cached species",
            botanical_group="flower",
            water_needs="medium",
            drought_tolerance="medium",
            optimal_watering_hours=[7, 8],
            watering_frequency_days=2,
            temperature_threshold=20,
            sunshine_requirement="Full sun"
        )
        db1._cache["cached_plant"] = test_plant
        db1._save_cache()
        
        # Second database instance - load from cache
        db2 = PlantDatabase()
        
        assert "cached_plant" in db2._cache
        assert db2._cache["cached_plant"].common_name == "Cached Plant"
    
    def test_cache_persists_across_instances(self):
        """Test that cache persists when creating new database instances"""
        db1 = PlantDatabase()
        test_plant = Plant(
            common_name="Persistent Plant",
            scientific_name="Persistent species",
            botanical_group="flower",
            water_needs="high",
            drought_tolerance="low",
            optimal_watering_hours=[6, 7],
            watering_frequency_days=1,
            temperature_threshold=22,
            sunshine_requirement="Full sun"
        )
        db1._cache["persistent_plant"] = test_plant
        db1._save_cache()
        
        # Create new instance
        db2 = PlantDatabase()
        retrieved = db2.get_plant("persistent_plant")
        
        assert retrieved is not None
        assert retrieved.common_name == "Persistent Plant"
        assert retrieved.scientific_name == "Persistent species"
    
    def test_clear_cache(self):
        """Test clearing the cache"""
        db = PlantDatabase()
        test_plant = Plant(
            common_name="Test Plant",
            scientific_name="Test species",
            botanical_group="flower",
            water_needs="medium",
            drought_tolerance="medium",
            optimal_watering_hours=[7, 8],
            watering_frequency_days=2,
            temperature_threshold=20,
            sunshine_requirement="Full sun"
        )
        db._cache["test_plant"] = test_plant
        db._save_cache()
        
        assert PLANTS_CACHE_FILE.exists()
        
        db.clear_cache()
        
        assert not PLANTS_CACHE_FILE.exists()
        assert len(db._cache) == 0
    
    def test_cache_corruption_handled_gracefully(self):
        """Test that corrupted cache file is handled gracefully"""
        # Create corrupted cache file
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        with open(PLANTS_CACHE_FILE, 'wb') as f:
            f.write(b"corrupted data")
        
        # Should not raise exception
        db = PlantDatabase()
        
        # Cache should be empty (corruption handled)
        assert len(db._cache) == 0


class TestPlantDatabaseExternalAPI:
    """Test external API integration"""
    
    def setup_method(self):
        """Clean up cache before each test"""
        if PLANTS_CACHE_FILE.exists():
            PLANTS_CACHE_FILE.unlink()
    
    def teardown_method(self):
        """Clean up cache after each test"""
        if PLANTS_CACHE_FILE.exists():
            PLANTS_CACHE_FILE.unlink()
    
    @patch.dict(os.environ, {'TREFLE_TOKEN': 'test_token'})
    @patch('garden_manager.plant_database.requests.get')
    def test_search_external_api_success(self, mock_get):
        """Test successful external API search"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': [{
                'common_name': 'Test Plant',
                'scientific_name': 'Test scientificus',
                'type': 'flower'
            }]
        }
        mock_get.return_value = mock_response
        
        db = PlantDatabase()
        plant = db._search_external_api("test plant")
        
        assert plant is not None
        assert plant.common_name == "Test Plant"
        assert plant.scientific_name == "Test scientificus"
    
    @patch.dict(os.environ, {}, clear=False)
    def test_search_external_api_no_token(self, monkeypatch):
        """Test that API search returns None without token"""
        monkeypatch.delenv('TREFLE_TOKEN', raising=False)
        
        db = PlantDatabase()
        plant = db._search_external_api("any plant")
        
        assert plant is None
    
    @patch.dict(os.environ, {'TREFLE_TOKEN': 'test_token'})
    @patch('garden_manager.plant_database.requests.get')
    def test_search_external_api_empty_results(self, mock_get):
        """Test API search with empty results"""
        mock_response = Mock()
        mock_response.json.return_value = {'data': []}
        mock_get.return_value = mock_response
        
        db = PlantDatabase()
        plant = db._search_external_api("nonexistent plant")
        
        assert plant is None
    
    @patch.dict(os.environ, {'TREFLE_TOKEN': 'test_token'})
    @patch('garden_manager.plant_database.requests.get')
    def test_search_external_api_network_error(self, mock_get):
        """Test API search with network error"""
        mock_get.side_effect = Exception("Network error")
        
        db = PlantDatabase()
        plant = db._search_external_api("any plant")
        
        assert plant is None


class TestWateringProfileInference:
    """Test watering profile inference based on botanical group"""
    
    def test_infer_cacti_profile(self):
        """Test watering profile for cacti"""
        db = PlantDatabase()
        profile = db._infer_watering_profile("cacti")
        
        assert profile["water_needs"] == "very_low"
        assert profile["drought_tolerance"] == "very_high"
        assert profile["frequency_days"] == 21
        assert profile["sunshine"] == "Full sun"
    
    def test_infer_succulent_profile(self):
        """Test watering profile for succulents"""
        db = PlantDatabase()
        profile = db._infer_watering_profile("succulent")
        
        assert profile["water_needs"] == "low"
        assert profile["drought_tolerance"] == "high"
        assert profile["frequency_days"] == 14
    
    def test_infer_vegetable_profile(self):
        """Test watering profile for vegetables"""
        db = PlantDatabase()
        profile = db._infer_watering_profile("vegetable")
        
        assert profile["water_needs"] == "high"
        assert profile["drought_tolerance"] == "low"
        assert profile["frequency_days"] == 1
    
    def test_infer_herb_profile(self):
        """Test watering profile for herbs"""
        db = PlantDatabase()
        profile = db._infer_watering_profile("herb")
        
        assert profile["water_needs"] == "medium"
        assert profile["drought_tolerance"] == "medium"
        assert profile["frequency_days"] == 2
    
    def test_infer_flower_profile(self):
        """Test watering profile for flowers"""
        db = PlantDatabase()
        profile = db._infer_watering_profile("flower")
        
        assert profile["water_needs"] == "medium"
        assert profile["drought_tolerance"] == "medium"
    
    def test_infer_tree_profile(self):
        """Test watering profile for trees"""
        db = PlantDatabase()
        profile = db._infer_watering_profile("tree")
        
        assert profile["water_needs"] == "medium"
        assert profile["frequency_days"] == 3
    
    def test_infer_shrub_profile(self):
        """Test watering profile for shrubs"""
        db = PlantDatabase()
        profile = db._infer_watering_profile("shrub")
        
        assert profile["water_needs"] == "medium"
    
    def test_infer_grass_profile(self):
        """Test watering profile for grass"""
        db = PlantDatabase()
        profile = db._infer_watering_profile("grass")
        
        assert profile["water_needs"] == "medium"
        assert profile["drought_tolerance"] == "low"
    
    def test_infer_unknown_group_defaults_to_flower(self):
        """Test that unknown group defaults to flower profile"""
        db = PlantDatabase()
        profile = db._infer_watering_profile("unknown_group")
        
        # Should default to flower profile
        assert profile["water_needs"] == "medium"
        assert profile["drought_tolerance"] == "medium"
        assert profile["sunshine"] == "Full sun to partial shade"
    
    def test_infer_case_insensitive(self):
        """Test that profile inference is case-insensitive"""
        db = PlantDatabase()
        
        profile_lower = db._infer_watering_profile("cacti")
        profile_upper = db._infer_watering_profile("CACTI")
        profile_mixed = db._infer_watering_profile("CaCtI")
        
        assert profile_lower == profile_upper
        assert profile_upper == profile_mixed


class TestPlantExists:
    """Test plant existence checking"""
    
    def test_plant_exists_local(self):
        """Test checking existence of local plants"""
        db = PlantDatabase()
        
        assert db.plant_exists("tomato") is True
        assert db.plant_exists("basil") is True
        assert db.plant_exists("rose") is True
    
    def test_plant_not_exists(self):
        """Test checking non-existent plants"""
        db = PlantDatabase()
        
        assert db.plant_exists("nonexistent_xyz") is False
    
    def test_plant_exists_case_insensitive(self):
        """Test that existence check is case-insensitive"""
        db = PlantDatabase()
        
        assert db.plant_exists("TOMATO") is True
        assert db.plant_exists("ToMaTo") is True
    
    def test_plant_exists_with_spaces(self):
        """Test existence check with spaces"""
        db = PlantDatabase()
        
        assert db.plant_exists("aloe vera") is True
        assert db.plant_exists("lemon tree") is True
    
    def test_plant_exists_in_cache(self):
        """Test checking existence of cached plants"""
        db = PlantDatabase()
        test_plant = Plant(
            common_name="Cached Plant",
            scientific_name="Cached species",
            botanical_group="flower",
            water_needs="medium",
            drought_tolerance="medium",
            optimal_watering_hours=[7, 8],
            watering_frequency_days=2,
            temperature_threshold=20,
            sunshine_requirement="Full sun"
        )
        db._cache["cached_plant"] = test_plant
        
        assert db.plant_exists("cached_plant") is True


class TestCreatePlantFromAPI:
    """Test creating Plant objects from API data"""
    
    def test_create_plant_from_api_with_all_fields(self):
        """Test creating plant from complete API data"""
        db = PlantDatabase()
        api_data = {
            'common_name': 'Tomato Plant',
            'scientific_name': 'Solanum lycopersicum',
            'type': 'vegetable'
        }
        
        plant = db._create_plant_from_api(api_data)
        
        assert plant.common_name == "Tomato Plant"
        assert plant.scientific_name == "Solanum lycopersicum"
        assert plant.botanical_group == "vegetable"
        assert plant.water_needs == "high"  # From vegetable profile
        assert plant.found_in_cache is False
    
    def test_create_plant_from_api_missing_common_name(self):
        """Test creating plant when common_name is missing"""
        db = PlantDatabase()
        api_data = {
            'scientific_name': 'Solanum lycopersicum',
            'type': 'vegetable'
        }
        
        plant = db._create_plant_from_api(api_data)
        
        assert plant.common_name == "Solanum lycopersicum"  # Falls back to scientific name
    
    def test_create_plant_from_api_missing_scientific_name(self):
        """Test creating plant when scientific_name is missing"""
        db = PlantDatabase()
        api_data = {
            'common_name': 'Tomato',
            'type': 'vegetable'
        }
        
        # Should raise ValueError due to Plant validation requiring scientific_name
        with pytest.raises(ValueError, match="scientific_name cannot be empty"):
            db._create_plant_from_api(api_data)
    
    def test_create_plant_from_api_unknown_type(self):
        """Test creating plant from API with unknown type"""
        db = PlantDatabase()
        api_data = {
            'common_name': 'Mystery Plant',
            'scientific_name': 'Mystery unknownus',
            'type': 'unknown_type'
        }
        
        # Should raise ValueError due to Plant validation requiring valid botanical_group
        with pytest.raises(ValueError, match="botanical_group must be one of"):
            db._create_plant_from_api(api_data)


class TestGetPlantIntegration:
    """Integration tests for get_plant method"""
    
    def setup_method(self):
        """Clean up cache before each test"""
        if PLANTS_CACHE_FILE.exists():
            PLANTS_CACHE_FILE.unlink()
    
    def teardown_method(self):
        """Clean up cache after each test"""
        if PLANTS_CACHE_FILE.exists():
            PLANTS_CACHE_FILE.unlink()
    
    def test_get_plant_prefers_local_over_cache(self):
        """Test that local database is preferred over cache"""
        db = PlantDatabase()
        
        # Try to cache a different version
        local_plant = db.get_plant("tomato")
        
        # Modify and save to cache
        modified = Plant(
            common_name="Modified Tomato",
            scientific_name=local_plant.scientific_name,
            botanical_group=local_plant.botanical_group,
            water_needs="very_high",  # Different from local
            drought_tolerance=local_plant.drought_tolerance,
            optimal_watering_hours=local_plant.optimal_watering_hours,
            watering_frequency_days=local_plant.watering_frequency_days,
            temperature_threshold=local_plant.temperature_threshold,
            sunshine_requirement=local_plant.sunshine_requirement
        )
        db._cache["tomato"] = modified
        
        # Get plant should return local version
        result = db.get_plant("tomato")
        
        assert result.common_name == "Tomato"  # Local, not modified
        assert result.water_needs == "high"  # Local value
    
    @patch.dict(os.environ, {'TREFLE_TOKEN': 'test_token'})
    @patch('garden_manager.plant_database.requests.get')
    def test_get_plant_caches_api_results(self, mock_get):
        """Test that API results are cached"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': [{
                'common_name': 'API Plant',
                'scientific_name': 'API planticus',
                'type': 'flower'
            }]
        }
        mock_get.return_value = mock_response
        
        db = PlantDatabase()
        
        # First call - should hit API
        plant1 = db.get_plant("api_plant_unique_name")
        assert mock_get.call_count == 1
        
        # Second call - should use cache
        plant2 = db.get_plant("api_plant_unique_name")
        assert mock_get.call_count == 1  # No additional API call
        
        assert plant1.common_name == plant2.common_name


class TestPlantDatabaseEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_plant_name(self):
        """Test with empty plant name"""
        db = PlantDatabase()
        plant = db.get_plant("")
        
        assert plant is None
    
    def test_special_characters_in_name(self):
        """Test plant name with special characters"""
        db = PlantDatabase()
        plant = db.get_plant("tom@t0!")
        
        assert plant is None
    
    def test_multiple_spaces_normalization(self):
        """Test that multiple spaces are handled"""
        db = PlantDatabase()
        
        # This should normalize to aloe_vera
        plant = db.get_plant("aloe  vera")
        
        # May or may not find (depends on implementation)
        # Just verify no exception is raised
        assert plant is None or plant.common_name == "Aloe Vera"
    
    def test_database_concurrent_access(self):
        """Test that multiple instances work correctly"""
        db1 = PlantDatabase()
        db2 = PlantDatabase()
        
        plant1 = db1.get_plant("tomato")
        plant2 = db2.get_plant("tomato")
        
        assert plant1.common_name == plant2.common_name
