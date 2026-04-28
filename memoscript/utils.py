# -*- coding: utf-8 -*-

import os
import re
import sqlite3
import json
import sys
import datetime
from pathlib import Path
from copy import copy

# is_field_exist function? ###

def validate_name(field_name):
    if re.fullmatch(r'[a-zA-Z0-9_]+', field_name):
        return field_name
    raise ValueError('Имя поля может содержать только латинские буквы, цифры и знак _.')

def validate_deck_name(deck_name):
    if re.fullmatch(r'[a-zA-Z0-9_/]+', deck_name):
        return deck_name
    
def get_db_path(deck_name, check_exist = True):
    p = copy(PATH_TO_DECK)
    path_components = deck_name.split('/')
    path_components[-1] += '.db'
    for c in path_components:
        p /= c
    if check_exist:
        if not os.path.isfile(p):
            raise ValueError('Нет колоды с таким именем!')
    else:
        if not re.fullmatch(r'[a-zA-Z0-9_/]+', deck_name): # ### БАРДАК! надо привести ошибки к одному виду, но сейчас мне лень
            raise ValueError('Имя колоды может содержать только латинские буквы, цифры и знаки _/.')
    return p

def is_template_exist(db_path, template_id):
    with sqlite3.connect(db_path) as c:
        i = c.execute("SELECT * FROM daily_stats WHERE template_id = ?", (template_id,))
        try:
            next(i)
        except StopIteration:
            raise ValueError(f"Нет такого '{template_id}' шаблона в этой колоде!")
    return template_id


def get_id_list(id_ranges):
    id_list = []
    if id_ranges:
        for id_range in id_ranges:
            id_list += ranger(id_range)
    return id_list


def ranger(id_range):
    id_list = []
    if re.fullmatch(r"\d+", id_range) is not None:
        id_list = [int(id_range)]
    if re.fullmatch(r"\d+-\d+", id_range) is not None:
        ss = id_range.split('-')
        n1 = int(ss[0])
        n2 = int(ss[1])
        id_list = list(range(n1, n2 + 1))
    if not id_list:
        raise ValueError(f"'{id_range}' is not correct option")
    return id_list


def is_field_exist(db_path, field_name):
    with sqlite3.connect(db_path) as c:
        i = c.execute("SELECT field_name FROM deck_fields WHERE field_name = ?", (field_name,))
        try:
            next(i)
        except StopIteration:
            raise ValueError(f"Unknown field name: {field_name}")
    return field_name


def get_field_count(db_path):
    with sqlite3.connect(db_path) as c:
        i = c.execute("SELECT COUNT(*) FROM deck_fields")
        count, = next(i)
        return count


def get_field_names(db_path):
    with sqlite3.connect(db_path) as c:
        q = "SELECT field_name FROM deck_fields ORDER BY field_position ASC"
        i = c.execute(q)
        return [row[0] for row in i]

def create_card(deck_id, fields):
    db_path = get_db_path(deck_id)
    maximum_count = get_field_count(db_path)
    actual_count = len(fields)
    dif = maximum_count - actual_count
    if dif < 0:
        raise Exception(f'Too much fields! Maximum is {maximum_count}, {actual_count} given')
    fields += [""] * dif
    with sqlite3.connect(db_path) as c:
        q = "INSERT INTO deck(card_id, fields_json) VALUES(?, ?)"
        db_form = [None, json.dumps(fields, ensure_ascii=False)]
        c.execute(q, db_form)

def update_card(deck_id, fields, card_id):
    db_path = get_db_path(deck_id)
    maximum_count = get_field_count(db_path)
    actual_count = len(fields)
    dif = maximum_count - actual_count
    if dif < 0:
        raise Exception(f'Too much fields! Maximum is {maximum_count}, {actual_count} given')
    fields += [""] * dif
    with sqlite3.connect(db_path) as c:
        q = "UPDATE deck SET fields_json = ? WHERE card_id = ?"
        db_form = [json.dumps(fields, ensure_ascii=False), card_id]
        c.execute(q, db_form)

def create_update_card(deck_id, fields, card_id = None):
    db_path = get_db_path(deck_id)
    maximum_count = get_field_count(db_path)
    actual_count = len(fields)
    dif = maximum_count - actual_count
    if dif < 0:
        raise Exception(f'Too much fields! Maximum is {maximum_count}, {actual_count} given')
    fields += [""] * dif
    with sqlite3.connect(db_path) as c:
        if card_id is not None:
            q = "UPDATE deck SET fields_json = ? WHERE card_id = ?"
            db_form = [json.dumps(fields, ensure_ascii=False), card_id]
        else:
            q = "INSERT INTO deck(card_id, fields_json) VALUES(?, ?)"
            db_form = [None, json.dumps(fields, ensure_ascii=False)]
        c.execute(q, db_form)



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

