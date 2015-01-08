#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   set.py
Author:     Chen Yanfei
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

from distutils.core import setup

VERSION = '1.0.1'

setup(
    version=VERSION,
    name='finance',
    author='Chen Yanfei',
    author_email='fasionchan@gmail.com',
    packages=[
        'finance',
    ],
    package_dir = {
        '': 'packages',
    },
    scripts=[
        'scripts/realtime',
    ],
)
