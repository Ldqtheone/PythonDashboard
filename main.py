"""Main module

Copyright (c) 2021 Brian Lecarpentier
All Rights Reserved
Released under the MIT license

"""

from Utils.utils_data import *

from Utils.database import *

from Utils.Config.parser import *


def main():
    """ main method """
    utils = UtilsClass()
    database = Database()

    agent_data = utils.get_current_data()
    point = {}
    agent_id = get_identifier()

    for key, value in agent_data.items():
        point[key] = value

    print(point)

    data_to_send = [
        {
            "measurement": "hardware_info",
            "tags": {"agent_number": f"{agent_id}"},
            "fields": point
        }]

    database.write_query(data_to_send)

    print(database.execute_query(agent_id))


if __name__ == '__main__':
    main()
