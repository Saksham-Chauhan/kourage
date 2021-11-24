import os
import praw
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class RedditConfig:
    def __init__(self):
        self.client_id = os.environ.get('REDDIT_CLIENT_ID')
        self.client_secret = os.environ.get('REDDIT_CLIENT_SECRET')
        self.user_agent = 'pythonpraw'

    def initialize(self):
        if self.client_id and self.client_secret is not None:
            reddit = praw.Reddit(client_id=self.client_id,
                                 client_secret=self.client_secret,
                                 user_agent=self.user_agent)
            return reddit
        else:
            return False
