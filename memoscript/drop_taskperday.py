#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import sqlite3
import sys
import types

import vyhuhol
from memo import is_db_exist, is_mode_exist

def taskperday_update(dbpath, mode_id):
    with sqlite3.connect(dbpath) as c:
        q = "UPDATE taskperday SET day = ?, new = 0, total = 0 WHERE mode_id = ?"
        db_form = [current_date, mode_id]
        c.execute(q, db_form)

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['deck_id'], keys = ['-d', '--deck-id'], valency = 1, positional = True, func = is_db_exist)
    p.add_pattern(write_to = ['mode_id'], keys = ['-m', '--mode-id'], valency = 1, positional = True)
    p.defaults = types.SimpleNamespace(deck_id = None, mode_id = None)
    r = p.parse()
    return r

if __name__ == '__main__':
    current_date = datetime.date.today().toordinal()
    r = handle_args(sys.argv)
    dbpath = r.deck_id[0]
    mode_id = r.mode_id[0]
    is_mode_exist(dbpath, mode_id)
    taskperday_update(dbpath, mode_id)
