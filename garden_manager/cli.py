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
    
    def __init__(self):
        """Initialize the CLI with all required components"""
        self.db = PlantDatabase()
        self.weather = WeatherFetcher()
        self.analyzer = GardenAnalyzer()
        self.parser = FileParser()
    
    def get_current_hour(self) -> int:
        """Get current hour (0-23)"""
        return datetime.now().hour
    
    def display_header(self):
        """Display application header with current date/time"""
        now = datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        time_str = now.strftime("%H:%M:%S")
        
        print("\n" + "=" * 60)
        print("🌱 Garden Manager - Plant Care Recommendations")
        print("=" * 60)
        print(f"📅 Date: {date_str}")
        print(f"🕐 Time: {time_str}")
        print("=" * 60 + "\n")
    
    def display_weather(self):
        """Display current weather information"""
        try:
            weather = self.weather.fetch_weather()
            print(f"🌡️  Current Weather in {weather.location}:")
            print(f"   Temperature: {weather.temperature}°C")
            print(f"   Humidity: {weather.humidity}%")
            print(f"   Precipitation: {weather.precipitation}mm")
            print()
        except Exception as e:
            print(f"⚠️  Could not fetch weather: {e}\n")
    
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
        except Exception as e:
            print(f"❌ Could not fetch weather data: {e}")
            return False
        
        # Get plant
        plant = self.db.get_plant(plant_name)
        if plant is None:
            print(f"❌ Plant '{plant_name}' not found in database")
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
            print(f"❌ File not found: {file_path}")
            return {"total": 0, "found": 0, "not_found": 0, "errors": []}
        
        if len(plants) == 0:
            print(f"❌ No plants found in file: {file_path}")
            return {"total": 0, "found": 0, "not_found": 0, "errors": []}
        
        # Check for duplicates
        unique_plants, duplicates = self.parser.get_unique_plants(plants)
        if duplicates:
            print(f"⚠️  {len(duplicates)} duplicate(s) found - processing unique names only\n")
        
        # Fetch weather once for all plants
        try:
            weather_data = self.weather.fetch_weather()
        except Exception as e:
            print(f"❌ Could not fetch weather data: {e}")
            return {"total": len(unique_plants), "found": 0, "not_found": len(unique_plants), "errors": [str(e)]}
        
        # Process each plant
        found_count = 0
        not_found = []
        
        print(f"Processing {len(unique_plants)} plant(s)...\n")
        
        for plant_name in unique_plants:
            plant = self.db.get_plant(plant_name)
            
            if plant is None:
                print(f"⚠️  ❌ '{plant_name}' - Not found")
                not_found.append(plant_name)
            else:
                found_count += 1
                self._display_plant_info_compact(plant, weather_data)
        
        # Display summary
        print("\n" + "=" * 60)
        print("📊 Summary:")
        print(f"   Total plants: {len(unique_plants)}")
        print(f"   Found: {found_count}")
        print(f"   Not found: {len(not_found)}")
        if not_found:
            print(f"   Missing: {', '.join(not_found)}")
        print("=" * 60 + "\n")
        
        return {
            "total": len(unique_plants),
            "found": found_count,
            "not_found": len(not_found),
            "errors": not_found
        }
    
    def _display_plant_info(self, plant, weather):
        """Display comprehensive plant care information"""
        analysis = self.analyzer.analyze_plant_care(plant, weather, self.get_current_hour())
        
        print("=" * 60)
        print(f"🌿 {plant.common_name}")
        print(f"   Scientific name: {plant.scientific_name}")
        print(f"   Type: {plant.botanical_group.title()}")
        print("=" * 60)
        
        print("\n💧 Watering Information:")
        print(f"   Should water now: {'✅ Yes' if analysis['should_water_now'] else '❌ No'}")
        print(f"   Reason: {analysis['watering_reason']}")
        print(f"   Optimal watering hour: {analysis['optimal_watering_hour']}:00")
        print(f"   Watering frequency: {analysis['watering_frequency']}")
        print(f"   Water needs: {analysis['water_needs']}")
        print(f"   Drought tolerance: {analysis['drought_tolerance']}")
        
        print("\n☀️  Sunshine Information:")
        print(f"   {analysis['sunshine_recommendation']}")
        
        print("\n" + "=" * 60 + "\n")
    
    def _display_plant_info_compact(self, plant, weather):
        """Display compact plant care information"""
        analysis = self.analyzer.analyze_plant_care(plant, weather, self.get_current_hour())
        
        water_status = "✅" if analysis['should_water_now'] else "❌"
        print(f"{water_status} {plant.common_name}")
        print(f"   → {analysis['watering_reason']}")
    
    def run_single_plant_mode(self):
        """Run single plant mode (interactive)"""
        self.display_header()
        self.display_weather()
        
        plant_name = input("Enter plant name (or 'quit' to exit): ").strip()
        
        if plant_name.lower() == 'quit':
            print("Goodbye! 👋\n")
            return
        
        if not plant_name:
            print("❌ Plant name cannot be empty")
            return
        
        success = self.process_single_plant(plant_name)
        
        if not success:
            print(f"💡 Available plants: {', '.join(self.db.get_all_local_plants()[:10])}")
    
    def run_batch_mode(self, file_path: str):
        """Run batch mode (file processing)"""
        self.display_header()
        self.display_weather()
        
        self.process_plant_file(file_path)
    
    def run(self, args: Optional[List[str]] = None):
        """
        Main entry point for the CLI.
        
        Args:
            args: Command line arguments. If None, will prompt for plant name.
                 If provided, first argument is plant name or file path
        """
        if args and len(args) > 0:
            # Check if it's a file (batch mode)
            file_path = args[0]
            if Path(file_path).exists() or file_path.endswith('.txt'):
                self.run_batch_mode(file_path)
            else:
                # Single plant mode
                self.display_header()
                self.display_weather()
                self.process_single_plant(file_path)
        else:
            # Interactive mode
            self.run_single_plant_mode()
