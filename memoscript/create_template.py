#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import sqlite3
import sys
import types

import vyhuhol
from create_deck import validate_new_name
from memo import is_db_exist

def daily_stats_update(dbpath, template_id):
    with sqlite3.connect(dbpath) as c:
        q = "UPDATE daily_stats SET stats_date = ?, new_count = 0, reviewed_count = 0 WHERE template_id = ?"
        db_form = [current_date, template_id]
        c.execute(q, db_form)

def add_daily_stats_record(dbpath, template_id):
    with sqlite3.connect(dbpath) as c:
        q = "INSERT INTO daily_stats VALUES(?, ?, 0, 0)"
        db_form = [template_id, current_date]
        c.execute(q, db_form)

def add_template_record(dbpath, template_id, auto_grade, answer_index, question_form):
    with sqlite3.connect(dbpath) as c:
        db_form = [template_id, auto_grade, answer_index, question_form]
        q = "INSERT INTO templates VALUES(?, ?, ?, ?)"
        c.execute(q, db_form)

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['deck_id'], keys = ['-d', '--deck-id'], valency = 1, positional = True, func = is_db_exist)
    p.add_pattern(write_to = ['template_id'], keys = ['-t', '--template-id'], valency = 1, positional = True, func = validate_new_name)
    p.add_pattern(write_to = ['answer_index'], keys = ['-i', '--answer-index'], valency = 1, positional = True, func = int)
    p.add_pattern(write_to = ['question_form'], keys = ['-q', '--question'], valency = 1, positional = True)
    p.add_pattern(set_to = {"auto_grade" : 0}, keys = ['-e', '--manual-evaluation'], valency = 0)
    p.defaults = types.SimpleNamespace(deck_id = None, template_id = None, answer_index = None, question_form = None, auto_grade = 1)
    r = p.parse()
    return r

if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath = r.deck_id[0]
    template_id = r.template_id[0]
    answer_index = r.answer_index[0]
    question_form = r.question_form[0]
    auto_grade = r.auto_grade
    current_date = datetime.date.today().toordinal()
    daily_stats_update(dbpath, template_id)
    add_daily_stats_record(dbpath, template_id)
    add_template_record(dbpath, template_id, auto_grade, answer_index, question_form)

