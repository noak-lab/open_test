"""
Unit tests for FileParser class
Tests file parsing, plant name validation, and duplicate detection
"""

import pytest
import tempfile
from pathlib import Path
from garden_manager.file_parser import FileParser


class TestParseFile:
    """Test file parsing functionality"""
    
    def test_parse_valid_file(self):
        """Test parsing a valid file with plant names"""
        parser = FileParser()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Tomato\nBasil\nRose\n")
            f.flush()
            temp_path = f.name
        
        try:
            plants = parser.parse_file(temp_path)
            
            assert plants is not None
            assert len(plants) == 3
            assert "Tomato" in plants
            assert "Basil" in plants
            assert "Rose" in plants
        finally:
            Path(temp_path).unlink()
    
    def test_parse_file_with_empty_lines(self):
        """Test parsing file with empty lines"""
        parser = FileParser()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Tomato\n\nBasil\n\n\nRose\n")
            f.flush()
            temp_path = f.name
        
        try:
            plants = parser.parse_file(temp_path)
            
            assert plants is not None
            assert len(plants) == 3
            assert plants == ["Tomato", "Basil", "Rose"]
        finally:
            Path(temp_path).unlink()
    
    def test_parse_file_with_whitespace(self):
        """Test that whitespace is stripped from plant names"""
        parser = FileParser()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("  Tomato  \nBasil   \n   Rose\n")
            f.flush()
            temp_path = f.name
        
        try:
            plants = parser.parse_file(temp_path)
            
            assert plants is not None
            assert len(plants) == 3
            assert plants[0] == "Tomato"
            assert plants[1] == "Basil"
            assert plants[2] == "Rose"
        finally:
            Path(temp_path).unlink()
    
    def test_parse_file_with_comments(self):
        """Test that comment lines are skipped"""
        parser = FileParser()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("# This is a comment\nTomato\n# Another comment\nBasil\n")
            f.flush()
            temp_path = f.name
        
        try:
            plants = parser.parse_file(temp_path)
            
            assert plants is not None
            assert len(plants) == 2
            assert "Tomato" in plants
            assert "Basil" in plants
            assert not any(p.startswith('#') for p in plants)
        finally:
            Path(temp_path).unlink()
    
    def test_parse_nonexistent_file(self):
        """Test parsing non-existent file returns None"""
        parser = FileParser()
        plants = parser.parse_file("/nonexistent/path/to/file.txt")
        
        assert plants is None
    
    def test_parse_directory_returns_none(self):
        """Test parsing directory instead of file returns None"""
        parser = FileParser()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            plants = parser.parse_file(temp_dir)
            
            assert plants is None
    
    def test_parse_empty_file(self):
        """Test parsing empty file"""
        parser = FileParser()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("")
            f.flush()
            temp_path = f.name
        
        try:
            plants = parser.parse_file(temp_path)
            
            assert plants is not None
            assert len(plants) == 0
        finally:
            Path(temp_path).unlink()
    
    def test_parse_file_with_only_comments_and_whitespace(self):
        """Test parsing file with only comments and whitespace"""
        parser = FileParser()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("# Comment 1\n\n# Comment 2\n   \n# Comment 3\n")
            f.flush()
            temp_path = f.name
        
        try:
            plants = parser.parse_file(temp_path)
            
            assert plants is not None
            assert len(plants) == 0
        finally:
            Path(temp_path).unlink()


class TestParseContent:
    """Test content parsing"""
    
    def test_parse_content_basic(self):
        """Test parsing basic content"""
        parser = FileParser()
        content = "Tomato\nBasil\nRose"
        
        plants = parser._parse_content(content)
        
        assert len(plants) == 3
        assert plants == ["Tomato", "Basil", "Rose"]
    
    def test_parse_content_with_tabs(self):
        """Test parsing content with tabs"""
        parser = FileParser()
        content = "\tTomato\n\tBasil\n\tRose"
        
        plants = parser._parse_content(content)
        
        assert len(plants) == 3
        assert plants == ["Tomato", "Basil", "Rose"]
    
    def test_parse_content_with_mixed_whitespace(self):
        """Test parsing content with mixed whitespace"""
        parser = FileParser()
        content = "  \t  Tomato  \t  \nBasil\n\t\tRose  "
        
        plants = parser._parse_content(content)
        
        assert len(plants) == 3
        assert plants[0] == "Tomato"
        assert plants[1] == "Basil"
        assert plants[2] == "Rose"


