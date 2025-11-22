from crewai.tools import tool
from news_research_crew.tools.news_fetcher import news_fetcher_tool
from news_research_crew.tools.news_store import save_articles, get_articles, get_all_topics
from news_research_crew.tools.simple_cache import get_cached, set_cached

@tool('news_fetcher')
def news_fetcher(topic: str):
    """Fetch merged news articles about a topic from NewsAPI, MediaStack, and GDELT."""
    return news_fetcher_tool(topic)  

@tool('news_store')
def save_news(topic: str, articles: list[dict]) -> str:
    """Persist a list of news articles for the given topic."""
    save_articles(topic, articles)
    return f"Saved {len(articles)} articles for topic '{topic}'."

@tool('news_retriever')
def retrieve_news(topic: str) -> list[dict]:
    """Retrieve stored news articles for a given topic."""
    return get_articles(topic)

@tool('news_topics')
def list_news_topics() -> list[str]:
    """List all topics for which news articles are stored."""
    return get_all_topics()

@tool('news_cache_getter')
def get_cached_news(topic: str):
    """Get cached news for a topic if it's still fresh, else return null."""
    return get_cached(topic)

@tool("set_cached_news")
def set_cached_news_tool(topic: str, articles: list[dict]):
    """Cache news articles for a topic for a short time."""
    set_cached(topic, articles)
    return "Cached."