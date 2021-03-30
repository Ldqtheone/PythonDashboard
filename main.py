"""Main module

Copyright (c) 2021 Brian Lecarpentier
All Rights Reserved
Released under the MIT license

"""

from influxdb_client import Point

import Utils.database as db
import Utils.data_temp as data


def main():
    """ main method """

    utils = data.UtilsClass()
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
    main()
