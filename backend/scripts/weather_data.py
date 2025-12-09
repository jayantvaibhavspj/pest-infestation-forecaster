"""
Weather Data Fetcher
Fetches weather forecast from Open-Meteo API
"""

import requests
import json
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config

class WeatherDataFetcher:
    def __init__(self):
        self.api_url = Config.WEATHER_API
        self.lat = Config.FARM_LAT
        self.lon = Config.FARM_LON
        
        # Create directories if they don't exist
        os.makedirs(Config.DATA_RAW, exist_ok=True)
        os.makedirs(Config.DATA_PROCESSED, exist_ok=True)
        
    def fetch_forecast(self, days=3):
        """
        Fetch weather forecast for next N days
        Returns: dict with temperature, wind_speed, precipitation
        """
        try:
            print(f"🌍 Fetching weather for: Lat {self.lat}, Lon {self.lon}")
            
            params = {
                'latitude': self.lat,
                'longitude': self.lon,
                'hourly': 'temperature_2m,wind_speed_10m,precipitation',
                'forecast_days': days
            }
            
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Save raw data
            output_path = os.path.join(Config.DATA_RAW, 'weather_forecast.json')
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Weather data saved to: {output_path}")
            return data
            
        except Exception as e:
            print(f"❌ Error fetching weather data: {e}")
            return None
    
    def process_weather(self, weather_data):
        """
        Process weather data into simple daily averages
        """
        if not weather_data:
            return None
            
        try:
            hourly = weather_data['hourly']
            temps = hourly['temperature_2m']
            wind_speeds = hourly['wind_speed_10m']
            
            # Calculate daily averages (24 hours = 1 day)
            daily_stats = []
            for day in range(3):
                start_idx = day * 24
                end_idx = start_idx + 24
                
                avg_temp = sum(temps[start_idx:end_idx]) / 24
                avg_wind = sum(wind_speeds[start_idx:end_idx]) / 24
                
                daily_stats.append({
                    'day': day + 1,
                    'avg_temperature': round(avg_temp, 2),
                    'avg_wind_speed': round(avg_wind, 2)
                })
            
            # Save processed data
            output_path = os.path.join(Config.DATA_PROCESSED, 'weather_processed.json')
            with open(output_path, 'w') as f:
                json.dump(daily_stats, f, indent=2)
            
            print(f"✅ Processed weather data saved to: {output_path}")
            return daily_stats
            
        except Exception as e:
            print(f"❌ Error processing weather data: {e}")
            return None


# Test function
if __name__ == "__main__":
    print("=" * 50)
    print("🌦️  Weather Data Fetcher Test")
    print("=" * 50)
    
    fetcher = WeatherDataFetcher()
    
    # Fetch forecast
    weather_data = fetcher.fetch_forecast(days=3)
    
    if weather_data:
        # Process it
        processed = fetcher.process_weather(weather_data)
        if processed:
            print("\n📊 Daily Weather Summary:")
            print("-" * 50)
            for day_data in processed:
                print(f"  Day {day_data['day']}: {day_data['avg_temperature']}°C, Wind: {day_data['avg_wind_speed']} km/h")
            print("=" * 50)