import logging

import tweepy
from daemonize import Daemonize

from mq_connector import mq_chanel_connect
from stream_listener import SatStreamListener
from util import read_json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
fh = logging.FileHandler("sat-producer.log", "w")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]


def twitter_api_init(credentials):
    auth = tweepy.OAuthHandler(credentials['consumer-key']['key'],
                               credentials['consumer-key']['secret'])

    auth.set_access_token(credentials['access-token']['token'],
                          credentials['access-token']['secret'])

    return tweepy.API(auth)


def main():
    logging.info('Session start')
    credentials = read_json('tweeter-api-credentials.json')
    keywords = read_json('person-config.json')

    twitter_api = twitter_api_init(credentials)
    mq_channel = mq_chanel_connect('localhost', 'tweets')

    stream_listener = SatStreamListener(logger=logger, mq_channel=mq_channel)

    tweet_stream = tweepy.Stream(auth=twitter_api.auth, listener=stream_listener)

    tweet_stream.filter(track=keywords['keywords'], languages=['en'], async=False)


pid_file = '/tmp/kyc-producer.pid'
daemon = Daemonize(app="kyc-producer", pid=pid_file, action=main(), keep_fds=keep_fds)
daemon.start()
