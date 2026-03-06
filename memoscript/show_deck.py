#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types

import vyhuhol
from memo import is_db_exist

def print_deck(dbpath):
    with sqlite3.connect(dbpath) as c:
        q = "SELECT * FROM deck ORDER BY card_id ASC"
        i = c.execute(q)
        for fields in i:
            print(fields)

def print_template(dbpath, template_id):
    with sqlite3.connect(dbpath) as c:
        q = "SELECT * FROM schedule WHERE template_id = ? ORDER BY due_date ASC"
        db_form = [template_id]
        i = c.execute(q, db_form)
        for template_id, card_id, delta, prev_delta, due_date in i:
            qq = "SELECT * FROM deck WHERE card_id = ?"
            db_form = [card_id]
            ii = c.execute(qq, db_form)
            fields = next(ii)
            print(f"{fields=}, {delta=}, {prev_delta=}, {due_date=}")

def get_templates(dbpath):
    with sqlite3.connect(dbpath) as c:
        q = "SELECT * FROM templates"
        i = c.execute(q)
        l = list(i)
    return l

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['deck_id'], keys = ['-d', '--deck-id'], valency = 1, positional = True, func = is_db_exist)
    p.defaults = types.SimpleNamespace(deck_id = None)
    r = p.parse()
    return r

if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath = r.deck_id[0]
    print_deck(dbpath)
    templates = get_templates(dbpath)
    for template_id, auto_grade, answer_index, question_form in templates:
        print()
        print(f"{template_id=}, {auto_grade=}, {answer_index=}, {question_form=}")
        print_template(dbpath, template_id)
