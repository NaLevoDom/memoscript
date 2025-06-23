#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types

import vyhuhol

def add_deck_record(dbpath, i):
    with sqlite3.connect(dbpath) as c:
        db_form = [None] + i
        count = len(db_form)
        string = ', '.join(['?'] * count)
        q = f"INSERT INTO deck VALUES({string})"
        c.execute(q, db_form)

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['name'], keys = ['-n', '--name'], valency = 1, positional = True)
    p.add_pattern(write_to = ['fields'], keys = ['-f', '--fields'], valency = '+', positional = True)
    p.defaults = types.SimpleNamespace(name = None, fields = None)
    r = p.parse()
    return r

if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath = 'decks/' + r.name[0] + '.db'
    i = r.fields
    add_deck_record(dbpath, i)
    