# -*- coding: utf-8 -*-
"""Общие утилиты для модулей memoscript."""

import os
import re
import sqlite3
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
            print('Нет колоды с таким именем!')
            exit(1)
    else:
        if not re.fullmatch(r'[a-zA-Z0-9_/]+', deck_name): # ### БАРДАК! надо привести ошибки к одному виду, но сейчас мне лень
            raise ValueError('Имя колоды может содержать только латинские буквы, цифры и знаки _/.')
    return p

def is_template_exist(dbpath, template_id):
    with sqlite3.connect(dbpath) as c:
        i = c.execute("SELECT * FROM daily_stats WHERE template_id = ?", (template_id,))
        try:
            next(i)
        except StopIteration:
            print(f"There's no '{template_id}' template in this deck")
            sys.exit(1)
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
        print(f"'{id_range}' is not correct option")
        sys.exit(1)
    return id_list


def is_field_exist(dbpath, field_name):
    with sqlite3.connect(dbpath) as c:
        i = c.execute("SELECT field_name FROM deck_fields WHERE field_name = ?", (field_name,))
        try:
            next(i)
        except StopIteration:
            raise ValueError(f"Unknown field name: {field_name}")
    return field_name


def get_field_count(dbpath):
    with sqlite3.connect(dbpath) as c:
        i = c.execute("SELECT COUNT(*) FROM deck_fields")
        count, = next(i)
        return count


def get_field_names(dbpath):
    with sqlite3.connect(dbpath) as c:
        q = "SELECT field_name FROM deck_fields ORDER BY field_position ASC"
        i = c.execute(q)
        return [row[0] for row in i]

current_date = datetime.date.today().toordinal()
PATH_TO_DECK = Path('decks')
