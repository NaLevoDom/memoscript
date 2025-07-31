#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types

import vyhuhol
from memo import is_db_exist

def add_deck_record(dbpath, fields):
    with sqlite3.connect(dbpath) as c:
        db_form = [None] + fields
        count = len(db_form)
        string = ', '.join(['?'] * count) # ### Порнография
        # print(string) # К тому же нужно намутить валидацию количества полей
        q = f"INSERT INTO deck VALUES({string})"
        c.execute(q, db_form)

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['deck_id'], keys = ['-d', '--deck-id'], valency = 1, positional = True, func = is_db_exist)
    p.add_pattern(write_to = ['fields'], keys = ['-f', '--fields'], valency = '+', positional = True)
    p.defaults = types.SimpleNamespace(deck_id = None, fields = None)
    r = p.parse()
    return r

if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath = r.deck_id[0]
    fields = r.fields
    add_deck_record(dbpath, fields)
    