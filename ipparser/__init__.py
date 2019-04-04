#!/usr/bin/env python3

"""
    IPParser v0.1dev
    Author: @m8r0wn
    https://github.com/m8r0wn/ipparser
    Released under BSD 3-Clause License, see LICENSE file for details
    Copyright (C) 2019 m8r0wn All rights reserved
"""

from dns.resolver import Resolver
from sys import stdout, exit
from re import compile
from os import path

REGEX = {
    'single': compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"),
    'range' : compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}-\d{1,3}$"),
    'dns'   : compile("^.+\.[a-z|A-Z]{2,}$")
}

def ipparser(host_input, resolve=False, verbose=False, debug=False):
    host_input = str(host_input).strip()
    output = []
    try:
        # TXT File
        if host_input.endswith(('.txt')):
            if debug:
                stdout.write("[-->] Input: {}, Classification: txt\n".format(host_input))
            if path.exists(host_input):
                output = parse_txt(host_input, resolve, verbose, debug)
            else:
                raise Exception('Input file not found')

        # Multiple (handle single IP & DNS names)
        elif "," in host_input:
            if debug:
                stdout.write("[-->] Input: {}, Classification: multi\n".format(host_input))
            output = parse_multi(host_input, resolve, verbose, debug)

        # DNS Name
        elif REGEX['dns'].match(host_input) and "," not in host_input:
            if debug:
                stdout.write("[-->] Input: {}, Classification: dns\n".format(host_input))
            if resolve:
                output = parse_dnsname(host_input)
            else:
                output = [host_input]

        # Regex (only: /8, /16, /24 supported at this time)
        elif host_input[-2] == "/" or host_input[-3] == "/":
            if debug:
                stdout.write("[-->] Input: {}, Classification: cidr\n".format(host_input))
            mask = host_input.split("/")[1]
            if mask == '24':
                output = parse_cidr24(host_input)
            elif mask == '16':
                output = parse_cidr16(host_input)
            elif mask == '8':
                output = parse_cidr8(host_input)
            else:
                raise Exception('Invalid CIDR (Supported Ranges: /24, /16, /18)')

        # IP Range
        elif REGEX['range'].match(host_input):
            if debug:
                stdout.write("[-->] Input: {}, Classification: range\n".format(host_input))
            output = parse_iprange(host_input)

        # Single IP
        elif REGEX['single'].match(host_input):
            if debug:
                stdout.write("[-->] Input: {}, Classification: single\n".format(host_input))
            output = [host_input]

        else:
            raise Exception('Invalid or unsupported input provided : \'{}\''.format(host_input))
    except KeyboardInterrupt:
        exit(0)
    except Exception as e:
        return str("IPParser Error: {}".format(str(e)))
    return output

def parse_txt(host_input, resolve, verbose, debug):
    output = []
    tmp_file = [line.strip() for line in open(host_input)]
    for item in tmp_file:
        try:
            tmp = ipparser(str(item).strip(), resolve, verbose, debug)
            if type(tmp) is list:
                output = output + tmp
            elif debug:
                # debug > verbose
                stdout.write("IPParser Error: \'{}\' ({}:{}), Reason: [{}]\n".format(str(item).strip(), host_input, str(tmp_file.index(item) + 1), tmp.split(":")[1]))
            elif verbose:
                stdout.write("IPParser Error: \'{}\' ({}:{})\n".format(str(item).strip(), host_input, str(tmp_file.index(item)+1)))
        except Exception as e:
            if verbose:
                stdout.write(e)
    return output

def parse_cidr24(host_input):
    output = []
    a = host_input.split("/")[0].split(".")
    for x in range(0, 256):
        tmp = a[0] + "." + a[1] + "." + a[2] + "." + str(x)
        output.append(tmp)
    return output

def parse_cidr16(host_input):
    output = []
    a = host_input.split("/")[0].split(".")
    for x in range(0, 256):
        for y in range(0, 256):
            tmp = a[0] + "." + a[1] + "." + str(x) + "." + str(y)
            output.append(tmp)
    return output

def parse_cidr8(host_input):
    output = []
    a = host_input.split("/")[0].split(".")
    for x in range(0, 256):
        for y in range(0, 256):
            for z in range(0, 256):
                tmp = a[0] + "." + str(x) + "." + str(y) + "." + str(z)
                output.append(tmp)
    return output

def parse_iprange(host_input):
    output = []
    a = host_input.split("-")
    if not REGEX['single'].match(a[0]) or int(a[1]) > 255:
        raise Exception('IPParser Error: Invalid IP range')
    b = a[0].split(".")
    for x in range(int(b[3]), int(a[1])+1):
        tmp = b[0] + "." + b[1] + "." + b[2] + "."+ str(x)
        output.append(tmp)
    return output

def parse_multi(host_input, resolve, verbose, debug):
    output = []
    for item in host_input.split(","):
        try:
            tmp = ipparser(str(item).strip(), resolve, verbose, debug)
            if type(tmp) is list:
                output = output + tmp
            elif debug:
                # debug > verbose
                stdout.write("IPParser Error: \'{}\', Reason: [{}]\n".format(str(item).strip(), tmp.split(":")[1]))
            elif verbose:
                stdout.write("IPParser Error: \'{}\'\n".format(str(item).strip()))
        except Exception as e:
            if verbose:
                stdout.write(e)
    return output

def parse_dnsname(host_input):
    output = []
    try:
        res = Resolver()
        res.timeout = 3
        res.lifetime = 3
        dns_query = res.query(host_input, "A")
        dns_query.nameservers = ['8.8.8.8', '8.8.4.4']
        for ip in dns_query:
            if REGEX['single'].match(str(ip)):
                output.append(str(ip))
    except Exception as e:
        raise Exception('IPParser Error: Could not Resolve \'{}\''.format(host_input))
    return output