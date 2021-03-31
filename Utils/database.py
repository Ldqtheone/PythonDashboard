"""Database module

Copyright (c) 2021 Brian Lecarpentier
All Rights Reserved
Released under the MIT license

"""

from Utils.Config.parser import *
from datetime import datetime

from influxdb_client import InfluxDBClient, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


class Database:
    """Database class"""

    def __init__(self):
        self.token = get_token()
        self.org = get_org()
        self.bucket = get_bucket()
        self.client = InfluxDBClient(url=get_url(), token=self.token)

    def write_query(self, data):
        """
        Write query and insert data to Database
        :param data: all hardware datas for current agent
        """
        write_api = self.client.write_api(write_options=SYNCHRONOUS)

        write_api.write(self.bucket, self.org, data)

    def execute_query(self, query):
        """
        Querying Database to get hardware info per agent
        :param query: query
        :return: all datas
        """

        # renvoyer un tableau de dictionnaire plutot
        result = self.client.query_api().query(org=self.org, query=query)
        results = []
        for table in result:
            for record in table.records:
                results.append((record.get_value(), record.get_field()))

        return results

    def insert_query(self, agent):
        """
        Insert data to influxDb depending on agent
        :param agent: current agent
        :type agent: str
        """
        query = f'from(bucket: "hardware")\
            |> range(start: -1h)\
            |> filter(fn: (r) => r._measurement == "hardware_info")\
            |> filter(fn: (r) => r.agent_number == "{agent}")'
        return self.execute_query(query)

    def get_cpu_query(self, agent, category):
        """
        Get data from influxDb depending on category search and agent
        :param category: category of data (cpu, network, disk ...)
        :type category: str
        :param agent: current agent
        :type agent: str
        """

        query = f'from(bucket: "hardware")\
            |> range(start: -1h)\
            |> filter(fn: (r) => r._measurement == "hardware_info")\
            |> filter(fn: (r) => r.agent_number == "{agent}" )\
            |> filter(fn: (r) => r.category == "{category}" )'
        return self.execute_query(query)


