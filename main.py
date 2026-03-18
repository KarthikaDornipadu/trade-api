import uvicorn
import uuid
from datetime import datetime
from typing import Optional, Dict, List
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel
import databases
import sqlalchemy

# Local imports
from services.search_service import search_sector_opportunities
from services.ai_service import analyze_sector_data
from core.security import limiter, get_api_key
from core.config import settings
from schemas.response import AnalysisResult
from core.logger import logger

# Database setup for persistence
database = databases.Database(settings.DATABASE_URL)
metadata = sqlalchemy.MetaData()

analyses = sqlalchemy.Table(
    "analyses",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("api_key", sqlalchemy.String),
    sqlalchemy.Column("sector", sqlalchemy.String),
    sqlalchemy.Column("report", sqlalchemy.Text),
    sqlalchemy.Column("timestamp", sqlalchemy.String)
)

# Create engine and tables
engine = sqlalchemy.create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
)
metadata.create_all(engine)

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="Analyzes market data for specific sectors in India and provides trade insights using Gemini AI."
)

# Rate limiting setup
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/", tags=["General"])
async def root():
    logger.info("Root endpoint accessed.")
    return {
        "status": "online",
        "service": settings.API_TITLE,
        "version": settings.API_VERSION,
        "endpoints": {
            "analyze": "/analyze/{sector}",
            "download": "/analyze/{sector}/download",
            "history": "/sessions/history",
            "docs": "/docs"
        },
        "instructions": "Pass X-API-KEY header with 'trade_api_secret_key_123' to authenticate."
    }

@app.get("/analyze/{sector}", response_model=AnalysisResult, tags=["Analysis"])
@limiter.limit("5/minute")
async def analyze_sector(
    request: Request,
    sector: str,
    api_key: str = Depends(get_api_key)
):
    """
    Accepts a sector name and returns a structured market analysis report for India.
    """
    logger.info(f"Received analysis request for sector: {sector}")
    
    if not sector:
        raise HTTPException(status_code=400, detail="Sector name is required.")

    # 1. Fetch current news and market data
    context = await search_sector_opportunities(sector)
    
    # 2. Analyze collected data with Gemini AI
    report = await analyze_sector_data(sector, context)
    
    # 3. Store in persistent history
    query = analyses.insert().values(
        api_key=api_key,
        sector=sector,
        report=report,
        timestamp=datetime.now().isoformat()
    )
    await database.execute(query)
    
    return AnalysisResult(
        sector=sector,
        report=report
    )

@app.get("/analyze/{sector}/download", tags=["Analysis"])
async def download_report(
    sector: str,
    api_key: str = Depends(get_api_key)
):
    """
    Returns the analysis report as a downloadable .md file content.
    """
    # Find the latest report for this sector in the current session
    query = analyses.select().where(
        sqlalchemy.and_(
            analyses.c.api_key == api_key,
            analyses.c.sector == sector
        )
    ).order_by(analyses.c.id.desc())
    
    record = await database.fetch_one(query)
    
    if record:
        latest_report = record["report"]
    else:
        # If not in session, trigger a new analysis
        context = await search_sector_opportunities(sector)
        latest_report = await analyze_sector_data(sector, context)
        
        # Save to history
        insert_query = analyses.insert().values(
            api_key=api_key,
            sector=sector,
            report=latest_report,
            timestamp=datetime.now().isoformat()
        )
        await database.execute(insert_query)

    return PlainTextResponse(
        content=latest_report,
        headers={
            "Content-Disposition": f"attachment; filename={sector}_market_analysis.md"
        }
    )

@app.get("/sessions/history", tags=["Session"])
async def get_session_history(api_key: str = Depends(get_api_key)):
    """
    Returns the analysis history for the current session/user.
    """
    logger.info("Fetching history for session.")
    
    query = analyses.select().where(analyses.c.api_key == api_key).order_by(analyses.c.id.desc())
    history = await database.fetch_all(query)
    
    # Masking for privacy (handle short keys gracefully)
    masked_id = "***" + str(api_key)[-4:] if api_key and len(str(api_key)) >= 4 else "***"
    
    # Return snippets instead of full reports for history list
    return {
        "session_id": masked_id,
        "history_count": len(history),
        "history": [
            {
                "timestamp": item["timestamp"],
                "sector": item["sector"],
                "report_preview": str(item["report"])[:150] + "..."
            } for item in history
        ]
    }

@app.on_event("startup")
async def startup_event():
    await database.connect()
    if not settings.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY is missing! Analysis calls will fail until it's added to .env.")
    else:
        logger.info("Service started successfully with valid API configuration.")

@app.on_event("shutdown")
async def shutdown_event():
    await database.disconnect()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
