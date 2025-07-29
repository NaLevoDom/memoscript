#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import sqlite3
import sys
import types

import vyhuhol

def taskperday_update(dbpath, mod_id):
    with sqlite3.connect(dbpath) as c:
        q = "UPDATE taskperday SET day = ?, new = 0, total = 0 WHERE mod_id = ?"
        db_form = [current_date, mod_id]
        c.execute(q, db_form)

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['deck_id'], keys = ['-d', '--deck-id'], valency = 1, positional = True)
    p.add_pattern(write_to = ['mod_id'], keys = ['-m', '--mod-id'], valency = 1, positional = True)
    p.defaults = types.SimpleNamespace(deck_id = None, mod_id = None)
    r = p.parse()
    return r

if __name__ == '__main__':
    current_date = datetime.date.today().toordinal()
    r = handle_args(sys.argv)
    dbpath = 'decks/' + r.deck_id[0] + '.db'
    mod_id = r.mod_id[0]
    taskperday_update(dbpath, mod_id)
