import datetime
import json

from daemonize import Daemonize
from pymongo import MongoClient
from textblob import TextBlob

from mq_connector import mq_chanel_connect
from util import clean_tweet, twitter_time_to_epoch

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
    # print('message %r' % body.decode())
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
        print(collection.insert_one(tweet).inserted_id)


def db_connect():
    global collection
    mongo_client = MongoClient('localhost', 27017)
    db = mongo_client.sat_db
    collection = db.tweet_collection


def main():
    db_connect()
    mq_channel = mq_chanel_connect('localhost', 'tweets')

    mq_channel.basic_consume(mq_consume_callback, queue='tweets', no_ack=True)
    mq_channel.start_consuming()


pid_file = '/tmp/kyc-consumer.pid'
daemon = Daemonize(app="kyc-consumer", pid=pid_file, action=main())
daemon.start()
