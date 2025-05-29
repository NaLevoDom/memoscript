#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlite3 import connect

# dbpath = "asd.db"
dbpath = "khjgng.db"

def one_time_function():
    with connect(dbpath) as c:
        q = f"ALTER TABLE months RENAME TO deck;"
        c.execute(q)

def add_record(identif, sym):
    with connect(dbpath) as c:
        db_form = [identif, sym]
        q = f"INSERT INTO elements VALUES(?, ?)"
        c.execute(q, db_form)

def create_db(): # / сделано
    with connect(dbpath) as c:
        q = """CREATE TABLE elements(
        id TEXT PRIMARY KEY,
        sym TEXT);
        """
        c.execute(q)
        c.execute("VACUUM")

def drop_elements(): # Элемент в номер / сделано
    with connect(dbpath) as c:
        q = "DROP TABLE elements"
        c.execute(q)

def ad_hoc_add(): # / сделано
    elements = [['1', 'H'], ['2', 'He'], ['3', 'Li'], ['4', 'Be'], ['5', 'B'], ['6', 'C'], ['7', 'N'], ['8', 'O'], ['9', 'F'], ['10', 'Ne'], ['11', 'Na'], ['12', 'Mg'], ['13', 'Al'], ['14', 'Si'], ['15', 'P'], ['16', 'S'], ['17', 'Cl'], ['18', 'Ar'], ['19', 'K'], ['20', 'Ca'], ['21', 'Sc'], ['22', 'Ti'], ['23', 'V'], ['24', 'Cr'], ['25', 'Mn'], ['26', 'Fe'], ['27', 'Co'], ['28', 'Ni'], ['29', 'Cu'], ['30', 'Zn'], ['31', 'Ga'], ['32', 'Ge'], ['33', 'As'], ['34', 'Se'], ['35', 'Br'], ['36', 'Kr']]
    for identif, sym in elements:
        add_record(identif, sym)




