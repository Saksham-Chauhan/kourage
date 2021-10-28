import json
import random

import requests


def fetch_quote():
    url = 'https://type.fit/api/quotes'
    raw_response = requests.get(url)
    response = json.loads(raw_response.text)
    random_index = random.randint(0, len(response))
    return response[random_index]['text'], response[random_index]['author']