#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types

import vyhuhol
from memo import is_db_exist

def drop_template(dbpath, template_id):
    with sqlite3.connect(dbpath) as c:
        q = "DELETE FROM schedule WHERE template_id = ?"
        db_form = [template_id]
        c.execute(q, db_form)

def delete_template(dbpath, template_id):
    with sqlite3.connect(dbpath) as c:
        q = "DELETE FROM templates WHERE template_id = ?"
        db_form = [template_id]
        c.execute(q, db_form)

def delete_daily_stats(dbpath, template_id):
    with sqlite3.connect(dbpath) as c:
        q = "DELETE FROM daily_stats WHERE template_id = ?"
        db_form = [template_id]
        c.execute(q, db_form)

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['deck_id'], keys = ['-d', '--deck-id'], valency = 1, positional = True, func = is_db_exist)
    p.add_pattern(write_to = ['template_id'], keys = ['-t', '--template-id'], valency = 1, positional = True)
    p.defaults = types.SimpleNamespace(deck_id = None, template_id = None)
    r = p.parse()
    return r

if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath, = r.deck_id
    template_id, = r.template_id
    drop_template(dbpath, template_id)
    delete_template(dbpath, template_id)
    delete_daily_stats(dbpath, template_id)

