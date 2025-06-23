#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types

import vyhuhol

def print_deck(dbpath):
    with sqlite3.connect(dbpath) as c:
        q = f"SELECT * FROM deck ORDER BY id ASC"
        i = c.execute(q)
        for fields in i:
            print(fields)

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['name'], keys = ['-n', '--name'], valency = 1, positional = True)
    p.defaults = types.SimpleNamespace(name = None)
    r = p.parse()
    return r

def print_mod(dbpath, mod_id):
    with sqlite3.connect(dbpath) as c:
        q = f"SELECT * FROM mod_{mod_id} ORDER BY date ASC"
        i = c.execute(q)
        for card_id, delta, old_delta, element_date in i:
            qq = f"SELECT * FROM deck WHERE id = {card_id}"
            ii = c.execute(qq)
            fields = next(ii)
            print(f"fields = {fields}, delta = {delta}, old_delta = {old_delta}, element_date = {element_date}")

def get_qa(dbpath):
    with sqlite3.connect(dbpath) as c:
        q = f"SELECT * FROM qa"
        i = c.execute(q)
        l = list(i)
    return l

if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath = r.name[0] + '.db'
    print_deck(dbpath)
    qa = get_qa(dbpath)
    for mod_id, auto_eval, answer_index, question in qa:
        print()
        print(f"mod_id = {mod_id}, auto_eval = {auto_eval}, answer_index = {answer_index}, question = '{question}'")
        print_mod(dbpath, mod_id)
