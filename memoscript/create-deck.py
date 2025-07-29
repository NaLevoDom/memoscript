#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types

import vyhuhol

def create_deck_table(dbpath, n):
    with sqlite3.connect(dbpath) as c:
        s = ''
        count = 1
        for i in range(n):
            s += f'column_{count} TEXT,\n'
            count += 1
        s = s[:-2]
        q = f"CREATE TABLE deck(\ncard_id INTEGER PRIMARY KEY,\n{s});"
        c.execute(q)

def create_taskperday_table(dbpath):
    with sqlite3.connect(dbpath) as c:
        q = """CREATE TABLE taskperday(
        mod_id TEXT PRIMARY KEY,
        day INT,
        new INT,
        total INT);
        """
        c.execute(q)

def create_qa_table(dbpath):
    with sqlite3.connect(dbpath) as c:
        q = """CREATE TABLE qa(
        mod_id TEXT PRIMARY KEY,
        auto_eval INT,
        answer_index INT,
        question TEXT);
        """
        c.execute(q)

def create_schedule_table(dbpath):
    with sqlite3.connect(dbpath) as c:
        q = """CREATE TABLE schedule(
        mod_id TEXT,
        card_id INT,
        delta INT,
        old_delta INT,
        schedule_date INT);
        """
        c.execute(q)

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['deck_id'], keys = ['-d', '--deck-id'], valency = 1, positional = True)
    p.add_pattern(write_to = ['count'], keys = ['-c', '--count'], valency = 1, positional = True, func = int)
    p.defaults = types.SimpleNamespace(deck_id = None, count = None)
    r = p.parse()
    return r

if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath = 'decks/' + r.deck_id[0] + '.db'
    n = r.count[0]
    create_deck_table(dbpath, n)
    create_taskperday_table(dbpath)
    create_qa_table(dbpath)
    create_schedule_table(dbpath)
