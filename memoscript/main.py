#!/usr/bin/env python
# -*- coding: utf-8 -*-

import readline
import datetime
import random
import sqlite3
import sys
import math
import time
import os
import types

import vyhuhol

def ctrl_l():
    print('\n' * (os.get_terminal_size().lines - 1) + "\033[H\033[J", end = '')

def get_input(text):
    try:
        return input(text)
    except EOFError:
        print("\nПока!")
        sys.exit()

def get_auto_s(delay, answer): # это всё ещё бред, но лучше чем было
    k = math.sqrt(len(answer))
    print(f"{2*k:0.2f} {4*k:0.2f} {6*k:0.2f}")
    if delay <= k * 2:
        return 4
    if delay <= k * 4:
        return 3
    if delay <= k * 6:
        return 2
    return 1

def get_manual_s():
        while True:
            try:
                s = int(get_input('Оцени (1-4)?: '))
            except ValueError:
                pass
            else:
                if 1 <= s <= 4:
                    return s
            print("Ещё раз. ", end = '')

def get_delta(step, s, delta, old_delta):
    if delta == 0:
        delta = 1
    if old_delta == 0:
        old_delta = 1
    if step == 2 and s == 3: # чтобы при инициализации стандартный срок был день а не 2
        return 1 # это уродливый адхок, но что поделать
    d = {2 : 0.5, 3 : 2, 4 : 4}
    new_k = d[s]
    new_delta = math.ceil(new_k * (5 * delta + old_delta) / 6)
    part = new_delta // 12
    new_delta += random.randint(-part, part)
    return new_delta

def handle_new(n, c):
    q = "SELECT * FROM deck"
    i = c.execute(q)
    counter = 0
    for container in i:
        if counter >= n: # n ведь отрицательный может быть, поэтому >= а не просто ==
            break
        idd = container[0]
        fields = container
        q = f"SELECT * FROM mod_{mod} WHERE card_id = '{idd}'"
        ii = c.execute(q)
        try:
            idd, delta, old_delta, date = next(ii)
            # print(f"fields = {fields}, date = {date} Есть старая карточка.")
        except StopIteration:
            print(f"fields = {fields} Есть НОВАЯ карточка. ЕЁ ДОКИДЫВАЕЕЕМ ЫЫЫАоаоа")
            db_form = [idd, 0, 0, current_date]
            q = f"INSERT INTO mod_{mod} VALUES(?, ?, ?, ?)"
            c.execute(q, db_form)
            counter += 1

def get_dict_infinite_mod():
    dictionary = dict()
    with sqlite3.connect(dbpath) as c:
        q = "SELECT * FROM deck"
        i = c.execute(q)
        for container in i:
            card_id = container[0]
            fields = container
            dictionary[card_id] = fields
    return dictionary
    
def proc_infinite_mod():
    with sqlite3.connect(dbpath) as c:
        q = f"SELECT * FROM qa WHERE mod_id = {mod}"
        i = c.execute(q)
        mod_id, auto_eval, answer_index, question = next(i)
    print(f"mod_id = {mod_id}, auto_eval = {auto_eval}, answer_index = {answer_index}, question = {question}")
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

def get_dict():
    dictionary = dict()
    init_list = []
    next_time = 0
    with sqlite3.connect(dbpath) as c:
        q = f"SELECT * FROM taskperday WHERE mod_id = {mod}"
        i = c.execute(q)
        try:
            idd, day, new, total = next(i)
        except StopIteration:
            print(f"There's no '{mod}' mod in this deck")
            sys.exit(1)
        old_new = new
        old_total = total
        print(f"В таскпердее было id = {idd}, day = {day}, new = {new}, total = {total}")
        if current_date != day:
            q = f"UPDATE taskperday SET day = {current_date}, new = 0, total = 0 WHERE mod_id = {mod}"
            c.execute(q)
            new = 0
            total = 0
            old_new = new
            old_total = total
            print(f"Так как дата устаревшая обнуляем счётчики.")
        q = f"SELECT * FROM mod_{mod} WHERE delta = 0 and old_delta = 0"
        i = c.execute(q)
        for card_id, delta, old_delta, element_date in i:
            if current_date < element_date or total >= total_limit:
                break
            if new == new_limit:
                break
            total += 1
            new += 1
        # print(init_list)
        # print(new_limit - new)
        handle_new(new_limit - new, c)
        total = old_total
        new = old_new
        # ещё раз то же самое
        q = f"SELECT * FROM mod_{mod} WHERE delta = 0 and old_delta = 0"
        i = c.execute(q)
        for card_id, delta, old_delta, element_date in i: # накидываю новых что есть уже моде.
            if current_date < element_date or total >= total_limit:
                break
            if new == new_limit:
                break
            qq = f"SELECT * FROM deck WHERE id = '{card_id}'"
            ii = c.execute(qq)
            fields = next(ii)
            step = 1 
            total += 1
            new += 1
            init_list.append([next_time, card_id, fields, delta, old_delta, element_date, step])
        # print(init_list)
        q = f"SELECT * FROM mod_{mod} WHERE delta != 0 or old_delta != 0 ORDER BY date ASC"
        i = c.execute(q)
        for card_id, delta, old_delta, element_date in i:
            if current_date < element_date or total >= total_limit:
                break
            qq = f"SELECT * FROM deck WHERE id = '{card_id}'"
            ii = c.execute(qq)
            # fields = next(ii)[1:]
            fields = next(ii) # ###
            step = 3
            total += 1
            dictionary[card_id] = [fields ,delta, old_delta, element_date, step]
        # print(init_list)
    print(f"Докидываем {new - old_new} новых, а в целом {total - old_total} карточек.")
    random.shuffle(init_list)
    return dictionary, init_list

