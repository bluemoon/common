#!/usr/bin/env python
# encoding: utf-8
"""
setup.py

Created by Bradford A Toney on 2010-06-27.
"""

import os, sys
import time, glob
from time import gmtime, strftime
from setuptools import setup, find_packages, Extension

extensions = [
    Extension('modular.base', ['modular/base.pyx'], include_dirs=includes),
    
]
setup(
    name = 'common',
    packages=['common', 'common.maths'],
    package_dir = {'common': 'src'},
    
    zip_safe=False,
    test_suite = 'nose.collector',
    setup_requires = ['nose>=0.10.4'],
    entry_points = {}
)