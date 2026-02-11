import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone

URL = "https://tw.tradingview.com/news/top-providers/reuters"

def main():
    r = requests.get(URL, headers={
        "User-Agent": "Mozilla/5.0 RSS Generator"
    }, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")

    items = []
    for a in soup.select("a[href*='/news/']"):
        title = a.get_text(strip=True)
        link = "https://tw.tradingview.com" + a["href"]

        if len(title) < 10:
            continue

        items.append((title, link))

    seen = set()
    uniq = []
    for t, l in items:
        if t in seen:
            continue
        seen.add(t)
        uniq.append((t, l))

    fg = FeedGenerator()
    fg.id(URL)
    fg.title("TradingView · Reuters 财经新闻")
    fg.link(href=URL, rel="alternate")
    fg.link(href="feed.xml", rel="self")
    fg.language("zh-Hant")
    fg.description("TradingView Reuters 新闻流（非官方 RSS）")

    now = datetime.now(timezone.utc)

    for title, link in uniq[:40]:
        fe = fg.add_entry()
        fe.id(link)
        fe.title(title)
        fe.link(href=link)
        fe.published(now)
        fe.description(title)

    fg.rss_file("feed.xml")

if __name__ == "__main__":
    main()
