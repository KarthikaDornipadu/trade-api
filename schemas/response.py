from pydantic import BaseModel
from typing import Optional

class AnalysisResult(BaseModel):
    sector: str
    report: str
    status: str = "success"
    message: Optional[str] = None
