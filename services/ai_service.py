import google.generativeai as genai
import os
from dotenv import load_dotenv
from core.logger import logger

load_dotenv()

# Pre-configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    logger.error("GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

async def analyze_sector_data(sector: str, context: str):
    """
    Analyzes collected market data and generates a structured markdown report.
    """
    logger.info(f"Starting Gemini analysis for sector: {sector}")
    
    prompt = f"""
    You are an expert market analyst specializing in trade opportunities within India.
    Your task is to analyze the following collected news/data for the '{sector}' sector and generate a comprehensive markdown report.

    CONTEXT FROM MARKET SEARCH:
    {context}

    Your report MUST include:
    1. Title: Market Analysis Report for {sector.capitalize()} Sector (India)
    2. Executive Summary - Brief overview of the current state of the sector.
    3. Key Market Insights - Trends and current dynamics.
    4. Top Trade Opportunities - At least 3 specific opportunities with rationale.
    5. Risk Assessment - Potential headwinds or challenges in this sector.
    6. Future Outlook - Predictions for the next 6-12 months.

    FORMATTING REQUIREMENTS:
    - Use clear markdown headers (#, ##).
    - Use bullet points for readability.
    - Ensure the report is professional and actionable.
    """
    
    try:
        response = model.generate_content(prompt)
        logger.info(f"Successfully generated analysis for {sector}")
        return response.text
    except Exception as e:
        logger.error(f"Error analyzing {sector} with Gemini: {e}")
        return f"# Analysis Error\nCould not generate the analysis report due to an AI service error: {str(e)}"