class TestValidatePlantNames:
    """Test plant name validation"""
    
    def test_validate_valid_names(self):
        """Test validating valid plant names"""
        parser = FileParser()
        names = ["Tomato", "Basil", "Rose"]
        
        valid, errors = parser.validate_plant_names(names)
        
        assert len(valid) == 3
        assert len(errors) == 0
        assert valid == names
    
    def test_validate_names_with_spaces(self):
        """Test validating names with spaces"""
        parser = FileParser()
        names = ["Lemon Tree", "Aloe Vera", "Jade Plant"]
        
        valid, errors = parser.validate_plant_names(names)
        
        assert len(valid) == 3
        assert len(errors) == 0
    
    def test_validate_names_with_hyphens(self):
        """Test validating names with hyphens"""
        parser = FileParser()
        names = ["Passion-Fruit", "Bird-of-Paradise"]
        
        valid, errors = parser.validate_plant_names(names)
        
        assert len(valid) == 2
        assert len(errors) == 0
    
    def test_validate_empty_name(self):
        """Test validating empty name"""
        parser = FileParser()
        names = ["Tomato", "", "Basil"]
        
        valid, errors = parser.validate_plant_names(names)
        
        assert len(valid) == 2
        assert len(errors) == 1
        assert "Empty" in errors[0][1]
    
    def test_validate_names_with_invalid_characters(self):
        """Test validating names with invalid characters"""
        parser = FileParser()
        names = ["Tom@to", "Bas$il", "Rose!"]
        
        valid, errors = parser.validate_plant_names(names)
        
        assert len(errors) == 3
        assert all("Invalid characters" in error[1] for error in errors)
    
    def test_validate_mixed_valid_and_invalid(self):
        """Test validating mix of valid and invalid names"""
        parser = FileParser()
        names = ["Tomato", "Tom@to", "Basil", "Rose!", "Mint"]
        
        valid, errors = parser.validate_plant_names(names)
        
        assert len(valid) == 3
        assert len(errors) == 2
        assert valid == ["Tomato", "Basil", "Mint"]
    
    def test_validate_returns_line_numbers(self):
        """Test that validation returns line numbers for errors"""
        parser = FileParser()
        names = ["Tomato", "", "Basil"]
        
        valid, errors = parser.validate_plant_names(names)
        
        assert len(errors) == 1
        assert errors[0][0] == 2  # Second line


class TestCountPlants:
    """Test plant counting"""
    
    def test_count_plants_in_file(self):
        """Test counting plants in a file"""
        parser = FileParser()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Tomato\nBasil\nRose\nMint\nCactus")
            f.flush()
            temp_path = f.name
        
        try:
            count = parser.count_plants(temp_path)
            
            assert count == 5
        finally:
            Path(temp_path).unlink()
    
    def test_count_plants_nonexistent_file(self):
        """Test counting plants in non-existent file"""
        parser = FileParser()
        count = parser.count_plants("/nonexistent/file.txt")
        
        assert count is None
    
    def test_count_plants_empty_file(self):
        """Test counting plants in empty file"""
        parser = FileParser()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("")
            f.flush()
            temp_path = f.name
        
        try:
            count = parser.count_plants(temp_path)
            
            assert count == 0
        finally:
            Path(temp_path).unlink()


