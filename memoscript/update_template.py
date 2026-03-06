#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types

import vyhuhol
from memo import is_db_exist, is_template_exist

def update_template(dbpath, template_id, answer_index, question_form, auto_grade):
    with sqlite3.connect(dbpath) as c:
        q = "UPDATE templates SET auto_grade = ?, answer_index = ?, question_form = ? WHERE template_id = ?"
        db_form = [auto_grade, answer_index, question_form, template_id]
        c.execute(q, db_form)
        
def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['deck_id'], keys = ['-d', '--deck-id'], valency = 1, positional = True, func = is_db_exist)
    p.add_pattern(write_to = ['template_id'], keys = ['-t', '--template-id'], valency = 1, positional = True)
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
    is_template_exist(dbpath, template_id)
    update_template(dbpath, template_id, answer_index, question_form, auto_grade)

