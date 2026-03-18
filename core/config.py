import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./trade_api.db")
    API_TITLE = "Trade Opportunities API"
    API_VERSION = "1.0.0"
    RATE_LIMIT_PER_MINUTE = 5

settings = Settings()
