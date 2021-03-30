"""Database module

Copyright (c) 2021 Brian Lecarpentier
All Rights Reserved
Released under the MIT license

"""

import yaml
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "4DszHczuRA9-bcnynoj2ifv9sXE7rJaIXNnUcHIL2eTSeoFhsK1O7UWivZL1nZXNj47ECdYy7dkdgNh024g8Lw=="
org = "brian.lecarpentier@edu.itescia.fr"
bucket = "hardware"
client = InfluxDBClient(url="https://eu-central-1-1.aws.cloud2.influxdata.com", token=token)

# with open(r'E:\data\config.yaml') as file:
#     # The FullLoader parameter handles the conversion from YAML
#     # scalar values to Python the dictionary format
#     config_list = yaml.load(file, Loader=yaml.FullLoader)
#     # You can generate a Token from the "Tokens Tab" in the UI


def write_query():
    """ Write a query """
    write_api = client.write_api(write_options=SYNCHRONOUS)

    data = Point("hardware_info").tag("agent_number", "1").field("temperature", 41.2)
    write_api.write(bucket, org, data)


def execute_query():
    """ Execute a query """
    query = 'from(bucket: "hardware")\
    |> range(start: -1h)\
    |> filter(fn: (r) => r._measurement == "hardware_info")\
    |> filter(fn: (r) => r._field == "temperature")\
    |> filter(fn: (r) => r.agent_number == "1")'

    result = client.query_api().query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_value(), record.get_field()))

    return results
