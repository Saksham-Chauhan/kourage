import os
from redminelib import Redmine
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class RedmineConfig:
    def __init__(self):
        self.url = 'https://kore.koders.in'
        self.key = os.environ.get('REDMINE_KEY')
        self.username = os.environ.get('REDMINE_USERNAME')
        self.password = os.environ.get('REDMINE_PASSWORD')

    def initialize(self):
        if self.username and self.password is not None:
            redmine = Redmine(self.url, username=self.username, password=self.password)
        elif self.key is not None:
            redmine = Redmine(self.url, key=self.key)
        else:
            return False
        return redmine
