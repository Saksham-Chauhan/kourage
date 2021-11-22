import os
from helper.reddit import RedditConfig
import random


def fetch_meme_url():
    reddit = RedditConfig().initialize()
    print(reddit)
    print(os.environ.get('REDDIT_CLIENT_ID'))
    print(os.environ.get('REDDIT_CLIENT_SECRET'))
    memes_submissions = reddit.subreddit('ProgrammerHumor').hot()
    post_to_pick = random.randint(1, 10)
    submission = None
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)

    return submission.url