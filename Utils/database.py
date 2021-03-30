"""Database module

Copyright (c) 2021 Brian Lecarpentier
All Rights Reserved
Released under the MIT license

"""

import yaml
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

with open(r'E:\data\config.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    config_list = yaml.load(file, Loader=yaml.FullLoader)
    # You can generate a Token from the "Tokens Tab" in the UI
    token = "4DszHczuRA9-bcnynoj2ifv9sXE7rJaIXNnUcHIL2eTSeoFhsK1O7UWivZL1nZXNj47ECdYy7dkdgNh024g8Lw=="
    org = "brian.lecarpentier@edu.itescia.fr"
    bucket = "all_person"
    client = InfluxDBClient(url="https://eu-central-1-1.aws.cloud2.influxdata.com", token=token)


def write_query(data):
    """ Write a query """
    write_api = client.write_api(write_options=SYNCHRONOUS)

    data = "mem,host=host1 used_percent=23.43234543"
    write_api.write(bucket, org, data)


def execute_query(query):
    """ Execute a query """
    query = f'from(bucket: \\"{bucket}\\") |> range(start: -1h)'
    tables = client.query_api().query(query, org=org)
