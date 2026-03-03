"""
Constants module for the Garden Manager application.

Defines all magic numbers and configuration values used throughout the application.
Organized by category for easy reference and maintenance.
"""

# ============================================================================
# TEMPERATURE CONSTANTS (Celsius)
# ============================================================================

# Validation bounds
TEMP_MIN_VALID = -50  # Minimum valid temperature for validation
TEMP_MAX_VALID = 60   # Maximum valid temperature for validation

# Temperature classification thresholds
TEMP_COLD_THRESHOLD = 10    # Temperature below which is considered cold
TEMP_HOT_THRESHOLD = 30     # Temperature above which is considered hot
TEMP_VERY_HOT_THRESHOLD = 35  # Temperature above which is very hot
TEMP_WATERING_OFFSET = 5    # Temperature offset for watering decisions

# Plant-specific minimum temperatures
PLANT_MIN_TEMP_ALOE = 10
PLANT_MIN_TEMP_JADE = 12
PLANT_MIN_TEMP_CACTUS = 15
PLANT_MIN_TEMP_ROSEMARY = 15
PLANT_MIN_TEMP_OLIVE = 15
PLANT_MIN_TEMP_TULIP = 15
PLANT_MIN_TEMP_LETTUCE = 18
PLANT_MIN_TEMP_MINT = 18
PLANT_MIN_TEMP_ROSE = 20
PLANT_MIN_TEMP_LEMON = 20
PLANT_MIN_TEMP_BASIL = 22
PLANT_MIN_TEMP_CUCUMBER = 22
PLANT_MIN_TEMP_TOMATO = 25
PLANT_MIN_TEMP_SUNFLOWER = 25


# ============================================================================
# HUMIDITY CONSTANTS (Percentage)
# ============================================================================

HUMIDITY_MIN_VALID = 0    # Minimum valid humidity percentage
HUMIDITY_MAX_VALID = 100  # Maximum valid humidity percentage
HUMIDITY_DRY_THRESHOLD = 40   # Below this is considered dry
HUMIDITY_HUMID_THRESHOLD = 80  # Above this is considered humid
HUMIDITY_VERY_HUMID_THRESHOLD = 90  # Above this is considered very humid


# ============================================================================
# PRECIPITATION CONSTANTS (Millimeters)
# ============================================================================

PRECIPITATION_MIN_VALID = 0   # Minimum valid precipitation
PRECIPITATION_RAIN_THRESHOLD = 1  # Precipitation threshold to consider it "raining"


# ============================================================================
# TIME CONSTANTS (Hours - 24-hour format)
# ============================================================================

# Optimal watering hours for different plants
WATERING_HOUR_EARLY_MORNING = 6  # 6 AM (tomato, cucumber)
WATERING_HOUR_MID_MORNING = 7    # 7 AM (lettuce, mint, lemon)
WATERING_HOUR_LATE_MORNING_1 = 8  # 8 AM (rosemary, tulip, olive)
WATERING_HOUR_LATE_MORNING_2 = 9  # 9 AM (aloe, cactus, jade)
WATERING_HOUR_LATE_MORNING_3 = 10  # 10 AM (jade)
WATERING_HOUR_EVENING_1 = 18    # 6 PM (rose, basil)
WATERING_HOUR_EVENING_2 = 19    # 7 PM (basil)

# Hour boundaries for day/night
HOURS_PER_DAY = 24


# ============================================================================
# WATERING FREQUENCY CONSTANTS (Days)
# ============================================================================

WATERING_FREQ_DAILY = 1       # Water every day
WATERING_FREQ_EVERY_2_DAYS = 2    # Water every 2 days
WATERING_FREQ_EVERY_3_DAYS = 3    # Water every 3 days
WATERING_FREQ_WEEKLY = 7      # Water once per week
WATERING_FREQ_EVERY_10_DAYS = 10  # Water every 10 days
WATERING_FREQ_BIWEEKLY = 14   # Water every 2 weeks
WATERING_FREQ_EVERY_3_WEEKS = 21  # Water every 3 weeks


# ============================================================================
# GEOGRAPHIC CONSTANTS
# ============================================================================

# Default location: Tel Aviv, Israel
DEFAULT_LOCATION_LATITUDE = 32.0853
DEFAULT_LOCATION_LONGITUDE = 34.7818
DEFAULT_LOCATION_NAME = "Tel Aviv, Israel"


# ============================================================================
# API CONFIGURATION CONSTANTS
# ============================================================================

# Timeout values for external API calls (in seconds)
WEATHER_API_TIMEOUT = 10  # Open-Meteo API timeout
TREFLE_API_TIMEOUT = 5    # Trefle plant API timeout

# WMO Weather Code thresholds
WMO_CLOUDY_THRESHOLD = 50  # WMO codes below this are clear, above are cloudy/rainy


# ============================================================================
# UI / DISPLAY CONSTANTS
# ============================================================================

# Number of plants to display in available plants list
AVAILABLE_PLANTS_DISPLAY_LIMIT = 10

# String formatting constants
ANSI_COLOR_LENGTH_MULTIPLIER = 9  # Approximate extra characters from ANSI codes
