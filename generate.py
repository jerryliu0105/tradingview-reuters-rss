import requests
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone

API = "https://news-headlines.tradingview.com/v1/headlines"
PARAMS = {
    "category": "reuters",
    "lang": "zh",
    "limit": 40
}

def main():
    r = requests.get(API, params=PARAMS, timeout=20)
    r.raise_for_status()
    data = r.json()

    fg = FeedGenerator()
    fg.id("https://tw.tradingview.com/news/top-providers/reuters")
    fg.title("TradingView · Reuters 财经新闻")
    fg.link(href="https://tw.tradingview.com/news/top-providers/reuters", rel="alternate")
    fg.link(href="feed.xml", rel="self")
    fg.language("zh-Hant")
    fg.description("TradingView Reuters 新闻流（非官方 RSS）")

    now = datetime.now(timezone.utc)

    for item in data:
        fe = fg.add_entry()
        fe.id(item["id"])
        fe.title(item["title"])
        fe.link(href=item["link"])
        fe.published(now)
        fe.description(item["title"])

    fg.rss_file("feed.xml")

if __name__ == "__main__":
    main()
