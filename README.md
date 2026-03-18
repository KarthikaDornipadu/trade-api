# Trade Opportunities API

A FastAPI-based service that analyzes market data for specific sectors in India and provides structured trade opportunity reports using Google Gemini AI.

## Features

- **Sector Analysis**: Accepts a sector name (e.g., "pharmaceuticals", "technology") and returns a markdown report.
- **AI-Powered**: Uses Google Gemini API for deep market analysis.
- **Fresh Data**: Integrates web search to fetch the latest market news and trends.
- **Security**: 
  - API Key Authentication (`X-API-KEY` header).
  - Rate Limiting (5 requests per minute).
  - Input validation with Pydantic.
- **Architecture**: Clean separation of data collection, AI analysis, and API layers.
- **Storage**: In-memory only (stateless/session-less for this version).

## Prerequisites

- Python 3.8+
- Google Gemini API Key (set in `.env`)

## Installation

1. Clone the repository and navigate to the project directory.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your `.env` file with your Gemini API key:
   ```env
   GEMINI_API_KEY="your_api_key_here"
   ```

## Running the Application

Start the FastAPI server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`.

## API Documentation

- **Interactive Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Authentication

Include the following header in your requests:
- `X-API-KEY: trade_api_secret_key_123`

### Single Endpoint: GET /analyze/{sector}

Analyze a specific sector in India.

**Sample Request:**
```bash
curl -H "X-API-KEY: trade_api_secret_key_123" http://localhost:8000/analyze/pharmaceuticals
```

**Expected Response:**
```json
{
  "sector": "pharmaceuticals",
  "report": "# Market Analysis Report for Pharmaceuticals Sector (India)...",
  "status": "success"
}
```

### Session History: GET /sessions/history

View the analysis history for the current session.

**Sample Request:**
```bash
curl -H "X-API-KEY: trade_api_secret_key_123" http://localhost:8000/sessions/history
```

## Project Structure

```
trade-api/
├── main.py              # Main API entry point and routes
├── .env                 # API Keys and sensitive configuration
├── requirements.txt     # List of project dependencies
├── README.md            # Setup and usage instructions
├── core/
│   ├── config.py        # Centralized configuration management
│   └── security.py      # Security (Auth & Rate Limiting)
├── services/
│   ├── search_service.py # Web scraping/searching logic
│   └── ai_service.py     # Gemini AI analysis logic
└── schemas/             # Pydantic models (optional, for scalability)
```

## Security & Best Practices

- **Rate Limiting**: Implemented via `slowapi` to prevent abuse.
- **Input Validation**: Sector names are validated using Pydantic models.
- **Environment Variables**: Sensitive keys are loaded from `.env`.
- **Async Handling**: All external I/O and AI calls are performed asynchronously.
