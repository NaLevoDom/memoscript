#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types

import vyhuhol

def update_deck_record(dbpath, fields):
    with sqlite3.connect(dbpath) as c:
        card_id = fields[0]
        q = "DELETE FROM deck WHERE id = ?"
        db_form = [card_id]
        c.execute(q, db_form)
        question_marks = '?, ' * len(fields)
        question_marks = question_marks[:-2]
        q = f'INSERT INTO deck VALUES({question_marks})'
        print(q)
        c.execute(q, fields)


def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['name'], keys = ['-n', '--name'], valency = 1, positional = True)
    p.add_pattern(write_to = ['fields'], keys = ['-f', '--fields-with-id'], valency = '+', positional = True)
    p.defaults = types.SimpleNamespace(name = None, fields = None)
    r = p.parse()
    return r


if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath = 'decks/' + r.name[0] + '.db'
    fields = r.fields
    update_deck_record(dbpath, fields)
    