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

def get_auto_s(delay):
    if delay <= 3:
        return 4
    if delay <= 6:
        return 3
    if delay <= 9:
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
    # new_k = 2 ** (s - 2) 
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
        elem_iterator = c.execute(q)
        for number, text in elem_iterator:
            q = f"SELECT * FROM {mod} WHERE element_id = {number}"
            mod1_iterator = c.execute(q)
            try:
                number, delta, old_delta, date = next(mod1_iterator)
                print(f"number = {number}, text = {text}, date = {date} Есть старая карточка, её НЕ добавляем.")
            except StopIteration:
                print(f"number = {number}, text = {text} Есть НОВАЯ карточка, её добавляем.")
                db_form = [number, 0, 0, current_date]
                q = f"INSERT INTO {mod} VALUES(?, ?, ?, ?)"
                c.execute(q, db_form)

def get_dict():
    dictionary = dict()
    with sqlite3.connect(dbpath) as c:
        q = f"SELECT * FROM {mod} ORDER BY date ASC"
        i = c.execute(q)
        new_counter = 0 # по идее тут он должен из базы его брать
        total_counter = 0
        for element_id, delta, old_delta, element_date in i:
            qq = f"SELECT id, sym FROM deck WHERE id = {element_id}"
            ii = c.execute(qq)
            number, text = next(ii)
            if current_date < element_date:
                break
            if delta ==0 and old_delta == 0: # 0 0 - это первый раз
                if total_counter < 24:
                    if new_counter < 6:
                        step = 1 
                        total_counter += 1 # а тут он должен обновлять значение в базе
                        new_counter += 1
                    else:
                        continue
                else:
                    break
            else:
                if total_counter < 24:
                    step = 3
                    total_counter += 1
                else:
                    break
            
            
            dictionary[element_id] = [number, text, delta, old_delta, element_date, step]
    print(f"\nToday we got {new_counter} new tasks, and {total_counter} total")
    return dictionary

def proc():
    while dictionary:
        element_id = random.choice(list(dictionary))
        number, text, delta, old_delta, element_date, step = dictionary[element_id]
        if auto_eval:
            get_input('\nНажмите Enter чтобы продолжить...')
        ctrl_l()
        start_time = time.time()
        if mod == "mod1":
            string = f'Напиши порядковый номер элемента <{text}>: '
            answer = number
        elif mod == "mod2":
            string = f'Напиши обозначение элемента №{number}: '
            answer = text
        guess = get_input(string)
        end_time = time.time()
        delay = end_time - start_time
        if auto_eval:
            print(f"delay = {delay:0.2f}")
            if guess == answer:
                print(f"{start_green}Ты молодец!{start_normal}")
                s = get_auto_s(delay)
            else:
                print(f"{start_red}Неправильно!{start_normal} Правильный ответ {start_blue}{answer}{start_normal}")
                s = 1
        else:
            print(f"Правильный ответ {answer}")
            s = get_manual_s()
        if step + s < 4:
            print("it goes to init")
            dictionary[element_id][5] = 1
        elif step + s == 4:
            print("it goes to good")
            dictionary[element_id][5] = 2
        else:
            new_delta = get_delta(step, s, delta, old_delta)
            next_date = current_date + new_delta
            del dictionary[element_id]
            print("let's do the procedure")
            print(f"delta = {delta}, old_delta = {old_delta}, element_date = {element_date}, step = {step}")
            print(f"new_delta = {new_delta}, current_date = {current_date}, next_date = {next_date}")
            with sqlite3.connect(dbpath) as c:
                q = f"UPDATE {mod} SET delta = {new_delta}, old_delta = {delta}, date = {next_date} WHERE element_id = {element_id}"
                c.execute(q)
    print("Всё изучено!\nПока!")

# dbpath = "asd.db"
dbpath = "khjgng.db"
# mod = "mod2"
mod = "mod1"
start_red = "\033[91m"
start_green = "\033[92m"
start_blue = "\033[94m"
start_normal = "\033[39m"
current_date = datetime.date.today().toordinal()
# current_date = 739404
auto_eval = True
if __name__ == '__main__':
    print(f"current_date = {current_date}")
    handle_new()
    dictionary = get_dict()
    proc()
    