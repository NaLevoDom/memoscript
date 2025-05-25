#!/usr/bin/env python
# -*- coding: utf-8 -*-

import readline
import datetime
import random
import sqlite3
import sys
import math

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
        q = "SELECT * FROM elements"
        elem_iterator = c.execute(q)
        for number, text in elem_iterator:
            q = f"SELECT * FROM mod1 WHERE element_id = {number}"
            mod1_iterator = c.execute(q)
            try:
                number, delta, old_delta, date = next(mod1_iterator)
            except StopIteration:
                print(f"number = {number}, text = {text} Есть НОВАЯ карточка, её добавляем.")
                db_form = [number, 0, 0, current_date]
                q = f"INSERT INTO mod1 VALUES(?, ?, ?, ?)"
                c.execute(q, db_form)
            else:
                print(f"number = {number}, text = {text}, date = {date} Есть старая карточка, её НЕ добавляем.")

def get_guess(text):
    try:
        return int(input(
            f'Напиши порядковый номер элемента <{text}>: '))
    except ValueError:
        return None
    except EOFError:
        print("\nПока!")
        sys.exit()

def get_s():
    while True:
        try:
            s = int(input('Насколько просто было (1-4)?: '))
        except ValueError:
            pass
        except EOFError:
            print("\nПока!")
            sys.exit()
        else:
            if 1 <= s <= 4:
                return s
        print("Ещё раз. ", end = '')

def get_dict():
    dictionary = dict()
    with sqlite3.connect(dbpath) as c:
        q = "SELECT * FROM mod1 ORDER BY date ASC"
        i = c.execute(q)
        for element_id, delta, old_delta, element_date in i:
            qq = f"SELECT id, sym FROM elements WHERE id = {element_id}"
            ii = c.execute(qq)
            number, text = next(ii)
            if current_date < element_date:
                break
            if delta ==0 and old_delta == 0: # 0 0 - это первый раз
                step = 1
            else:
                step = 3
            dictionary[element_id] = [number, text, delta, old_delta, element_date, step]
    return dictionary

def proc():
    while dictionary:
        element_id = random.choice(list(dictionary))
        number, text, delta, old_delta, element_date, step = dictionary[element_id]
        print(f"\ndelta = {delta}, old_delta = {old_delta}, element_date = {element_date}, step = {step}")
        guess = get_guess(text)
        if guess == number:
            print("Ты молодец!")
            s = get_s()
        else:
            print(f"Неправильно! Правильный ответ {number}")
            s = 1
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
            print(f"new_delta = {new_delta}")
            print(f"current_date = {current_date}, next_date = {next_date}")
            with sqlite3.connect(dbpath) as c:
                q = f"UPDATE mod1 SET delta = {new_delta}, old_delta = {delta}, date = {next_date} WHERE element_id = {element_id}"
                c.execute(q)
    print("Всё изучено!\nПока!")

if __name__ == '__main__':
    dbpath = "asd.db"
    current_date = datetime.date.today().toordinal()
    current_date = 739408
    auto_eval = True
    print(f"current_date = {current_date}")
    handle_new()
    dictionary = get_dict()
    proc()
    