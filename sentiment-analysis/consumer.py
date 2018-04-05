import json
import pika

from daemonize import Daemonize
from textblob import TextBlob

from tweet import Tweet
from util import clean_tweet


def determine_sentiment(text):
    analysis = TextBlob(clean_tweet(text))
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


def callback(ch, method, props, body):
    # print('message %r' % body.decode())
    tweet_json = json.loads(body, encoding='utf-8')
    sentiment = determine_sentiment(tweet_json['text'])
    tweet = Tweet(tweet_json['id'], tweet_json['text'], tweet_json['created_at'], sentiment)
    print(tweet.text)
    print(tweet.sentiment)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='tweets')

    channel.basic_consume(callback, queue='tweets', no_ack=True)
    channel.start_consuming()


pid_file = '/tmp/kyc-consumer.pid'
daemon = Daemonize(app="kyc-consumer", pid=pid_file, action=main())
daemon.start()
