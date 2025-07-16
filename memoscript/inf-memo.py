#!/usr/bin/env python
# -*- coding: utf-8 -*-

import readline
import datetime
import random
import sqlite3
import sys
import time
import os
import types
import re

import vyhuhol
from memo import get_input, ctrl_l

def get_id_list(infinite_ids):
    l = []
    for idd in infinite_ids:
        l += ranger(idd)
    return l

def ranger(s):
    l = []
    if re.fullmatch(r"\d+", s) is not None:
        l = [int(s)]
    if re.fullmatch(r"\d+-\d+", s) is not None:
        ss = s.split('-')
        n1 = int(ss[0])
        n2 = int(ss[1])
        l = list(range(n1, n2 + 1))
    if not(l):
        print(f"'{s}' is not correct option")
        sys.exit(0)
    return l

def get_dict_infinite_mod(ifinite_id_list):
    with sqlite3.connect(dbpath) as c:
        dictionary = dict()
        if ifinite_id_list:
            for idd in ifinite_id_list:
                q = f"SELECT * FROM deck WHERE id = ?"
                db_form = [idd]
                i = c.execute(q, db_form)
                container = next(i)
                card_id = container[0]
                fields = container
                dictionary[card_id] = fields
        else:
            q = "SELECT * FROM deck"
            i = c.execute(q)
            for container in i:
                card_id = container[0]
                fields = container
                dictionary[card_id] = fields
    return dictionary

def proc_infinite_mod(dictionary):
    with sqlite3.connect(dbpath) as c:
        q = f"SELECT * FROM qa WHERE mod_id = ?"
        db_form = [mod]
        i = c.execute(q, db_form)
        mod_id, auto_eval, answer_index, question = next(i)
    print(f"{mod_id=}, {auto_eval=}, {answer_index=}, {question=}")
    if dictionary:
        while True:
            card_id = random.choice(list(dictionary))
            fields = dictionary[card_id]
            string = question.format(*fields)
            answer = fields[answer_index]
            get_input('\nНажмите Enter чтобы продолжить...')
            ctrl_l()
            start_time = time.time()
            guess = get_input(string)
            end_time = time.time()
            delay = end_time - start_time
            if auto_eval:
                print(f"delay = {delay:0.2f}")
                if guess.lower() == answer.lower():
                    print(f"{start_green}Ты молодец!{start_normal}")
                else:
                    print(f"{start_red}Неправильно!{start_normal} Правильный ответ {start_blue}{answer}{start_normal}")
            else:
                print(f"Правильный ответ {answer}")
    print("колода пуста")

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['name'], keys = ['-n', '--name'], valency = 1, positional = True)
    p.add_pattern(write_to = ['mod_id'], keys = ['-m', '--mod-id'], valency = 1, positional = True)
    p.add_pattern(write_to = ['infinite_ids'], keys = ['-i', '--infinite'], valency = '*', positional = True)
    p.defaults = types.SimpleNamespace(name = None, mod_id = None)
    r = p.parse()
    return r

start_red = "\033[91m"
start_green = "\033[92m"
start_blue = "\033[94m"
start_normal = "\033[39m"
os.chdir(os.path.dirname(__file__))
current_date = datetime.date.today().toordinal()
if __name__ == '__main__':
    print(f"current_date = {current_date}")
    r = handle_args(sys.argv)
    dbpath = 'decks/' + r.name[0] + '.db'
    mod = r.mod_id[0]
    infinite_ids = r.infinite_ids
    ifinite_id_list = get_id_list(infinite_ids)
    dictionary = get_dict_infinite_mod(ifinite_id_list)
    proc_infinite_mod(dictionary)