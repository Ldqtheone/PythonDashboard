"""Publish module

Copyright (c) 2021 Brian Lecarpentier
All Rights Reserved
Released under the MIT license

"""

import pika


def publish_message(message):
    """
    RabbitMq publisher
    :param message:
    """
    # Create a new instance of the Connection object
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    # Create a new channel with the next available channel number or pass in a channel number to use
    channel = connection.channel()

    # Declare queue, create if needed. This method creates or checks a queue. When creating a new queue the client can
    # specify various properties that control the durability of the queue and its contents, and the level of sharing for
    # the queue.
    channel.queue_declare(queue='InfosLog', durable=True)

    channel.basic_publish(exchange='InfosLog', routing_key='', body=message)

    print(f"[x] Sent '{message}'")

    connection.close()
