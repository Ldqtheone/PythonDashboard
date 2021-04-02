"""database module

Need to use pip install influxdb-client

-*- coding: utf-8 -*-

Copyright (c) 2021 Brian Lecarpentier
All Rights Reserved
Released under the MIT license
"""

from utils.config.parser import *
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS


class Database:
    """Database class"""

    def __init__(self):
        self.token = get_data_config("token")
        self.org = get_data_config("org")
        self.bucket = get_data_config("bucket")
        self.client = InfluxDBClient(url=get_data_config("url"), token=self.token)

    def write_query(self, data):
        """
        Write query used to insert data into Database
        :param data: all hardware data for current agent
        :type data: list
        """
        write_api = self.client.write_api(write_options=SYNCHRONOUS)
        write_api.write(self.bucket, self.org, data)

    def execute_query(self, query):
        """
        Querying Database to get data.
        Create an array of dict containing a key corresponding to psUtils data.
        Each key is associated to another dict with a key as record time and value as the value get.
        :param query: query
        :type query: str
        :return: all data as an array of dict
        """

        result = self.client.query_api().query(org=self.org, query=query)
        print(result)
        results = []

        for table in result:
            for record in table.records:
                results.append({record.get_field(): {f"{record.get_time()}": record.get_value()}})

        return results

    def get_all_by_agent(self, agent, start_time=7, start_unit="d"):
        """
        Get all data in influxDb depending on agent
        :param agent: current agent
        :type agent: str
        :param start_time: used to get data in a range from this time to now
        :type start_time: int
        :param start_unit: a time unit
        :type start_unit: str
        :return: data from DB as an array of dict
        """
        query = f'from(bucket: "{self.bucket}")\
            |> range(start: -{start_time}{start_unit})\
            |> filter(fn: (r) => r._measurement == "hardware_info")\
            |> filter(fn: (r) => r.agent_number == "{agent}")'
        return self.execute_query(query)

    def get_data_by_category_query(self, agent, category, start_time=2, start_unit="d"):
        """
        Get data from influxDb depending on category search and agent
        :param agent: current agent
        :type agent: str
        :param category: category of data (cpu, network, disk ...)
        :type category: str
        :param start_time: used to get data in a range from this time to now
        :type start_time: int
        :param start_unit: a time unit
        :type start_unit: str
        :return: data from DB as an array of dict
        """
        query = f'from(bucket: "{self.bucket}")\
            |> range(start: -{start_time}{start_unit})\
            |> filter(fn: (r) => r._measurement == "hardware_info")\
            |> filter(fn: (r) => r.agent_number == "{agent}" )\
            |> filter(fn: (r) => r.category == "{category}" )'
        return self.execute_query(query)

    def get_agent_query(self):
        """
        Get all agent from influxDb
        :return: an array of string containing all agents name
        """

        query = f"""
        import \"influxdata/influxdb/schema\"

        schema.tagValues(bucket: \"{self.bucket}\",  tag: "agent_number")
        """

        query_api = self.client.query_api()
        tables = query_api.query(query=query, org=self.org)

        # transform data into an array
        agents = [row.values["_value"] for table in tables for row in table]
        return agents
