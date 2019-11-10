# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
from statistics import mean
import time
import tweepy
import numpy as np

# Import API key
# import sys
# sys.path.append('..\..\..\config_files')

from config import (consumer_key,
                    consumer_secret,
                    access_token,
                    access_token_secret)

# Import Sentiment Analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

# Twitter authorization
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# Get last id analyzed in mentions
last_tweet_id = api.user_timeline()[0]['id']

# list of accounts already analyzed
accounts_analyzed = []


# returns all mentions not already seen
def get_mentions(latest):
    ment = api.mentions_timeline(since_id=latest)
    l = []
    for m in ment:
        l.append(m)
    return (l)


# gets compound sentiments for last 500 tweets for a user
def get_sentiments(source):
    sentiments = []

    for p in range(1, 26):
        public_tweets = api.user_timeline(source, page=p)
        for tweet in public_tweets:
            sentiment_scores = analyzer.polarity_scores(tweet["text"])
            sentiments.append(sentiment_scores['compound'])

    return (sentiments)


# creates a plot and tweet it
def create_plot(data, source):
    plt.figure(figsize=(12, 7))
    plt.plot(data, marker='o', ms=5)
    plt.title(f'Sentiment Analysis of Tweets for User @{source}')
    plt.ylim(-1, 1)
    plt.xlabel('Tweets Ago')
    plt.ylabel('Tweet Polarity')
    plt.savefig('Output.png')
    api.update_with_media('Output.png', f'Sentiment Analysis for User @{source}')
    plt.show()

    # infinite loop to get all mentions, analyze them, and then plot them every 5 min


while (True):
    mentions = get_mentions(last_tweet_id)
    for m in mentions:
        m_name = m['user']['screen_name']
        if m_name not in accounts_analyzed:
            sentiments = get_sentiments(m_name)
            create_plot(sentiments, m_name)
            accounts_analyzed.append(m_name)

    if len(mentions) != 0:
        last_tweet_id = mentions[0]['id']

    time.sleep(300)