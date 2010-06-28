#!/usr/bin/env python
# encoding: utf-8
"""
math.py

Created by Bradford A Toney on 2010-06-27.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
import math
def logistic(x):
    """
    @todo: WRITEME
    """
    return 1./(1+math.exp(-x))

def round(f):
    return int(f + 0.5)