def create_deck(deck_id, field_names):
    if not os.path.exists('decks'):
        os.makedirs('decks')
    db_path = get_db_path(deck_id, False)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    create_deck_table(db_path)
    create_deck_fields_table(db_path, field_names)
    create_daily_stats_table(db_path)
    create_templates_table(db_path)
    create_schedule_table(db_path)

def daily_stats_update(db_path, template_id):
    with sqlite3.connect(db_path) as c:
        q = "UPDATE daily_stats SET stats_date = ?, new_count = 0, total_count = 0 WHERE template_id = ?"
        db_form = [current_date, template_id]
        c.execute(q, db_form)

def add_daily_stats_record(db_path, template_id):
    with sqlite3.connect(db_path) as c:
        q = "INSERT INTO daily_stats VALUES(?, ?, 0, 0)"
        db_form = [template_id, current_date]
        c.execute(q, db_form)

def add_template_record(db_path, template_id, auto_grade, answer_field, question_forms):
    with sqlite3.connect(db_path) as c:
        json_items = json.dumps(question_forms, ensure_ascii = False)
        db_form = [template_id, auto_grade, answer_field, json_items]
        q = "INSERT INTO templates VALUES(?, ?, ?, ?)"
        c.execute(q, db_form)

def create_template(deck_id, template_id, answer_field, question_forms, auto_grade):
    db_path = get_db_path(deck_id)
    template_id = validate_name(template_id)
    is_field_exist(db_path, answer_field)
    daily_stats_update(db_path, template_id)
    add_daily_stats_record(db_path, template_id)
    add_template_record(db_path, template_id, auto_grade, answer_field, question_forms)

def delete_deck_record(db_path, card_id):
    with sqlite3.connect(db_path) as c:
        q = "DELETE FROM deck WHERE card_id = ?"
        db_form = [card_id]
        c.execute(q, db_form)

def delete_schedule_records(db_path, card_id):
    with sqlite3.connect(db_path) as c:
        q = "DELETE FROM schedule WHERE card_id = ?"
        db_form = [card_id]
        c.execute(q, db_form)

def delete_card(deck_id, card_ids):
    db_path = get_db_path(deck_id)
    card_id_list = get_id_list(card_ids)
    for card_id in card_id_list: # n + 1 problem ###
        delete_deck_record(db_path, card_id)
        delete_schedule_records(db_path, card_id)

def drop_template(db_path, template_id):
    with sqlite3.connect(db_path) as c:
        q = "DELETE FROM schedule WHERE template_id = ?"
        db_form = [template_id]
        c.execute(q, db_form)

def delete_daily_stats(db_path, template_id):
    with sqlite3.connect(db_path) as c:
        q = "DELETE FROM daily_stats WHERE template_id = ?"
        db_form = [template_id]
        c.execute(q, db_form)

def delete_template(deck_id, template_id):
    db_path = get_db_path(deck_id)
    drop_template(db_path, template_id)
    delete_daily_stats(db_path, template_id)
    with sqlite3.connect(db_path) as c:
        q = "DELETE FROM templates WHERE template_id = ?"
        db_form = [template_id]
        c.execute(q, db_form)
    
def print_deck(db_path):
    with sqlite3.connect(db_path) as c:
        q = "SELECT card_id, fields_json FROM deck ORDER BY card_id ASC"
        i = c.execute(q)
        for card_id, fields_json in i:
            fields = json.loads(fields_json)
            print((card_id, *fields))

def print_template(db_path, template_id):
    with sqlite3.connect(db_path) as c:
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

def get_templates(db_path):
    with sqlite3.connect(db_path) as c:
        q = "SELECT * FROM templates"
        i = c.execute(q)
        l = list(i)
    return l

def show_deck(deck_id):
    db_path = get_db_path(deck_id)
    field_names = get_field_names(db_path)
    print(f"{field_names=}")
    print_deck(db_path)
    templates = get_templates(db_path)
    for template_id, auto_grade, answer_field, question_form in templates:
        print()
        print(f"{template_id=}, {auto_grade=}, {answer_field=}, {question_form=}")
        print_template(db_path, template_id)

def update_template(deck_id, template_id, answer_field, question_forms, auto_grade):
    db_path = get_db_path(deck_id)
    is_field_exist(db_path, answer_field)
    is_template_exist(db_path, template_id)
    with sqlite3.connect(db_path) as c:
        json_items = json.dumps(question_forms, ensure_ascii = False)
        q = "UPDATE templates SET auto_grade = ?, answer_field = ?, question_forms_json = ? WHERE template_id = ?"
        db_form = [auto_grade, answer_field, json_items, template_id]
        c.execute(q, db_form)
    
current_date = datetime.date.today().toordinal()
PATH_TO_DECK = Path('decks')
