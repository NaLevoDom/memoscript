#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types

import vyhuhol
from memo import is_db_exist

def drop_mod(dbpath, mod_id):
    with sqlite3.connect(dbpath) as c:
        q = "DELETE FROM schedule WHERE mod_id = ?"
        db_form = [mod_id]
        c.execute(q, db_form)

def delete_qa_mod(dbpath, mod_id):
    with sqlite3.connect(dbpath) as c:
        q = "DELETE FROM qa WHERE mod_id = ?"
        db_form = [mod_id]
        c.execute(q, db_form)

def delete_taskperday_mod(dbpath, mod_id):
    with sqlite3.connect(dbpath) as c:
        q = "DELETE FROM taskperday WHERE mod_id = ?"
        db_form = [mod_id]
        c.execute(q, db_form)

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['deck_id'], keys = ['-d', '--deck-id'], valency = 1, positional = True, func = is_db_exist)
    p.add_pattern(write_to = ['mod_id'], keys = ['-m', '--mod-id'], valency = 1, positional = True)
    p.defaults = types.SimpleNamespace(deck_id = None, mod_id = None)
    r = p.parse()
    return r

if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath = r.deck_id[0]
    mod_id = r.mod_id[0]
    drop_mod(dbpath, mod_id)
    delete_qa_mod(dbpath, mod_id)
    delete_taskperday_mod(dbpath, mod_id)
