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


def write_db(mode_id, new_delta, next_date, task):
    with sqlite3.connect(dbpath) as c:
        q = "SELECT * FROM taskperday WHERE mode_id = ?"
        db_form = [mode_id]
        i = c.execute(q, db_form)
        mode_id, day, new, total = next(i)
        if task.delta + task.old_delta == 0:
            q = "UPDATE taskperday SET new = ?, total = ? WHERE mode_id = ?"
            db_form = [new + 1, total + 1, mode_id]
        else:
            q = "UPDATE taskperday SET total = ? WHERE mode_id = ?"
            db_form = [total + 1, mode_id]
        c.execute(q, db_form)
        q = "UPDATE schedule SET delta = ?, old_delta = ?, schedule_date = ? WHERE card_id = ? and mode_id = ?"
        db_form = [new_delta, task.delta, next_date, task.card_id, mode_id]
        c.execute(q, db_form)


def is_mode_exist(dbpath, mode_id):
    with sqlite3.connect(dbpath) as c:
        i = c.execute("SELECT * FROM taskperday WHERE mode_id = ?", (mode_id,))
        try:
            next(i)
        except StopIteration:
            print(f"There's no '{mode_id}' mode in this deck")
            sys.exit(1)
    return mode_id


class Task:
    def __init__(
        self,
        next_time,
        answer,
        question,
        delta = None,
        old_delta = None,
        card_id = None,
        limit = None,
    ):
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


def handle_newest(mode_id):
    with sqlite3.connect(dbpath) as c:
        select_cursor = c.cursor()
        insert_cursor = c.cursor()
        q_select = """
            SELECT d.card_id FROM deck d
            LEFT JOIN schedule s ON d.card_id = s.card_id AND s.mode_id = ?
            WHERE s.card_id IS NULL
        """
        rows_iter = select_cursor.execute(q_select, (mode_id,))
        to_insert = ((mode_id, row[0], 0, 0, current_date) for row in rows_iter)
        before_changes = c.total_changes
        insert_cursor.executemany("INSERT INTO schedule VALUES(?, ?, ?, ?, ?)", to_insert)
        inserted = c.total_changes - before_changes
        print(f"Докинуто {inserted} новейших задач в расписание")


def get_taskperday_stats(dbpath, mode_id):
    with sqlite3.connect(dbpath) as c:
        q = "SELECT * FROM taskperday WHERE mode_id = ?"
        db_form = [mode_id]
        i = c.execute(q, db_form)
        mode_id, day, new, total = next(i)
        if current_date != day:
            q = "UPDATE taskperday SET day = ?, new = 0, total = 0 WHERE mode_id = ?"
            db_form = [current_date, mode_id]
            c.execute(q, db_form)
            new = 0
            total = 0
        print(f"Сегодня было выполнено задач всего: {total}, новых: {new}, репитов: {total - new}")
        return new, total


def get_sub_list(dbpath, mode_id, answer_index, question_form, size, char, next_time):
    with sqlite3.connect(dbpath) as c:
        q = f"""
            SELECT s.card_id, s.delta, s.old_delta, d.*
            FROM schedule s
            JOIN deck d ON s.card_id = d.card_id
            WHERE s.delta + s.old_delta {char} 0
              AND s.mode_id = ?
              AND s.schedule_date <= ?
            ORDER BY s.schedule_date ASC
            LIMIT ?
        """
        i = c.execute(q, (mode_id, current_date, size))
        sub_list = []
        for row in i:
            card_id, delta, old_delta = row[0:3]
            fields = row[3:]
            answer = fields[answer_index]
            question = question_form.format(*fields)
            task = Task(next_time, answer, question, delta, old_delta, card_id)
            sub_list.append(task)
        return sub_list


def get_adhoc_list(dbpath, mode_id, answer_index, question_form, id_list, limit):
    with sqlite3.connect(dbpath) as c:
        if id_list:
            placeholders = ', '.join(['?'] * len(id_list))
            q = f"SELECT * FROM deck WHERE card_id IN ({placeholders})"
            rows = c.execute(q, id_list)
        else:
            rows = c.execute("SELECT * FROM deck")
        task_list = []
        for fields in rows:
            answer = fields[answer_index]
            question = question_form.format(*fields)
            task = Task(float('+inf'), answer, question, limit=limit)
            task_list.append(task)
        random.shuffle(task_list)
        return task_list



def get_qa(dbpath, mode_id):
    with sqlite3.connect(dbpath) as c:
        q = "SELECT auto_grade, answer_index, question_form FROM qa WHERE mode_id = ?"
        db_form = [mode_id]
        i = c.execute(q, db_form)
        return next(i)


def get_scheduled_list(dbpath, mode_id, answer_index, question_form):
    old_new, old_total = get_taskperday_stats(dbpath, mode_id)
    new, total = old_new, old_total
    size = max(total_limit - total, 0)
    repeat_list = get_sub_list(dbpath, mode_id, answer_index, question_form, size, '>', float('+inf'))
    total += len(repeat_list)
    size = max(min(new_limit - new, total_limit - total), 0)
    new_list = get_sub_list(dbpath, mode_id, answer_index, question_form, size, '=', 0)
    total += len(new_list)
    new += len(new_list)
    task_list = new_list + repeat_list
    random.shuffle(task_list)
    added_total = total - old_total
    added_new = new - old_new
    print(f"В текущей сессии всего задач: {added_total}, новых: {added_new}, репитов: {added_total - added_new}\n")
    return task_list


