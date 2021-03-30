"""Main module

Copyright (c) 2021 Brian Lecarpentier
All Rights Reserved
Released under the MIT license

"""

from Utils.utils_data import *
from influxdb_client import Point

import Utils.database as db


def main():
    """ main method """

    utils = UtilsClass()
    print(utils.get_current_data())
    print(utils.get_current_data()["load_avg"][0])
    partitions = utils.get_disk_partitions()
    print(partitions)
    print(utils.get_disk_usage(partitions[0].device))
    print(utils.get_disk_usages_list())

    agent_data = utils.get_current_data()
    point = {}

    for key, value in agent_data.items():
        point[key] = value

    print(point)

    data_to_send = [
        {
            "measurement": "hardware_info",
            "tags": {"agent_number": "Brian"},
            "fields": point
        }]

    db.write_query(data_to_send)

    print(db.execute_query("Brian"))


if __name__ == '__main__':
    utils = UtilsClass()
    print(utils.get_current_data())
    partitions = utils.get_disk_partitions()
    print(partitions)
    print(utils.get_disk_usage(partitions[0].device))
    print(utils.get_disk_usages_list())

    main()
