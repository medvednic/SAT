import datetime
import json
import logging

import sys

import os
from textblob import TextBlob

from services import clean_tweet, twitter_time_to_epoch, LogProvider, get_hosts_config
from services.connectors import *

"""
Consumer - receives tweets from message queue, determines their sentiment using TextBlob and stores the tweet in DB
"""

log_wrapper = LogProvider("sat-consumer.log", logging.ERROR)
logger = log_wrapper.get_logger()
mq_channel = None
collection = None


def determine_sentiment(text):
    analysis = TextBlob(clean_tweet(text))
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


def mq_consume_callback(ch, method, props, body):
    tweet_json = json.loads(body, encoding='utf-8')
    sentiment = determine_sentiment(tweet_json['text'])
    ts = twitter_time_to_epoch(tweet_json['created_at'])
    tweet = {
        'id': tweet_json['id'],
        'text': tweet_json['text'],
        'created_at': datetime.datetime.fromtimestamp(ts, None),
        'sentiment': sentiment
    }

    if None is not collection:
        collection.insert_one(tweet)
        logger.debug(tweet['id'])


def main():
    global collection, mq_channel
    logger.info('SAT Consumer started')
    print('SAT Consumer started')
    hosts_config = get_hosts_config()
    collection = get_db_collection(hosts_config['db']['host'], 27017, 'sat_db', 'tweet_collection')

    mq_channel = get_mq_channel(hosts_config['rabbitmq']['host'], 'tweets')
    mq_channel.basic_consume(mq_consume_callback, queue='tweets', no_ack=True)
    mq_channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        mq_channel.stop_consuming()
        mq_channel.connection.close()
        logger.info('SAT Consumer stopped')
        print('SAT Consumer stopped')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

