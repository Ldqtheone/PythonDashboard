"""Main module

Copyright (c) 2021 Brian Lecarpentier
All Rights Reserved
Released under the MIT license

"""

from Utils.influx_class import *


def main():
    """ main method """
    influx = DataStorageClass()
    influx.send_data_to_influx_db()


if __name__ == '__main__':
    main()
