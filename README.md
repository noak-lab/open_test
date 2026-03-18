# 🌱 Garden Manager

A Python-based plant care management system that provides intelligent watering and sunlight recommendations based on current weather conditions and plant-specific requirements.

## Features

- **Intelligent Watering Recommendations**: Analyzes weather conditions (temperature, humidity, precipitation) to provide optimal watering advice
- **Plant Database**: 15+ pre-configured plants across multiple categories (vegetables, herbs, flowers, succulents, cacti, trees)
- **Weather Integration**: Fetches real-time weather data using the Open-Meteo API
- **External Plant Discovery**: Integrates with Trefle API for discovering new plants with auto-generated watering profiles
- **Smart Caching**: Pickle-based caching system to reduce API calls and improve performance
- **Batch Processing**: Process multiple plants from a text file
- **Flexible Interface**: Both single-plant and batch file modes

## Installation

### Prerequisites
- Python 3.10+
- pip

### Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd garden_manager
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up Trefle API token for external plant discovery:
```bash
export TREFLE_TOKEN=your_token_here
```

## Usage

### Interactive Mode
Run the program without arguments for an interactive prompt:
```bash
python main.py
```

### Single Plant Mode
Get recommendations for a specific plant:
```bash
python main.py tomato
python main.py "aloe vera"
```

### Batch File Mode
Process multiple plants from a text file:
```bash
python main.py plants.txt
```

**plants.txt format:**
```
Tomato
Basil
Rose
# Comments start with #
Cactus
```

## Architecture

### Core Modules

#### `plant.py`
- **Plant** dataclass with 9 attributes:
  - Common and scientific names
  - Botanical group classification
  - Water needs and drought tolerance levels
  - Optimal watering hours
  - Watering frequency (days)
  - Temperature threshold
  - Sunshine requirement

#### `weather_data.py`
- **WeatherData** dataclass with:
  - Temperature, humidity, precipitation
  - WMO weather code classification
  - Location and timezone information
  - Helper methods: `is_humid()`, `is_dry()`, `is_hot()`, `is_cold()`, etc.

#### `weather_fetcher.py`
- **WeatherFetcher** class:
  - Fetches weather data from Open-Meteo API
  - Supports custom locations with timezone handling
  - Default location: Tel Aviv, Israel

#### `plant_database.py`
- **PlantDatabase** class:
  - 15+ pre-configured local plants
  - Pickle-based caching at `~/.garden_manager_cache/plants.pkl`
  - External API integration (Trefle)
  - Auto-profile generation for discovered plants
  - Watering profile inference for 8 botanical groups

#### `garden_analyzer.py`
- **GardenAnalyzer** class:
  - Watering decision logic based on weather and plant needs
  - Analyzes temperature, humidity, precipitation effects
  - Plant-specific considerations (vegetables, succulents, drought-tolerant)
  - Sunlight recommendations
  - Comprehensive plant care analysis

#### `file_parser.py`
- **FileParser** class:
  - Parses newline-separated plant lists from text files
  - Supports comments (lines starting with #)
  - Plant name validation with error tracking
  - Duplicate detection (case-insensitive)
  - Unique plant extraction

#### `cli.py`
- **CommandLine** class:
  - Main user interface
  - Single plant and batch file modes
  - Weather display
  - Formatted output with plant care information
  - Processing summary for batch mode

### Test Coverage

- **test_plant_database.py**: 41 tests covering database operations, caching, and API integration
- **test_garden_analyzer.py**: 21 tests for watering logic and recommendations
- **test_file_parser.py**: 31 tests for file parsing and validation

**Total**: 93+ unit tests with 100% pass rate

## Display Format

For each plant, the system shows:

1. **Plant Information**
   - Common name
   - Scientific name
   - Botanical group

2. **Watering Recommendations**
   - Should water now (Yes/No)
   - Reason for recommendation
   - Optimal watering hour
   - Watering frequency
   - Water needs level
   - Drought tolerance level

3. **Sunlight Recommendations**
   - Required sunshine level
   - Current weather conditions

## Example Output

```
============================================================
🌱 Garden Manager - Plant Care Recommendations
============================================================
📅 Date: Monday, March 03, 2025
🕐 Time: 14:30:45
============================================================

🌡️  Current Weather in Tel Aviv:
   Temperature: 28°C
   Humidity: 45%
   Precipitation: 0mm

============================================================
🌿 Tomato
   Scientific name: Solanum lycopersicum
   Type: Vegetable
============================================================

💧 Watering Information:
   Should water now: ✅ Yes
   Reason: ✓ Dry conditions (humidity 45%) - plant needs water
   Optimal watering hour: 6:00
   Watering frequency: Daily
   Water needs: high
   Drought tolerance: low

☀️  Sunshine Information:
   Plant needs: Full sun (6-8 hours) | Current: Clear (good sunlight)

============================================================
```

## Watering Profiles

The system includes pre-configured watering profiles for:

- **Vegetables**: High water needs, frequent watering (daily)
- **Herbs**: Medium water needs, moderate frequency (2 days)
- **Flowers**: Medium water needs, moderate frequency (2 days)
- **Succulents**: Low water needs, weekly watering (14 days)
- **Cacti**: Very low water needs, infrequent watering (21 days)
- **Trees**: Medium water needs, weekly watering (7 days)

## Available Local Plants

**Vegetables**: Tomato, Cucumber, Lettuce
**Herbs**: Basil, Mint, Rosemary
**Flowers**: Rose, Sunflower, Tulip
**Succulents/Cacti**: Aloe Vera, Cactus, Jade Plant
**Trees**: Lemon Tree, Olive Tree

## External Dependencies

- **Open-Meteo API**: Free weather data (no authentication required)
- **Trefle API**: Plant discovery (requires TREFLE_TOKEN environment variable)

## Caching

The system uses a pickle-based cache for plant data:
- **Location**: `~/.garden_manager_cache/plants.pkl`
- **Purpose**: Reduce API calls for previously discovered plants
- **Management**: Cache is automatically updated when new plants are discovered

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run specific module tests
pytest garden_manager/tests/test_plant_database.py -v

# Run with coverage
pytest --cov=garden_manager
```

### Project Structure

```
garden_manager/
├── __init__.py
├── plant.py                 # Plant data model
├── weather_data.py          # Weather data model
├── weather_fetcher.py       # Weather API integration
├── plant_database.py        # Plant database with caching
├── garden_analyzer.py       # Analysis and recommendations
├── file_parser.py           # File parsing
├── cli.py                   # Command-line interface
└── tests/
    ├── test_plant_database.py
    ├── test_garden_analyzer.py
    └── test_file_parser.py
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
├── pytest.ini               # Pytest configuration
└── .gitignore               # Git ignore rules
```

## Future Enhancements

- Soil moisture sensor integration
- Plant growth tracking and history
- Multiple garden/location support
- Mobile app interface
- Database persistence (SQLite/PostgreSQL)
- Advanced scheduling and notifications
- Plant disease detection using image recognition

## License

MIT License

## Contributing

Contributions are welcome! Please follow these guidelines:
1. Create a feature branch from `develop`
2. Write tests for new features
3. Ensure all tests pass
4. Submit a pull request with clear description

## Contact

For questions or suggestions, please open an issue on the repository.

---

🌿 *Happy gardening!*
