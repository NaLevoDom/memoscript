#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types

import vyhuhol

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['name'], keys = ['-n', '--name'], valency = 1, positional = True)
    p.add_pattern(write_to = ['card_id'], keys = ['-c', '--card-id'], valency = 1, positional = True)
    p.defaults = types.SimpleNamespace(name = None, card_id = None)
    r = p.parse()
    return r

def delete_deck_record(dbpath, card_id):
    with sqlite3.connect(dbpath) as c:
        q = f"DELETE FROM deck WHERE id = {card_id}"
        c.execute(q)

def delete_mod_record(dbpath, card_id, mod_id):
    with sqlite3.connect(dbpath) as c:
        q = f"DELETE FROM mod_{mod_id} WHERE card_id = {card_id}"
        c.execute(q)

def get_qa(dbpath):
    with sqlite3.connect(dbpath) as c:
        q = f"SELECT * FROM qa"
        i = c.execute(q)
        l = list(i)
    return l

if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath = 'decks/' + r.name[0] + '.db'
    card_id = r.card_id[0]
    delete_deck_record(dbpath, card_id)
    qa = get_qa(dbpath)
    for mod_id, auto_eval, answer_index, question in qa:
        delete_mod_record(dbpath, card_id, mod_id)
