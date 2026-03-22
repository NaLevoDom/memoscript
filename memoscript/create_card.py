#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types
import json
import argparse

from common import get_field_count, is_db_exist


def add_deck_record(dbpath, fields):
    expected_count = get_field_count(dbpath)
    if len(fields) != expected_count:
        raise ValueError(f"Expected {expected_count} fields, got {len(fields)}")
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
    
