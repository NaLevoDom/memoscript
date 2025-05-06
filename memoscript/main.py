#!/usr/bin/env python
# -*- coding: utf-8 -*-

import readline
import datetime
from sqlite3 import connect
import sys

"""
Текущие проблемы и задачи:
Нет никакой рандомизированности, я иду строго от водорода до аргона.
Дельта никак не участвует в расчётах
Дельт в таблице будет мб даже две
Добавить режим обуения

"""

def today():
    # return 900000
    return datetime.date.today().toordinal()

def preproc(): # РАБОТАЕТ!!!
    with connect(dbpath) as c:
        q = "SELECT * FROM elements"
        elem_iterator = c.execute(q)
        for number, text in elem_iterator:
            # print(f"number = {number}, text = {text}")
            q = f"SELECT * FROM mod1 WHERE element_id = {number}"
            mod1_iterator = c.execute(q)
            try:
                nnumber, ttext, time = next(mod1_iterator)
            except StopIteration: # это новая карточка, надо добавить в мод.
                print(f"number = {number}, text = {text} Есть НОВАЯ карточка, её добавляем.")
                d = int(today())
                db_form = [number, 0, d]
                q = f"INSERT INTO mod1 VALUES(?, ?, ?)"
                c.execute(q, db_form)
            else:
                print(f"number = {number}, text = {text}, time = {time} Есть старая карточка, её НЕ добавляем.")

def proc():
    while True:
        with connect(dbpath) as c:
            q = "SELECT element_id, counter, time FROM mod1 ORDER BY time ASC"
            i = c.execute(q)
            element_id, counter, elemenet_time = next(i)
            current_date = int(today())
            if current_date < elemenet_time: 
                print("Всё отдрочено!") # Текущая карточка уже отдрочена, а отсортированно всё так что значит что отдрочены все
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
                
                delta = 2 ** (s - 2)
                print(f"delta = {delta}")
                
                current_date = int(today())
                next_date = current_date + delta
                
                print(f"current_date = {current_date}, next_date = {next_date}")
                q = f"UPDATE mod1 SET counter = {counter + 1}, time = {next_date} WHERE element_id = {element_id}"
                c.execute(q)
                # Перезаписать ту хню и время на 10 минут, каунтер +1 (пока в нём смыслу нет, просто на будущее)
            else:
                print(f"Неправильно! Правильный ответ {number}")
                # впринципе не надо пока трогать, позднее можно будет перезаписать каунтер мб
                # можно время апать на пару минут


dbpath = "asd.db"
if __name__ == '__main__':
    preproc()
    proc()
    