class TestGetUniquePlants:
    """Test duplicate detection and unique plant extraction"""
    
    def test_get_unique_plants_no_duplicates(self):
        """Test getting unique plants when none are duplicates"""
        parser = FileParser()
        names = ["Tomato", "Basil", "Rose"]
        
        unique, duplicates = parser.get_unique_plants(names)
        
        assert len(unique) == 3
        assert len(duplicates) == 0
        assert unique == names
    
    def test_get_unique_plants_with_duplicates(self):
        """Test getting unique plants with duplicates"""
        parser = FileParser()
        names = ["Tomato", "Basil", "Tomato", "Rose", "Basil"]
        
        unique, duplicates = parser.get_unique_plants(names)
        
        assert len(unique) == 3
        assert len(duplicates) == 2
        assert "Tomato" in unique
        assert "Basil" in unique
        assert "Rose" in unique
        assert "Tomato" in duplicates
        assert "Basil" in duplicates
    
    def test_get_unique_plants_case_insensitive(self):
        """Test that duplicate detection is case-insensitive"""
        parser = FileParser()
        names = ["Tomato", "tomato", "TOMATO"]
        
        unique, duplicates = parser.get_unique_plants(names)
        
        assert len(unique) == 1
        assert len(duplicates) == 2
    
    def test_get_unique_plants_preserves_original_case(self):
        """Test that original case is preserved in unique list"""
        parser = FileParser()
        names = ["Tomato", "tomato", "TOMATO"]
        
        unique, duplicates = parser.get_unique_plants(names)
        
        # First occurrence should be preserved
        assert unique[0] == "Tomato"
    
    def test_get_unique_plants_empty_list(self):
        """Test with empty list"""
        parser = FileParser()
        names = []
        
        unique, duplicates = parser.get_unique_plants(names)
        
        assert len(unique) == 0
        assert len(duplicates) == 0
    
    def test_get_unique_plants_all_duplicates(self):
        """Test with all duplicate names"""
        parser = FileParser()
        names = ["Tomato", "Tomato", "Tomato"]
        
        unique, duplicates = parser.get_unique_plants(names)
        
        assert len(unique) == 1
        assert len(duplicates) == 1  # Only tracks Tomato once as a duplicate
        assert unique[0] == "Tomato"
        assert duplicates[0] == "Tomato"


class TestParserEdgeCases:
    """Test edge cases and special scenarios"""
    
    def test_parse_file_with_unicode_names(self):
        """Test parsing file with unicode plant names"""
        parser = FileParser()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', encoding='utf-8', delete=False) as f:
            f.write("Tomaté\nBasilíc\nRosé\n")
            f.flush()
            temp_path = f.name
        
        try:
            plants = parser.parse_file(temp_path)
            
            assert plants is not None
            assert len(plants) == 3
        finally:
            Path(temp_path).unlink()
    
    def test_parse_file_with_numbers(self):
        """Test parsing plant names with numbers"""
        parser = FileParser()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Tomato 1\nBasil 2\nRose 3\n")
            f.flush()
            temp_path = f.name
        
        try:
            plants = parser.parse_file(temp_path)
            
            assert plants is not None
            assert len(plants) == 3
            assert "Tomato 1" in plants
        finally:
            Path(temp_path).unlink()
    
    def test_parse_very_long_file(self):
        """Test parsing file with many plant names"""
        parser = FileParser()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            for i in range(1000):
                f.write(f"Plant{i}\n")
            f.flush()
            temp_path = f.name
        
        try:
            plants = parser.parse_file(temp_path)
            
            assert plants is not None
            assert len(plants) == 1000
        finally:
            Path(temp_path).unlink()
    
    def test_parse_file_mixed_line_endings(self):
        """Test parsing file with mixed line endings"""
        parser = FileParser()
        
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.txt', delete=False) as f:
            # Mix of \n and \r\n
            f.write(b"Tomato\nBasil\r\nRose\n")
            f.flush()
            temp_path = f.name
        
        try:
            plants = parser.parse_file(temp_path)
            
            assert plants is not None
            assert len(plants) == 3
        finally:
            Path(temp_path).unlink()
