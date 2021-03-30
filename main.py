"""Main module

Copyright (c) 2021 Brian Lecarpentier
All Rights Reserved
Released under the MIT license

"""

import Utils.database as db


def main():
    """ main method """
    #db.write_query()
    print(db.execute_query())


if __name__ == '__main__':
    main()
