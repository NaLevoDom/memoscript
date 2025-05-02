#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import readline
from sqlite3 import connect
# 
# 
# q = f"""
# SELECT text, gram, pron, freq, id, mid
# FROM forms
# {where_string}
# ORDER BY mid, num
# """


dbpath = "asd.db"
if __name__ == '__main__':
    with connect(dbpath) as c:
        q = f"SELECT * FROM elements"
        i = c.execute(q)
        elements = list(i)
        number, text = random.choice(elements)
        while True:
            try:
                guess = int(input(
                    f'Напиши порядковый номер элемента <{text}>: '))
            except ValueError:
                guess = None
            except EOFError:
                break
            if guess == number:
                print('Ты молодец!')
                number, text = random.choice(elements)
            else:
                print(f"Неправильно! Правильный ответ {number}")
        print("\nПока!")
    
    
    