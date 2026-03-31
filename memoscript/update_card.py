#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import json

from common import get_field_count, get_db_path


def update_card(args):
    db_path = get_db_path(args.deck_id)
    maximum_count = get_field_count(db_path)
    actual_count = len(args.fields)
    dif = maximum_count - actual_count
    if dif < 0:
        raise Exception(f'Too much fields! Maximum is {maximum_count}, {actual_count} given')
    args.fields += [""] * dif
    with sqlite3.connect(db_path) as c:
        q = "UPDATE deck SET fields_json = ? WHERE card_id = ?"
        db_form = [json.dumps(args.fields, ensure_ascii=False), args.card_id]
        c.execute(q, db_form)
