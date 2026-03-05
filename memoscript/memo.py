#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import random
import sqlite3
import sys
import time
import os
import types
import math
import re
if os.name == 'posix':
    import readline
import vyhuhol


def ctrl_l():
    print('\n' * (os.get_terminal_size().lines - 1) + "\033[H\033[J", end='')


def get_input(text):
    try:
        return input(text)
    except EOFError:
        print("\nПока!")
        sys.exit()


def is_db_exist(deck_id):
    dbpath = 'decks/' + deck_id + '.db'
    if os.path.isfile(dbpath):
        return dbpath
    raise ValueError('Нет колоды с таким именем')


def get_auto_grade(delay, answer):
    l = len(answer)
    t = delay - 1 - l / 4
    print(f"{t=:0.2f}")
    if t < 3:
        return 4
    if t < 6:
        return 3
    if t < 9:
        return 2
    return 1


def get_manual_grade():
    while True:
        try:
            s = int(get_input('Оцени (1-4)?: '))
        except ValueError:
            pass
        else:
            if 1 <= s <= 4:
                return s
        print("Ещё раз. ", end='')


def write_db(mod_id, new_delta, next_date, task):
    with sqlite3.connect(dbpath) as c:
        q = "SELECT * FROM taskperday WHERE mod_id = ?"
        db_form = [mod_id]
        i = c.execute(q, db_form)
        mod_id, day, new, total = next(i)
        if task.delta + task.old_delta == 0:
            q = "UPDATE taskperday SET new = ?, total = ? WHERE mod_id = ?"
            db_form = [new + 1, total + 1, mod_id]
            print("инит пошел под запись")
        else:
            q = "UPDATE taskperday SET total = ? WHERE mod_id = ?"
            db_form = [total + 1, mod_id]
            print("репит пошел под запись")
        c.execute(q, db_form)
        q = "UPDATE schedule SET delta = ?, old_delta = ?, schedule_date = ? WHERE card_id = ? and mod_id = ?"
        db_form = [new_delta, task.delta, next_date, task.card_id, mod_id]
        c.execute(q, db_form)


def is_mod_exist(dbpath, mod_id):
    with sqlite3.connect(dbpath) as c:
        q = "SELECT * FROM taskperday WHERE mod_id = ?"
        db_form = [mod_id]
        i = c.execute(q, db_form)
        try:
            mod_id, day, new, total = next(i)
        except StopIteration:
            print(f"There's no '{mod_id}' mod in this deck")
            sys.exit(1)


class Task:
    def __init__(self, next_time, card_id, answer, question, delta, old_delta, limit = None): # ### card_id можно сделать необязательным аргументом (по дефолту будет -1)
        self.next_time = next_time
        self.card_id = card_id
        self.answer = answer
        self.question = question
        self.delta = delta
        self.old_delta = old_delta
        self.attempts = 0
        self.counter = 0
        self.limit = self._get_limit(limit)

    def _get_limit(self, limit):
        if not limit:
            summ = self.delta + self.old_delta
            if summ <= 3:
                return 5 - summ
            return 1
        return limit

    def get_new_delta(self):
        delta = self.delta
        old_delta = self.old_delta
        if delta == 0:
            delta = 1
        if old_delta == 0:
            old_delta = 1
        mean = (13 * delta + 3 * old_delta) / 16
        factor = 2 * self.counter / self.attempts
        new_delta = math.ceil(mean * factor + 1 / 8)
        part = new_delta // 8
        if part:
            new_delta += int(random.triangular(-part, part, 0))
        return new_delta


def handle_newest(mod_id):
    with sqlite3.connect(dbpath) as c:
        print("Докидываем инитов в schedule")
        select_cursor = c.cursor()
        insert_cursor = c.cursor()
        q_select = """
            SELECT d.card_id FROM deck d
            LEFT JOIN schedule s ON d.card_id = s.card_id AND s.mod_id = ?
            WHERE s.card_id IS NULL
        """
        rows_iter = select_cursor.execute(q_select, (mod_id,))
        to_insert = ((mod_id, row[0], 0, 0, current_date) for row in rows_iter)
        before_changes = c.total_changes
        insert_cursor.executemany("INSERT INTO schedule VALUES(?, ?, ?, ?, ?)", to_insert)
        inserted = c.total_changes - before_changes
        print(f"Докинуто {inserted} инитов в schedule")


def update_taskperday(dbpath, mod_id):
    with sqlite3.connect(dbpath) as c:
        q = "SELECT * FROM taskperday WHERE mod_id = ?"
        db_form = [mod_id]
        i = c.execute(q, db_form)
        mod_id, day, new, total = next(i)
        print(f"В таскпердее было {mod_id=}, {day=}, {new=}, {total=}")
        if current_date != day:
            q = "UPDATE taskperday SET day = ?, new = 0, total = 0 WHERE mod_id = ?"
            db_form = [current_date, mod_id]
            c.execute(q, db_form)
            new = 0
            total = 0
            print(f"Так как дата устаревшая обнуляем счётчики.")
        return new, total


