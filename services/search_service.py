import asyncio
from duckduckgo_search import DDGS
from core.logger import logger

async def search_sector_opportunities(sector: str):
    """
    Search for market news and trade opportunities in a specific sector within India.
    """
    query = f"current trade opportunities and market analysis for {sector} sector in India"
    logger.info(f"Searching web for: {query}")
    results = []
    
    # Run duckduckgo_search in a thread pool as it's blocking
    loop = asyncio.get_event_loop()
    
    def fetch_search_results():
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=5))

    try:
        results = await loop.run_in_executor(None, fetch_search_results)
        logger.info(f"Successfully fetched {len(results)} search results for {sector}")
    except Exception as e:
        logger.error(f"Error during DuckDuckGo search for {sector}: {e}")
        return f"Could not fetch data for {sector}. Error: {str(e)}"

    if not results:
        logger.warning(f"No results found for {sector} after web search.")
        return f"No recent data found for {sector} in India."

    # Join results into a single context string
    context = "\n\n".join([f"Title: {res['title']}\nSnippet: {res['body']}" for res in results])
    return context
