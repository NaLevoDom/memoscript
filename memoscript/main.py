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

def handle_new():
    with sqlite3.connect(dbpath) as c:
        q = "SELECT * FROM deck"
        i = c.execute(q)
        for idd, number, text in i:
            q = f"SELECT * FROM mod_{mod} WHERE card_id = '{idd}'"
            ii = c.execute(q)
            try:
                idd, delta, old_delta, date = next(ii)
                print(f"number = {number}, text = {text}, date = {date} Есть старая карточка, её НЕ добавляем.")
            except StopIteration:
                print(f"number = {number}, text = {text} Есть НОВАЯ карточка, её добавляем.")
                db_form = [idd, 0, 0, current_date]
                q = f"INSERT INTO mod_{mod} VALUES(?, ?, ?, ?)"
                c.execute(q, db_form)

def get_dict():
    dictionary = dict()
    with sqlite3.connect(dbpath) as c:
        q = f"SELECT * FROM taskperday WHERE mod_id = {mod}"
        i = c.execute(q)
        idd, day, new, total = next(i)
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
        q = f"SELECT * FROM mod_{mod} ORDER BY date ASC"
        i = c.execute(q)
        for card_id, delta, old_delta, element_date in i:
            qq = f"SELECT * FROM deck WHERE id = '{card_id}'"
            ii = c.execute(qq)
            fields = next(ii)
            fields = fields[1:]
            if current_date < element_date:
                break
            if delta ==0 and old_delta == 0: # 0 0 - это первый раз
                if total < 24:
                    if new < 8:
                        step = 1 
                        total += 1
                        new += 1
                    else:
                        continue
                else:
                    break
            else:
                if total < 24:
                    step = 3
                    total += 1
                else:
                    break
            dictionary[card_id] = [fields ,delta, old_delta, element_date, step]
    print(f"Докидываем {new - old_new} новых, а в целом {total - old_total} карточек.")
    return dictionary

def proc():
    with sqlite3.connect(dbpath) as c:
        q = f"SELECT * FROM qa WHERE mod_id = {mod}"
        i = c.execute(q)
        mod_id, auto_eval, answer_index, question = next(i)
    while dictionary:
        card_id = random.choice(list(dictionary))
        fields, delta, old_delta, element_date, step = dictionary[card_id]
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
            print(answer)
            if guess.lower() == answer.lower():
                print(f"{start_green}Ты молодец!{start_normal}")
                s = get_auto_s(delay, answer)
            else:
                print(f"{start_red}Неправильно!{start_normal} Правильный ответ {start_blue}{answer}{start_normal}")
                s = 1
        else:
            print(f"Правильный ответ {answer}")
            s = get_manual_s()
        if step + s < 4:
            print("it goes to init")
            dictionary[card_id][4] = 1
        elif step + s == 4:
            print("it goes to good")
            dictionary[card_id][4] = 2
        else:
            new_delta = get_delta(step, s, delta, old_delta)
            next_date = current_date + new_delta
            del dictionary[card_id]
            print("let's do the procedure")
            print(f"delta = {delta}, old_delta = {old_delta}, element_date = {element_date}, step = {step}")
            print(f"new_delta = {new_delta}, current_date = {current_date}, next_date = {next_date}")
            with sqlite3.connect(dbpath) as c:
                q = f"SELECT * FROM taskperday WHERE mod_id = {mod}"
                i = c.execute(q)
                idd, day, new, total = next(i)
                if step < 3:
                    q = f"UPDATE taskperday SET new = {new + 1}, total = {total + 1} WHERE mod_id = {mod}"
                else:
                    q = f"UPDATE taskperday SET total = {total + 1} WHERE mod_id = {mod}"
                c.execute(q)
                q = f"UPDATE mod_{mod} SET delta = {new_delta}, old_delta = {delta}, date = {next_date} WHERE card_id = '{card_id}'"
                c.execute(q)
    print("Всё изучено!\nПока!")

# dbpath = "asd.db"
dbpath = "asd2.db"
# dbpath = "asd3.db"
# mod = "2"
mod = "1"
start_red = "\033[91m"
start_green = "\033[92m"
start_blue = "\033[94m"
start_normal = "\033[39m"
current_date = datetime.date.today().toordinal()
# current_date = 739406
if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    print(f"current_date = {current_date}")
    handle_new()
    dictionary = get_dict()
    proc()
    