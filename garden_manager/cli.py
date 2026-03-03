"""
CommandLine - Main CLI interface for the Garden Manager application

Handles both single plant mode and batch file mode with intelligent recommendations
"""

from datetime import datetime
from pathlib import Path
from typing import Optional, List
from .plant_database import PlantDatabase
from .weather_fetcher import WeatherFetcher
from .garden_analyzer import GardenAnalyzer
from .file_parser import FileParser


class CommandLine:
    """
    Main command-line interface for the Garden Manager application.
    Provides single plant and batch file processing modes.
    """
    
    # Color codes for better terminal output
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    def __init__(self):
        """Initialize the CLI with all required components"""
        self.db = PlantDatabase()
        self.weather = WeatherFetcher()
        self.analyzer = GardenAnalyzer()
        self.parser = FileParser()
    
    def get_current_hour(self) -> int:
        """Get current hour (0-23)"""
        return datetime.now().hour
    
    def _colored(self, text: str, color: str) -> str:
        """Apply color to text (graceful fallback for non-ANSI terminals)"""
        try:
            return f"{color}{text}{self.END}"
        except:
            return text
    
    def display_header(self):
        """Display application header with current date/time"""
        now = datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        time_str = now.strftime("%H:%M:%S")
        
        print("\n")
        print(self._colored("+-------------------------------------------------------+", self.CYAN))
        print(self._colored("|", self.CYAN) + self._colored("      GARDEN MANAGER - Plant Care Recommendations        ", self.BOLD) + self._colored("|", self.CYAN))
        print(self._colored("+-------------------------------------------------------+", self.CYAN))
        print()
        print(f"  Date: {self._colored(date_str, self.GREEN)}")
        print(f"  Time: {self._colored(time_str, self.GREEN)}")
        print()
    
    def display_weather(self):
        """Display current weather information"""
        try:
            weather = self.weather.fetch_weather()
            if weather is None:
                print(self._colored("  !! Could not fetch weather data\n", self.YELLOW))
                return
            
            print(self._colored("  +- WEATHER INFO -----------------------------------------------+", self.BLUE))
            print(self._colored("  |", self.BLUE) + f" Location: {weather.location}")
            print(self._colored("  |", self.BLUE) + f" Temperature: {self._colored(f'{weather.temperature}C', self.YELLOW)}")
            print(self._colored("  |", self.BLUE) + f" Humidity: {self._colored(f'{weather.humidity}%', self.CYAN)}")
            print(self._colored("  |", self.BLUE) + f" Precipitation: {self._colored(f'{weather.precipitation}mm', self.CYAN)}")
            print(self._colored("  +-------------------------------------------------------+", self.BLUE))
            print()
        except Exception as e:
            print(self._colored(f"  !! Could not fetch weather: {e}\n", self.YELLOW))
    
    def process_single_plant(self, plant_name: str) -> bool:
        """
        Process a single plant and display recommendations.
        
        Args:
            plant_name: Name of the plant
        
        Returns:
            True if plant was found and processed, False otherwise
        """
        # Fetch weather
        try:
            weather_data = self.weather.fetch_weather()
            if weather_data is None:
                print(self._colored("  [X] Could not fetch weather data\n", self.RED))
                return False
        except Exception as e:
            print(self._colored(f"  [X] Could not fetch weather data: {e}\n", self.RED))
            return False
        
        # Get plant
        plant = self.db.get_plant(plant_name)
        if plant is None:
            print(self._colored(f"  [X] Plant '{plant_name}' not found in database\n", self.RED))
            return False
        
        # Display plant info
        self._display_plant_info(plant, weather_data)
        
        return True
    
    def process_plant_file(self, file_path: str) -> dict:
        """
        Process a file with plant names and display recommendations for each.
        
        Args:
            file_path: Path to the file with plant names
        
        Returns:
            Dictionary with processing statistics
        """
        # Parse file
        plants = self.parser.parse_file(file_path)
        if plants is None:
            print(self._colored(f"  [X] File not found: {file_path}\n", self.RED))
            return {"total": 0, "found": 0, "not_found": 0, "errors": []}
        
        if len(plants) == 0:
            print(self._colored(f"  [X] No plants found in file: {file_path}\n", self.RED))
            return {"total": 0, "found": 0, "not_found": 0, "errors": []}
        
        # Check for duplicates
        unique_plants, duplicates = self.parser.get_unique_plants(plants)
        if duplicates:
            print(self._colored(f"  !! {len(duplicates)} duplicate(s) found - processing unique names only\n", self.YELLOW))
        
        # Fetch weather once for all plants
        try:
            weather_data = self.weather.fetch_weather()
            if weather_data is None:
                print(self._colored(f"  [X] Could not fetch weather data\n", self.RED))
                return {"total": len(unique_plants), "found": 0, "not_found": len(unique_plants), "errors": ["Weather fetch failed"]}
        except Exception as e:
            print(self._colored(f"  [X] Could not fetch weather data: {e}\n", self.RED))
            return {"total": len(unique_plants), "found": 0, "not_found": len(unique_plants), "errors": [str(e)]}
        
        # Process each plant
        found_count = 0
        not_found = []
        
        print(self._colored(f"  Processing {len(unique_plants)} plant(s)...\n", self.CYAN))
        
        for plant_name in unique_plants:
            plant = self.db.get_plant(plant_name)
            
            if plant is None:
                print(self._colored(f"  [X] {plant_name}", self.RED))
                not_found.append(plant_name)
            else:
                found_count += 1
                self._display_plant_info_compact(plant, weather_data)
        
        # Display summary
        print()
        print(self._colored("  +- BATCH SUMMARY ----------------------------------------------+", self.BLUE))
        print(self._colored("  |", self.BLUE) + f" Total plants: {self._colored(str(len(unique_plants)), self.BOLD)}")
        print(self._colored("  |", self.BLUE) + f" Found: {self._colored(str(found_count), self.GREEN)}")
        print(self._colored("  |", self.BLUE) + f" Not found: {self._colored(str(len(not_found)), self.RED)}")
        if not_found:
            print(self._colored("  |", self.BLUE) + f" Missing: {', '.join(not_found)}")
        print(self._colored("  +-------------------------------------------------------+", self.BLUE))
        print()
        
        return {
            "total": len(unique_plants),
            "found": found_count,
            "not_found": len(not_found),
            "errors": not_found
        }
    
    def _display_plant_info(self, plant, weather):
        """Display comprehensive plant care information"""
        analysis = self.analyzer.analyze_plant_care(plant, weather, self.get_current_hour())
        
        # Water status
        water_status = self._colored("[OK] WATER NOW", self.GREEN) if analysis['should_water_now'] else self._colored("[--] NO WATERING", self.YELLOW)
        
        # Pre-compute optimal hour to avoid nested f-strings
        optimal_hour = analysis['optimal_watering_hour']
        optimal_hour_str = self._colored(f'{optimal_hour}:00', self.BOLD)
        
        print(self._colored("  +- PLANT INFORMATION ------------------------------------------+", self.GREEN))
        print(self._colored("  |", self.GREEN) + f" {self._colored(plant.common_name.upper(), self.BOLD)}")
        print(self._colored("  |", self.GREEN) + f" Scientific: {plant.scientific_name}")
        print(self._colored("  |", self.GREEN) + f" Type: {plant.botanical_group.title()}")
        print(self._colored("  +-------------------------------------------------------+", self.GREEN))
        print()
        
        print(self._colored("  +- WATERING ANALYSIS ------------------------------------------+", self.CYAN))
        print(self._colored("  |", self.CYAN) + f" Status: {water_status}")
        print(self._colored("  |", self.CYAN) + f" Reason: {analysis['watering_reason']}")
        print(self._colored("  |", self.CYAN))
        print(self._colored("  |", self.CYAN) + f" Optimal hour: {optimal_hour_str}")
        print(self._colored("  |", self.CYAN) + f" Frequency: {analysis['watering_frequency']}")
        print(self._colored("  |", self.CYAN) + f" Water needs: {analysis['water_needs'].upper()}")
        print(self._colored("  |", self.CYAN) + f" Drought tolerance: {analysis['drought_tolerance'].upper()}")
        print(self._colored("  +-------------------------------------------------------+", self.CYAN))
        print()
        
        print(self._colored("  +- SUNSHINE REQUIREMENTS ----------------------------------+", self.YELLOW))
        print(self._colored("  |", self.YELLOW) + f" {analysis['sunshine_recommendation']}")
        print(self._colored("  +-------------------------------------------------------+", self.YELLOW))
        print()
    
    def _display_plant_info_compact(self, plant, weather):
        """Display compact plant care information"""
        analysis = self.analyzer.analyze_plant_care(plant, weather, self.get_current_hour())
        
        water_status = self._colored("[OK]", self.GREEN) if analysis['should_water_now'] else self._colored("[--]", self.YELLOW)
        print(f"  {water_status} {self._colored(plant.common_name, self.BOLD)}")
        print(f"     {self._colored(analysis['watering_reason'], self.CYAN)}")
    
    def run_single_plant_mode(self):
        """Run single plant mode (interactive)"""
        self.display_header()
        self.display_weather()
        
        plant_name = input(self._colored("  Enter plant name (or 'quit' to exit): ", self.BOLD)).strip()
        
        if plant_name.lower() == 'quit':
            print(self._colored("\n  Goodbye! Happy gardening!\n", self.GREEN))
            return
        
        if not plant_name:
            print(self._colored("  [X] Plant name cannot be empty\n", self.RED))
            return
        
        success = self.process_single_plant(plant_name)
        
        if not success:
            plants = self.db.get_all_local_plants()
            print(self._colored("  Available plants (first 10):", self.CYAN))
            for i, p in enumerate(plants[:10], 1):
                print(f"    {i}. {p}")
            print()
    
    def run_batch_mode(self, file_path: str):
        """Run batch mode (file processing)"""
        self.display_header()
        self.display_weather()
        self.process_plant_file(file_path)
    
    def run(self, *args):
        """Main entry point for the CLI"""
        if len(args) == 0:
            # Interactive mode
            self.run_single_plant_mode()
        else:
            # Batch mode with file
            file_path = args[0]
            self.run_batch_mode(file_path)
