#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlite3 import connect

dbpath = "asd.db"

def add_record(identif, sym):
    with connect(dbpath) as c:
        db_form = [identif, sym]
        q = f"INSERT INTO elements VALUES(?, ?)"
        c.execute(q, db_form)

def create_db():
    with connect(dbpath) as c:
        q = """CREATE TABLE elements(
        id INT PRIMARY KEY,
        sym TEXT);
        """
        c.execute(q)
        c.execute("VACUUM")

def ad_hoc_add():
    elements = [[1, 'H'], [2, 'He'], [3, 'Li'], [4, 'Be'], [5, 'B'], [6, 'C'], [7, 'N'], [8, 'O'], [9, 'F'], [10, 'Ne'], [11, 'Na'], [12, 'Mg']]
    for identif, sym in elements:
        add_record(identif, sym)