def get_sub_list(dbpath, mod_id, answer_index, question_form, size, char, next_time):
    with sqlite3.connect(dbpath) as c:
        q = f"""
            SELECT s.card_id, s.delta, s.old_delta, d.*
            FROM schedule s
            JOIN deck d ON s.card_id = d.card_id
            WHERE s.delta + s.old_delta {char} 0
              AND s.mod_id = ?
              AND s.schedule_date <= ?
            ORDER BY s.schedule_date ASC
            LIMIT ?
        """
        i = c.execute(q, (mod_id, current_date, size))
        sub_list = []
        counter = 0
        for row in i:
            card_id, delta, old_delta = row[0:3]
            fields = row[3:]
            answer = fields[answer_index]
            question = question_form.format(*fields)
            task = Task(next_time, card_id, answer, question, delta, old_delta)
            sub_list.append(task)
            counter += 1
        return sub_list, counter


def get_qa(dbpath, mod_id):
    with sqlite3.connect(dbpath) as c:
        q = "SELECT auto_eval, answer_index, question FROM qa WHERE mod_id = ?"
        db_form = [mod_id]
        i = c.execute(q, db_form)
        return next(i)


def get_task_list(dbpath, mod_id, answer_index, question_form):
    new, total = update_taskperday(dbpath, mod_id)
    print(f"update_taskperday: {new=}, {total=}")
    size = max(total_limit - total, 0)
    print("Насыпаем репитов из schedule")
    repeat_list, counter = get_sub_list(dbpath, mod_id, answer_index, question_form, size, '>', float('+inf'))
    total += counter
    print(f"get_repeat_list: {new=}, {total=}")
    print("Насыпаем новых из schedule")
    size = max(min(new_limit - new, total_limit - total), 0)
    new_list, counter = get_sub_list(dbpath, mod_id, answer_index, question_form, size, '=', 0)
    total += counter
    new += counter
    print(f"get_new_list: {new=}, {total=}")
    task_list = new_list + repeat_list
    random.shuffle(task_list)
    return task_list


def check_exit_conditions(task_list, mod_id, previous):
    if previous:
        temp_list = task_list + [previous]
    else:
        temp_list = task_list
    if len(temp_list) <= 2:
        for temp in temp_list:
            if temp.limit - temp.counter <= 1.5:
                break
        else:
            for temp in temp_list:
                write_db(mod_id, 0, current_date + 1, temp)
                print(f'{temp.question}{temp.answer} откладывается')
            print("Пока!")
            sys.exit()


def get_task(task_list):
    task_list.sort(key=lambda t: t.next_time)
    current_time = time.time()
    if task_list[0].next_time <= current_time:
        return task_list.pop(0) # созрела карточка
    elif task_list[-1].next_time == float('+inf'):
        return task_list.pop() # берём репит в работу
    return task_list.pop(0) # берём ближайшую к зрелости


def get_guess(task):
    get_input('\nНажмите Enter чтобы продолжить...')
    ctrl_l()
    start_time = time.time()
    guess = get_input(task.question)
    end_time = time.time()
    delay = end_time - start_time
    return guess, delay


def get_grade(auto_eval, task, guess, delay):
    if auto_eval:
        print(f"delay = {delay:0.2f}")
        if guess.lower() == task.answer.lower():
            print(f"{start_green}Ты молодец!{start_normal}")
            grade = get_auto_grade(delay, task.answer)
        else:
            print(
                f"{start_red}Неправильно!{start_normal} Правильный ответ {start_blue}{task.answer}{start_normal}")
            grade = 1
    else:
        print(f"Правильный ответ {task.answer}")
        grade = get_manual_grade()
    return grade


def update_counter(task, s):
        current_time = time.time()
        task.attempts += 1
        task.next_time = current_time + s * 30
        if s == 1:
            print("s = 1, обнуляем счётчик")
            task.counter = 0
        elif s == 2:
            print("s = 2, do nothing")
        elif s == 3:
            print("s = 3, счётчик + 1")
            task.counter += 1
        elif s == 4:
            print("s = 4, счётчик + 1.5")
            task.counter += 1.5
        print(f"{task.attempts=}, {task.counter=}, {task.limit=}")


def update_task_list(task, previous, task_list):
    if previous:
        task_list.append(previous)
    if task.counter >= task.limit:
        new_delta = task.get_new_delta()
        next_date = current_date + new_delta
        write_db(mod_id, new_delta, next_date, task)
        previous = None
        print("let's do the procedure")
        print(f"{new_delta=}")
    else:
        previous = task
    return previous, task_list


