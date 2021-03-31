"""Process module

Copyright (c) 2021 Brian Lecarpentier
All Rights Reserved
Released under the MIT license

"""

import os
from multiprocessing import Pool

processes = ('main.py', 'subscribe.py')


def run_process(process):
    """
    MultiProcess Luancher
    :param process:
    """
    os.system('python {}'.format(process))


if __name__ == '__main__':
    pool = Pool(processes=2)
    pool.map(run_process, processes)
