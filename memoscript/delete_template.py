#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types
import argparse

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

def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest = "deck_id", type = is_db_exist)
    parser.add_argument(dest ='template_id')
    return parser.parse_args()

if __name__ == '__main__':
    args = handle_args()
    dbpath = args.deck_id
    template_id = args.template_id
    drop_template(dbpath, template_id)
    delete_template(dbpath, template_id)
    delete_daily_stats(dbpath, template_id)

