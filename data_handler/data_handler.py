"""data_handler module

-*- coding: utf-8 -*-

Copyright (c) 2021 Gwenael Marchetti--Waternaux
All Rights Reserved
Released under the MIT license
"""

from utils.utils_data import *
from utils.config.parser import *
import utils.database as db
from data_bus import publish as publisher


class DataHandler:
    """
    A class to send data to influx db.
    Use UtilsClass to get psUtils data from an agent.
    Use Database class to send a writing request to influxDB.
    """

    def __init__(self):
        self.utils = UtilsData()
        self.database = db.Database()

    def get_agent_data_by_category(self, category):
        """
        Return agent data corresponding to the given category,
        or all if any match
        :param category: data category to return
        :type category: str
        :return: a dict containing appropriate data
        """
        if category == Interval.cpu.name:
            return self.utils.get_cpu_data()
        elif category == Interval.memory.name:
            return self.utils.get_memory_data()
        elif category == Interval.disk.name:
            return self.utils.get_disk_data()
        elif category == Interval.network.name:
            return self.utils.get_net_data()
        elif category == Interval.sensor.name:
            return self.utils.get_sensor_data()
        else:
            # return all the data from psUtils
            return self.utils.get_current_data()

    def prepare_data_to_send(self, category, agent_id, check_data_type=True):
        """
        Prepare data to send in influxDB (cloud)
        :param category: name of the data to get, used as tag in influxDB
        :type category: str
        :param agent_id: agent's id , used as tag in influxDB
        :type agent_id: str
        :param check_data_type: if True, filter none numeric value from agent data
        :type check_data_type: bool
        :return: a dict with all prepared data to push into DB
        """

        agent_data = self.get_agent_data_by_category(category)
        point = {}

        if check_data_type:
            for key, value in agent_data.items():
                try:
                    val = (int(value))
                    point[key] = value
                except:
                    pass


        else:
            point = agent_data

        return [
            {
                "measurement": "hardware_info",
                "tags": {"agent_number": f"{agent_id}", "category": category},
                "fields": point
            }
        ]

    def send_data_with_pika(self, category, check_data_type=False):
        """
        Send data to influxDB with pika (dataBus)
        """
        data_to_send = self.prepare_data_to_send(category,  get_data_config("identifier"), check_data_type)
        publisher.publish_message(data_to_send)
        print(data_to_send)

    def send_data_to_influx_db(self, category, check_data_type=False):
        """
        Send data directly to influxDB (without DataBus)
        """
        data_to_send = self.prepare_data_to_send(category,  get_data_config("identifier"), check_data_type)
        self.database.write_query(data_to_send)
        print(data_to_send)
