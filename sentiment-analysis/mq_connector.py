import pika


def mq_chanel_connect(host, queue_name):
    broker_connection = pika.BlockingConnection(pika.ConnectionParameters(host))
    channel = broker_connection.channel()
    channel.queue_declare(queue=queue_name)
    return channel
