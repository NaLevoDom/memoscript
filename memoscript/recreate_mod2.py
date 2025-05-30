#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from sqlite3 import connect

dbpath = "asd.db"
current_date = datetime.date.today().toordinal()

def taskperday_update():
    with connect(dbpath) as c:
        q = f"UPDATE taskperday SET day = {current_date}, new = 0, total = 0 WHERE id = 2"
        c.execute(q)

def drop_dbmod_1(): # Элемент в номер / сделано
    with connect(dbpath) as c:
        q = "DROP TABLE mod2"
        c.execute(q)

def create_dbmod_1(): # Элемент в номер / сделано
    with connect(dbpath) as c:
        q = """CREATE TABLE mod2(
        element_id INT PRIMARY KEY,
        delta INT,
        old_delta INT,
        date INT);
        """
        # element_id integer references elements(id)); # Пока без выебонов. По басяцки напишем.
        c.execute(q)
        c.execute("VACUUM")

if __name__ == '__main__':
    taskperday_update()
    drop_dbmod_1()
    create_dbmod_1()