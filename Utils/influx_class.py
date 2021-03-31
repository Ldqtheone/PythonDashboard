"""Module 

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

from Utils.utils_data import *
from Utils.Config.parser import *
import Utils.database as db
import pika


class DataStorageClass:
    """A class to send data to influx db"""
    utils = UtilsClass()

    def __init__(self):
            pass

    def producer(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        ##loop here
        channel.queue_declare(queue='hello')
        channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
        print(" [x] Sent 'Hello World!'")

        connection.close()

    def consumer(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='hello')

        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)

        channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    def send_data_to_influx_db(self, check_data_type=False):
        """
        Send data to influxDB on cloud
        :param check_data_type: if True, filter none numeric value from agent data
        :type check_data_type: bool
        """
        agent_data = self.utils.get_current_data()
        agent_id = get_identifier()
        point = {}

        if check_data_type:
            # need to be completed
            for key, value in agent_data.items():
                point[key] = value

        else:
            point = agent_data

        print(point)
        data_to_send = [
            {
                "measurement": "hardware_info",
                "tags": {"agent_number": f"{agent_id}"},
                "fields": point
            }]

        db.write_query(data_to_send)
        print(db.execute_query(agent_id))

    def send_data_with_pika(self):
        """
        Send data with pika (dataBus)
        """
        pass

