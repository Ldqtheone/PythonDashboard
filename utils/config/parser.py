"""parser module

Load and write the configuration data from config file

-*- coding: utf-8 -*-

Copyright (c) 2021 Guillaume Pinheiro
All Rights Reserved
Released under the MIT license
"""

import argparse
import sys
from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from enum import Enum


class Interval(Enum):
    """
    Define interval enum to match data.yaml interval values names
    """
    cpu = 1
    memory = 2
    disk = 3
    network = 4
    sensor = 5


class ArgParser:
    """
    A class to parse cli args
    """
    parser = argparse.ArgumentParser(description="Process some integers.")

    def __init__(self):
        self.parser.add_argument("--cpu", metavar="-c", type=int, nargs="+", help="an integer for the cpu interval")
        self.parser.add_argument("--memory", metavar="-m", type=int, nargs="+",
                                 help="an integer for the memory interval")
        self.parser.add_argument("--disk", metavar="-d", type=int, nargs="+", help="an integer for the disk interval")
        self.parser.add_argument("--network", metavar="-n", type=int, nargs="+",
                                 help="an integer for the network interval")
        self.parser.add_argument("--sensor", metavar="-s", type=int, nargs="+",
                                 help="an integer for the sensor interval")

        self.parser.add_argument("--token", metavar="-t", type=str, nargs="+",
                                 help="a token to connect to influxDb")
        self.parser.add_argument("--org", metavar="-o", type=str, nargs="+",
                                 help="an organisation name")
        self.parser.add_argument("--bucket", metavar="-b", type=str, nargs="+",
                                 help="a bucket name")
        self.parser.add_argument("--url", metavar="-u", type=str, nargs="+",
                                 help="an url for influxDb ")
        self.parser.add_argument("--identifier", metavar="-i", type=str, nargs="+",
                                 help="an identifier for your system, use to sort in DB")
        self.parser.add_argument("--display", metavar="-d", type=str, nargs="+",
                                 help="full / basic")

        self.args = self.parser.parse_args()

    def get_data(self, name):
        try:
            return vars(self.args)[name]
        except:
            return None


def get_cli_args_to_string(self):
    """
    Get all cli args if any used
    """
    # Output argument-wise
    position = 1
    txt = ""
    while len(sys.argv) - 1 >= position:
        txt += sys.argv[position] + " "
        position = position + 1
    return txt


# region get data from yaml or cli args

def get_data_config(name):
    """
    Get configuration data from given args if used, else from .yaml file
    """
    if parser.get_data(name):
        return parser.get_data(name)[0]
    else:
        # used to check if our Enum Interval contain the searched key
        try:
            value = Interval[name]
            return get_data()["interval"][name]
        except:
            pass

        # then, used to check if .yaml file contain the specified key
        try:
            value = get_data()[name]
            return value
        except:
            pass


def get_data():
    """
    Load data from config file
    :return: all the data
    """
    stream = open("utils/config/data.yaml", "r")
    infos = load(stream, Loader=Loader)
    return infos

# endregion

parser = ArgParser()