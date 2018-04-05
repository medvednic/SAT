import tweepy
import logging
import json

from listener import SatStreamListener
from daemonize import Daemonize

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
fh = logging.FileHandler("sat-producer.log", "w")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]


def read_file(file_name):
    with open('config/' + file_name, encoding="utf-8") as f:
        return json.load(f)


def main():
    logging.info('Session start')
    credentials = read_file('tweeter-api-credentials.json')
    keywords = read_file('person-config.json')

    auth = tweepy.OAuthHandler(credentials['consumer-key']['key'],
                               credentials['consumer-key']['secret'])

    auth.set_access_token(credentials['access-token']['token'],
                          credentials['access-token']['secret'])

    api = tweepy.API(auth)
    tweet_stream = tweepy.Stream(auth=api.auth, listener=SatStreamListener(logger=logger))
    tweet_stream.filter(track=keywords['keywords'], async=False)


pid_file = '/tmp/kyc-producer.pid'
daemon = Daemonize(app="kyc-producer", pid=pid_file, action=main(), keep_fds=keep_fds)
daemon.start()
