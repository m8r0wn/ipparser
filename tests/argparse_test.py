#!/usr/bin/env python3
# Author: @m8r0wn
# Description: Test ipparser compatibility with argparse
# Usage: python3 argparse_test.py -host [input-1] [input-2]

from ipparser import ipparser
from argparse import ArgumentParser

args = ArgumentParser(description='IPParser Integration with ArgParse')
args.add_argument('-host', dest='host', default=False, type=lambda x: ipparser(x, resolve=True, debug=True), help='Host Input')
args.add_argument(dest='positional_host', nargs='+', type=lambda x: ipparser(x, resolve=True, debug=True), help='Host Input')
args = args.parse_args()
print(args)