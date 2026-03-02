#!/usr/bin/env python
# -*- coding: utf-8 -*-

import readline
import random
import sqlite3
import sys
import time
import os
import types


import vyhuhol
from memo import get_input, ctrl_l, is_db_exist, is_mod_exist


def get_id_list(infinite_ids):
    l = []
    for card_id in infinite_ids:
        l += ranger(card_id)
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

def get_dict_infinite(dbpath, ifinite_id_list):
    with sqlite3.connect(dbpath) as c:
        dictionary = dict()
        if ifinite_id_list:
            for card_id in ifinite_id_list:
                q = "SELECT * FROM deck WHERE card_id = ?"
                db_form = [card_id]
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

def proc_infinite(dbpath, dictionary, mod_id):
    with sqlite3.connect(dbpath) as c:
        q = "SELECT * FROM qa WHERE mod_id = ?"
        db_form = [mod_id]
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
                print(f"{delay=:0.2f}")
                if guess.lower() == answer.lower():
                    print(f"{start_green}Ты молодец!{start_normal}")
                else:
                    print(f"{start_red}Неправильно!{start_normal} Правильный ответ {start_blue}{answer}{start_normal}")
            else:
                print(f"Правильный ответ {answer}")
    print("колода пуста")

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['deck_id'], keys = ['-d', '--deck-id'], valency = 1, positional = True, func = is_db_exist)
    p.add_pattern(write_to = ['mod_id'], keys = ['-m', '--mod-id'], valency = 1, positional = True)
    p.add_pattern(write_to = ['infinite_ids'], keys = ['-i', '--infinite'], valency = '*', positional = True)
    p.defaults = types.SimpleNamespace(deck_id = None, mod_id = None)
    r = p.parse()
    return r

start_red = "\033[91m"
start_green = "\033[92m"
start_blue = "\033[94m"
start_normal = "\033[39m"
os.chdir(os.path.dirname(__file__))
current_date = datetime.date.today().toordinal()
if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath = r.deck_id[0]
    mod_id = r.mod_id[0]
    is_mod_exist(dbpath, mod_id)
    infinite_ids = r.infinite_ids
    ifinite_id_list = get_id_list(infinite_ids)
    dictionary = get_dict_infinite(dbpath, ifinite_id_list)
    proc_infinite(dbpath, dictionary, mod_id)