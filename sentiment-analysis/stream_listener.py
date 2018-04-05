import json
import tweepy


class SatStreamListener(tweepy.StreamListener):
    def __init__(self,
                 api=None,
                 logger=None,
                 mq_channel=None):

        super().__init__(api)
        self.logger = logger
        self.mq_channel = mq_channel

    def on_status(self, status):
        self.logger.debug('status %d' % status.text)

    def on_data(self, data):
        tweet_json = json.loads(data, encoding='utf-8')
        if 'id' and 'text' and 'created_at' in tweet_json:
            tweet = {
                'id': tweet_json['id'],
                'text': tweet_json['text'],
                'created_at':tweet_json['created_at']
            }
            tweet_json = json.dumps(tweet, indent=4)
            self.mq_channel.basic_publish(exchange='', routing_key='tweets', body=tweet_json)

    def on_error(self, status_code):
        self.logger.error('stream error: %d' % status_code)