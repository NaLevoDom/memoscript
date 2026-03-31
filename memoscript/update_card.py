#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types
import json
import argparse

from common import get_field_count

def update_deck_record(dbpath, fields, card_id):
    maximum_count = get_field_count(dbpath)
    actual_count = len(fields)
    dif = maximum_count - actual_count
    if dif < 0:
        raise Exception(f'Too much fields! Maximum is {maximum_count}, {actual_count} given')
    fields += [""] * dif
    with sqlite3.connect(dbpath) as c:
        q = "UPDATE deck SET fields_json = ? WHERE card_id = ?"
        db_form = [json.dumps(fields, ensure_ascii=False), card_id]
        c.execute(q, db_form)

def update_card(args):
    dbpath = args.deck_id
    fields = args.fields
    card_id = args.card_id
    update_deck_record(dbpath, fields) # где card_id лол ###
    