def get_task(task_list):
    task_list.sort(key=lambda t: t.next_time)
    current_time = time.time()
    if task_list[0].next_time <= current_time:
        return task_list.pop(0) # созрела задача
    elif task_list[-1].next_time == float('+inf'):
        return task_list.pop() # берём репит в работу
    return task_list.pop(0) # берём ближайшую к зрелости


def get_guess(task):
    get_input('\nНажмите Enter чтобы показать задачу...')
    ctrl_l()
    start_time = time.time()
    guess = get_input(task.question)
    end_time = time.time()
    delay = end_time - start_time
    return guess, delay


def get_auto_grade(delay, answer):
    l = len(answer)
    estimated_recall_time = delay - 1 - l / 4
    print(f"Расчётное время вспоминания: {estimated_recall_time:0.2f}")
    if estimated_recall_time < 3:
        return 4
    if estimated_recall_time < 6:
        return 3
    if estimated_recall_time < 9:
        return 2
    return 1


def get_grade(auto_grade, task, guess, delay):
    if auto_grade:
        if guess.lower() == task.answer.lower():
            print(f"{start_green}Ты молодец!{start_normal}")
            print(f"Время ответа: {delay:0.2f}")
            grade = get_auto_grade(delay, task.answer)
        else:
            print(
                f"{start_red}Неправильно!{start_normal} Правильный ответ {start_blue}{task.answer}{start_normal}")
            grade = 1
    else:
        print(f"Правильный ответ {task.answer}")
        grade = get_manual_grade()
    return grade


def update_counter(task, grade):
        current_time = time.time()
        task.attempts += 1
        task.next_time = current_time + grade * 30
        if grade == 1:
            print("Обнуляем счётчик")
            task.counter = 0
        elif grade == 2:
            print("Не делаем ничего")
        elif grade == 3:
            print("Счётчик + 1")
            task.counter += 1
        elif grade == 4:
            print("Счётчик + 1.5")
            task.counter += 1.5
        print(f"Попыток: {task.attempts}, счётчик: {task.counter}, лимит: {task.limit}")


def check_exit_conditions(task_list, mode_id, previous):
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
                if temp.card_id is not None:
                    write_db(mode_id, 0, current_date + 1, temp)
                print(f'{temp.question}{temp.answer} откладывается')
            print("Пока!")
            sys.exit()


def update_task_list(task, mode_id, previous, task_list):
    if previous:
        task_list.append(previous)
    if task.counter >= task.limit:
        if task.card_id is not None:
            new_delta = task.get_new_delta()
            next_date = current_date + new_delta
            write_db(mode_id, new_delta, next_date, task)
            print(f"{new_delta=}")
        previous = None
        print('Задача добита')
    else:
        previous = task
    return previous, task_list


def proc(task_list, mode_id, auto_grade):
    previous = None
    while True:
        check_exit_conditions(task_list, mode_id, previous)
        task = get_task(task_list)
        guess, delay = get_guess(task)
        grade = get_grade(auto_grade, task, guess, delay)
        update_counter(task, grade)
        previous, task_list = update_task_list(task, mode_id, previous, task_list)


def get_id_list(id_ranges):
    id_list = []
    for id_range in id_ranges:
        id_list += ranger(id_range)
    return id_list


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


def get_limit(limit):
    if limit == 'inf':
        return float('+inf')
    return float(limit)


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
        write_to=['mode_id'],
        keys=['-m', '--mode-id'],
        valency = 1, 
        positional = True
        )
    p.add_pattern(
        write_to = ['ids'], # а если принимать не id, а sql запрос? или псевдо-sql запрос...
        set_to = {"ad_hoc" : True},
        keys = ['-i', '--ad-hoc-ids'],
        valency = '+',
        positional = False
        )
    p.add_pattern(
        write_to = ['limit'],
        set_to = {"ad_hoc" : True},
        keys = ['-l', '--ad-hoc-limits'],
        valency = 1,
        positional = False,
        func = get_limit
        )
    p.add_pattern(
        set_to = {"ad_hoc" : True},
        keys = ['-a', '--ad-hoc'],
        valency = 0,
        positional = False
        )
    p.defaults = types.SimpleNamespace(
        deck_id=None,
        mode_id=None,
        ad_hoc=False,
        limit=[float('+inf')]
        )
    r = p.parse()
    return r


start_red = "\033[91m"
start_green = "\033[92m"
start_blue = "\033[94m"
start_normal = "\033[39m"
os.chdir(os.path.dirname(__file__))
current_date = datetime.date.today().toordinal()
new_limit = 8
total_limit = 24
if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath = r.deck_id[0]
    mode_id = r.mode_id[0]
    is_mode_exist(dbpath, mode_id)
    auto_grade, answer_index, question_form = get_qa(dbpath, mode_id)
    if r.ad_hoc:
        print("Режим ad-hoc")
        id_list = get_id_list(r.ids)
        task_list = get_adhoc_list(dbpath, mode_id, answer_index, question_form, id_list, r.limit[0])
    else:
        print("Режим scheduled")
        handle_newest(mode_id)
        task_list = get_scheduled_list(dbpath, mode_id, answer_index, question_form)
    proc(task_list, mode_id, auto_grade)
    
