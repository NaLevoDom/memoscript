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
import re

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

def get_auto_s(delay, answer):
    l = len(answer)
    # t = delay - 0.8 - 0.16 * l
    t = delay - 1 - l / 4
    print(f"{t=:0.2f}")
    if t < 3:
        return 4
    if t < 6:
        return 3
    if t < 9:
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

def get_delta(delta, old_delta, counter, attempts):
    if delta == 0:
        delta = 1
    if old_delta == 0:
        old_delta = 1
    new_delta = int(counter * (5 * delta + old_delta) / (3 * attempts))
    part = new_delta // 12
    new_delta += random.randint(-part, part)
    if new_delta < 1:
        new_delta = 1
    return new_delta

def get_dict_infinite_mod(ifinite_id_list):
    with sqlite3.connect(dbpath) as c:
        dictionary = dict()
        if ifinite_id_list:
            for idd in ifinite_id_list:
                q = f"SELECT * FROM deck WHERE id = {idd}"
                i = c.execute(q)
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
        q = f"SELECT * FROM qa WHERE mod_id = {mod}"
        i = c.execute(q)
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

def write_db(mod, new_delta, delta, old_delta, next_date, card_id):
    with sqlite3.connect(dbpath) as c:
        q = f"SELECT * FROM taskperday WHERE mod_id = {mod}"
        i = c.execute(q)
        idd, day, new, total = next(i)
        if delta + old_delta == 0:
            q = f"UPDATE taskperday SET new = {new + 1}, total = {total + 1} WHERE mod_id = {mod}"
            print("инит пошел под запись")
        else:
            q = f"UPDATE taskperday SET total = {total + 1} WHERE mod_id = {mod}"
            print("репит пошел под запись")
        c.execute(q)
        q = f"UPDATE mod_{mod} SET delta = {new_delta}, old_delta = {delta}, date = {next_date} WHERE card_id = '{card_id}'"
        c.execute(q)

def handle_new(n, c):
    print(f"В расписание мода можем докинуть {n} инитов")
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
            print(f"fields = {fields} Есть НОВАЯ карточка")
            db_form = [idd, 0, 0, current_date]
            q = f"INSERT INTO mod_{mod} VALUES(?, ?, ?, ?)"
            c.execute(q, db_form)
            counter += 1
    print(f"Докидываем {counter} инитов")

def get_limit(delta, old_delta):
    summ = delta + old_delta
    if summ <= 3:
        return 5 - summ
    return 1

def get_list():
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
        print(f"В таскпердее было id={idd}, {day=}, {new=}, {total=}")
        if current_date != day:
            q = f"UPDATE taskperday SET day = {current_date}, new = 0, total = 0 WHERE mod_id = {mod}"
            c.execute(q)
            new = 0
            total = 0
            old_new = new
            old_total = total
            print(f"Так как дата устаревшая обнуляем счётчики.")
        # q = f"SELECT * FROM mod_{mod} WHERE delta = 0 and old_delta = 0 ORDER BY date ASC"
        q = f"SELECT * FROM mod_{mod} WHERE delta + old_delta = 0 ORDER BY date ASC"
        i = c.execute(q)
        for card_id, delta, old_delta, element_date in i:
            if  total >= total_limit:
                break
            if current_date < element_date:
                break
            if new == new_limit:
                break
            total += 1
            new += 1
        handle_new(new_limit - new, c)
        total = old_total
        new = old_new
        print("Насыпаем инитов из мода")
        i = c.execute(q)
        for card_id, delta, old_delta, element_date in i: # накидываю новых что есть уже моде.
            if total >= total_limit:
                print("Сработал первый брейк")
                break
            if current_date < element_date:
                print("Сработал второй брейк")
                print(f"{current_date=}, {element_date=}")
                break
            if new == new_limit:
                print("Сработал третий брейк")
                break
            qq = f"SELECT * FROM deck WHERE id = '{card_id}'"
            ii = c.execute(qq)
            fields = next(ii)
            attempts = 0
            counter = 0
            limit = get_limit(delta, old_delta)
            total += 1
            new += 1
            container = [next_time, card_id, fields, delta, old_delta, element_date, attempts, counter, limit]
            init_list.append(container)
            print(container)
        print("Насыпаем репитов из мода")
        q = f"SELECT * FROM mod_{mod} WHERE delta + old_delta > 0 ORDER BY date ASC"
        i = c.execute(q)
        for card_id, delta, old_delta, element_date in i:
            if current_date < element_date or total >= total_limit:
                break
            qq = f"SELECT * FROM deck WHERE id = '{card_id}'"
            ii = c.execute(qq)
            fields = next(ii)
            attempts = 0
            counter = 0
            limit = get_limit(delta, old_delta)
            total += 1
            next_time = float('+inf')
            container = [next_time, card_id, fields, delta, old_delta, element_date, attempts, counter, limit]
            init_list.append(container)
            print(container)
        # print(init_list)
    print(f"Докидываем {new - old_new} новых, а в целом {total - old_total} карточек.")
    random.shuffle(init_list)
    return init_list

