#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types
import re
import argparse

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

def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest = "deck_id", type = is_db_exist)
    parser.add_argument('-c', '--card-ids', nargs = '+') # сделать обработку айди как в адхоке
    return parser.parse_args()

if __name__ == '__main__':
    args = handle_args()
    dbpath = args.deck_id
    card_id_raw_list = args.card_ids
    card_id_list = get_id_list(card_id_raw_list)
    for card_id in card_id_list: # n + 1 problem
        delete_deck_record(dbpath, card_id)
        delete_schedule_records(dbpath, card_id)
