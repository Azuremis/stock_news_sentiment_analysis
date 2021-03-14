from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

finviz_url = "https://finviz.com/quote.ashx?t="
tickers = ["GME", "TSLA", "NVDA", "ATVI", "MTCH"]

news_tables = {}

for ticker in tickers:
    # form url for chosen ticker
    url = finviz_url + ticker
    # submit request to finwiz website
    req = Request(url=url, headers={"user-agent": "senti-app"})
    # parse html from request object
    html = BeautifulSoup(urlopen(req), "html")
    # extract table which holds news titles
    news_tables[ticker] = html.find(id="news-table")

    print(news_tables)
