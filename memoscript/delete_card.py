#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

from common import get_id_list, get_db_path

def delete_deck_record(db_path, card_id):
    with sqlite3.connect(db_path) as c:
        q = "DELETE FROM deck WHERE card_id = ?"
        db_form = [card_id]
        c.execute(q, db_form)

def delete_schedule_records(db_path, card_id):
    with sqlite3.connect(db_path) as c:
        q = "DELETE FROM schedule WHERE card_id = ?"
        db_form = [card_id]
        c.execute(q, db_form)

def delete_card(args):
    db_path = get_db_path(args.deck_id)
    card_id_list = get_id_list(args.card_ids)
    for card_id in card_id_list: # n + 1 problem ###
        delete_deck_record(db_path, card_id)
        delete_schedule_records(db_path, card_id)
