#!/usr/bin/env python
# encoding: utf-8

def sign(i, assertions=True):
    """
    + or - 1
    @precondition: i != 0
    """
    if assertions:
        assert i != 0
    else:
        if i == 0: return 0

    return +1 if i > 0 else -1
