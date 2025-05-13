#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlite3 import connect

dbpath = "asd.db"

def drop_dbmod_1(): # Элемент в номер / сделано
    with connect(dbpath) as c:
        q = "DROP TABLE mod1"
        c.execute(q)
        c.execute("VACUUM")

def create_dbmod_1(): # Элемент в номер / сделано
    with connect(dbpath) as c:
        q = """CREATE TABLE mod1(
        element_id INT PRIMARY KEY,
        delta INT,
        old_delta INT,
        date INT);
        """
        # element_id integer references elements(id)); # Пока без выебонов. По басяцки напишем.
        c.execute(q)
        c.execute("VACUUM")

if __name__ == '__main__':
    drop_dbmod_1()
    create_dbmod_1()
