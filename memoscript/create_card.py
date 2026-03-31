#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import json

from common import get_field_count, get_db_path


def create_card(args):
    dbpath = get_db_path(args.deck_id)
    maximum_count = get_field_count(dbpath)
    actual_count = len(args.fields)
    dif = maximum_count - actual_count
    if dif < 0:
        raise Exception(f'Too much fields! Maximum is {maximum_count}, {actual_count} given')
    args.fields += [""] * dif
    with sqlite3.connect(dbpath) as c:
        q = "INSERT INTO deck(card_id, fields_json) VALUES(?, ?)"
        db_form = [None, json.dumps(args.fields, ensure_ascii=False)]
        c.execute(q, db_form)
