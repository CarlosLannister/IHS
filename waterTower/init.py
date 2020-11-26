#!/usr/bin/env python

"""
swat-s1 init.py

Run this script just once to create and init the sqlite table.
"""

from minicps.states import SQLiteState
from utils import PATH, SCHEMA, SCHEMA_INIT, PATH2, SCHEMA2, SCHEMA_INIT2
from sqlite3 import OperationalError


if __name__ == "__main__":

    try:
        SQLiteState._create(PATH, SCHEMA)
        SQLiteState._init(PATH, SCHEMA_INIT)

        SQLiteState._create(PATH2, SCHEMA2)
        SQLiteState._init(PATH2, SCHEMA_INIT2)
        print("{} successfully created.".format(PATH))
    except OperationalError:
        print("{} already exists.".format(PATH))

