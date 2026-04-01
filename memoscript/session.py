#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import sqlite3
import sys
import time
import os
import math
import json
if os.name == 'posix':
    import readline

from utils import is_template_exist, get_field_names, get_id_list, current_date, get_db_path


def ctrl_l():
    print('\n' * (os.get_terminal_size().lines - 1) + "\033[H\033[J", end='')


def get_input(text):
    try:
        return input(text)
    except EOFError:
        print("\nПока!")
        sys.exit()


def get_limit(limit):
    try:
        limit = float(limit)
    except ValueError:
        print('Недопустимое значение лимита!')
        exit(1)
    if limit <= 0: # ### по идее вместо нуля должна быть минимальная граница нестрогая
        return float('+inf')
    return limit

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


def write_db(template_id, new_delta, next_date, task, db_path):
    with sqlite3.connect(db_path) as c:
        q = "SELECT * FROM daily_stats WHERE template_id = ?"
        db_form = [template_id]
        i = c.execute(q, db_form)
        template_id, stats_date, new_count, total_count = next(i)
        if task.delta + task.prev_delta == 0:
            q = "UPDATE daily_stats SET new_count = ?, total_count = ? WHERE template_id = ?"
            db_form = [new_count + 1, total_count + 1, template_id]
        else:
            q = "UPDATE daily_stats SET total_count = ? WHERE template_id = ?"
            db_form = [total_count + 1, template_id]
        c.execute(q, db_form)
        q = "UPDATE schedule SET delta = ?, prev_delta = ?, due_date = ? WHERE card_id = ? and template_id = ?"
        db_form = [new_delta, task.delta, next_date, task.card_id, template_id]
        c.execute(q, db_form)


class Task:
    def __init__(
        self,
        next_time,
        answer,
        question,
        delta = None,
        prev_delta = None,
        card_id = None,
        limit = None,
    ):
        self.next_time = next_time
        self.card_id = card_id
        self.question = question
        self.delta = delta
        self.prev_delta = prev_delta
        self.attempts = 0
        self.counter = 0
        self.limit = self._get_limit(limit)
        self.answers = answer.split('|')

    def _get_limit(self, limit):
        if not limit:
            summ = self.delta + self.prev_delta
            if summ <= 3:
                return 5 - summ
            return 1
        return limit

    def get_new_delta(self):
        delta = self.delta
        prev_delta = self.prev_delta
        if delta == 0:
            delta = 1
        if prev_delta == 0:
            prev_delta = 1
        mean = (13 * delta + 3 * prev_delta) / 16
        factor = 2 * self.counter / self.attempts
        new_delta = math.ceil(mean * factor + 1 / 8)
        part = new_delta // 8
        if part:
            new_delta += int(random.triangular(-part, part, 0))
        return new_delta


def decode_deck_fields_map(card_id, fields_json, field_names):
    fields = json.loads(fields_json)
    fields_map = dict(zip(field_names, fields))
    fields_map["card_id"] = card_id
    fields_map = {k: v for k, v in fields_map.items() if v != ""}
    return fields_map


def handle_newest(template_id, db_path):
    with sqlite3.connect(db_path) as c:
        select_cursor = c.cursor()
        insert_cursor = c.cursor()
        q_select = """
            SELECT d.card_id FROM deck d
            LEFT JOIN schedule rs ON d.card_id = rs.card_id AND rs.template_id = ?
            WHERE rs.card_id IS NULL
        """
        rows_iter = select_cursor.execute(q_select, (template_id,))
        to_insert = ((template_id, row[0], 0, 0, current_date) for row in rows_iter)
        before_changes = c.total_changes
        insert_cursor.executemany("INSERT INTO schedule VALUES(?, ?, ?, ?, ?)", to_insert)
        inserted = c.total_changes - before_changes
        print(f"Докинуто {inserted} новейших задач в расписание")


def get_daily_stats(db_path, template_id):
    with sqlite3.connect(db_path) as c:
        q = "SELECT * FROM daily_stats WHERE template_id = ?"
        db_form = [template_id]
        i = c.execute(q, db_form)
        template_id, stats_date, new_count, total_count = next(i)
        if current_date != stats_date:
            q = "UPDATE daily_stats SET stats_date = ?, new_count = 0, total_count = 0 WHERE template_id = ?"
            db_form = [current_date, template_id]
            c.execute(q, db_form)
            new_count = 0
            total_count = 0
        print(f"Сегодня было выполнено задач всего: {total_count}, новых: {new_count}, репитов: {total_count - new_count}")
        return new_count, total_count


def get_sub_list(db_path, template_id, answer_field, question_forms, size, char, next_time, field_names):
    with sqlite3.connect(db_path) as c:
        q = f"""
            SELECT rs.card_id, rs.delta, rs.prev_delta, d.fields_json
            FROM schedule rs
            JOIN deck d ON rs.card_id = d.card_id
            WHERE rs.delta + rs.prev_delta {char} 0
              AND rs.template_id = ?
              AND rs.due_date <= ?
            ORDER BY rs.due_date ASC
            LIMIT ?
        """
        i = c.execute(q, (template_id, current_date, size))
        sub_list = []
        for row in i:
            card_id, delta, prev_delta = row[:3]
            fields_map = decode_deck_fields_map(card_id, row[3], field_names)
            answer = fields_map[answer_field]
            for question_form in question_forms:
                try:
                    question = question_form.format(**fields_map)
                    break
                except KeyError:
                    pass
            else:
                raise Exception('Нет подходящей формы!') # ### А что если не вбрасывать исключение, а просто не добавлять карточку? не баг, а фича!
            task = Task(next_time, answer, question, delta, prev_delta, card_id)
            sub_list.append(task)
        return sub_list


