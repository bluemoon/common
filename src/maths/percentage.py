#!/usr/bin/env python
# encoding: utf-8
"""
percentage.py

"""

import unittest

def percent(a, b):
    """
    Return percentage string of a and b, e.g.:
        "1 of 10 (10%)"
    """
    assert a <= b
    assert a >= 0
    assert b > 0
    return "%s of %s (%.2f%%)" % (a, b, 100.*a/b)

class percentage(unittest.TestCase):
    def setUp(self):
        pass
    

    
if __name__ == '__main__':
    unittest.main()