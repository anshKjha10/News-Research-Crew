import sqlite3
from pathlib import Path

# Store DB in the tools directory for consistency
db_path = Path(__file__).parent / "news_store.db"

def __init__db():
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS articles(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                source TEXT,
                title TEXT,
                url TEXT UNIQUE,
                description TEXT,
                published_at TEXT
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error initializing database: {e}")

__init__db()


def save_articles(topic: str, articles: list[dict]) -> int:
    """Save articles to database. Returns count of articles saved."""
    if not articles:
        return 0
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    saved_count = 0
    
    for a in articles:
        try:
            cur.execute("""
                INSERT OR IGNORE INTO articles (topic, source, title, url, description, published_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                topic,
                a.get("source", "Unknown"),
                a.get("title", "No title"),
                a.get("url", ""),
                a.get("description", ""),
                a.get("published_at", ""),
            ))
            if cur.rowcount > 0:
                saved_count += 1
        except Exception as e:
            print(f"Error saving article {a.get('url', 'unknown')}: {e}")
            continue
    
    conn.commit()
    conn.close()
    return saved_count

def get_articles(topic: str, limit: int = 20) -> list[dict]:
    """Retrieve articles for a given topic from the database."""
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""
            SELECT source, title, url, description, published_at
            FROM articles WHERE topic = ?
            ORDER BY published_at DESC
            LIMIT ?
        """, (topic, limit))
        rows = cur.fetchall()
        conn.close()

        return [
            {
                'source': r[0],
                'title': r[1],
                'url': r[2],
                'description': r[3],
                'published_at': r[4],       
            }
            for r in rows
        ]
    except Exception as e:
        print(f"Error retrieving articles for topic '{topic}': {e}")
        return []


def get_article_count(topic: str) -> int:
    """Get the count of stored articles for a topic."""
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM articles WHERE topic = ?", (topic,))
        count = cur.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        print(f"Error counting articles for topic '{topic}': {e}")
        return 0


def get_all_topics() -> list[str]:
    """Get list of all unique topics in the database."""
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT topic FROM articles ORDER BY topic")
        topics = [row[0] for row in cur.fetchall()]
        conn.close()
        return topics
    except Exception as e:
        print(f"Error retrieving topics: {e}")
        return []