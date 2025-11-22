import json
from pathlib import Path
from datetime import datetime, timedelta

# Store cache in the tools directory for consistency
CACHE_PATH = Path(__file__).parent / "news_cache.json"
MAX_AGE_MINUTES = 30 

def _load_cache():
    """Load cache from JSON file."""
    try:
        if not CACHE_PATH.exists():
            return {}
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading cache: {e}")
        return {}

def _save_cache(cache):
    """Save cache to JSON file."""
    try:
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2)
    except Exception as e:
        print(f"Error saving cache: {e}")

def get_cached(topic: str):
    """Get cached articles for a topic if they exist and are fresh."""
    try:
        cache = _load_cache()
        item = cache.get(topic)
        if not item:
            return None
        
        ts = datetime.fromisoformat(item["timestamp"])
        age = datetime.now() - ts
        
        if age > timedelta(minutes=MAX_AGE_MINUTES):
            print(f"Cache expired for '{topic}' (age: {age})")
            return None
        
        print(f"Cache hit for '{topic}' ({len(item['articles'])} articles, age: {age})")
        return item["articles"]
    except Exception as e:
        print(f"Error getting cached data for '{topic}': {e}")
        return None

def set_cached(topic: str, articles: list[dict]):
    """Cache articles for a topic with current timestamp."""
    try:
        if not articles:
            print(f"Warning: Attempting to cache empty articles for '{topic}'")
            return
        
        cache = _load_cache()
        cache[topic] = {
            "timestamp": datetime.now().isoformat(),
            "articles": articles,
        }
        _save_cache(cache)
        print(f"Cached {len(articles)} articles for '{topic}'")
    except Exception as e:
        print(f"Error caching data for '{topic}': {e}")
