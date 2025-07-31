#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types

import vyhuhol
from memo import is_db_exist

def update_deck_record(dbpath, fields):
    with sqlite3.connect(dbpath) as c:
        card_id = fields[0]
        q = "DELETE FROM deck WHERE card_id = ?"
        db_form = [card_id]
        c.execute(q, db_form)
        question_marks = '?, ' * len(fields)
        question_marks = question_marks[:-2]
        q = f'INSERT INTO deck VALUES({question_marks})'
        print(q)
        c.execute(q, fields)


def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['deck_id'], keys = ['-d', '--deck-id'], valency = 1, positional = True, func = is_db_exist)
    p.add_pattern(write_to = ['fields'], keys = ['-f', '--fields-with-id'], valency = '+', positional = True)
    p.defaults = types.SimpleNamespace(deck_id = None, fields = None)
    r = p.parse()
    return r


if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath = r.deck_id[0]
    fields = r.fields
    update_deck_record(dbpath, fields)
    