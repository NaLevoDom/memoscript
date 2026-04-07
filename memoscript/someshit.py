#!/usr/bin/env python
# -*- coding: utf-8 -*-

from session import session


if __name__ == '__main__':
    i = session() # помимо прочего нужно передать несколько callback функций, а именно:
    while True:
        try:
            r = next(i)
        except Exception as e:
            pass
        # someshit here
        if r.type == 'end':
            pass
        elif r.type == ''









