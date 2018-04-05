import json
import tweepy

from tweet import Tweet


class SatStreamListener(tweepy.StreamListener):
    def __init__(self, api=None, logger=None, mq_channel=None):
        super().__init__(api)
        self.logger = logger
        self.mq_channel = mq_channel

    def on_status(self, status):
        self.logger.debug('status %d' % status.text)

    def on_data(self, data):
        tweet = Tweet(json.loads(data, encoding='utf-8'))
        msg = 'id: %s, created-at: %s, text: %s' % (tweet.id, tweet.created_at, tweet.text)
        self.logger.debug(msg)
        tweet_json = json.dumps(tweet.__dict__, indent=4)
        self.mq_channel.basic_publish(exchange='', routing_key='tweets', body=tweet_json)

    def on_error(self, status_code):
        self.logger.error('stream error: %d' % status_code)