def get_adhoc_list(db_path, answer_field, question_forms, id_list, limit, field_names):
    with sqlite3.connect(db_path) as c:
        if id_list:
            placeholders = ', '.join(['?'] * len(id_list))
            q = f"SELECT card_id, fields_json FROM deck WHERE card_id IN ({placeholders})"
            rows = c.execute(q, id_list)
        else:
            rows = c.execute("SELECT card_id, fields_json FROM deck")
        task_list = []
        for card_id, fields_json in rows:
            fields_map = decode_deck_fields_map(card_id, fields_json, field_names)
            answer = fields_map[answer_field]
            for question_form in question_forms:
                try:
                    question = question_form.format(**fields_map)
                    break
                except KeyError:
                    pass
            else:
                raise Exception('Нет подходящей формы!')
            task = Task(float('+inf'), answer, question, limit=limit)
            task_list.append(task)
        random.shuffle(task_list)
        return task_list


def get_template(db_path, template_id):
    with sqlite3.connect(db_path) as c:
        q = "SELECT auto_grade, answer_field, question_forms_json FROM templates WHERE template_id = ?"
        db_form = [template_id]
        i = c.execute(q, db_form)
        auto_grade, answer_field, question_forms_json = next(i)
        auto_grade = bool(auto_grade)
        question_forms = json.loads(question_forms_json)
        return auto_grade, answer_field, question_forms


def get_scheduled_list(db_path, template_id, answer_field, question_form, field_names):
    new_limit = 8
    total_limit = 24
    old_new_count, old_total_count = get_daily_stats(db_path, template_id)
    new_count, total_count = old_new_count, old_total_count
    size = max(total_limit - total_count, 0)
    repeat_list = get_sub_list(db_path, template_id, answer_field, question_form, size, '>', float('+inf'), field_names)
    total_count += len(repeat_list)
    size = max(min(new_limit - new_count, total_limit - total_count), 0)
    new_list = get_sub_list(db_path, template_id, answer_field, question_form, size, '=', 0, field_names)
    total_count += len(new_list)
    new_count += len(new_list)
    task_list = new_list + repeat_list
    random.shuffle(task_list)
    added_total = total_count - old_total_count
    added_new = new_count - old_new_count
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
    start_red = "\033[91m"
    start_green = "\033[92m"
    start_blue = "\033[94m"
    start_normal = "\033[39m"
    if auto_grade:
        for answer in task.answers:
            if guess.lower() == answer.lower():
                print(f"{start_green}Ты молодец!{start_normal}")
                print(f"Время ответа: {delay:0.2f}")
                return get_auto_grade(delay, answer)
        print(f"{start_red}Неправильно!{start_normal} Правильный ответ {start_blue}{task.answers}{start_normal}")
        return 1
    print(f"Правильный ответ {task.answers}")
    return get_manual_grade()


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


def check_exit_conditions(task_list, template_id, previous, db_path):
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
                    write_db(template_id, 0, current_date + 1, temp, db_path)
                print(f'{temp.question}{temp.answers} откладывается')
            print("Пока!")
            sys.exit()


def update_task_list(task, template_id, previous, task_list, db_path):
    if previous:
        task_list.append(previous)
    if task.counter >= task.limit:
        if task.card_id is not None:
            new_delta = task.get_new_delta()
            next_date = current_date + new_delta
            write_db(template_id, new_delta, next_date, task, db_path)
            print(f"{new_delta=}")
        previous = None
        print('Задача добита')
    else:
        previous = task
    return previous, task_list


def proc(task_list, template_id, auto_grade, db_path):
    previous = None
    while True:
        check_exit_conditions(task_list, template_id, previous, db_path)
        task = get_task(task_list)
        guess, delay = get_guess(task)
        grade = get_grade(auto_grade, task, guess, delay)
        update_counter(task, grade)
        previous, task_list = update_task_list(task, template_id, previous, task_list, db_path)


def session(args):
    os.chdir(os.path.dirname(__file__))
    ad_hoc = False
    if args.ad_hoc or args.limit or args.card_ids:
        ad_hoc = True
        limit = get_limit(args.limit)
    db_path = get_db_path(args.deck_id)
    template_id = args.template_id
    is_template_exist(db_path, template_id)
    auto_grade, answer_field, question_forms = get_template(db_path, template_id)
    field_names = get_field_names(db_path)
    if ad_hoc:
        print("Режим ad-hoc")
        id_list = get_id_list(args.card_ids)
        task_list = get_adhoc_list(db_path, answer_field, question_forms, id_list, limit, field_names)
    else:
        print("Режим scheduled")
        handle_newest(template_id, db_path)
        task_list = get_scheduled_list(db_path, template_id, answer_field, question_forms, field_names)
    proc(task_list, template_id, auto_grade, db_path)
