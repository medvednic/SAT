import logging

import pika
import tweepy
from daemonize import Daemonize

import file_reader
from listener import SatStreamListener

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
fh = logging.FileHandler("sat-producer.log", "w")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]


def mq_chanel_connect(host, queue_name):
    broker_connection = pika.BlockingConnection(pika.ConnectionParameters(host))
    channel = broker_connection.channel()
    channel.queue_declare(queue=queue_name)
    return channel


def twitter_api_init(credentials):
    auth = tweepy.OAuthHandler(credentials['consumer-key']['key'],
                               credentials['consumer-key']['secret'])

    auth.set_access_token(credentials['access-token']['token'],
                          credentials['access-token']['secret'])

    return tweepy.API(auth)


def main():
    logging.info('Session start')
    credentials = file_reader.read_json('tweeter-api-credentials.json')
    keywords = file_reader.read_json('person-config.json')

    twitter_api = twitter_api_init(credentials)
    mq_channel = mq_chanel_connect('localhost', 'tweets')

    stream_listener = SatStreamListener(logger=logger,
                                        mq_channel=mq_channel)

    tweet_stream = tweepy.Stream(auth=twitter_api.auth,
                                 listener=stream_listener)

    tweet_stream.filter(track=keywords['keywords'],
                        async=False)


pid_file = '/tmp/kyc-producer.pid'
daemon = Daemonize(app="kyc-producer",
                   pid=pid_file, action=main(),
                   keep_fds=keep_fds)
daemon.start()
