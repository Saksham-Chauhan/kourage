import os
from helper.reddit import RedditConfig
import random
import json


def fetch_meme_url():
    reddit = RedditConfig().initialize()

    meme_channels = json.loads(os.environ.get('MEME_CHANNELS'))
    meme_channel = random.choice(meme_channels)

    memes_submissions = reddit.subreddit(meme_channel).hot()
    post_to_pick = random.randint(1, 10)
    submission = None
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)

    return submission.title, submission.url
