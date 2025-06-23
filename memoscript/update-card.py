#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import types

import vyhuhol

def update_deck_record(dbpath, i):
    with sqlite3.connect(dbpath) as c:
        idd = i.pop(0)
        count = 1
        s = ''
        while i:
            element = i.pop(0)
            s += f"column_{count} = '{element}', "
            count += 1
        s = s[:-2]
        q = f"UPDATE deck SET " + s + f" WHERE id = {idd}"
        c.execute(q, i)

def handle_args(args):
    p = vyhuhol.Parser(args)
    p.add_pattern(write_to = ['name'], keys = ['-n', '--name'], valency = 1, positional = True)
    p.add_pattern(write_to = ['fields'], keys = ['-f', '--fields-with-id'], valency = '+', positional = True)
    p.defaults = types.SimpleNamespace(name = None, fields = None)
    r = p.parse()
    return r

if __name__ == '__main__':
    r = handle_args(sys.argv)
    dbpath = r.name[0] + '.db'
    i = r.fields
    update_deck_record(dbpath, i)
    