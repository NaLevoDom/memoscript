#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os

from common import get_db_path, current_date, get_db_path, validate_name, validate_deck_name


def create_deck_table(db_path):
    with sqlite3.connect(db_path) as c:
        q = "CREATE TABLE deck(card_id INTEGER PRIMARY KEY, fields_json TEXT NOT NULL);"
        c.execute(q)

def create_deck_fields_table(db_path, field_names):
    with sqlite3.connect(db_path) as c:
        q = """CREATE TABLE deck_fields(
        field_position INT PRIMARY KEY,
        field_name TEXT UNIQUE);
        """
        c.execute(q)
        rows = [(position, validate_name(field_name)) for position, field_name in enumerate(field_names)]
        c.executemany("INSERT INTO deck_fields VALUES(?, ?)", rows)

def create_daily_stats_table(db_path):
    with sqlite3.connect(db_path) as c:
        q = """CREATE TABLE daily_stats(
        template_id TEXT PRIMARY KEY,
        stats_date INT,
        new_count INT,
        total_count INT);
        """
        c.execute(q)

def create_templates_table(db_path):
    with sqlite3.connect(db_path) as c:
        q = """CREATE TABLE templates(
        template_id TEXT PRIMARY KEY,
        auto_grade INT,
        answer_field TEXT,
        question_forms_json TEXT);
        """
        c.execute(q)

def create_schedule_table(db_path):
    with sqlite3.connect(db_path) as c:
        q = """CREATE TABLE schedule(
        template_id TEXT,
        card_id INT,
        delta INT,
        prev_delta INT,
        due_date INT);
        """
        c.execute(q)

def create_deck(args):
    if not os.path.exists('decks'):
        os.makedirs('decks')
    db_path = get_db_path(args.deck_id, False)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    create_deck_table(db_path)
    create_deck_fields_table(db_path, args.field_names)
    create_daily_stats_table(db_path)
    create_templates_table(db_path)
    create_schedule_table(db_path)
