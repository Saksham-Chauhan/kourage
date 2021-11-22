from process.subreddit.subreddit import fetch_meme_url
from helper.webhook import send_webhook
import os


def reddit_tech_meme():
    webhook_url = os.environ.get('TECH_MEME_WEBHOOK_URL')
    send_webhook(webhook_url, fetch_meme_url())