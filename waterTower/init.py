#!/usr/bin/env python

"""
swat-s1 init.py

Run this script just once to create and init the sqlite table.
"""

from minicps.states import SQLiteState
from utils import PATH, SCHEMA, SCHEMA_INIT, PATH2, SCHEMA2, SCHEMA_INIT2, PATH_2, PATH_3, SCHEMA_2, SCHEMA_3, SCHEMA_INIT_2, SCHEMA_INIT_3
from utils import PATH3, SCHEMA3, SCHEMA_INIT3
from utils import PATH4, SCHEMA4, SCHEMA_INIT4
from sqlite3 import OperationalError


if __name__ == "__main__":

    try:
        SQLiteState._create(PATH, SCHEMA)
        SQLiteState._init(PATH, SCHEMA_INIT)

        SQLiteState._create(PATH2, SCHEMA2)
        SQLiteState._init(PATH2, SCHEMA_INIT2)

        SQLiteState._create(PATH_2, SCHEMA_2)
        SQLiteState._init(PATH_2, SCHEMA_INIT_2)

        SQLiteState._create(PATH_3, SCHEMA_3)
        SQLiteState._init(PATH_3, SCHEMA_INIT_3)

        SQLiteState._create(PATH3, SCHEMA3)
        SQLiteState._init(PATH3, SCHEMA_INIT3)

        SQLiteState._create(PATH4, SCHEMA4)
        SQLiteState._init(PATH4, SCHEMA_INIT4)


        print("{} successfully created.".format(PATH))
    except OperationalError:
        print("{} already exists.".format(PATH))

