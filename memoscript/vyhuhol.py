#!/usr/bin/env python
# -*- coding: utf-8 -*-

from re import fullmatch
from types import SimpleNamespace
from copy import copy

class ZeroValentPositionalPattern(Exception):
    pass
    
def type_check(obj, name, types_list):
    if type(obj) not in types_list:
        l = [tp.__name__ for tp in types_list]
        s = ' or '.join(l)
        raise TypeError(f"{name}: expected {s} instance, {type(obj).__name__} found")
    
class Parser:
    def __init__(self, argv):
        type_check(argv, 'argv', [list])
        for i, arg in enumerate(argv):
            type_check(arg, 'argv[i]', [str])
        self._argv = argv
        self._positional_patterns = list()
        self._nonpositional_patterns = list()
        self._help_pattern = None
        self._help_msg = None
        self._help_clue = None
        self._defaults = None
        
    def add_pattern(self, *args, **kwargs):
        p = self._Pattern(*args, **kwargs)
        if p.positional:
            self._positional_patterns.append(p)
        else:
            self._nonpositional_patterns.append(p)
    
    def set_help_pattern(self, *args, **kwargs):
        self._help_pattern = self._Pattern(*args, **kwargs)
    
    def create_help_pattern(self):
        self._help_pattern = self._Pattern(keys = ['-h', '--help'], comment = "show this message")
    
    def create_help_clue(self):
        if self._help_pattern == None:
            self.create_help_pattern()
        self._help_clue = f"Execute «{self._argv[0]} {self._help_pattern.keys[0]}» for help"
    
    def create_help_msg(self):
        if self._help_pattern == None:
            self.create_help_pattern()
        s = 'options:\n'
        s += self._get_help_line(self._help_pattern)
        for p in self._nonpositional_patterns:
            s += self._get_help_line(p)
        if self._positional_patterns:
            s += '\npositional args:\n'
        for p in self._positional_patterns:
            s += self._get_help_line(p)
        self._help_msg = s

    def _get_help_line(self, p):
        keys_string = f" ({', '.join(p.keys)})" if p.keys else "\t\t"
        s = f"{keys_string}\t\t{p.comment}"
        if p.valency != 0:
            s += f" (takes {p.valency} args.)"
        s += '\n'
        return s
    
    class _Pattern:
        def __init__(self, 
                     set_to = dict(),
                     add_to = list(),
                     write_to = list(),
                     positional = False,
                     valency = 0,
                     keys = list(),
                     func = lambda x : x,
                     comment = ""
                     ):
            if not(callable(func)):
                raise TypeError(f'{type(func).__name__} object is not callable')
            type_check(comment, 'comment', [str])
            type_check(positional, 'positional', [bool])
            type_check(keys, 'keys', [list])
            type_check(add_to, 'add_to', [list])
            type_check(write_to, 'write_to', [list])
            type_check(set_to, 'set_to', [dict])
            self.set_to = copy(set_to)
            self.add_to = copy(add_to)
            self.set_write_to(write_to)
            self.positional = positional
            self.set_valency(valency)
            self.set_keys(keys)
            self.func = func
            self.comment = comment
            self.is_called = False
            
        def set_write_to(self, write_to):
            for name in write_to:
                self.set_to[name] = list()
                self.add_to.append(name)
        
        def set_keys(self, keys):
            for i, key in enumerate(keys):
                type_check(key, f'keys[{i}]', [str])
            self.keys = keys
        
        def set_valency(self, valency):
            self.valency = str(valency)
            if type(valency) == str:
                if valency == '*':
                    self.mn = 0
                    self.mx = float('inf')
                elif valency == '+':
                    self.mn = 1
                    self.mx = float('inf')
                elif valency == '?':
                    self.mn = 0
                    self.mx = 1
                else:
                    raise ValueError(f"valency: invalid literal, expected '*', '+' or '?', '{valency}' found")
            elif type(valency) == int:
                if valency >= 0:
                    self.mn = valency
                    self.mx = valency
                else:
                    raise ValueError(f'valency: expected int instance greater than or equal to zero, {valency} found')
            elif type(valency) == list:
                if len(valency) == 2:
                    if type(valency[0]) == int:
                        if valency[0] >= 0:
                            self.mn = valency[0]
                        else:
                            raise ValueError(f'valency[0]: expected int instance greater than or equal to zero, {valency[0]} found')
                    else:
                        raise TypeError(f'valency[0]: expected int instance, {type(valency[0]).__name__} found')
                    if type(valency[1]) == int:
                        if valency[1] >= 0:
                            self.mx = valency[1]
                        else:
                            raise ValueError(f'valency[1]: expected int instance greater than or equal to zero, {valency[1]} found')
                    elif type(valency[1]) == float:
                        if valency[1] == float('inf'):
                            self.mx = valency[1]
                        else:
                            raise ValueError(f'valency[1]: expected float("inf"), {valency[1]} found')
                    else:
                        raise TypeError(f'valency[1]: expected int or float instance, {type(valency[1]).__name__} found')
                else:
                    raise ValueError('valency: expected list 2 items long')
            else:
                raise TypeError(f'valency: expected str or int or list instance, {type(valency).__name__} found')
            if self.mx == 0 and self.positional == True:
                raise ZeroValentPositionalPattern("Zero valent pattern can't be positional")
    
    @property
    def defaults(self):
        return self._defaults
    
    @defaults.setter
    def defaults(self, a):
        type_check(a, 'defaults', [SimpleNamespace])
        self._defaults = a
    
    @property
    def help_clue(self):
        return self._help_clue
    
    @help_clue.setter
    def help_clue(self, a):
        type_check(a, 'help_clue', [str])
        self._help_clue = a
    
    @property
    def help_msg(self):
        return self._help_msg
    
    @help_msg.setter
    def help_msg(self, a):
        type_check(a, 'help_msg', [str])
        self._help_msg = a
    
    def _get_pattern_by_key(self, arg):
        for p in self._patterns:
            if arg in p.keys:
                return p
    
    def _set_values(self, p, result):
        p.is_called = True
        for set_name, set_value in p.set_to.items():
            result.__dict__[set_name] = copy(set_value)
    
    def parse(self):
        self._patterns = self._nonpositional_patterns + self._positional_patterns
        if self._help_clue == None:
            self.create_help_clue()
        if self._help_msg == None:
            self.create_help_msg()
        if self._defaults == None:
            self._defaults = SimpleNamespace()
        self._patterns.append(self._help_pattern) # DO NOT RAISE IT UP!
        positional_pattern_iter = iter(self._positional_patterns)
        result = SimpleNamespace()
        result.__dict__['argv_0'] = [self._argv[0]]
        for p in self._patterns:
            for add_name in p.add_to:
                result.__dict__[add_name] = list()
            for set_name in p.set_to:
                result.__dict__[set_name] = list()
        i = 0
        p = None
        ban = False
        for arg in self._argv[1:]:
            if not(ban) and (p == None or i >= p.mn):
                if arg == '--':
                    ban = True
                    p = None
                    continue
                pp = self._get_pattern_by_key(arg)
                if pp is self._help_pattern:
                    print(self._help_msg)
                    exit(0)
                if pp:
                    p = pp
                    i = 0
                    self._set_values(p, result)
                    if not(p.mx):
                        p = None
                    continue
                if fullmatch(r'-[a-zA-Z]{2,}', arg) != None:
                    keys = arg[1:]
                    for char in keys:
                        pp = self._get_pattern_by_key(f"-{char}")
                        if pp == None or pp.mx:
                            break
                    else:
                        p = None
                        for char in keys:
                            pp = self._get_pattern_by_key(f"-{char}")
                            self._set_values(pp, result)
                        continue
                if fullmatch(r'--.+=.*', arg) != None:
                    key, value = arg.split('=', maxsplit = 1)
                    pp = self._get_pattern_by_key(key)
                    if pp and pp.mx: # если не флаг
                        p = pp
                        i = 0
                        arg = value
                        self._set_values(p, result)
            if p == None:
                try:
                    p = next(positional_pattern_iter)
                    while p.is_called:
                        p = next(positional_pattern_iter)
                    self._set_values(p, result)
                except StopIteration:
                    exit(f"{arg} is untended arg!\n" + self._help_clue)
            try:
                add_value = p.func(arg)
                for add_name in p.add_to:
                    result.__dict__[add_name].append(add_value)
            except Exception as e:
                print(e)
                exit(f"the option can't take {arg} argument")
            i += 1
            if p and i == p.mx:
                p = None
                i = 0
        if p and i < p.mn:
            if p.mn == p.mx:
                exit(f'the option takes {p.mn} args, {i} given\n' + self._help_clue)
            exit(f'the option takes at least {p.mn} args, {i} given\n' + self._help_clue)
        for name, default_value in self._defaults.__dict__.items(): 
            try:
                result_value = result.__dict__[name]
            except KeyError:
                result_value = None
            if result_value in [None, list()]:
                if default_value == None:
                    exit(f"Missing required option '{name}'\n" + self._help_clue)
                else:
                    result.__dict__[name] = default_value
        return result
