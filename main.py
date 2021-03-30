"""Main module

Copyright (c) 2021 Brian Lecarpentier
All Rights Reserved
Released under the MIT license

"""
import psutil

from Utils.Config.parser import *


def main():
    """ main method """
    get_data()
    print(get_interval(Interval.memory.name))
    pass


if __name__ == '__main__':
    main()

