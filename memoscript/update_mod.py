#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types

import vyhuhol

def update_mod(dbpath, mod_id, answer_index, question, auto_eval):
    with sqlite3.connect(dbpath) as c:
        q = "UPDATE qa SET auto_eval = ?, answer_index = ?, question = ? WHERE mod_id = ?"
        db_form = [auto_eval, answer_index, question, mod_id]
        c.execute(q, db_form)
        
def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['deck_id'], keys = ['-d', '--deck-id'], valency = 1, positional = True)
    p.add_pattern(write_to = ['mod_id'], keys = ['-m', '--mod-id'], valency = 1, positional = True)
    p.add_pattern(write_to = ['answer_index'], keys = ['-i', '--answer-index'], valency = 1, positional = True, func = int)
    p.add_pattern(write_to = ['question'], keys = ['-q', '--question'], valency = 1, positional = True)
    p.add_pattern(set_to = {"auto_eval" : 0}, keys = ['-e', '--manual-evaluation'], valency = 0)
    p.defaults = types.SimpleNamespace(deck_id = None, mod_id = None, answer_index = None, question = None, auto_eval = 1)
    r = p.parse()
    return r

if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath = 'decks/' + r.deck_id[0] + '.db'
    mod_id = r.mod_id[0]
    answer_index = r.answer_index[0]
    question = r.question[0]
    auto_eval = r.auto_eval
    update_mod(dbpath, mod_id, answer_index, question, auto_eval)
