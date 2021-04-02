"""utils_data module

Need to use pip install psutils.

-*- coding: utf-8 -*-

Copyright (c) 2021 Gwenael Marchetti--Waternaux
All Rights Reserved
Released under the MIT license
"""

import psutil


class UtilsData:
    """
    A class to have all data from psUtils.
    """
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
        :return: sensor temperature
        """
        return psutil.sensors_temperatures()

    def get_sensor_fans(self):
        """
        Get hardware fans speed from psUtils
        issue when used on MacOS (method doesn't exist), Availability: Linux
        :return: sensor fans
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

    # region category getters
    def get_disk_usage_data(self, should_update=False):
        """
        Get all disk usage data from psUtils thanks disk partition
        if should_update is true, we update UtilsData class attribute data with this data
        :param should_update: need to return disk usages data or update data class attribute
        :type should_update: bool
        :return: a dict containing data
        """
        partitions_list = self.get_disk_partitions()

        disk_usage = {}
        for i in range(0, len(partitions_list), 1):
            if "\\" in partitions_list[i].device:
                device = "device_" + str(i)
            else:
                device = partitions_list[i].device.split("/")[len(partitions_list[i].device.split("/")) - 1]

            disk_usage["disk_usage_total_" + device] = self.get_disk_usage(partitions_list[i].mountpoint).total
            disk_usage["disk_usage_used_" + device] = self.get_disk_usage(partitions_list[i].mountpoint).used
            disk_usage["disk_usage_free_" + device] = self.get_disk_usage(partitions_list[i].mountpoint).free
            disk_usage["disk_usage_percent_" + device] = self.get_disk_usage(partitions_list[i].mountpoint).percent
        return self.handle_get_data(disk_usage, should_update)

    def get_cpu_data(self, should_update=False):
        """
        Get all cpu data from psUtils
        if should_update is true, we update UtilsData class attribute data with this data
        :param should_update: need to return cpu data or update data class attribute
        :type should_update: bool
        :return: a dict containing data
        """
        cpu_data = {
            "user": self.get_user(),
            "system": self.get_system(),
            "idle": self.get_idle(),
            "cpu_percent": self.get_cpu_percent(),
            "cpu_times_percent_user": self.get_cpu_times_percent().user,
            # "cpu_times_percent_nice": self.get_cpu_times_percent().nice,
            "cpu_times_percent_system": self.get_cpu_times_percent().system,
            "cpu_times_percent_idle": self.get_cpu_times_percent().idle,
            "ctx_switches": self.get_ctx_switches(),
            "interrupts": self.get_cpu_interrupts(),
            "load_avg_1": self.get_load_avg()[0],
            "load_avg_5": self.get_load_avg()[1],
            "load_avg_15": self.get_load_avg()[2],
        }
        return self.handle_get_data(cpu_data, should_update)

    def get_memory_data(self, should_update=False):
        """
        Get all memory data from psUtils
        if should_update is true, we update UtilsData class attribute data with this data
        :param should_update: need to return memory data or update data class attribute
        :type should_update: bool
        :return: a dict containing data
        """
        memory_data = {
            "vm_total": self.get_vm_total(),
            "vm_available": self.get_vm_available(),

            "sm_total": self.get_sm_total(),
            "sm_used": self.get_sm_used(),
            "sm_free": self.get_sm_free(),
            "sm_percent": self.get_sm_percent(),
            "sm_sin": self.get_sm_sin(),
            "sm_sout": self.get_sm_sout(),
        }
        return self.handle_get_data(memory_data, should_update)

    def get_disk_data(self, should_update=False):
        """
        Get all disk data from psUtils
        if should_update is true, we update UtilsData class attribute data with this data
        :param should_update: need to return disk data or update data class attribute
        :type should_update: bool
        :return: a dict containing data
        """
        disk_data = {
            # "disk_partitions": self.get_disk_partitions(),
            #"disk_usage_list": self.get_disk_usages_list(),
            "disk_io_read_count": self.get_disk_io_read_count(),
            "disk_io_write_count": self.get_disk_io_write_count(),
            "disk_io_read_bytes": self.get_disk_io_read_bytes(),
            "disk_io_write_bytes": self.get_disk_io_write_bytes(),
        }
        return self.handle_get_data(disk_data, should_update)

    def get_net_data(self, should_update=False):
        """
        Get all net data from psUtils
        if should_update is true, we update UtilsData class attribute data with this data
        :param should_update: need to return net data or update data class attribute
        :type should_update: bool
        :return: a dict containing data
        """
        net_data = {
            "net_io_bytes_sent": self.get_net_io_bytes_sent(),
            "net_io_bytes_recv": self.get_net_io_bytes_recv(),
            "net_io_packets_sent": self.get_net_io_packets_sent(),
            "net_io_packets_recv": self.get_net_io_packets_recv(),
            "net_io_errin": self.get_net_io_errin(),
            "net_io_errout": self.get_net_io_errout(),
            "net_io_dropin": self.get_net_io_dropin(),
            "net_io_dropout": self.get_net_io_dropout(),
        }
        return self.handle_get_data(net_data, should_update)

    def get_sensor_data(self, should_update=False):
        """
        Get all sensor data from psUtils
        if should_update is true, we update UtilsData class attribute data with this data
        :param should_update: need to return sensor data or update data class attribute
        :type should_update: bool
        :return: a dict containing data
        """
        # All is comment in this dict because some agent could not access to these or are not numbers.
        # It then lead to issue in influxDB.
        # some can just be not callable, as sensor temp that lead to error
        sensor_data = {
            # "sensor_temp": self.get_sensor_temp(),
            # "sensor_fans": self.get_sensor_fans(),
            # "sensor_battery_percent": self.get_sensor_battery().percent,
            # "sensor_battery_secsleft": self.get_sensor_battery().secsleft,
            # "sensor_battery_power_plugged": self.get_sensor_battery().power_plugged,
        }

        return self.handle_get_data(sensor_data, should_update)

    # endregion

    def handle_get_data(self, new_data, should_update):
        """
        Handle the data to return.
        If should_update is true, we update UtilsData class attribute data with the new data,
        and return the current data.
        Else, we only return the wanted data.
        :param new_data: all data to return or update
        :type new_data: dict
        :param should_update: need to return sensor data or update data class attribute
        :type should_update: bool
        :return: a dict new data OR all data collected until now
        """
        if should_update:
            self.data.update(new_data)
            return self.data
        else:
            return new_data

    def get_current_data(self):
        """
        Get all data from psUtils and save these in UtilsData class data attribute
        :return: a dict containing all these data
        """
        self.get_cpu_data(True)
        self.get_memory_data(True)
        self.get_disk_data(True)
        self.get_disk_usage_data(True)
        self.get_net_data(True)
        self.get_sensor_data(True)

        return self.data

    def get_last_data(self):
        """
        Get all collected data from psUtils until now
        :return: a dict containing all these data
        """
        return self.data

    def create_user_id(self):
        """
        Create and get a user id from first user name and pid.
        This could have be used has agent_number for influxDb tag
        :return: a string containing first user name and pid
        """
        return str(psutil.users()[0].name) + "_" + str(psutil.users()[0].pid)
