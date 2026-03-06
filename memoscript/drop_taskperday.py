#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import sqlite3
import sys
import types

import vyhuhol
from memo import is_db_exist, is_template_exist

def daily_stats_update(dbpath, template_id):
    with sqlite3.connect(dbpath) as c:
        q = "UPDATE daily_stats SET stats_date = ?, new_count = 0, reviewed_count = 0 WHERE template_id = ?"
        db_form = [current_date, template_id]
        c.execute(q, db_form)

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['deck_id'], keys = ['-d', '--deck-id'], valency = 1, positional = True, func = is_db_exist)
    p.add_pattern(write_to = ['template_id'], keys = ['-t', '--template-id'], valency = 1, positional = True)
    p.defaults = types.SimpleNamespace(deck_id = None, template_id = None)
    r = p.parse()
    return r

if __name__ == '__main__':
    current_date = datetime.date.today().toordinal()
    r = handle_args(sys.argv)
    dbpath = r.deck_id[0]
    template_id = r.template_id[0]
    is_template_exist(dbpath, template_id)
    daily_stats_update(dbpath, template_id)
