import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Copernicus credentials
    COPERNICUS_USER = os.getenv('COPERNICUS_USERNAME', 'your_username')
    COPERNICUS_PASS = os.getenv('COPERNICUS_PASSWORD', 'your_password')
    
    # Farm location (Patna, Bihar example)
    FARM_LAT = float(os.getenv('FARM_LATITUDE', 25.5941))
    FARM_LON = float(os.getenv('FARM_LONGITUDE', 85.1376))
    FARM_AREA = float(os.getenv('FARM_AREA_KM', 2))
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_RAW = os.path.join(BASE_DIR, 'data', 'raw')
    DATA_PROCESSED = os.path.join(BASE_DIR, 'data', 'processed')
    DATA_UPLOADS = os.path.join(BASE_DIR, 'data', 'uploads')
    MODEL_DIR = os.path.join(BASE_DIR, 'models', 'trained')
    
    # Weather API
    WEATHER_API = os.getenv('WEATHER_API_URL', 'https://api.open-meteo.com/v1/forecast')
    
    # Model parameters
    IMAGE_SIZE = (256, 256)
    FORECAST_DAYS = 3