import feedparser
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon', quiet=True)

def get_news_sentiment(stock_name):
    url = f"https://news.google.com/rss/search?q={stock_name}+stock&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)

    news_list = []
    sia = SentimentIntensityAnalyzer()

    for entry in feed.entries[:10]:
        title = entry.title
        link = entry.link
        published = entry.published

        score = sia.polarity_scores(title)
        compound = score['compound']

        if compound >= 0.05:
            sentiment = "😊 Positive"
        elif compound <= -0.05:
            sentiment = "😟 Negative"
        else:
            sentiment = "😐 Neutral"

        news_list.append({
            "title": title,
            "link": link,
            "published": published,
            "sentiment": sentiment,
            "score": compound
        })

    return news_list