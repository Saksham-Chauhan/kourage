import os
import praw


class RedditConfig:
    def __init__(self):
        self.client_id = os.environ.get('REDDIT_CLIENT_ID')
        self.client_secret = os.environ.get('REDDIT_CLIENT_SECRET')
        self.user_agent = 'python'

    def initialize(self):
        if self.client_id or self.client_secret is None:
            return False
        else:
            reddit = praw.Reddit(client_id=self.client_id,
                                 client_secret=self.client_secret,
                                 user_agent=self.user_agent)
            return reddit
