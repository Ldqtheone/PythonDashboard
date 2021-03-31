"""Name module

Copyright (c) 2021 Brian Lecarpentier
All Rights Reserved
Released under the MIT license

"""

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost:15672'))

channel = connection.channel()

channel.queue_declare(queue='InfosLog', durable=True)


def callback(ch, method, properties, body):
    """
    Method callback
    :param ch:
    :param method:
    :param properties:
    :param body:
    """
    print(" [x] Received %r" % body)

    channel.basic_consume("InfosLog", callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.start_consuming()
