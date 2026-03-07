#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types
import re
import os

import vyhuhol

def validate_new_name(name):
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

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['deck_id'], keys = ['-d', '--deck-id'], valency = 1, positional = True, func = validate_new_name)
    p.add_pattern(write_to = ['field_names'], keys = ['-f', '--field-names'], valency = '+', positional = True, func = validate_new_name)
    p.defaults = types.SimpleNamespace(deck_id = None, field_names = None)
    r = p.parse()
    return r

if __name__ == '__main__':
    r = handle_args(sys.argv)
    if not os.path.exists('decks'):
        os.makedirs('decks')
    dbpath, = r.deck_id
    create_deck_table(dbpath)
    create_deck_fields_table(dbpath, r.field_names)
    create_daily_stats_table(dbpath)
    create_templates_table(dbpath)
    create_schedule_table(dbpath)
