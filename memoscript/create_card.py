#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types
import json
import argparse

from common import get_field_count, is_db_exist


def add_deck_record(dbpath, fields):
    maximum_count = get_field_count(dbpath)
    actual_count = len(fields)
    dif = maximum_count - actual_count
    if dif < 0:
        raise Exception(f'Too much arguments! Maximum is {maximum_count}, {actual_count} given')
    fields += [""] * dif
    with sqlite3.connect(dbpath) as c:
        q = "INSERT INTO deck(card_id, fields_json) VALUES(?, ?)"
        db_form = [None, json.dumps(fields, ensure_ascii=False)]
        c.execute(q, db_form)

def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest = "deck_id", type = is_db_exist)
    parser.add_argument(dest = 'fields', nargs = '+')
    return parser.parse_args()

if __name__ == '__main__':
    args = handle_args()
    dbpath = args.deck_id
    fields = args.fields
    add_deck_record(dbpath, fields)
    
