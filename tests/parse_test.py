#!/usr/bin/env python3
# Author: @m8r0wn
# Description: Test ipparser module

from ipparser import ipparser
from os import remove

print("[ * ] DNS Name")
print("[ * ] Resolve=False, silent=False, exit_on_error=True, debug=True")
tmp = ipparser('m8r0wn.com', resolve=False, debug=True)
print("[<--] {}\n".format(tmp))


print("[ * ] DNS Name")
print("[ * ] Resolve=True, silent=False, exit_on_error=True, debug=True")
tmp = ipparser('google-public-dns-a.google.com', resolve=True, debug=True)
print("[<--] {}\n".format(tmp))


print("[ * ] Internal DNS Name")
print("[ * ] Resolve=False, silent=False, exit_on_error=True, debug=True")
tmp = ipparser('m8r0wn.demo.local', resolve=False, debug=True)
print("[<--] {}\n".format(tmp))


print("[ * ] CIDR /24")
print("[ * ] Resolve=False, silent=False, exit_on_error=True, debug=True")
tmp = len(ipparser('192.168.1.0/24', resolve=False, debug=True))
print("[<--] count: {}\n".format(tmp))


print("[ * ] CIDR /19")
print("[ * ] Resolve=False, silent=False, exit_on_error=True, debug=True")
tmp = len(ipparser('192.168.1.0/16', resolve=False, debug=True))
print("[<--] count: {}\n".format(tmp))


print("[ * ] IP Range")
print("[ * ] Resolve=False, silent=False, exit_on_error=True, debug=True")
tmp = ipparser('10.0.0.1-5', resolve=False, debug=True)
print("[<--] {}\n".format(tmp))


print("[ * ] Multiple IP's")
print("[ * ] Resolve=False, silent=False, exit_on_error=True, debug=True")
tmp = ipparser('10.0.0.1,192.168.1.1', resolve=False, debug=True)
print("[<--] {}\n".format(tmp))


print("[ * ] Multiple IP's + DNS")
print("[ * ] Resolve=True, silent=False, exit_on_error=True, debug=True")
tmp = ipparser('10.0.0.1,google-public-dns-a.google.com', resolve=True, debug=True)
print("[<--] {}\n".format(tmp))


print("[ * ] Multiple IP's + DNS")
print("[ * ] Resolve=False, silent=False, exit_on_error=True, debug=True")
tmp = ipparser('10.0.0.1,m8r0wn.com', resolve=False, debug=True)
print("[<--] {}\n".format(tmp))


print("[ * ] Single IP")
print("[ * ] Resolve=False, silent=False, exit_on_error=True, debug=True")
tmp = ipparser('10.0.0.1', resolve=False, debug=True)
print("[<--] {}\n".format(tmp))


op = open('tmp.txt', 'w')
op.write('127.0.0.1\n')
op.write('google-public-dns-a.google.com\n')
op.write('10.0.0.1,10.0.0.2\n')
op.write('172.16.0.1-25\n')
op.close()

print("[ * ] Txt File")
print("[ * ] Resolve=False, silent=False, exit_on_error=True, debug=True")
tmp = ipparser('tmp.txt', debug=True)
print("[<--] {}\n".format(tmp))


print("[ * ] Txt File")
print("[ * ] Resolve=True, silent=False, exit_on_error=True, debug=False")
tmp = ipparser('tmp.txt', resolve=True, debug=False)
print("[<--] {}\n".format(tmp))

remove('tmp.txt')