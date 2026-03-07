#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import sqlite3
import sys
import types

import vyhuhol
from create_deck import validate_new_name
from memo import is_db_exist

def is_field_exist(dbpath, field_name):
    with sqlite3.connect(dbpath) as c:
        i = c.execute("SELECT field_name FROM deck_fields WHERE field_name = ?", (field_name,))
        try:
            next(i)
        except StopIteration:
            raise ValueError(f"Unknown field name: {field_name}")
    return field_name

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

def add_template_record(dbpath, template_id, auto_grade, answer_field, question_form):
    with sqlite3.connect(dbpath) as c:
        db_form = [template_id, auto_grade, answer_field, question_form]
        q = "INSERT INTO templates VALUES(?, ?, ?, ?)"
        c.execute(q, db_form)

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['deck_id'], keys = ['-d', '--deck-id'], valency = 1, positional = True, func = is_db_exist)
    p.add_pattern(write_to = ['template_id'], keys = ['-t', '--template-id'], valency = 1, positional = True, func = validate_new_name)
    p.add_pattern(write_to = ['answer_field'], keys = ['-a', '--answer-field'], valency = 1, positional = True)
    p.add_pattern(write_to = ['question_form'], keys = ['-q', '--question-form'], valency = 1, positional = True)
    p.add_pattern(set_to = {"auto_grade" : 0}, keys = ['-e', '--manual-evaluation'], valency = 0)
    p.defaults = types.SimpleNamespace(deck_id = None, template_id = None, answer_field = None, question_form = None, auto_grade = 1)
    r = p.parse()
    return r

if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath = r.deck_id
    template_id, = r.template_id
    answer_field, = r.answer_field
    question_form, = r.question_form
    auto_grade = r.auto_grade
    is_field_exist(dbpath, answer_field)
    current_date = datetime.date.today().toordinal()
    daily_stats_update(dbpath, template_id)
    add_daily_stats_record(dbpath, template_id)
    add_template_record(dbpath, template_id, auto_grade, answer_field, question_form)

