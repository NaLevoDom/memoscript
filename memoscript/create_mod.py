#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import datetime

dbpath = "asd.db"
mod_id = "1"
qa = "'1', 0, 'Напиши порядковый номер элемента <{1}>: '"
# mod_id = "2"
# qa = "2, 1, 'Напиши обозначение элемента №{0}: '"

# qa = "1, 0, 'Напиши порядковый номер месяца <{1}>: '"
# qa = "2, 1, 'Напиши месяц №{0}: '"

current_date = datetime.date.today().toordinal()

def taskperday_update():
    with sqlite3.connect(dbpath) as c:
        q = f"UPDATE taskperday SET day = {current_date}, new = 0, total = 0 WHERE mod_id = 1"
        c.execute(q)

def drop_mod():
    with sqlite3.connect(dbpath) as c:
        q = f"DROP TABLE IF EXISTS mod{mod_id}"
        c.execute(q)

def create_mod():
    with sqlite3.connect(dbpath) as c:
        q = f"""CREATE TABLE IF NOT EXISTS mod_{mod_id}(
        card_id INT PRIMARY KEY,
        delta INT,
        old_delta INT,
        date INT);
        """
        c.execute(q)

def add_taskperday_record():
    with sqlite3.connect(dbpath) as c:
        q = f"INSERT INTO taskperday VALUES({mod_id}, {current_date}, 0, 0)"
        c.execute(q)

def add_qa_record():
    with sqlite3.connect("asd.db") as c:
        q = f"INSERT INTO qa VALUES({qa})"
        c.execute(q)
    
if __name__ == '__main__':
    taskperday_update()
    drop_mod()
    create_mod()
    add_taskperday_record()
    add_qa_record()