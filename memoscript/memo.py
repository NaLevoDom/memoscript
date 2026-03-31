#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys

from common import is_db_exist, validate_name, validate_deck_name
from session import session
from create_card import create_card
from create_template import create_template
from create_deck import create_deck
from update_card import update_card
from update_template import update_template
from delete_card import delete_card
from delete_template import delete_template
from show_deck import show_deck

# Обеспечиваем, что при запуске скрипта его директория в sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
os.chdir(SCRIPT_DIR)

def get_limit(limit):
    if limit == 'inf':
        return float('+inf')
    limit = float(limit)
    if limit == 0:
        raise ValueError()
    return limit

def build_parser():
    parser = argparse.ArgumentParser(
        prog='memo.py',
        description='memoscript система интервального повторения',
    )
    subparsers = parser.add_subparsers(dest='command', help='доступные команды')
    p_session = subparsers.add_parser('session', help='запустить сессию повторений')
    p_session.add_argument(dest = "deck_id", type = is_db_exist)
    p_session.add_argument(dest ='template_id')
    p_session.add_argument('-c', '--card-ids', nargs = '+')
    p_session.add_argument('-l', '--limit', type = get_limit)
    p_session.add_argument('-a', '--ad-hoc', action = 'store_true')
    p_create = subparsers.add_parser('create', help='создать deck/card/template')
    create_sub = p_create.add_subparsers(dest='create_cmd', required=True)
    cc_sub = create_sub.add_parser('card', help='создать карточку')
    cc_sub.add_argument(dest = "deck_id", type = is_db_exist)
    cc_sub.add_argument(dest = 'fields', nargs = '+')
    ct_sub = create_sub.add_parser('template', help='создать шаблон')
    ct_sub.add_argument(dest = "deck_id", type = is_db_exist)
    ct_sub.add_argument(dest ='template_id', type = validate_name)
    ct_sub.add_argument(dest = 'answer_field')
    ct_sub.add_argument(dest = 'question_forms', nargs = '+')
    ct_sub.add_argument('-e', '--manual-evaluation', action = 'store_true')
    cd_sub = create_sub.add_parser('deck', help='создать колоду')
    cd_sub.add_argument(dest = "deck_id", type = validate_deck_name)
    cd_sub.add_argument(dest = 'field_names', nargs = '+', type = validate_name)
    p_update = subparsers.add_parser('update', help='обновить card/template')
    update_sub = p_update.add_subparsers(dest='update_cmd', required=True)
    uc_sub = update_sub.add_parser('card', help='обновить карточку')
    uc_sub.add_argument(dest = "deck_id", type = is_db_exist)
    uc_sub.add_argument(dest = "card_id")
    uc_sub.add_argument(dest = 'fields', nargs = '+')
    ut_sub = update_sub.add_parser('template', help='обновить шаблон')
    ut_sub.add_argument(dest = "deck_id", type = is_db_exist)
    ut_sub.add_argument(dest ='template_id')
    ut_sub.add_argument(dest = 'answer_field')
    ut_sub.add_argument(dest = 'question_forms', nargs = '+')
    ut_sub.add_argument('-e', '--manual-evaluation', action = 'store_true')
    p_delete = subparsers.add_parser('delete', help='удалить card/template')
    delete_sub = p_delete.add_subparsers(dest='delete_cmd', required=True)
    dc_sub = delete_sub.add_parser('card', help='удалить карточку')
    dc_sub.add_argument(dest = "deck_id", type = is_db_exist)
    dc_sub.add_argument('-c', '--card-ids', nargs = '+')
    dt_sub = delete_sub.add_parser('template', help='удалить шаблон')
    dt_sub.add_argument(dest = "deck_id", type = is_db_exist)
    dt_sub.add_argument(dest ='template_id')
    p_show = subparsers.add_parser('show', help='показать deck')
    show_sub = p_show.add_subparsers(dest='show_cmd', required=True)
    sd_sub = show_sub.add_parser('deck', help='показать колоду')
    sd_sub.add_argument(dest = "deck_id", type = is_db_exist)
    return parser


def main():
    parser = build_parser()
    args, remaining = parser.parse_known_args()
    if args.command == 'session':
        session(args)
    elif args.command == 'create':
        if args.create_cmd == 'card':
            create_card(args)
        elif args.create_cmd == 'template':
            create_template(args)
        elif args.create_cmd == 'deck':
            create_deck(args)
    elif args.command == 'update':
        if args.update_cmd == 'card':
            update_card(args)
        elif args.update_cmd == 'template':
            update_template(args)
    elif args.command == 'delete':
        if args.delete_cmd == 'card':
            delete_card(args)
        elif args.command == 'template':
            delete_template(args)
    elif args.command == 'show':
        if args.show_cmd == 'deck':
            show_deck(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
