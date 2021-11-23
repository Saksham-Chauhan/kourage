import os

from process.tickets.ticket import *
from helper.webhook import send_webhook

webhook_url = os.environ.get('TICKET_URL_WEBHOOK')


def ticket_status():
    send_webhook(webhook_url, prepare_embed_message(get_open_issues()))
    send_webhook(webhook_url, prepare_embed_message(get_resolved_issues()))



