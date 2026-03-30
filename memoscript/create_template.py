#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import sqlite3
import sys
import types
import argparse
import json

from common import is_db_exist, is_field_exist, validate_name

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

def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest = "deck_id", type = is_db_exist)
    parser.add_argument(dest ='template_id', type = validate_name)
    parser.add_argument(dest = 'answer_field')
    parser.add_argument(dest = 'question_forms', nargs = '+')
    parser.add_argument('-e', '--manual-evaluation', action = 'store_true')
    return parser.parse_args()

if __name__ == '__main__':
    args = handle_args()
    auto_grade = 1
    if args.manual_evaluation == True:
        auto_grade = 0
    dbpath = args.deck_id
    template_id = args.template_id
    answer_field = args.answer_field
    question_forms = args.question_forms
    is_field_exist(dbpath, answer_field)
    current_date = datetime.date.today().toordinal()
    daily_stats_update(dbpath, template_id)
    add_daily_stats_record(dbpath, template_id)
    add_template_record(dbpath, template_id, auto_grade, answer_field, question_forms)

