#!/usr/bin/env python
# -*- coding: utf-8 -*-

import readline
import datetime
import random
from sqlite3 import connect
import sys

"""
Текущие проблемы и задачи:
Дельт должно быть больше, 2 или 3.
Добавить режим первичного заучивания.

"""

def today():
    # return 739381
    return datetime.date.today().toordinal()

def get_delta(s, delta):
    new_delta = (2 ** (s - 2)) * delta
    eighth = new_delta // 8
    new_delta += random.randint(-eighth, eighth)
    return new_delta

def preproc():
    with connect(dbpath) as c:
        q = "SELECT * FROM elements"
        elem_iterator = c.execute(q)
        for number, text in elem_iterator:
            q = f"SELECT * FROM mod1 WHERE element_id = {number}"
            mod1_iterator = c.execute(q)
            try:
                number, delta, date = next(mod1_iterator)
            except StopIteration:
                print(f"number = {number}, text = {text} Есть НОВАЯ карточка, её добавляем.")
                d = today()
                db_form = [number, 1, d]
                q = f"INSERT INTO mod1 VALUES(?, ?, ?)"
                c.execute(q, db_form)
            else:
                print(f"number = {number}, text = {text}, date = {date} Есть старая карточка, её НЕ добавляем.")

def proc():
    while True:
        with connect(dbpath) as c:
            q = "SELECT element_id, delta, date FROM mod1 ORDER BY date ASC"
            i = c.execute(q)
            element_id, delta, elemenet_time = next(i)
            current_date = today()
            if current_date < elemenet_time:
                print("Всё отдрочено!")
                break
            q = f"SELECT id, sym FROM elements WHERE id = {element_id}"
            i = c.execute(q)
            number, text = next(i)
            try:
                guess = int(input(
                    f'Напиши порядковый номер элемента <{text}>: '))
            except ValueError:
                guess = None
            except EOFError:
                print("\nПока!")
                sys.exit()
            if guess == number:
                print("Ты молодец!")
                while True:
                    try:
                        s = int(input('Насколько просто было (2-4)?: '))
                    except ValueError:
                        pass
                    except EOFError:
                        print("\nПока!")
                        sys.exit()
                    else:
                        if 2 <= s <= 4:
                            break
                    print("Ещё раз. ", end = '')
                new_delta = get_delta(s, delta)
                current_date = today()
                next_date = current_date + new_delta
                print(f"new_delta = {new_delta}")
                print(f"current_date = {current_date}, next_date = {next_date}")
                q = f"UPDATE mod1 SET delta = {new_delta}, date = {next_date} WHERE element_id = {element_id}"
                c.execute(q)
            else:
                print(f"Неправильно! Правильный ответ {number}")


dbpath = "asd.db"
if __name__ == '__main__':
    preproc()
    proc()
    