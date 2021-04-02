"""Main module

Need to use pip install APScheduler

-*- coding: utf-8 -*-

Copyright (c) 2021 Brian Lecarpentier
All Rights Reserved
Released under the MIT license
"""

from data_handler.data_handler import *
from apscheduler.schedulers.background import BackgroundScheduler
from utils.config.parser import *
import time


def main():
    """ main method """
    influx = DataHandler()

    scheduler = BackgroundScheduler()
    job = scheduler.add_job(influx.send_data_with_pika, "interval", args=[Interval.cpu.name],
                            seconds=get_data_config(Interval.cpu.name))
    job2 = scheduler.add_job(influx.send_data_with_pika, "interval", args=[Interval.memory.name],
                             seconds=get_data_config(Interval.memory.name))
    job3 = scheduler.add_job(influx.send_data_with_pika, "interval", args=[Interval.disk.name],
                             seconds=get_data_config(Interval.disk.name))
    job4 = scheduler.add_job(influx.send_data_with_pika, "interval", args=[Interval.network.name],
                             seconds=get_data_config(Interval.network.name))
    job5 = scheduler.add_job(influx.send_data_with_pika, "interval", args=[Interval.sensor.name],
                             seconds=get_data_config(Interval.sensor.name))
    scheduler.print_jobs()
    scheduler.start()
    try:
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == "__main__":
    main()
