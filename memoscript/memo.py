#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys

import utils
from session import session

# Обеспечиваем, что при запуске скрипта его директория в sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
os.chdir(SCRIPT_DIR)


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
    ct_sub.add_argument('-e', '--manual-evaluation', action = 'store_true')
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
    ut_sub.add_argument('-e', '--manual-evaluation', action = 'store_true')
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
    if args.command == 'session':        
        session(args)
    elif args.command == 'create':
        if args.create_cmd == 'card':
            utils.create_card(args)
        elif args.create_cmd == 'template':
            utils.create_template(args)
        elif args.create_cmd == 'deck':
            utils.create_deck(args)
    elif args.command == 'update':
        if args.update_cmd == 'card':
            utils.update_card(args)
        elif args.update_cmd == 'template':
            utils.update_template(args)
    elif args.command == 'delete':
        if args.delete_cmd == 'card':
            utils.delete_card(args)
        elif args.command == 'template':
            utils.delete_template(args)
    elif args.command == 'show':
        if args.show_cmd == 'deck':
            utils.show_deck(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
