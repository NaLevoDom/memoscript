#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import runpy
import sys

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

    subparsers.add_parser('session', help='запустить сессию повторений')

    p_create = subparsers.add_parser('create', help='создать deck/card/template')
    create_sub = p_create.add_subparsers(dest='create_cmd', required=True)
    create_sub.add_parser('deck', help='создать колоду')
    create_sub.add_parser('card', help='создать карточку')
    create_sub.add_parser('template', help='создать шаблон')

    p_update = subparsers.add_parser('update', help='обновить card/template')
    update_sub = p_update.add_subparsers(dest='update_cmd', required=True)
    update_sub.add_parser('card', help='обновить карточку')
    update_sub.add_parser('template', help='обновить шаблон')

    p_delete = subparsers.add_parser('delete', help='удалить card/template')
    delete_sub = p_delete.add_subparsers(dest='delete_cmd', required=True)
    delete_sub.add_parser('card', help='удалить карточку')
    delete_sub.add_parser('template', help='удалить шаблон')

    p_show = subparsers.add_parser('show', help='показать deck')
    show_sub = p_show.add_subparsers(dest='show_cmd', required=True)
    show_sub.add_parser('deck', help='показать колоду')

    return parser


def main():
    parser = build_parser()
    args, remaining = parser.parse_known_args()

    if args.command == 'session':
        module_name = 'session'
    elif args.command == 'create':
        module_name = f'create_{args.create_cmd}'
    elif args.command == 'update':
        module_name = f'update_{args.update_cmd}'
    elif args.command == 'delete':
        module_name = f'delete_{args.delete_cmd}'
    elif args.command == 'show':
        module_name = f'show_{args.show_cmd}'
    else:
        parser.print_help()
        sys.exit(1)

    sys.argv = ['memo.py'] + remaining
    runpy.run_module(module_name, run_name='__main__')


if __name__ == '__main__':
    main()
