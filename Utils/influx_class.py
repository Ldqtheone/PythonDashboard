"""Module 

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

from Utils.utils_data import *
from Utils.Config.parser import *
import Utils.database as db
import publish as publisher


class DataStorageClass:
    """A class to send data to influx db"""
    utils = UtilsClass()
    database = db.Database()

    def __init__(self):
            pass

    def send_data_to_influx_db(self, mode,  check_data_type=False):
        """
        Send data to influxDB on cloud
        :param mode: name of the data to get
        :type mode: str
        :param check_data_type: if True, filter none numeric value from agent data
        :type check_data_type: bool
        """

        if mode == Interval.cpu.name:
            agent_data = self.utils.get_cpu_data()
        elif mode == Interval.memory.name:
            agent_data = self.utils.get_memory_data()
        elif mode == Interval.disk.name:
            agent_data = self.utils.get_disk_data()
        elif mode == Interval.network.name:
            agent_data = self.utils.get_net_data()
        elif mode == Interval.sensor.name:
            agent_data = self.utils.get_sensor_data()
        else:
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

        publisher.publish_message(data_to_send)

        # self.database.write_query(data_to_send)
        print(self.database.execute_query(agent_id))

    def send_data_with_pika(self):
        """
        Send data with pika (dataBus)
        """
        pass

