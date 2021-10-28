from requests.structures import CaseInsensitiveDict
from helper.logger import Logger
import json
import requests

logger = Logger('Kourage')


def send_webhook(webhook, embed, resp=None):
    """
    This module sends webhook to the specified discord URL
    :param: webhook = Webhook address, embed = embed
    :rtype: None
    """
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    data = json.dumps({
        'embed': embed
    })

    try:
        resp = requests.post(webhook, headers=headers, data=data)
        resp.raise_for_status()
    except requests.exceptions.MissingSchema:
        logger.error("\nSomething went wrong while setting up the webhook. Reason - bad webhook structure")
    except requests.exceptions.HTTPError:
        logger.error("\nSomething went wrong while setting up the webhook. Reason - bad internet connection")
    finally:
        logger.warning("\nWebhook sent successfully, code {}.".format(resp.status_code))
        if resp.status_code == 204:
            logger.warning("Webhook sent successfully to " + webhook)