def proc(init_list):
    with sqlite3.connect(dbpath) as c:
        q = f"SELECT * FROM qa WHERE mod_id = {mod}"
        i = c.execute(q)
        mod_id, auto_eval, answer_index, question = next(i)
    while init_list:
        init_list.sort(key = lambda l: l[0])
        current_time = time.time()
        if init_list[0][0] <= current_time: # созрела карточка
            # print("\nягодка созрела")
            next_time, card_id, fields, delta, old_delta, element_date, attempts, counter, limit = init_list.pop(0)
        elif init_list[-1][0] == float('+inf'):
            # print("\nберём репит в работу")
            next_time, card_id, fields, delta, old_delta, element_date, attempts, counter, limit = init_list.pop()
        else:
            # print('\nберём в работу ближайшую к зрелости')
            next_time, card_id, fields, delta, old_delta, element_date, attempts, counter, limit = init_list.pop(0)
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
        current_time = time.time()
        attempts += 1
        next_time = current_time + s * 30
        if s == 1:
            print("s = 1, счётчик - 2.5")
            counter -= 2.5
            if counter < 0:
                counter = 0
        elif s == 2:
            print("s = 2, do nothing")
        elif s == 3:
            print("s = 3, счётчик + 1")
            counter += 1
        elif s == 4:
            print("s = 4, счётчик + 1.5")
            counter += 1.5
        if counter >= limit:
            print("let's do the procedure")
            new_delta = get_delta(delta, old_delta, counter, attempts)
            print(f"{new_delta=}")
            next_date = current_date + new_delta
            write_db(mod, new_delta, delta, old_delta, next_date, card_id)
        else:
            init_list.append([next_time, card_id, fields, delta, old_delta, element_date, attempts, counter, limit])
        # print(f"attempts = {attempts}, counter = {counter}, limit = {limit}")
        print(f"{attempts=}, {counter=}, {limit=}")
    print("Всё изучено!\nПока!")

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

def get_id_list(infinite_ids):
    l = []
    for idd in infinite_ids:
        l += ranger(idd)
    return l

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['name'], keys = ['-n', '--name'], valency = 1, positional = True)
    p.add_pattern(write_to = ['mod_id'], keys = ['-m', '--mod-id'], valency = 1, positional = True)
    p.add_pattern(set_to = {"is_infinite" : 1}, write_to = ['infinite_ids'], keys = ['-i', '--infinite'], valency = '*')
    p.defaults = types.SimpleNamespace(name = None, mod_id = None, is_infinite = 0)
    r = p.parse()
    return r

if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath = 'decks/' + r.name[0] + '.db'
    mod = r.mod_id[0]
    infinite_mod = r.is_infinite
    infinite_ids = r.infinite_ids
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
        ifinite_id_list = get_id_list(infinite_ids)
        dictionary = get_dict_infinite_mod(ifinite_id_list)
        proc_infinite_mod(dictionary)
    else:
        init_list = get_list()
        proc(init_list)
    