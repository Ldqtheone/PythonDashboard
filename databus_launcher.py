"""Process module

-*- coding: utf-8 -*-

Copyright (c) 2021 Brian Lecarpentier
All Rights Reserved
Released under the MIT license
"""

import os
from multiprocessing import Pool
from utils.config.parser import *

processes = ('main.py', 'data_bus/subscribe.py')


def run_process(process):
    """
    MultiProcess Launcher
    :param process:
    """
    os.system('python3 {}'.format(process))


if __name__ == '__main__':
    pool = Pool(processes=2)
    pool.map(run_process, processes)
    print(parser.get_cli_args_to_string())
