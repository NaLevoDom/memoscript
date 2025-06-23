#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re

def sss(s):
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
        sys.exit(0)
    return l

if __name__ == '__main__':
    
    print(sss("42-53"))
    print(sss('4'))
    print(sss("8-3"))
    
    
    
    