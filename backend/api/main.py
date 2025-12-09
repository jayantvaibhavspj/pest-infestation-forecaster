"""
FastAPI Backend for Pest Infestation Forecaster
"""

import os
import sys
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from scripts.weather_data import WeatherDataFetcher
from scripts.pest_detector import PestDetector

# Initialize FastAPI app
app = FastAPI(
    title="Pest Infestation Forecaster API",
    description="AI-powered pest forecasting for agriculture",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models
weather_fetcher = WeatherDataFetcher()
pest_detector = PestDetector()

# Load trained model
try:
    if not pest_detector.load_model():
        print("⚠️  No trained model found. Please train the model first.")
except Exception as e:
    print(f"⚠️  Could not load model: {e}")


@app.get("/")
async def root():
    """API Health Check"""
    return {
        "status": "online",
        "message": "Pest Infestation Forecaster API",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/weather")
async def get_weather():
    """
    Fetch current weather forecast
    """
    try:
        # Fetch weather data
        weather_data = weather_fetcher.fetch_forecast(days=3)
        
        if weather_data:
            # Process it
            processed = weather_fetcher.process_weather(weather_data)
            
            return JSONResponse({
                "success": True,
                "data": {
                    "location": {
                        "latitude": Config.FARM_LAT,
                        "longitude": Config.FARM_LON
                    },
                    "forecast": processed,
                    "timestamp": datetime.now().isoformat()
                }
            })
        else:
            raise HTTPException(status_code=500, detail="Failed to fetch weather data")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload-image")
async def upload_drone_image(file: UploadFile = File(...)):
    """
    Upload drone image for pest detection
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Save uploaded file
        upload_path = os.path.join(Config.DATA_UPLOADS, file.filename)
        
        with open(upload_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Verify image can be opened
        try:
            img = Image.open(upload_path)
            img_size = img.size
        except Exception as e:
            os.remove(upload_path)
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        return JSONResponse({
            "success": True,
            "data": {
                "filename": file.filename,
                "path": upload_path,
                "size": img_size,
                "message": "Image uploaded successfully"
            }
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/detect-pests")
async def detect_pests(filename: str):
    """
    Run pest detection on uploaded image
    """
    try:
        image_path = os.path.join(Config.DATA_UPLOADS, filename)
        
        if not os.path.exists(image_path):
            raise HTTPException(status_code=404, detail="Image not found")
        
        # Run pest detection
        result = pest_detector.predict_image(image_path)
        
        if result is None:
            raise HTTPException(status_code=500, detail="Pest detection failed")
        
        return JSONResponse({
            "success": True,
            "data": {
                "filename": filename,
                "detection_result": result,
                "timestamp": datetime.now().isoformat()
            }
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/create-pest-map")
async def create_pest_map(filename: str):
    """
    Create a full pest infestation map from uploaded image
    """
    try:
        image_path = os.path.join(Config.DATA_UPLOADS, filename)
        
        if not os.path.exists(image_path):
            raise HTTPException(status_code=404, detail="Image not found")
        
        # Create pest map
        pest_map = pest_detector.create_pest_map(image_path, patch_size=64)
        
        if pest_map is None:
            raise HTTPException(status_code=500, detail="Pest map creation failed")
        
        # Calculate statistics
        total_patches = pest_map.size
        infected_patches = (pest_map > 0.5).sum()
        infection_rate = (infected_patches / total_patches) * 100
        
        return JSONResponse({
            "success": True,
            "data": {
                "filename": filename,
                "map_shape": pest_map.shape,
                "statistics": {
                    "total_patches": int(total_patches),
                    "infected_patches": int(infected_patches),
                    "infection_rate": round(infection_rate, 2)
                },
                "map_file": "pest_map.npy",
                "timestamp": datetime.now().isoformat()
            }
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/forecast")
async def get_pest_forecast():
    """
    Get 3-day pest spread forecast
    """
    try:
        # This would combine:
        # 1. Current pest map
        # 2. Weather forecast
        # 3. ML model prediction
        
        # For now, return mock forecast
        forecast = []
        for day in range(1, 4):
            forecast.append({
                "day": day,
                "risk_level": "MEDIUM" if day == 1 else "HIGH",
                "spread_probability": 0.45 + (day * 0.15),
                "recommended_action": "Monitor closely" if day == 1 else "Consider preventive treatment"
            })
        
        return JSONResponse({
            "success": True,
            "data": {
                "forecast": forecast,
                "timestamp": datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Email alert endpoints
@app.post("/api/setup-alerts")
async def setup_alerts(request: dict):
    """Setup email alerts for user"""
    try:
        email = request.get("email")
        enabled = request.get("enabled", True)
        
        print(f"\n📧 Email alerts enabled for: {email}")
        
        return {
            "status": "success",
            "message": f"Alerts enabled for {email}",
            "data": {"email": email, "enabled": enabled}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/send-alert")
async def send_alert(request: dict):
    """Send email alert (logs to console for now)"""
    try:
        recipient = request.get("email")
        subject = request.get("subject")
        message = request.get("message")
        
        # Log the alert to console
        print(f"\n{'='*60}")
        print(f"📧 EMAIL ALERT")
        print(f"{'='*60}")
        print(f"To: {recipient}")
        print(f"Subject: {subject}")
        print(f"Message: {message}")
        print(f"{'='*60}\n")
        
        return {
            "status": "success",
            "message": "Alert logged successfully",
            "data": {
                "recipient": recipient,
                "note": "Email logged to console (configure SMTP for actual sending)"
            }
        }
    except Exception as e:
        return {
            "status": "success",
            "message": "Email feature needs configuration",
            "data": {"note": "Setup Gmail App Password to enable emails"}
        }


@app.get("/api/generate-report")
async def generate_pdf_report():
    """
    Generate comprehensive PDF report (simplified version)
    """
    try:
        # For now, return a success message
        # In production, you would generate actual PDF using reportlab
        return JSONResponse({
            "success": True,
            "message": "PDF generation feature - Install reportlab to enable",
            "data": {
                "note": "Run: pip install reportlab",
                "timestamp": datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🚀 Starting Pest Infestation Forecaster API...")
    print(f"📍 Farm Location: {Config.FARM_LAT}, {Config.FARM_LON}")
    print("🌐 API will be available at: http://localhost:8000")
    print("📖 Docs available at: http://localhost:8000/docs")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)