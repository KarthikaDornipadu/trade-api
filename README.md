# Trade Opportunities API

A FastAPI-based service that analyzes market data for specific sectors in India and provides structured trade opportunity reports using Google Gemini AI.

## 🚀 Live Demo
- **Public API Link**: `https://YOUR_LINK_HERE.onrender.com`
- **Interactive Documentation**: `https://YOUR_LINK_HERE.onrender.com/docs`

## Features

- **Sector Analysis**: Accepts a sector name (e.g., "pharmaceuticals", "technology") and returns a markdown report.
- **AI-Powered**: Uses Google Gemini API for deep market analysis.
- **Fresh Data**: Integrates web search to fetch the latest market news and trends.
- **Persistence**: SQLite database stores analysis history, so sessions aren't lost on restart.
- **Security**: 
  - API Key Authentication (`X-API-KEY` header).
  - Rate Limiting (5 requests per minute).
  - Input validation with Pydantic.
- **Architecture**: Clean separation of data collection, AI analysis, and API layers.

## Prerequisites

- Python 3.8+
- Google Gemini API Key (set in `.env` or as an environment variable)

## 🔑 Authentication

All endpoints require an API Key.

- **Header Name**: `X-API-KEY`
- **Key Value**: `trade_api_secret_key_123`

**How to Authorize on Swagger UI:**
1. Navigate to `/docs`.
2. Click the **"Authorize"** button (green lock icon).
3. Paste `trade_api_secret_key_123` into the `Value` field.
4. Click **"Authorize"** and then **"Close"**.

---

## Installation & Setup (Local)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/trade-api.git
   cd trade-api
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment**:
   Create a `.env` file:
   ```env
   GEMINI_API_KEY="your_actual_gemini_api_key"
   DATABASE_URL="sqlite:///./trade_api.db"
   ```

## Running the Application

### Locally:
```bash
python main.py
```

### Production (on Render):
Your `Procfile` is already configured for Gunicorn.
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

---

## 🛠️ API Endpoints

### 1. Root: `GET /`
Check service status and instructions.

### 2. Analyze: `GET /analyze/{sector}`
Analyze a specific sector in India.
**Sample Request:**
```bash
curl -H "X-API-KEY: trade_api_secret_key_123" http://localhost:8000/analyze/pharmaceuticals
```

### 3. Session History: `GET /sessions/history`
View the analysis history for your session.

### 4. Download Report: `GET /analyze/{sector}/download`
Download the analysis as a `.md` file.

---

## Project Structure

```
trade-api/
├── main.py              # Main API entry point and routes
├── .env                 # API Keys and sensitive configuration
├── requirements.txt     # List of project dependencies
├── README.md            # Setup and usage instructions
├── Procfile             # Deployment configuration for Render
├── core/
│   ├── config.py        # Centralized configuration management
│   └── security.py      # Security (Auth & Rate Limiting)
├── services/
│   ├── search_service.py # Web scraping/searching logic
│   └── ai_service.py     # Gemini AI analysis logic
└── schemas/             # Pydantic models for responses
```

## Security & Best Practices

- **Rate Limiting**: Implemented via `slowapi` to prevent abuse.
- **Input Validation**: Pydantic models ensure inputs are valid.
- **Environment Variables**: Sensitive keys are loaded securely.
- **Async Handling**: All external I/O and AI calls are non-blocking.
