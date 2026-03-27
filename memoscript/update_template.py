#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types
import argparse

from common import is_db_exist, is_field_exist, is_template_exist

def update_template(dbpath, template_id, answer_field, question_forms, auto_grade):
    with sqlite3.connect(dbpath) as c:
        json_items = json.dumps(question_forms, ensure_ascii = False)
        q = "UPDATE templates SET auto_grade = ?, answer_field = ?, question_forms_json = ? WHERE template_id = ?"
        db_form = [auto_grade, answer_field, json_items, template_id]
        c.execute(q, db_form)
        
def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest = "deck_id", type = is_db_exist)
    parser.add_argument(dest ='template_id')
    parser.add_argument(dest = 'answer_field')
    parser.add_argument(dest = 'question_forms', nargs = '+-')
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
    is_template_exist(dbpath, template_id)
    update_template(dbpath, template_id, answer_field, question_forms, auto_grade)

