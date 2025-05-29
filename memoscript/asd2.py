#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlite3 import connect

dbpath = "khjgng.db"

def add_record(identif, sym):
    with connect(dbpath) as c:
        db_form = [identif, sym]
        q = f"INSERT INTO deck VALUES(?, ?)"
        c.execute(q, db_form)

def create_db(): # / сделано
    with connect(dbpath) as c:
        q = """CREATE TABLE deck(
        id TEXT PRIMARY KEY,
        sym TEXT);
        """
        c.execute(q)
        c.execute("VACUUM")

def drop_elements(): # Элемент в номер / сделано
    with connect(dbpath) as c:
        q = "DROP TABLE deck"
        c.execute(q)

def ad_hoc_add(): # / сделано
    elements = [['1', 'Январь'], ['2', 'Февраль'], ['3', 'Март'], ['4', 'Апрель'], ['5', 'Май'], ['6', 'Июнь'], ['7', 'Июль'], ['8', 'Август'], ['9', 'Сентябрь'], ['10', 'Октябрь'], ['11', 'Ноябрь'], ['12', 'Декабрь']]
    for identif, sym in elements:
        add_record(identif, sym)




