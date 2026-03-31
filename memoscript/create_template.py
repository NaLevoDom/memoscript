#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types
import argparse
import json

from common import is_field_exist, current_date

def daily_stats_update(dbpath, template_id):
    with sqlite3.connect(dbpath) as c:
        q = "UPDATE daily_stats SET stats_date = ?, new_count = 0, total_count = 0 WHERE template_id = ?"
        db_form = [current_date, template_id]
        c.execute(q, db_form)

def add_daily_stats_record(dbpath, template_id):
    with sqlite3.connect(dbpath) as c:
        q = "INSERT INTO daily_stats VALUES(?, ?, 0, 0)"
        db_form = [template_id, current_date]
        c.execute(q, db_form)

def add_template_record(dbpath, template_id, auto_grade, answer_field, question_forms):
    with sqlite3.connect(dbpath) as c:
        json_items = json.dumps(question_forms, ensure_ascii = False)
        db_form = [template_id, auto_grade, answer_field, json_items]
        q = "INSERT INTO templates VALUES(?, ?, ?, ?)"
        c.execute(q, db_form)

def create_template(args):
    auto_grade = 1
    if args.manual_evaluation == True:
        auto_grade = 0
    dbpath = args.deck_id
    template_id = args.template_id
    answer_field = args.answer_field
    question_forms = args.question_forms
    is_field_exist(dbpath, answer_field)
    daily_stats_update(dbpath, template_id)
    add_daily_stats_record(dbpath, template_id)
    add_template_record(dbpath, template_id, auto_grade, answer_field, question_forms)

