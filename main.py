from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt

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

# extract article info from table rows
parsed_data = []
for ticker, news_table in news_tables.items():
    for row in news_table.findAll("tr"):
        # specify elements
        title = row.a.text
        date_data = row.td.text.split()

        # if only time is given
        if len(date_data) == 1:
            time = date_data[0]
        # if both time and date are given
        else:
            date = date_data[0]
            time = date_data[1]

        parsed_data.append([ticker, date, time, title])

# apply sentiment analysis to headlines using nltk vader package
df = pd.DataFrame(parsed_data, columns=["ticker", "date", "time", "title"])
vader = SentimentIntensityAnalyzer()
df["Sentiment"] = df.title.map(lambda t: vader.polarity_scores(t)["compound"])

# process data for easy visualisation
df["date"] = pd.to_datetime(df.date).dt.date
mean_df = df.groupby(["ticker", "date"]).mean()
mean_df = mean_df.unstack()  # have date as the first column
mean_df = mean_df.xs("Sentiment", axis="columns").transpose()  # remove Sentiment as column title

# visualise sentiment across dates
plt.figure(figsize=(20, 16))
mean_df.plot(kind="bar")
plt.show()