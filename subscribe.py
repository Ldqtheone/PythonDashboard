"""Subscribe module

Copyright (c) 2021 Brian Lecarpentier
All Rights Reserved
Released under the MIT license

"""

import pika
import json
from Utils.database import Database


def subscribe():
    """
    Subscribe
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='InfosLog', durable=True)

    channel.basic_consume("InfosLog", callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.start_consuming()


def callback(ch, method, properties, body):
    """
    Method callback
    :param ch:
    :param method:
    :param properties:
    :param body:
    """

    db = Database()

    message = (json.loads(body))
    db.write_query(message)


if __name__ == "__main__":
    subscribe()
