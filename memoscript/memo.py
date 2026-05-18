#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import time

import utils
from session import session

# Обеспечиваем, что при запуске скрипта его директория в sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
os.chdir(SCRIPT_DIR)

def ctrl_l():
    print('\n' * (os.get_terminal_size().lines - 1) + "\033[H\033[J", end='')

def get_input(text):
    try:
        return input(text)
    except EOFError:
        print("\nПока!")
        sys.exit()

def get_guess(task):
    get_input('\nНажмите Enter чтобы показать задачу...')
    ctrl_l()
    start_time = time.time()
    guess = get_input(task.question)
    end_time = time.time()
    delay = end_time - start_time
    return guess, delay

def get_manual_grade(task):
    print(f"Правильный ответ {task.answers}")
    while True:
        try:
            s = int(get_input('Оцени (1-4)?: '))
        except ValueError:
            pass
        else:
            if 1 <= s <= 4:
                return s
        print("Ещё раз. ", end='')

def build_parser():
    parser = argparse.ArgumentParser(
        prog='memo.py',
        description='memoscript система интервального повторения',
    )
    subparsers = parser.add_subparsers(dest='command', help='доступные команды')
    p_session = subparsers.add_parser('session', help='запустить сессию')
    session_sub = p_session.add_subparsers(dest='session_cmd', required=True)
    ss_sub = session_sub.add_parser('scheduled', help='запустить сессию по расписанию')
    ss_sub.add_argument(dest = "deck_id")
    ss_sub.add_argument(dest ='template_id')
    sa_sub = session_sub.add_parser('adhoc', help='запустить адхок сессию')
    sa_sub.add_argument(dest = "deck_id")
    sa_sub.add_argument(dest ='template_id')
    sa_sub.add_argument('-c', '--card-ids', nargs = '+')
    sa_sub.add_argument('-l', '--limit')
    p_create = subparsers.add_parser('create', help='создать deck/card/template')
    create_sub = p_create.add_subparsers(dest='create_cmd', required=True)
    cc_sub = create_sub.add_parser('card', help='создать карточку')
    cc_sub.add_argument(dest = "deck_id")
    cc_sub.add_argument(dest = 'fields', nargs = '+')
    ct_sub = create_sub.add_parser('template', help='создать шаблон')
    ct_sub.add_argument(dest = "deck_id")
    ct_sub.add_argument(dest = 'template_id')
    ct_sub.add_argument(dest = 'answer_field')
    ct_sub.add_argument(dest = 'question_forms', nargs = '+')
    ct_sub.add_argument('-m', '--manual-evaluation', action = 'store_true')
    cd_sub = create_sub.add_parser('deck', help='создать колоду')
    cd_sub.add_argument(dest = "deck_id")
    cd_sub.add_argument(dest = 'field_names', nargs = '+')
    p_update = subparsers.add_parser('update', help='обновить card/template')
    update_sub = p_update.add_subparsers(dest='update_cmd', required=True)
    uc_sub = update_sub.add_parser('card', help='обновить карточку')
    uc_sub.add_argument(dest = "deck_id")
    uc_sub.add_argument(dest = "card_id")
    uc_sub.add_argument(dest = 'fields', nargs = '+')
    ut_sub = update_sub.add_parser('template', help='обновить шаблон')
    ut_sub.add_argument(dest = "deck_id")
    ut_sub.add_argument(dest ='template_id')
    ut_sub.add_argument(dest = 'answer_field')
    ut_sub.add_argument(dest = 'question_forms', nargs = '+')
    ut_sub.add_argument('-m', '--manual-evaluation', action = 'store_true')
    p_delete = subparsers.add_parser('delete', help='удалить card/template')
    delete_sub = p_delete.add_subparsers(dest='delete_cmd', required=True)
    dc_sub = delete_sub.add_parser('card', help='удалить карточку')
    dc_sub.add_argument(dest = "deck_id")
    dc_sub.add_argument('-c', '--card-ids', nargs = '+')
    dt_sub = delete_sub.add_parser('template', help='удалить шаблон')
    dt_sub.add_argument(dest = "deck_id")
    dt_sub.add_argument(dest ='template_id')
    p_show = subparsers.add_parser('show', help='показать deck')
    show_sub = p_show.add_subparsers(dest='show_cmd', required=True)
    sd_sub = show_sub.add_parser('deck', help='показать колоду')
    sd_sub.add_argument(dest = "deck_id")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    start_red = "\033[91m"
    start_green = "\033[92m"
    start_blue = "\033[94m"
    start_normal = "\033[39m"
    if args.command == 'session':
        if args.session_cmd == 'adhoc':
            i = session(args.deck_id, args.template_id, get_guess, get_manual_grade, True, args.limit, args.card_ids)
        else:
            i = session(args.deck_id, args.template_id, get_guess, get_manual_grade, False)
        for r in i:
            if r.type == 'exit':
                print()
                for temp in r.temp_list:
                    print(f'{temp.question}{temp.answers} откладывается')
            elif r.type == 'regular':
                if r.right:
                    print(f"{start_green}Ты молодец!{start_normal}")
                    print(f"Время ответа: {r.delay:0.2f}")
                    print(f"Расчётное время вспоминания: {r.recall_time:0.2f}")
                else:
                    print(f"{start_red}Неправильно!{start_normal} Правильный ответ {start_blue}{r.task.answers}{start_normal}")
                if r.grade == 1:
                    print("Обнуляем счётчик")
                elif r.grade == 2:
                    print("Счётчик + 0.5")
                elif r.grade == 3:
                    print("Счётчик + 1")
                elif r.grade == 4:
                    print("Счётчик + 1.5")
                elif r.grade == 5:
                    print("Счётчик + 2")
                print(f"Попыток: {r.task.attempts}, счётчик: {r.task.counter}, лимит: {r.task.limit}")
                print(f"Сделано {r.start_task_count - r.task_count}/{r.start_task_count}")
                # print(f"{r.task_count=}")
                if r.task_done:
                    print('Задача добита')
                    if r.task.card_id is not None:
                        print(f"{r.new_delta=}")
            elif r.type == 'stats':
                print(f"Сегодня было выполнено задач всего: {r.old_total_count}, новых: {r.old_new_count}, репитов: {r.old_total_count - r.old_new_count}")
                print(f"В текущей сессии всего задач: {r.added_total}, новых: {r.added_new}, репитов: {r.added_total - r.added_new}\n")
                
            else:
                raise Exception
    elif args.command == 'create':
        if args.create_cmd == 'card':
            utils.create_update_card(args.deck_id, args.fields)
        elif args.create_cmd == 'template':
            utils.create_template(args.deck_id, args.template_id, args.answer_field, args.question_forms, not args.manual_evaluation)
        elif args.create_cmd == 'deck':
            utils.create_deck(args.deck_id, args.field_names)
    elif args.command == 'update':
        if args.update_cmd == 'card':
            utils.create_update_card(args.deck_id, args.fields, args.card_id)
        elif args.update_cmd == 'template':
            utils.update_template(args.deck_id, args.template_id, args.answer_field, args.question_forms, not args.manual_evaluation)
    elif args.command == 'delete':
        if args.delete_cmd == 'card':
            utils.delete_card(args.deck_id, args.card_ids)
        elif args.command == 'template':
            utils.delete_template(args.deck_id, args.template_id)
    elif args.command == 'show':
        if args.show_cmd == 'deck':
            utils.show_deck(args.deck_id)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
