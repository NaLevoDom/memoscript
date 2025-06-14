#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import datetime

current_date = datetime.date.today().toordinal()

def taskperday_update(dbpath):
    with sqlite3.connect(dbpath) as c:
        q = f"UPDATE taskperday SET day = {current_date}, new = 0, total = 0 WHERE mod_id = 1"
        c.execute(q)

def drop_mod(dbpath, mod_id):
    with sqlite3.connect(dbpath) as c:
        q = f"DROP TABLE IF EXISTS mod_{mod_id}"
        c.execute(q)

def create_mod(dbpath, mod_id):
    with sqlite3.connect(dbpath) as c:
        q = f"""CREATE TABLE IF NOT EXISTS mod_{mod_id}(
        card_id INT PRIMARY KEY,
        delta INT,
        old_delta INT,
        date INT);
        """
        c.execute(q)

def add_taskperday_record(dbpath, mod_id):
    with sqlite3.connect(dbpath) as c:
        q = f"INSERT INTO taskperday VALUES({mod_id}, {current_date}, 0, 0)"
        c.execute(q)

def add_qa_record(dbpath, qa):
    with sqlite3.connect(dbpath) as c:
        q = f"INSERT INTO qa VALUES({qa})"
        c.execute(q)
    
if __name__ == '__main__':
    
    l = [
        ["asd.db",
             [
                 ["1", "1, 1, 0, 'Напиши порядковый номер элемента <{1}>: '"], # mod_id, mod_id, auto_eval, answer_index, question
                 ["2", "2, 1, 1, 'Напиши обозначение элемента №{0}: '"], # зачем mod_id 2 раза писать??? надо переделать чтоб без дубляжа
                 ["3", "3, 1, 2, 'Напиши название элемента <{1}>: '"]
             ]
        ],
        ["asd2.db",
             [
                 ["1", "1, 1, 0, 'Какой страны столица {1}?: '"],
                 ["2", "2, 1, 1, 'Какая столица страны {0}?: '"]
             ]
        ],
        ["asd3.db",
             [
                 ["1", "1, 1, 0, 'Напиши порядковый номер месяца <{1}>: '"],
                 ["2", "2, 1, 1, 'Напиши месяц №{0}: '"]
             ]
        ]
    ]

    for dbpath, couple in l:
        for mod_id, qa in couple:
            taskperday_update(dbpath)
            drop_mod(dbpath, mod_id)
            create_mod(dbpath, mod_id)
            add_taskperday_record(dbpath, mod_id)
            add_qa_record(dbpath, qa)
