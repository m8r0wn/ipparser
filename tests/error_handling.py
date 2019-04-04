#!/usr/bin/env python3
# Author: @m8r0wn
# Description: Test ipparser module error handling

from ipparser import ipparser
from os import remove

op = open('tmp.txt', 'w')
op.write('127.0.1\n')
op.write('google\n')
op.write('10.0.0.1,10.2\n')
op.write('172.16.0.1-172.16.0.6\n')
op.close()

print("[ * ] Txt File with Intentional Errors")
print("[ * ] Resolve=False, Verbose=True, Debug=True")
tmp = ipparser('tmp.txt', verbose=True, debug=True)
print("[<--] {}\n".format(tmp))

print("[ * ] Txt File with Intentional Errors")
print("[ * ] Resolve=True, Verbose=True, Debug=True")
tmp = ipparser('tmp.txt', resolve=True, verbose=True, debug=True)
print("[<--] {}\n".format(tmp))

print("[ * ] Txt File with Intentional Errors")
print("[ * ] Resolve=True, Verbose=True, Debug=False")
tmp = ipparser('tmp.txt', resolve=True, verbose=True, debug=False)
print("[<--] {}\n".format(tmp))

print("[ * ] Txt File with Intentional Errors")
print("[ * ] Resolve=True, Verbose=False, Debug=False")
tmp = ipparser('tmp.txt', resolve=True, verbose=False, debug=False)
print("[<--] {}\n".format(tmp))

remove('tmp.txt')