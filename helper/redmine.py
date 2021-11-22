import os
from redminelib import Redmine


class RedmineConfig:
    def __init__(self, url=None, key=None, username=None, password=None):
        self.url = url
        self.key = key
        self.username = username
        self.password = password

    def initialize(self):
        if self.username and self.password is not None:
            redmine = Redmine(self.url, username=self.username, password=self.password)
        elif self.key is not None:
            redmine = Redmine(self.url, key=self.key)
        else:
            return False
        return redmine


class RedmineConfigKey(RedmineConfig):
    def __init__(self):
        super().__init__()
        self.url = 'https://kore.koders.in'
        self.key = os.environ.get('REDMINE_KEY')


class RedmineConfigUsernamePassword(RedmineConfig):
    def __init__(self):
        super().__init__()
        self.url = 'https://kore.koders.in'
        self.username = os.environ.get('REDMINE_USERNAME')
        self.password = os.environ.get('REDMINE_PASSWORD')
        RedmineConfig(self.url, None, self.username, self.password).initialize()
