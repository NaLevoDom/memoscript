#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types
import re

import vyhuhol
from memo import is_db_exist, get_id_list, ranger

def delete_deck_record(dbpath, card_id):
    with sqlite3.connect(dbpath) as c:
        q = "DELETE FROM deck WHERE card_id = ?"
        db_form = [card_id]
        c.execute(q, db_form)

def delete_schedule_records(dbpath, card_id):
    with sqlite3.connect(dbpath) as c:
        q = "DELETE FROM schedule WHERE card_id = ?"
        db_form = [card_id]
        c.execute(q, db_form)

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['deck_id'], keys = ['-d', '--deck-id'], valency = 1, positional = True, func = is_db_exist)
    p.add_pattern(write_to = ['card_id'], keys = ['-c', '--card-id'], valency = '+', positional = True)
    p.defaults = types.SimpleNamespace(deck_id = None, card_id = None)
    r = p.parse()
    return r

if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath = r.deck_id[0]
    card_id_raw_list = r.card_id
    card_id_list = get_id_list(card_id_raw_list)
    for card_id in card_id_list:
        delete_deck_record(dbpath, card_id)
        delete_schedule_records(dbpath, card_id)
