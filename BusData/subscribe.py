"""Subscribe module

Copyright (c) 2021 Brian Lecarpentier
All Rights Reserved
Released under the MIT license

"""

import pika
import json
import Utils.database as db

database = db.Database()

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

    message = (json.loads(body))
    database.write_query(message)

    channel.start_consuming()
