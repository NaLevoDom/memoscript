#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types
import json
import argparse

from common import get_field_names

def print_deck(dbpath):
    with sqlite3.connect(dbpath) as c:
        q = "SELECT card_id, fields_json FROM deck ORDER BY card_id ASC"
        i = c.execute(q)
        for card_id, fields_json in i:
            fields = json.loads(fields_json)
            print((card_id, *fields))

def print_template(dbpath, template_id):
    with sqlite3.connect(dbpath) as c:
        q = """
            SELECT s.card_id, s.delta, s.prev_delta, s.due_date, d.fields_json
            FROM schedule s
            JOIN deck d ON s.card_id = d.card_id
            WHERE s.template_id = ?
            ORDER BY s.due_date ASC
        """
        i = c.execute(q, [template_id])
        for card_id, delta, prev_delta, due_date, fields_json in i:
            fields = (card_id, *json.loads(fields_json))
            print(f"{fields=}, {delta=}, {prev_delta=}, {due_date=}")

def get_templates(dbpath):
    with sqlite3.connect(dbpath) as c:
        q = "SELECT * FROM templates"
        i = c.execute(q)
        l = list(i)
    return l

def show_deck(args):
    dbpath = args.deck_id
    field_names = get_field_names(dbpath)
    print(f"{field_names=}")
    print_deck(dbpath)
    templates = get_templates(dbpath)
    for template_id, auto_grade, answer_field, question_form in templates:
        print()
        print(f"{template_id=}, {auto_grade=}, {answer_field=}, {question_form=}")
        print_template(dbpath, template_id)
