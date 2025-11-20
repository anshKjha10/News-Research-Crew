import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
MEDIASTACK_API_KEY = os.getenv("MEDIASTACK_API_KEY")

news_api_url = "https://newsapi.org/v2/everything"
mediastack_url = "http://api.mediastack.com/v1/news"
gdelt_url = "https://api.gdeltproject.org/api/v2/doc/doc"

async def _fetch(client, url, params):
    try:
        response = await client.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching from {url}: {e}")
        return {}

async def _fetchall(topic: str):
    async with httpx.AsyncClient() as client:
        tasks = []

        tasks.append(
            _fetch(client, news_api_url, {
                "q" : topic,
                "apikey": NEWS_API_KEY,
                "language": "en",
                "sortBy": "publishedAt"
            })
        )

        tasks.append(
            _fetch(client, mediastack_url, {
                "access_key" : MEDIASTACK_API_KEY,
                "keywords": topic,
                "languages": "en"
            })
        )

        tasks.append(
            _fetch(client, gdelt_url, {
                "query": topic,
                "mode": "artlist",  # Changed to lowercase
                "format": "json",   # Changed to lowercase
                "maxrecords": "100",
                "timespan": "24h"
            })
        )

        newsapi_res, mediastack_res, gdelt_res = await asyncio.gather(*tasks)

    articles = []

    for a in newsapi_res.get("articles", []):
        articles.append({
            "source": a.get("source", {}).get("name", "Unknown"),
            "title": a.get("title", "No title"),
            "url": a.get("url", ""),
            "description": a.get("description", ""),
            "published_at": a.get("publishedAt", "")
        })

    for a in mediastack_res.get("data", []):
        articles.append({
            "source": a.get("source", "Unknown"),
            "title": a.get("title", "No title"),
            "url": a.get("url", ""),
            "description": a.get("description", ""),
            "published_at": a.get("published_at", "")
        })

    for a in gdelt_res.get("articles", []):
        articles.append({
            "source": a.get("domain", "Unknown"),  # GDELT uses 'domain' not 'source'
            "title": a.get("title", "No title"),
            "url": a.get("url", ""),
            "description": a.get("title", ""),  # GDELT doesn't have separate description
            "published_at": a.get("seendate", "")
        })

    return articles

def news_fetcher_tool(topic: str) -> list[dict]:
    """Fetch news articles related to the given topic from multiple sources."""
    if not topic or not topic.strip():
        print("Error: Topic cannot be empty")
        return []
    
    if not NEWS_API_KEY:
        print("Warning: NEWS_API_KEY not found in environment")
    
    if not MEDIASTACK_API_KEY:
        print("Warning: MEDIASTACK_API_KEY not found in environment")
    
    return asyncio.run(_fetchall(topic))