#!/usr/bin/env python
# -*- coding: utf-8 -*-

import readline
from time import time
from sqlite3 import connect

"""
Текущие проблемы:
Скрипт пока умеет откладывать только на 10 минут.
Нет никакой рандомизированности, я иду строго от водорода до аргона.
Рефактор нужен.
"""

def preproc(): # РАБОТАЕТ!!!
    with connect(dbpath) as c:
        q = "SELECT * FROM elements"
        iterator = c.execute(q)
        for number, text in iterator:
            # print(f"number = {number}, text = {text}")
            q = f"SELECT * FROM mod1 WHERE element_id = {number}"
            iterator = c.execute(q)
            try:
                next(iterator)
            except StopIteration: # это новая карточка, надо добавить в мод.
                print(f"number = {number}, text = {text} Есть НОВАЯ карточка, её добавляем.")
                t = int(time())
                db_form = [number, 0, t]
                q = f"INSERT INTO mod1 VALUES(?, ?, ?)"
                c.execute(q, db_form)
            else:
                print(f"number = {number}, text = {text} Есть старая карточка, её НЕ добавляем.")

def proc():
    with connect(dbpath) as c:
        while True:
            q = "SELECT element_id, counter, time FROM mod1 ORDER BY time ASC"
            i = c.execute(q)
            element_id, counter, elemenet_time = next(i)
            current_time = int(time())
            if current_time < elemenet_time: 
                print("Всё отдрочено!") # Текущая карточка уже отдрочена, а отсортированно всё так что значит что отдрочены все
                break
            q = f"SELECT id, sym FROM elements WHERE id = {element_id}"
            i = c.execute(q)
            number, text = next(i)
            try:
                guess = int(input(
                    f'Напиши порядковый номер элемента <{text}>: ')) # это должно лежать в ДБ?
            except ValueError:
                guess = None
            except EOFError:
                break
            if guess == number:
                print('Ты молодец!')
                current_time = int(time())
                next_time = current_time + 10 * 60 # через 10 мин
                q = f"UPDATE mod1 SET counter = {counter + 1}, time = {next_time} WHERE element_id = {element_id}"
                c.execute(q)
                
                # Перезаписать ту хню и время на 10 минут, каунтер +1 (пока в нём смыслу нет, просто на будущее)
            else:
                print(f"Неправильно! Правильный ответ {number}")
                # впринципе не надо пока трогать, позднее можно будет перезаписать каунтер мб
                # можно время апать на пару минут
        print("Пока!")


dbpath = "asd.db"
if __name__ == '__main__':
    preproc()
    proc()
    