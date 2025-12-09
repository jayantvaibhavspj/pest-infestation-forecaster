# 🌾 Pest Infestation Forecaster

An AI-powered hyper-local pest infestation forecasting system for precision agriculture. Uses deep learning and weather data to predict pest outbreaks and provide actionable insights to farmers.

## 📋 Features

- **🤖 AI-Powered Pest Detection**: CNN-based model trained on drone imagery to detect pests
- **🌤️ Weather Integration**: Real-time weather data fetching and analysis
- **📍 Hyper-Local Forecasting**: Predictions based on farm-specific location and conditions
- **🗺️ Pest Mapping**: Visual representation of pest-infested areas on farm maps
- **📧 Email Alerts**: Automated notifications for pest outbreak warnings
- **📊 Detailed Reports**: PDF reports with pest analysis and recommendations
- **🚀 REST API**: FastAPI backend with comprehensive endpoints
- **⚛️ Modern UI**: React frontend for easy interaction

## 🛠️ Tech Stack

**Backend:**
- Python 3.8+
- FastAPI (REST API)
- TensorFlow/Keras (Deep Learning)
- Pillow (Image Processing)
- OpenWeatherMap API (Weather Data)

**Frontend:**
- React
- Axios (HTTP Client)
- Leaflet/Mapbox (Maps)
- Chart.js (Data Visualization)

**Database:**
- SQLite (Development)
- PostgreSQL (Production)

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 14+ and npm
- Git

### Backend Setup

```bash
# Clone repository
git clone https://github.com/jayantvaibhavspj/pest-infestation-forecaster.git
cd pest-infestation-forecaster

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Create .env file
copy .env.example .env
# Edit .env with your configuration
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

## ⚙️ Configuration

### Backend Configuration

Edit `backend/.env`:

```env
# Farm Location
FARM_LAT=25.5941
FARM_LON=85.1376

# Weather API
OPENWEATHER_API_KEY=your_api_key_here
WEATHER_UPDATE_INTERVAL=3600

# Email Alerts
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# Model Path
MODEL_PATH=models/trained/pest_detector.h5
```

## 🚀 Running the Application

### Start Backend API

```bash
cd backend
python api/main.py
```

API will be available at:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs

### Start Frontend (in new terminal)

```bash
cd frontend
npm start
```

Frontend will open at: http://localhost:3000

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/weather` | GET | Fetch current weather forecast |
| `/api/upload-image` | POST | Upload drone image |
| `/api/detect-pests` | POST | Detect pests in image |
| `/api/create-pest-map` | POST | Generate pest distribution map |
| `/api/forecast` | GET | Get pest infestation forecast |
| `/api/setup-alerts` | POST | Setup email alerts |
| `/api/send-alert` | POST | Send pest alert |
| `/api/generate-report` | GET | Generate PDF report |

## 🧠 Model Training

To train the pest detection model:

```bash
cd backend/scripts
python train_model.py --data-path ./data/training --epochs 50 --batch-size 32
```

Training data should be organized as:
```
data/training/
├── pests/
│   ├── pest_image_1.jpg
│   └── pest_image_2.jpg
└── healthy/
    ├── healthy_image_1.jpg
    └── healthy_image_2.jpg
```

## 📊 Project Structure

```
pest-infestation-forecaster/
├── backend/
│   ├── api/
│   │   └── main.py              # FastAPI application
│   ├── scripts/
│   │   ├── pest_detector.py     # Pest detection model
│   │   ├── weather_data.py      # Weather API integration
│   │   └── train_model.py       # Model training script
│   ├── models/
│   │   └── trained/
│   │       └── pest_detector.h5 # Trained model
│   ├── config.py                # Configuration
│   └── requirements.txt          # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   └── App.js               # Main App
│   └── package.json             # Node dependencies
├── data/
│   └── uploads/                 # Uploaded images
└── README.md
```

## 📝 Usage

1. **Upload Drone Image**: Navigate to upload section and select drone imagery
2. **Detect Pests**: System automatically analyzes image using trained model
3. **View Pest Map**: See visual representation of pest distribution
4. **Check Forecast**: Get AI-powered pest outbreak predictions
5. **Setup Alerts**: Configure email notifications for outbreak warnings
6. **Generate Report**: Download detailed PDF analysis report

## 🔐 Security Considerations

- Keep API keys in `.env` file (never commit)
- Use HTTPS in production
- Implement authentication for API endpoints
- Validate all file uploads
- Use environment-specific configurations

## 🐛 Troubleshooting

**Port 8000 already in use:**
```bash
# Kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

**Model not found:**
- Ensure `pest_detector.h5` exists in `backend/models/trained/`
- Run training script if model doesn't exist

**Weather API errors:**
- Verify `OPENWEATHER_API_KEY` in `.env`
- Check API rate limits

## 📈 Performance Metrics

- Model Accuracy: ~94%
- Inference Time: ~2-3 seconds per image
- API Response Time: <500ms
- Supports up to 100 concurrent API requests

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👤 Author

**Prashant Vaibhav**
- GitHub: [@jayantvaibhavspj](https://github.com/jayantvaibhavspj)

## 📧 Support

For issues and questions, please open a GitHub issue or contact the author.

## 🙏 Acknowledgments

- TensorFlow/Keras for deep learning framework
- FastAPI for modern web framework
- OpenWeatherMap for weather data
- Agricultural research community for datasets

---

**Made with ❤️ for sustainable agriculture**
