"""Main module

Copyright (c) 2021 Brian Lecarpentier
All Rights Reserved
Released under the MIT license

"""

from Utils.utils_data import *


def main():
    """ main method """
    pass


if __name__ == '__main__':
    utils = UtilsClass()
    print(utils.get_current_data())
    print(utils.get_current_data()["load_avg"][0])
    partitions = utils.get_disk_partitions()
    print(partitions)
    print(utils.get_disk_usage(partitions[0].device))
    print(utils.get_disk_usages_list())

    main()
