"""Database module

Copyright (c) 2021 Brian Lecarpentier
All Rights Reserved
Released under the MIT license

"""

from Utils.Config.parser import *
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = get_token()
org = get_org()
bucket = get_bucket()
client = InfluxDBClient(url=get_url(), token=token)


def write_query(data):
    """ Write a query """
    write_api = client.write_api(write_options=SYNCHRONOUS)

    write_api.write(bucket, org, data)


def execute_query(agent):
    """ Execute a query """
    query = f'from(bucket: "hardware")\
        |> range(start: -1h)\
        |> filter(fn: (r) => r._measurement == "hardware_info")\
        |> filter(fn: (r) => r.agent_number == "{agent}")'

    result = client.query_api().query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_value(), record.get_field()))

    return results
