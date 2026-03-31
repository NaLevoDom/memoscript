#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

from common import get_db_path

def drop_template(db_path, template_id):
    with sqlite3.connect(db_path) as c:
        q = "DELETE FROM schedule WHERE template_id = ?"
        db_form = [template_id]
        c.execute(q, db_form)

def delete_template(db_path, template_id):
    with sqlite3.connect(db_path) as c:
        q = "DELETE FROM templates WHERE template_id = ?"
        db_form = [template_id]
        c.execute(q, db_form)

def delete_daily_stats(db_path, template_id):
    with sqlite3.connect(db_path) as c:
        q = "DELETE FROM daily_stats WHERE template_id = ?"
        db_form = [template_id]
        c.execute(q, db_form)

def delete_template(args):
    db_path = get_db_path(args.deck_id)
    template_id = args.template_id
    drop_template(db_path, template_id)
    delete_template(db_path, template_id)
    delete_daily_stats(db_path, template_id)
