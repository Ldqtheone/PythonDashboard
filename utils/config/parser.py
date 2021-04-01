"""Parser module
Load and write the configuration data from config file
"""

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


def get_data():
    """
    Load data from config file
    :return: all the data
    """
    stream = open("utils/config/data.yaml", "r")
    infos = load(stream, Loader=Loader)
    return infos


def get_interval(value):
    """
    Load an interval data from config file of the specified value
    :param value : A string of type Interval (Enum)
    :return: int of the interval value
    """
    return get_data()["interval"][value]


def get_token():
    """
    Load token data from config file
    :return: the token
    """
    return get_data()["token"]


def get_org():
    """
    Load org data from config file
    :return: the org
    """
    return get_data()["org"]


def get_bucket():
    """
    Load bucket data from config file
    :return: the bucket
    """
    return get_data()["bucket"]


def get_url():
    """
    Load url data from config file
    :return: the url
    """
    return get_data()["url"]


def get_display():
    """
    Load display data from config file
    :return: the display
    """
    return get_data()["display"]


def get_identifier():
    """
    Load identifier data from config file
    :return: the identifier
    """
    return get_data()["identifier"]