def write_db(mod, step, new_delta, delta, next_date, card_id):
    with sqlite3.connect(dbpath) as c:
        q = f"SELECT * FROM taskperday WHERE mod_id = {mod}"
        i = c.execute(q)
        idd, day, new, total = next(i)
        if step < 3: # пахнет ошибкой... ### а что если степ был 3 а стал 1 или 2?
            q = f"UPDATE taskperday SET new = {new + 1}, total = {total + 1} WHERE mod_id = {mod}"
        else:
            q = f"UPDATE taskperday SET total = {total + 1} WHERE mod_id = {mod}"
        c.execute(q)
        q = f"UPDATE mod_{mod} SET delta = {new_delta}, old_delta = {delta}, date = {next_date} WHERE card_id = '{card_id}'"
        c.execute(q)

def proc():
    with sqlite3.connect(dbpath) as c:
        q = f"SELECT * FROM qa WHERE mod_id = {mod}"
        i = c.execute(q)
        mod_id, auto_eval, answer_index, question = next(i)
    while True:
        if init_list:
            init_list.sort(key = lambda l: l[0])
            card_time = init_list[0][0]
            current_time = time.time()
            if card_time <= current_time: # созрела карточка
                # print("\nягодка созрела")
                next_time, card_id, fields, delta, old_delta, element_date, step = init_list.pop(0)
            elif dictionary:
                # print("\nягодка не созрела")
                card_id = random.choice(list(dictionary))
                fields, delta, old_delta, element_date, step = dictionary[card_id]
            else:
                for card in init_list: # всё остальное откладывается на следующий день
                    next_time, card_id, fields ,delta, old_delta, element_date, step = card
                    print("\nперенос оставшегося инита на следующий день")
                    print(f"fileds = {fields}")
                    write_db(mod, step, delta, old_delta, current_date + 1, card_id)
                break
        elif dictionary:
            card_id = random.choice(list(dictionary))
            fields, delta, old_delta, element_date, step = dictionary[card_id]
            # print("\nЖив только dictinary, едим что есть")
        else:
            break
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
                s = get_auto_s(delay, answer)
            else:
                print(f"{start_red}Неправильно!{start_normal} Правильный ответ {start_blue}{answer}{start_normal}")
                s = 1
        else:
            print(f"Правильный ответ {answer}")
            s = get_manual_s()
        if step == 3:
            del dictionary[card_id]
        current_time = time.time()
        if step + s < 4:
            print("it goes to init")
            init_list.append([current_time + 1 * 60, card_id, fields, delta, old_delta, element_date, 1])
        elif step + s == 4:
            print("it goes to good")
            init_list.append([current_time + 2 * 60, card_id, fields, delta, old_delta, element_date, 2])
        else: # step + s > 4
            print("let's do the procedure")
            new_delta = get_delta(step, s, delta, old_delta)
            if step != 3 and next_time != 0:
                new_delta = 1
            print(f"new_delta is {new_delta}")
            next_date = current_date + new_delta
            write_db(mod, step, new_delta, delta, next_date, card_id)
    print("Всё изучено!\nПока!")

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['name'], keys = ['-n', '--name'], valency = 1, positional = True)
    p.add_pattern(write_to = ['mod_id'], keys = ['-m', '--mod-id'], valency = 1, positional = True)
    p.add_pattern(set_to = {"infinite" : 1}, keys = ['-i', '--infinite'], valency = 0)
    p.defaults = types.SimpleNamespace(name = None, mod_id = None, infinite = 0)
    r = p.parse()
    return r

if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath = 'decks/' + r.name[0] + '.db'
    mod = r.mod_id[0]
    infinite_mod = r.infinite
    start_red = "\033[91m"
    start_green = "\033[92m"
    start_blue = "\033[94m"
    start_normal = "\033[39m"
    # new_limit = 100
    new_limit = 8
    # total_limit = 100
    total_limit = 24
    current_date = datetime.date.today().toordinal()
    # current_date = 739418
    os.chdir(os.path.dirname(__file__))
    print(f"current_date = {current_date}")
    # print_mod()
    if infinite_mod:
        dictionary = get_dict_infinite_mod()
        proc_infinite_mod()
    else:
        dictionary, init_list = get_dict()
        proc()
    