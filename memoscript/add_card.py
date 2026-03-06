#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types
import json

import vyhuhol
from memo import is_db_exist

def get_field_count(dbpath):
    with sqlite3.connect(dbpath) as c:
        i = c.execute("SELECT COUNT(*) FROM deck_fields")
        count, = next(i)
        return count

def add_deck_record(dbpath, fields):
    expected_count = get_field_count(dbpath)
    if len(fields) != expected_count:
        raise ValueError(f"Expected {expected_count} fields, got {len(fields)}")
    with sqlite3.connect(dbpath) as c:
        q = "INSERT INTO deck(card_id, fields_json) VALUES(?, ?)"
        db_form = [None, json.dumps(fields, ensure_ascii=False)]
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
    