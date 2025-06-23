#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import sqlite3
import sys
import types

import vyhuhol

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

def add_qa_record(dbpath, mod_id, auto_eval, answer_index, question):
    with sqlite3.connect(dbpath) as c:
        db_form = [mod_id, auto_eval, answer_index, question]
        q = "INSERT INTO qa VALUES(?, ?, ?, ?)"
        c.execute(q, db_form)

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['name'], keys = ['-n', '--name'], valency = 1, positional = True)
    p.add_pattern(write_to = ['mod_id'], keys = ['-m', '--mod-id'], valency = 1, positional = True)
    p.add_pattern(write_to = ['answer_index'], keys = ['-i', '--answer-index'], valency = 1, positional = True, func = int)
    p.add_pattern(write_to = ['question'], keys = ['-q', '--question'], valency = 1, positional = True)
    p.add_pattern(set_to = {"auto_eval" : 0}, keys = ['-e', '--manual-evaluation'], valency = 0)
    p.defaults = types.SimpleNamespace(name = None, mod_id = None, answer_index = None, question = None, auto_eval = 1)
    r = p.parse()
    return r

if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath = r.name[0] + '.db'
    mod_id = r.mod_id[0]
    answer_index = r.answer_index[0]
    question = r.question[0]
    auto_eval = r.auto_eval
    current_date = datetime.date.today().toordinal()
    taskperday_update(dbpath)
    drop_mod(dbpath, mod_id)
    create_mod(dbpath, mod_id)
    add_taskperday_record(dbpath, mod_id)
    add_qa_record(dbpath, mod_id, auto_eval, answer_index, question)
