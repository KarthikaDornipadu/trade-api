# 🇮🇳 Trade Opportunities API (India)

A high-performance **FastAPI** service that analyzes market data for specific sectors in India. This project integrates the **Google Gemini AI** and real-time **web search capabilities** to deliver structured, actionable trade opportunity reports.

---

## 🚀 Deployment Links
- **Public API URL**: `https://trade-api-xxxx.onrender.com` (Replace with your actual Render URL)
- **Interactive Documentation**: `https://trade-api-xxxx.onrender.com/docs`


---

## 📑 Project Overview

The **Trade Opportunities API** is designed for investors, analysts, and developers looking for automated market insights. By simply providing a sector name (e.g., "Renewable Energy", "EV Infrastructure"), the system performs deep-dive research and returns a professional-grade analysis report in Markdown format.

### **Core Functionality**
- **🔍 Intelligent Sector Research**: Dynamically scrapes the latest news and market trends using DuckDuckGo search integration.
- **🤖 AI Analysis**: Processes raw market context through the **Gemini 1.5 Pro/Flash** model to extract insights, risks, and specific trade opportunities.
- **📦 Reliable Persistence**: Uses an **asynchronous SQLite database** (`databases` + `sqlalchemy`) to ensure your sector analysis history is saved across server restarts.
- **🛡️ Shielded Security**: Protected by API Key authentication and custom rate limiting.

---

## 🔑 Authentication & Authorization

This API is protected to prevent unauthorized usage and quota exhaustion.

### **Credentials**
- **Header Name**: `X-API-KEY`
- **API Key**: `trade_api_secret_key_123`

### **How to Authorize (Swagger UI Guide)**
1.  Open the `/docs` URL in your browser.
2.  Locate and click the green **"Authorize"** button at the top right.
3.  In the popup, paste `trade_api_secret_key_123` into the text field.
4.  Click **"Authorize"**, then **"Close"**.

### **How to Generate an Analysis**
1.  After authorizing, scroll down to the **"Analysis"** section.
2.  Click on the **`GET /analyze/{sector}`** endpoint to expand it.
3.  Click the **"Try it out"** button on the right side.
4.  Under **Parameters**, type the sector/topic you want to know about (e.g., `Renewable Energy`) in the **sector** field.
5.  Click the large blue **"Execute"** button.
6.  Scroll down to the **"Server response"** to see your professional market analysis!

---

## 🛠️ Technical Architecture

The project follows a modular, clean-code architecture for maximum scalability:

1.  **API Layer (`main.py`)**: Handles routing, dependency injection (security), and database connection life-cycles.
2.  **Service Layer**:
    - `services/search_service.py`: Responsible for external I/O (fetching real-time market news).
    - `services/ai_service.py`: Handles Gemini prompt engineering and response parsing.
3.  **Persistence Layer**: Uses **SQLAlchemy** to manage a local SQLite database for storing analysis results.
4.  **Security Layer (`core/security.py`)**: Implements the `X-API-KEY` verification and utilizes `slowapi` for request throttling.

---

## 📖 Endpoint Documentation

### **1. Analyze Sector**
- **Endpoint**: `GET /analyze/{sector}`
- **Description**: Triggers a real-time crawl and AI analysis of the specified sector.
- **Response**: Returns a JSON object containing the sector name and a comprehensive report.

### **2. Download Markdown Report**
- **Endpoint**: `GET /analyze/{sector}/download`
- **Description**: Fetches the latest analysis for a sector and returns it as a downloadable `.md` file.

### **3. Session History**
- **Endpoint**: `GET /sessions/history`
- **Description**: Provides a history of all analyses performed by the current API key holder.

---

## 💻 Local Installation & Setup

1.  **Clone the Repo**:
    ```bash
    git clone https://github.com/KarthikaDornipadu/trade-api.git
    cd trade-api
    ```

2.  **Environment Variables**:
    Create a `.env` file in the root directory:
    ```env
    GEMINI_API_KEY="your_api_key_from_google_ai_studio"
    DATABASE_URL="sqlite:///./trade_api.db"
    ```

3.  **Install & Run**:
    ```bash
    pip install -r requirements.txt
    python main.py
    ```

---

## 🛡️ Best Practices & Features
- **Rate Limiting**: Users are capped at 5 requests per minute to ensure service stability.
- **Asynchronous Execution**: The API uses `async/await` throughout to handle non-blocking I/O (AI calls and web searching).
- **Environment Management**: Sensitive keys are never hardcoded; they are managed via `.env` or system environment variables.
- **Pydantic Validation**: Ensures all inputs are sanitized and outputs follow a strict schema.
