#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types
import json
import argparse

from memo import is_db_exist

def get_field_count(dbpath):
    with sqlite3.connect(dbpath) as c:
        i = c.execute("SELECT COUNT(*) FROM deck_fields")
        count, = next(i)
        return count

def update_deck_record(dbpath, fields):
    with sqlite3.connect(dbpath) as c:
        card_id = int(fields[0])
        new_fields = fields[1:]
        expected_count = get_field_count(dbpath)
        if len(new_fields) != expected_count:
            raise ValueError(f"Expected {expected_count} fields, got {len(new_fields)}")
        q = "UPDATE deck SET fields_json = ? WHERE card_id = ?"
        db_form = [json.dumps(new_fields, ensure_ascii=False), card_id]
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
    update_deck_record(dbpath, fields)
    
