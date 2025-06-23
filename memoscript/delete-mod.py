#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types

import vyhuhol

def drop_mod(dbpath, mod_id):
    with sqlite3.connect(dbpath) as c:
        q = f"DROP TABLE IF EXISTS mod_{mod_id}"
        c.execute(q)

def delete_qa_mod(dbpath, mod_id):
    with sqlite3.connect(dbpath) as c:
        q = f"DELETE FROM qa WHERE mod_id = {mod_id}"
        c.execute(q)

def delete_taskperday_mod(dbpath, mod_id):
    with sqlite3.connect(dbpath) as c:
        q = f"DELETE FROM taskperday WHERE mod_id = {mod_id}"
        c.execute(q)

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['name'], keys = ['-n', '--name'], valency = 1, positional = True)
    p.add_pattern(write_to = ['mod_id'], keys = ['-m', '--mod-id'], valency = 1, positional = True)
    p.defaults = types.SimpleNamespace(name = None, mod_id = None)
    r = p.parse()
    return r

if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath = r.name[0] + '.db'
    mod_id = r.mod_id[0]
    drop_mod(dbpath, mod_id)
    delete_qa_mod(dbpath, mod_id)
    delete_taskperday_mod(dbpath, mod_id)
