from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from starlette.requests import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

# API Key Authentication
API_KEY = "trade_api_secret_key_123" # In a real app, this should be in .env
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

# Rate Limiting
limiter = Limiter(key_func=get_remote_address)
