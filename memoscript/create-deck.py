#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types

import vyhuhol

def create_deck(dbpath, n):
    with sqlite3.connect(dbpath) as c:
        s = ''
        count = 1
        for i in range(n):
            s += f'column_{count} TEXT,\n'
            count += 1
        s = s[:-2]
        q = f"CREATE TABLE deck(\nid INTEGER PRIMARY KEY,\n{s});"
        c.execute(q)

def create_taskperday(dbpath):
    with sqlite3.connect(dbpath) as c:
        q = """CREATE TABLE taskperday(
        mod_id TEXT PRIMARY KEY,
        day INT,
        new INT,
        total INT);
        """
        c.execute(q)

def create_qa(dbpath):
    with sqlite3.connect(dbpath) as c:
        q = """CREATE TABLE qa(
        mod_id TEXT PRIMARY KEY,
        auto_eval INT,
        answer_index INT,
        question TEXT);
        """
        c.execute(q)

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['name'], keys = ['-n', '--name'], valency = 1, positional = True)
    p.add_pattern(write_to = ['count'], keys = ['-c', '--count'], valency = 1, positional = True, func = int)
    p.defaults = types.SimpleNamespace(name = None, count = None)
    r = p.parse()
    return r

if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath = r.name[0] + '.db'
    n = r.count[0]
    create_deck(dbpath, n)
    create_taskperday(dbpath)
    create_qa(dbpath)
