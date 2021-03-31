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

    def execute_query(self, agent):
        """
        Querying Database to get hardware info per agent
        :param agent: current user agent
        :return: all datas
        """
        query = f'from(bucket: "hardware")\
            |> range(start: -1h)\
            |> filter(fn: (r) => r._measurement == "hardware_info")\
            |> filter(fn: (r) => r.agent_number == "{agent}")'

        result = self.client.query_api().query(org=self.org, query=query)
        results = []
        for table in result:
            for record in table.records:
                results.append((record.get_value(), record.get_field()))

        return results
