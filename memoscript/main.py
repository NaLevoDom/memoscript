#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import readline

elements = [['H', 1], ['He', 2], ['Li', 3], ['Be', 4]]

if __name__ == '__main__':
    while True:
        text, number = random.choice(elements)
        try:
            guess = int(input(
                f'Напиши порядковый номер элемента <{text}>: '))
        except ValueError:
            guess = None
        except EOFError:
            break
        if guess == number:
            print('Ты молодец!')
        else:
            print(f"Неправильно! Правильный ответ {number}")
    print("\nПока!")
    