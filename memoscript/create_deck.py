#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types
import re
import os
import argparse

def validate_new_name(name):
    if re.fullmatch(r'[a-zA-Z0-9_]+', name):
        return name
    raise ValueError('Имя может содержать только латинские буквы, цифры и знак _.')

def get_db_path(name): # по хорошему путь к каталогу с колодами не должен быть захардкожен, потом изменю
    if re.fullmatch(r'[a-zA-Z0-9_]+', name):
        return 'decks/' + name + '.db'
    raise ValueError('Имя может содержать только латинские буквы, цифры и знак _.')

def create_deck_table(dbpath):
    with sqlite3.connect(dbpath) as c:
        q = "CREATE TABLE deck(card_id INTEGER PRIMARY KEY, fields_json TEXT NOT NULL);"
        c.execute(q)

def create_deck_fields_table(dbpath, field_names):
    with sqlite3.connect(dbpath) as c:
        q = """CREATE TABLE deck_fields(
        field_position INT PRIMARY KEY,
        field_name TEXT UNIQUE);
        """
        c.execute(q)
        rows = [(position, field_name) for position, field_name in enumerate(field_names)]
        c.executemany("INSERT INTO deck_fields VALUES(?, ?)", rows)

def create_daily_stats_table(dbpath):
    with sqlite3.connect(dbpath) as c:
        q = """CREATE TABLE daily_stats(
        template_id TEXT PRIMARY KEY,
        stats_date INT,
        new_count INT,
        total_count INT);
        """
        c.execute(q)

def create_templates_table(dbpath):
    with sqlite3.connect(dbpath) as c:
        q = """CREATE TABLE templates(
        template_id TEXT PRIMARY KEY,
        auto_grade INT,
        answer_field TEXT,
        question_form TEXT);
        """
        c.execute(q)

def create_schedule_table(dbpath):
    with sqlite3.connect(dbpath) as c:
        q = """CREATE TABLE schedule(
        template_id TEXT,
        card_id INT,
        delta INT,
        prev_delta INT,
        due_date INT);
        """
        c.execute(q)

def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest = "deck_id", type = get_db_path)
    parser.add_argument(dest = 'field_names', nargs = '+', type = validate_new_name)
    return parser.parse_args()

if __name__ == '__main__':
    args = handle_args()
    if not os.path.exists('decks'):
        os.makedirs('decks')
    dbpath = args.deck_id
    create_deck_table(dbpath)
    create_deck_fields_table(dbpath, args.field_names)
    create_daily_stats_table(dbpath)
    create_templates_table(dbpath)
    create_schedule_table(dbpath)