def proc(task_list, mod_id, auto_eval):
    previous = None
    while True:
        check_exit_conditions(task_list, mod_id, previous)
        task = get_task(task_list)
        guess, delay = get_guess(task)
        grade = get_grade(auto_eval, task, guess, delay)
        update_counter(task, grade)
        previous, task_list = update_task_list(task, previous, task_list)


def get_id_list(infinite_ids):
    l = []
    for card_id in infinite_ids:
        l += ranger(card_id)
    return l


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
        sys.exit(1)
    return l


def proc_inf(dbpath, dictionary, mod_id):
    with sqlite3.connect(dbpath) as c:
        q = "SELECT * FROM qa WHERE mod_id = ?"
        db_form = [mod_id]
        i = c.execute(q, db_form)
        mod_id, auto_eval, answer_index, question = next(i)
    print(f"{mod_id=}, {auto_eval=}, {answer_index=}, {question=}")
    if dictionary:
        while True:
            card_id = random.choice(list(dictionary))
            fields = dictionary[card_id]
            string = question.format(*fields)
            answer = fields[answer_index]
            get_input('\nНажмите Enter чтобы продолжить...') # \n отсюда надо переставить в другое место? в инфините некрасиво смотрится
            ctrl_l()
            start_time = time.time()
            guess = get_input(string)
            end_time = time.time()
            delay = end_time - start_time
            if auto_eval:
                print(f"{delay=:0.2f}")
                if guess.lower() == answer.lower():
                    print(f"{start_green}Ты молодец!{start_normal}")
                else:
                    print(f"{start_red}Неправильно!{start_normal} Правильный ответ {start_blue}{answer}{start_normal}")
            else:
                print(f"Правильный ответ {answer}")
    print("колода пуста")


def get_inf_list(dbpath, mod_id, answer_index, question_form, ifinite_id_list):
    with sqlite3.connect(dbpath) as c:
        task_list = []
        if ifinite_id_list:
            for card_id in ifinite_id_list:
                q = "SELECT * FROM deck WHERE card_id = ?"
                i = c.execute(q, (card_id,))
                fields = next(i)
                answer = fields[answer_index]
                question = question_form.format(*fields)
                task = Task(float('+inf'), card_id, answer, question, -1, -1, float('+inf'))
                task_list.append(task)
        else:
            q = "SELECT * FROM deck"
            i = c.execute(q)
            for fields in i:
                card_id = fields[0]
                answer = fields[answer_index]
                question = question_form.format(*fields)
                task = Task(float('+inf'), card_id, answer, question, -1, -1, float('+inf'))
                task_list.append(task)
        return task_list


def proc_inf(task_list, mod_id, auto_eval):
    previous = None
    while True:
        # check_exit_conditions(task_list, mod_id, previous) # потом пригодится
        task = get_task(task_list)
        guess, delay = get_guess(task)
        grade = get_grade(auto_eval, task, guess, delay)
        update_counter(task, grade)
        previous, task_list = update_task_list(task, previous, task_list)


def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(
        write_to = ['deck_id'],
        keys = ['-d', '--deck-id'], 
        valency = 1,
        positional = True, 
        func = is_db_exist
        )
    p.add_pattern(
        write_to=['mod_id'],
        keys=['-m', '--mod-id'],
        valency=1, 
        positional = True
        )
    p.add_pattern(
        write_to = ['infinite_ids'], # а если принимать не id, а sql запрос? или псевдо-sql запрос...
        set_to = {"inf_flag" : True},
        keys = ['-i', '--infinite'],
        valency = '*',
        positional = False
        )
    p.defaults = types.SimpleNamespace(
        deck_id=None,
        mod_id=None,
        inf_flag=False
        )
    r = p.parse()
    return r


start_red = "\033[91m"
start_green = "\033[92m"
start_blue = "\033[94m"
start_normal = "\033[39m"
os.chdir(os.path.dirname(__file__))
current_date = datetime.date.today().toordinal()
# current_date = 739682
new_limit = 8
total_limit = 24
if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath = r.deck_id[0]
    mod_id = r.mod_id[0]
    is_mod_exist(dbpath, mod_id) # ### его надо поставить как функцию в парсере
    if r.inf_flag:
        ifinite_id_list = get_id_list(r.infinite_ids)
        auto_eval, answer_index, question_form = get_qa(dbpath, mod_id)
        task_list = get_inf_list(dbpath, mod_id, answer_index, question_form, ifinite_id_list)
        random.shuffle(task_list)
        proc_inf(task_list, mod_id, auto_eval)
    else:
        print(f"{current_date=}")
        handle_newest(mod_id)
        auto_eval, answer_index, question_form = get_qa(dbpath, mod_id)
        task_list = get_task_list(dbpath, mod_id, answer_index, question_form)
        proc(task_list, mod_id, auto_eval)
    
