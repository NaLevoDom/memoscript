#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types
import re
import argparse

from common import get_id_list

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

def delete_card(args):
    dbpath = args.deck_id
    card_id_list = get_id_list(args.card_ids)
    for card_id in card_id_list: # n + 1 problem ###
        delete_deck_record(dbpath, card_id)
        delete_schedule_records(dbpath, card_id)
