import pika
import tweepy
from pymongo import MongoClient


""" 
This module has functions which connect to different services (DB, TwitterAPI and RabbitMQ),
each function returns instance of a specific connection.
"""


def get_mq_channel(host, queue_name):
    broker_connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, connection_attempts=15,
                                                                          retry_delay=10))
    channel = broker_connection.channel()
    channel.queue_declare(queue=queue_name)
    return channel


def get_db_collection(host, port, db_name, collection):
    mongo_client = MongoClient(host=host, port=port)
    db = mongo_client[db_name]
    return db[collection]


def get_twitter_api(credentials):
    auth = tweepy.OAuthHandler(credentials['consumer-key']['key'],
                               credentials['consumer-key']['secret'])

    auth.set_access_token(credentials['access-token']['token'],
                          credentials['access-token']['secret'])

    return tweepy.API(auth)
