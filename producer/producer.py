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


def main():
    logging.info('Session start')
    with open('tweeter-api-credentials.json', encoding="utf-8") as f:
        credz = json.load(f)

    auth = tweepy.OAuthHandler(credz['consumer-key']['key'], credz['consumer-key']['secret'])
    auth.set_access_token(credz['access-token']['token'], credz['access-token']['secret'])
    api = tweepy.API(auth)

    tweet_stream = tweepy.Stream(auth=api.auth, listener=SatStreamListener(logger=logger))
    tweet_stream.filter(track=['Trump'], async=False)


pid_file = '/tmp/kyc-producer.pid'
daemon = Daemonize(app="kyc-producer", pid=pid_file, action=main(), keep_fds=keep_fds)
daemon.start()
