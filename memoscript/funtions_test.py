#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt

def fun0(s, delta, old_delta):
    new_k = 2 ** (s - 2)
    new_delta = int(new_k * sqrt(delta * old_delta))
    return new_delta

def fun1(s, delta, old_delta):
    new_k = 2 ** (s - 2)
    new_delta = int(new_k * (5 * delta + old_delta) / 6)
    return new_delta

def fun2(s, delta, old_delta):
    new_k = 2 ** (s - 2)
    new_delta = int(new_k * (11 * delta + old_delta) / 12)
    return new_delta
    
def run_scenario(f, l):
    old_delta = 1
    delta = 1
    print(f"f.__name__ = {f.__name__}")
    c = 1
    for s in l:
        new_delta = f(s, delta, old_delta)
        print(f"{c}) f({s}) = {new_delta}")
        old_delta = delta
        delta = new_delta
        c += 1
        
if __name__ == '__main__':
    run_scenario(fun1, [4] * 3 + [2] + [4] * 4)
    
    run_scenario(fun1, [4] * 8)
    
    
    
    
    