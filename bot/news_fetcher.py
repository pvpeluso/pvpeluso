import feedparser
from dataclasses import dataclass


@dataclass
class NewsItem:
    title: str
    description: str
    link: str
    published: str


def fetch_ai_news(max_items: int = 10) -> list[NewsItem]:
    url = (
        "https://news.google.com/rss/search"
        "?q=artificial+intelligence&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    )
    feed = feedparser.parse(url)
    items = []
    for entry in feed.entries[:max_items]:
        items.append(NewsItem(
            title=entry.get("title", ""),
            description=entry.get("summary", ""),
            link=entry.get("link", ""),
            published=entry.get("published", ""),
        ))
    return items
