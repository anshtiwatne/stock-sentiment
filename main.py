import configparser
import re
import statistics
import pandas as pd
from textblob import TextBlob
import tweepy

config = configparser.RawConfigParser()
config.read("config.ini")

API_KEY = config["twitter"]["API_KEY"]
API_KEY_SECRET = config["twitter"]["API_KEY_SECRET"]
BEARER_TOKEN = config["twitter"]["BEARER_TOKEN"]
ACCESS_TOKEN = config["twitter"]["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = config["twitter"]["ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
API = tweepy.API(auth)


def get_tweets(cashtag: str) -> list:
    """get tweets since yesterday using the specified hashtag"""

    yesterday = pd.to_datetime("now") - pd.Timedelta(days=1)
    yesterday = yesterday.strftime("%Y-%m-%d")
    tweets = tweepy.Cursor(API.search_tweets, q=f"(${cashtag}) since:{str(yesterday)}", count=100, tweet_mode="extended").items(500)
    
    data = []
    for tweet in tweets:
        tweet = tweet.full_text
        tweet = re.sub(r"http\S+", "", tweet)
        tweet = re.sub(r"\#\S+", "", tweet)
        tweet = re.sub(r"\$\S+", "", tweet)
        tweet = re.sub(r"\@\S+", "", tweet)
        tweet = re.sub(r"RT \S+", "", tweet)
        tweet = tweet.strip()
        # TODO: clean tweets better
        data.append(tweet)

    return data


def get_sentiment(tweets: list) -> float:
    """get average sentiment for a given set of tweets"""

    sentiments = []
    for tweet in tweets:
        sentiments.append(TextBlob(tweet).polarity)

    return statistics.mean(sentiments)
    

if __name__ == "__main__":
    print(f"AAPL: {get_sentiment(get_tweets('AAPL'))}")
    print(f"GOOGL: {get_sentiment(get_tweets('GOOGL'))}")
    print(f"TSLA: {get_sentiment(get_tweets('TSLA'))}")