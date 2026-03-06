#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types

import vyhuhol
from memo import is_db_exist

def drop_mode(dbpath, mode_id):
    with sqlite3.connect(dbpath) as c:
        q = "DELETE FROM schedule WHERE mode_id = ?"
        db_form = [mode_id]
        c.execute(q, db_form)

def delete_qa_mode(dbpath, mode_id):
    with sqlite3.connect(dbpath) as c:
        q = "DELETE FROM qa WHERE mode_id = ?"
        db_form = [mode_id]
        c.execute(q, db_form)

def delete_taskperday_mode(dbpath, mode_id):
    with sqlite3.connect(dbpath) as c:
        q = "DELETE FROM taskperday WHERE mode_id = ?"
        db_form = [mode_id]
        c.execute(q, db_form)

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['deck_id'], keys = ['-d', '--deck-id'], valency = 1, positional = True, func = is_db_exist)
    p.add_pattern(write_to = ['mode_id'], keys = ['-m', '--mode-id'], valency = 1, positional = True)
    p.defaults = types.SimpleNamespace(deck_id = None, mode_id = None)
    r = p.parse()
    return r

if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath = r.deck_id[0]
    mode_id = r.mode_id[0]
    drop_mode(dbpath, mode_id)
    delete_qa_mode(dbpath, mode_id)
    delete_taskperday_mode(dbpath, mode_id)
