import logging

import sys

import os

from services import read_json, get_hosts_config, SatStreamListener, LogProvider
from services.connectors import *

"""
Producer - receives tweets according to a filter from Twitter streamAPI and sends them to a message queue
"""

log_wrapper = LogProvider("sat-producer.log", logging.ERROR)
logger = log_wrapper.get_logger()
tweet_stream = None


def main():
    global tweet_stream
    print('SAT Producer started')
    logger.info('SAT Producer started')
    hosts_config = get_hosts_config()
    mq_channel = get_mq_channel(hosts_config['rabbitmq']['host'], 'tweets')

    keywords = read_json('person-config.json')
    twitter_credentials = read_json('tweeter-api-credentials.json')
    twitter_api = get_twitter_api(twitter_credentials)

    stream_listener = SatStreamListener(logger=logger, mq_channel=mq_channel)
    tweet_stream = tweepy.Stream(auth=twitter_api.auth, listener=stream_listener)
    tweet_stream.filter(track=keywords['keywords'], languages=['en'], async=False)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        tweet_stream.disconnect()
        logger.info('SAT Producer stopped')
        print('SAT Producer stopped')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

