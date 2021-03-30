"""Module 

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

import psutil


class UtilsClass:
    """A class to have all data from psutils"""
    data = {}

    def __init__(self):
        pass

    # region CPU
    def get_user(self):
        """
        Get time spent by normal processes executing in user mode from psUtils
        :return: a float
        """
        return psutil.cpu_times().user

    def get_system(self):
        """
        Get time spent by processes executing in kernel mode from psUtils
        :return: a float
        """
        return psutil.cpu_times().system

    def get_idle(self):
        """
        Get time spent doing nothing from psUtils
        :return: a float
        """
        return psutil.cpu_times().idle

    def get_cpu_percent(self):
        """
        Get a float representing the current system-wide CPU utilization as a percentage from psUtils
        :return: a float
        """
        return psutil.cpu_percent()

    def get_cpu_times_percent(self):
        """
        Get the utilization percentages for each specific CPU time as is returned by
        psutil.cpu_times(percpu=True)
        :return: a tuple (user, nice, system, idle)
        """
        return psutil.cpu_times_percent()

    def get_ctx_switches(self):
        """
        Get number of context switches (voluntary + involuntary) since boot from psUtils
        :return: an int
        """
        return psutil.cpu_stats().ctx_switches

    def get_cpu_interrupts(self):
        """
        Get number of interrupts since boot from psUtils
        :return: an int
        """
        return psutil.cpu_stats().interrupts

    def get_load_avg(self):
        """
        Get the average system load over the last 1, 5 and 15 minutes as a tuple from psUtils
        :return: a list of int
        """
        return psutil.getloadavg()

    # endregion

    # region MEMORY

    # region virtual machine

    def get_vm_total(self):
        """
        Get total physical memory (exclusive swap) from psUtils
        :return: an int
        """
        return psutil.virtual_memory().total

    def get_vm_available(self):
        """
        Get the memory that can be given instantly to processes without the system going into swap from psUtils
        :return: an int
        """
        return psutil.virtual_memory().available

    # endregion

    # region swap machine

    def get_sm_total(self):
        """
        Get total swap memory in bytes from psUtils
        :return: an int
        """
        return psutil.swap_memory().total

    def get_sm_used(self):
        """
        Get used swap memory in bytes from psUtils
        :return: an int
        """
        return psutil.swap_memory().used

    def get_sm_free(self):
        """
        Get free swap memory in bytes from psUtils
        :return: an int
        """
        return psutil.swap_memory().free

    def get_sm_percent(self):
        """
        Get  the percentage usage calculated as (total - available) / total * 100 from psUtils
        :return: a float
        """
        return psutil.swap_memory().percent

    def get_sm_sin(self):
        """
        Get the number of bytes the system has swapped in from disk (cumulative) from psUtils
        :return: an int
        """
        return psutil.swap_memory().sin

    def get_sm_sout(self):
        """
        Get the number of bytes the system has swapped out from disk (cumulative) from psUtils
        :return: an int
        """
        return psutil.swap_memory().sout

    # endregion

    # endregion

    # region DISK

    # region disk partitions
    def get_disk_partitions(self):
        """
        Get all mounted disk partitions as a list of named tuples including device,
        mount point and filesystem type from psUtils
        :return: a list of partitions tuple
        """
        return psutil.disk_partitions()

    def get_disk_usages_list(self):
        """
        Get all disk usage statistics about the disk partition thanks to its mount point.
        :param path: path to device
        :type path: str
        :return: a list of disk usage tuple (total, used, free, percent)
        """
        usage_list = []
        for part in self.get_disk_partitions():
            usage_list.append(self.get_disk_usage(part.mountpoint))
        return usage_list

    def get_disk_usage(self, path):
        """
        Get disk usage statistics about the partition which contains the given path as
        a named tuple including total, used and free space expressed in bytes,
        plus the percentage usage from psUtils
        :param path: path to device
        :type path: str
        :return: a disk usage tuple (total, used, free, percent)
        """
        return psutil.disk_usage(path)

    # endregion

    def get_disk_io_read_count(self):
        """
        Get number of reads from psUtils
        :return: an int
        """
        return psutil.disk_io_counters().read_count

    def get_disk_io_write_count(self):
        """
        Get number of writes from psUtils
        :return: an int
        """
        return psutil.disk_io_counters().write_count

    def get_disk_io_read_bytes(self):
        """
        Get number of bytes read from psUtils
        :return: an int
        """
        return psutil.disk_io_counters().read_bytes

    def get_disk_io_write_bytes(self):
        """
        Get number of bytes written from psUtils
        :return: an int
        """
        return psutil.disk_io_counters().write_bytes

    # endregion

    # region NETWORK

    def get_net_io_bytes_sent(self):
        """
        Get number of bytes sent from psUtils
        :return: an int
        """
        return psutil.net_io_counters().bytes_sent

    def get_net_io_bytes_recv(self):
        """
        Get number of bytes received from psUtils
        :return: an int
        """
        return psutil.net_io_counters().bytes_recv

    def get_net_io_packets_sent(self):
        """
        Get number of packets sent from psUtils
        :return: an int
        """
        return psutil.net_io_counters().packets_sent

    def get_net_io_packets_recv(self):
        """
        Get number of packets received from psUtils
        :return: an int
        """
        return psutil.net_io_counters().packets_recv

    def get_net_io_errin(self):
        """
        Get total number of errors while receiving from psUtils
        :return: an int
        """
        return psutil.net_io_counters().errin

    def get_net_io_errout(self):
        """
        Get total number of errors while sending from psUtils
        :return: an int
        """
        return psutil.net_io_counters().errout

    def get_net_io_dropin(self):
        """
        Get total number of incoming packets which were dropped from psUtils
        :return: an int
        """
        return psutil.net_io_counters().dropin

    def get_net_io_dropout(self):
        """
        Get total number of outgoing packets which were dropped (always 0 on macOS and BSD) from psUtils
        :return: an int
        """
        return psutil.net_io_counters().dropout

    # endregion

    # region SENSOR
    def get_sensor_temp(self):
        """
        Get hardware temperatures from psUtils
        issue when used on MacOS (method doesn't exist), Availability: Linux, FreeBSD
        """
        return psutil.sensors_temperatures()

    def get_sensor_fans(self):
        """
        Get hardware fans speed from psUtils
        issue when used on MacOS (method doesn't exist), Availability: Linux
        """
        return psutil.sensors_fans()

    def get_sensor_battery(self):
        """
        Get  battery status information as a named tuple including the following values :
        (percent, secsleft, power_plugged ) from psUtils
        :return: a tuple
        """
        return psutil.sensors_battery()

    # endregion

    def get_current_data(self):
        """
        Get all data from psutils
        """

        self.data = {
            "user": self.get_user(),
            "system": self.get_system(),
            "idle": self.get_idle(),
            "cpu_percent": self.get_cpu_percent(),
            "cpu_times_percent_user": self.get_cpu_times_percent().user,
            "cpu_times_percent_nice": self.get_cpu_times_percent().nice,
            "cpu_times_percent_system": self.get_cpu_times_percent().system,
            "cpu_times_percent_idle": self.get_cpu_times_percent().idle,
            "ctx_switches": self.get_ctx_switches(),
            "interrupts": self.get_cpu_interrupts(),
            "load_avg_1": self.get_load_avg()[0],
            "load_avg_5": self.get_load_avg()[1],
            "load_avg_15": self.get_load_avg()[2],

            "vm_total": self.get_vm_total(),
            "vm_available": self.get_vm_available(),

            "sm_total": self.get_sm_total(),
            "sm_used": self.get_sm_used(),
            "sm_free": self.get_sm_free(),
            "sm_percent": self.get_sm_percent(),
            "sm_sin": self.get_sm_sin(),
            "sm_sout": self.get_sm_sout(),

            # "disk_partitions": self.get_disk_partitions(),
            #"disk_usage_list": self.get_disk_usages_list(),
            "disk_io_read_count": self.get_disk_io_read_count(),
            "disk_io_write_count": self.get_disk_io_write_count(),
            "disk_io_read_bytes": self.get_disk_io_read_bytes(),
            "disk_io_write_bytes": self.get_disk_io_write_bytes(),

            "net_io_bytes_sent": self.get_net_io_bytes_sent(),
            "net_io_bytes_recv": self.get_net_io_bytes_recv(),
            "net_io_packets_sent": self.get_net_io_packets_sent(),
            "net_io_packets_recv": self.get_net_io_packets_recv(),
            "net_io_errin": self.get_net_io_errin(),
            "net_io_errout": self.get_net_io_errout(),
            "net_io_dropin": self.get_net_io_dropin(),
            "net_io_dropout": self.get_net_io_dropout(),

            # "sensor_temp": self.get_sensor_temp(),
            # "sensor_fans": self.get_sensor_fans(),
            "sensor_battery_percent": self.get_sensor_battery().percent,
            "sensor_battery_secsleft": self.get_sensor_battery().secsleft,
            "sensor_battery_power_plugged": self.get_sensor_battery().power_plugged,
        }

        for part in self.get_disk_partitions():
            self.data["disk_usage_" + part.device + "_total"] = self.get_disk_usage(part.mountpoint).total
            self.data["disk_usage_" + part.device + "_used"] = self.get_disk_usage(part.mountpoint).used
            self.data["disk_usage_" + part.device + "_free"] = self.get_disk_usage(part.mountpoint).free
            self.data["disk_usage_" + part.device + "_percent"] = self.get_disk_usage(part.mountpoint).percent

        return self.data

    def get_last_data(self):
        """
        Get last data get from psutils
        """
        return self.data
