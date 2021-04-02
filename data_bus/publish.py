"""publish module

Need to use pip install pika.
Also need to launch rabbitMQ.

-*- coding: utf-8 -*-

Copyright (c) 2021 Brian Lecarpentier
All Rights Reserved
Released under the MIT license
"""

import pika
import json


def publish_message(data):
    """
    RabbitMq publisher.
    Used to send data into the DataBus.

    Example:
        data =
            [
                {
                    "measurement": "hardware_info",
                    "tags": {"agent_number": f"PC1", "category": cpu},
                    "fields": {cpu_times_percent: 5.4, user:623402}
                }
            ]
    :param data: hardware data to send in DB thanks to our DataBus
    :type data: list
    """
    # Create a new instance of the Connection object
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    # Create a new channel with the next available channel number or pass in a channel number to use
    channel = connection.channel()

    # Declare queue, create if needed. This method creates or checks a queue. When creating a new queue the client can
    # specify various properties that control the durability of the queue and its contents, and the level of sharing for
    # the queue.
    channel.queue_declare(queue='InfosLog', durable=True)

    print(data)

    channel.basic_publish(exchange='', routing_key='InfosLog', body=json.dumps(data))

    print(f"[x] Sent '{data}'")

    connection.close()
