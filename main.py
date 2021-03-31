"""Main module

Copyright (c) 2021 Brian Lecarpentier
All Rights Reserved
Released under the MIT license

"""

from Utils.utils_data import *
from influxdb_client import Point

import Utils.database as db
import time

from Utils.Config.parser import *

from apscheduler.schedulers.background import BackgroundScheduler


def send_data():

    utils = UtilsClass()
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

    db.write_query(data_to_send)
    print(db.execute_query(agent_id))


def main():
    """ main method """

    scheduler = BackgroundScheduler()
    job = scheduler.add_job(send_data, 'interval', seconds=get_interval(Interval.disk.name))
    scheduler.print_jobs()
    scheduler.start()

    try:
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == '__main__':
    main()
