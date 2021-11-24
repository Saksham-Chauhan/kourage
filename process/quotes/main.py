import os
from typing import Final

from helper.webhook import send_webhook
from process.quotes.embeds import *
from process.quotes.quotes import fetch_quote

# Webhook for general channel - env var - GENERAL_WEBHOOK
webhook: Final = os.environ.get('GENERAL_WEBHOOK')


def job_morning_quote():
    quote, author = fetch_quote()
    embed = morning_embed(quote, author)
    send_webhook(webhook, embed)


def job_evening_work_log():
    embed = evening_embed()
    send_webhook(webhook, embed)


def job_friday_meeting():
    embed = friday_embed()
    send_webhook(webhook, embed)
