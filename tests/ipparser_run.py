#!/usr/bin/env python3
# Author: @m8r0wn
# Description: test ipparser development changes.

from sys import path, argv
path.append('..')
from ipparser import ipparser

target=argv[-1]
print('[*] Testing Input: {}'.format(target))
x= ipparser(target, resolve=True, ns=['1.1.1.1'], debug=True)
print('[*] {} Result(s)'.format(len(x)))
print(x)