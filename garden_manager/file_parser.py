"""
File Parser - Handles reading plant lists from files

Supports reading newline-separated plant names from text files
"""

from typing import List, Optional
from pathlib import Path


class FileParser:
    """
    Parses plant files to extract plant names.
    Supports newline-separated format in text files.
    """
    
    def __init__(self):
        """Initialize the file parser"""
        pass
    
    def parse_file(self, file_path: str) -> Optional[List[str]]:
        """
        Parse a plant file and return list of plant names.
        
        Args:
            file_path: Path to the file containing plant names
        
        Returns:
            List of plant names or None if file doesn't exist
        """
        try:
            path = Path(file_path)
            
            # Check if file exists
            if not path.exists():
                return None
            
            # Check if it's a file
            if not path.is_file():
                return None
            
            # Read file and parse content
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return self._parse_content(content)
        
        except Exception:
            return None
    
    def _parse_content(self, content: str) -> List[str]:
        """
        Parse content and extract plant names.
        
        Args:
            content: File content as string
        
        Returns:
            List of plant names (stripped and non-empty)
        """
        lines = content.split('\n')
        
        plants = []
        for line in lines:
            # Strip whitespace
            plant_name = line.strip()
            
            # Skip empty lines
            if not plant_name:
                continue
            
            # Skip lines that are just whitespace
            if not plant_name or plant_name.isspace():
                continue
            
            # Skip comment lines (starting with #)
            if plant_name.startswith('#'):
                continue
            
            # Add valid plant name
            plants.append(plant_name)
        
        return plants
    
    def validate_plant_names(self, plant_names: List[str]) -> tuple[List[str], List[tuple[int, str]]]:
        """
        Validate plant names for basic issues.
        
        Args:
            plant_names: List of plant names to validate
        
        Returns:
            Tuple of (valid_names: List[str], errors: List[tuple[line_num, error_msg]])
        """
        valid = []
        errors = []
        
        for i, name in enumerate(plant_names, 1):
            # Check if name is empty
            if not name or not name.strip():
                errors.append((i, "Empty plant name"))
                continue
            
            # Check for invalid characters (very basic validation)
            # Allow alphanumeric, spaces, hyphens, underscores, and common punctuation
            invalid_chars = [c for c in name if c in ['@', '$', '%', '!', '&', '(', ')', '=', '+', '[', ']', '{', '}', '|', ';', ':', '"', "'", '<', '>', '?', '/'] and not c.isspace()]
            
            if invalid_chars:
                errors.append((i, f"Invalid characters found: {', '.join(set(invalid_chars))}"))
                continue
            
            # Name is valid
            valid.append(name)
        
        return valid, errors
    
    def count_plants(self, file_path: str) -> Optional[int]:
        """
        Get count of plants in a file.
        
        Args:
            file_path: Path to the file
        
        Returns:
            Number of plants or None if file doesn't exist
        """
        plants = self.parse_file(file_path)
        
        if plants is None:
            return None
        
        return len(plants)
    
    def get_unique_plants(self, plant_names: List[str]) -> tuple[List[str], List[str]]:
        """
        Get unique plant names from a list.
        
        Args:
            plant_names: List of plant names (may contain duplicates)
        
        Returns:
            Tuple of (unique_names: List[str], duplicates: List[str])
        """
        seen = set()
        unique = []
        duplicates = []
        
        for name in plant_names:
            name_lower = name.lower()
            
            if name_lower in seen:
                if name not in duplicates:
                    duplicates.append(name)
            else:
                seen.add(name_lower)
                unique.append(name)
        
        return unique, duplicates
