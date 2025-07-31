#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types

import vyhuhol

def print_deck(dbpath):
    with sqlite3.connect(dbpath) as c:
        q = "SELECT * FROM deck ORDER BY id ASC"
        i = c.execute(q)
        for fields in i:
            print(fields)

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['deck_id'], keys = ['-d', '--deck-id'], valency = 1, positional = True)
    p.defaults = types.SimpleNamespace(deck_id = None)
    r = p.parse()
    return r

def print_mod(dbpath, mod_id):
    with sqlite3.connect(dbpath) as c:
        q = "SELECT * FROM schedule WHERE mod_id = ? ORDER BY schedule_date ASC"
        db_form = [mod_id]
        i = c.execute(q, db_form)
        for mod_id, card_id, delta, old_delta, schedule_date in i:
            qq = "SELECT * FROM deck WHERE card_id = ?"
            db_form = [card_id]
            ii = c.execute(qq, db_form)
            fields = next(ii)
            print(f"{fields=}, {delta=}, {old_delta=}, {schedule_date=}")

def get_qa(dbpath):
    with sqlite3.connect(dbpath) as c:
        q = "SELECT * FROM qa"
        i = c.execute(q)
        l = list(i)
    return l

if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath = 'decks/' + r.deck_id[0] + '.db'
    print_deck(dbpath)
    qa = get_qa(dbpath)
    for mod_id, auto_eval, answer_index, question in qa:
        print()
        print(f"{mod_id=}, {auto_eval=}, {answer_index=}, {question=}")
        print_mod(dbpath, mod_id)
