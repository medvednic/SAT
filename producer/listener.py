import tweepy
import json

from tweet import Tweet


class SatStreamListener(tweepy.StreamListener):
    def __init__(self, api=None, logger=None):
        super().__init__(api)
        self.logger = logger

    def on_status(self, status):
        self.logger.debug('status %d' % status.text)

    def on_data(self, data):
        tweet = Tweet(json.loads(data))
        msg = 'id: %s, created-at: %s, text: %s' % (tweet.id, tweet.created_at, tweet.text)
        self.logger.debug(msg)

    def on_error(self, status_code):
        self.logger.error('stream error: %d' % status_code)