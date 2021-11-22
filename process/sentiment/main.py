from nltk.sentiment import SentimentIntensityAnalyzer
from helper.logger import Logger
from helper.plotter import plot_sentiment_graph
from helper.webhook import send_webhook
from process.sentiment.embeds import get_sentiment_graph_embed
from dotenv import load_dotenv, find_dotenv
import pandas as pd
import datetime
import os
import re

logger = Logger()


def create_date_time_object():
    return lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f').strftime('%m-%d-%Y')


def remove_urls():
    return lambda x: re.sub(r'^http\S+', '', x)


def remove_punctuations():
    return lambda x: re.sub(r'[^\w\s]', '', x)


def remove_stopwords():
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    return lambda x: ' '.join(word.lower() for word in x.split() if word not in stop_words)


def remove_extras():
    return lambda x: None if x == '' else x


def get_polarity_score(sentiment):
    return lambda x: sentiment.polarity_scores(x)


def get_analysis():
    return lambda x: 'neutral' if x == 0 else ('positive' if x > 0 else 'negative')


async def read_messages(bot, file_name="sentiment_data.csv"):
    load_dotenv(find_dotenv())
    channels = os.environ.get('SENTIMENT_CHANNELS')
    print(channels)
    data = pd.DataFrame(columns=['content', 'time', 'author'])
    for channel in channels:
        channel = bot.get_channel(channel)
        async for msg in channel.history(limit=1000):  # set high limit
            msg_date = msg.created_at.strftime('%Y-%m-%d')
            today = datetime.date.today().strftime('%Y-%m-%d')
            if msg_date == today:
                data = data.append({'content': msg.content, 'time': msg.created_at, 'author': msg.author.name},
                                   ignore_index=True)
            else:
                break

        data.to_csv(file_name, index=False)
    await sentiment_analysis()

    sentiment_embed = get_sentiment_graph_embed()
    webhook_url = os.environ.get("SENTIMENT_WEBHOOK_URL")
    send_webhook(webhook_url, sentiment_embed)


async def sentiment_analysis():
    data = pd.read_csv("sentiment_data.csv")
    data.dropna(inplace=True)
    data.time = data.time.apply(create_date_time_object())
    data_url = data.content.apply(remove_urls())  # Remove URL
    data_url_rp = data_url.apply(remove_punctuations())  # Remove punctuations
    data_url_rp_sw = data_url_rp.apply(remove_stopwords())  # Removing stopwords
    data_url_rp_sw_re = data_url_rp_sw.apply(remove_extras())  # Removing extras
    data.loc[:, "content"] = data_url_rp_sw_re
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)
    sentiment = SentimentIntensityAnalyzer()
    sentiment_score = data.content.apply(get_polarity_score(sentiment))
    score = pd.DataFrame(list(sentiment_score))
    analysis = get_analysis()

    await plot_sentiment_graph(data, score, analysis)


async def daily_sentiment_job(bot):
    await read_messages(bot)
