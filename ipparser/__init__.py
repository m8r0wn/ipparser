"""
    IPParser v0.3.3
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

def ipparser(host_input, resolve=False, allow_port=False, silent=False, exit_on_error=True, debug=False):
    host_input = str(host_input).strip()
    output = []
    try:
        # TXT File
        if host_input.endswith(('.txt')):
            if debug:
                stdout.write("[-->] Input: {}, Classification: .txt File\n".format(host_input))
            if path.exists(host_input):
                output = parse_txt(host_input, resolve, allow_port, silent,exit_on_error, debug)
            else:
                raise Exception('Input file: \'{}\' not found\n'.format(host_input))

        # Multiple (handle single IP & DNS names)
        elif "," in host_input:
            if debug:
                stdout.write("[-->] Input: {}, Classification: Multi\n".format(host_input))
            output = parse_multi(host_input, resolve, allow_port, silent, exit_on_error, debug)

        # DNS Name
        elif REGEX['dns'].match(host_input) and "," not in host_input:
            if debug:
                stdout.write("[-->] Input: {}, Classification: DNS\n".format(host_input))
            if resolve:
                output = parse_dnsname(host_input)
            else:
                output = [host_input]

        # CIDR
        elif host_input[-2] == "/" or host_input[-3] == "/":
            if debug:
                stdout.write("[-->] Input: {}, Classification: CIDR\n".format(host_input))
            cidr = int(host_input.split("/")[1])
            if cidr < 8 or cidr > 32:
                raise Exception('Invalid CIDR detected: \'{}\'\n'.format(host_input))
            output = parse_cidr(host_input)

        # IP Range
        elif REGEX['range'].match(host_input):
            if debug:
                stdout.write("[-->] Input: {}, Classification: range\n".format(host_input))
            output = parse_iprange(host_input)

        # Single IP
        elif REGEX['single'].match(host_input):
            if debug:
                stdout.write("[-->] Input: {}, Classification: Single\n".format(host_input))
            output = [host_input]

        # Single IP + Port ("127.0.0.1:8080")
        elif allow_port and ":" in host_input:
            if debug:
                stdout.write("[-->] Input: {}, Classification: Port\n".format(host_input))
            output = verify_port(host_input, silent, exit_on_error)

        else:
            raise Exception('Invalid or unsupported input provided: \'{}\'\n'.format(host_input))
    except KeyboardInterrupt:
        exit(0)
    except Exception as e:
        if not silent:
            stdout.write(str("IPParser Error: {}".format(str(e))))
        if exit_on_error:
            exit(1)
    return output

def parse_txt(host_input, resolve, allow_port, silent, exit_on_error, debug):
    output = []
    tmp_file = [line.strip() for line in open(host_input)]
    for item in tmp_file:
        try:
            tmp = ipparser(str(item).strip(), resolve, allow_port, silent, exit_on_error, debug)
            if type(tmp) is list:
                output = output + tmp
        except Exception as e:
            if not silent:
                stdout.write(str("IPParser Error: {}\n".format(str(e))))
            if exit_on_error:
                exit(1)
    return output

def cidr_ranges(cidr):
    a = []
    b = []
    c = []
    div = (cidr//8)
    mod = (cidr%8)
    mod = abs(mod-8)
    classes = {}
    power = (2 ** mod)
    if div == 4:
        a = range(0,1)
        b = range(0,1)
        c = range(0,1)
    elif div == 3:
        a = range(0,1)
        b = range(0,1)
        c = range(0,power)
    elif div ==2:
        a = range(0,1)
        b = range(0,power)
        c = range(0,256)
    elif div == 1:
        a = range(0,power)
        b = range(0,256)
        c = range(0,256)
    elif div == 0:
        a = range(0,255)
        b = range(0,255)
        c = range(0,255)
    classes["a"] = a
    classes["b"] = b
    classes["c"] = c
    return classes

def parse_cidr(host_input):
    output = []
    ip_base = host_input.split("/")[0]
    cidr = int(host_input.split("/")[1])
    ip_base = ip_base.split(".")
    classes = cidr_ranges(cidr)
    for a in classes["a"]:
        for b in classes["b"]:
            for c in classes["c"]:
                tmp = ip_base[0] + "." + str(int(ip_base[1]) + a) + "." + str(int(ip_base[2]) + b) + "." + str(int(ip_base[3]) + c)
                output.append(tmp)
    return output

def parse_iprange(host_input):
    output = []
    a = host_input.split("-")
    if not REGEX['single'].match(a[0]) or int(a[1]) > 255:
        raise Exception('IPParser Error: Invalid IP range\n')
    b = a[0].split(".")
    for x in range(int(b[3]), int(a[1])+1):
        tmp = b[0] + "." + b[1] + "." + b[2] + "."+ str(x)
        output.append(tmp)
    return output

def parse_multi(host_input, resolve, allow_port, silent, exit_on_error, debug):
    output = []
    for item in host_input.split(","):
        try:
            tmp = ipparser(str(item).strip(), resolve, allow_port, silent, exit_on_error, debug)
            if type(tmp) is list:
                output = output + tmp
        except Exception as e:
            if not silent:
                stdout.write(str("IPParser Error: {}\n".format(str(e))))
            if exit_on_error:
                exit(1)
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
    except:
        raise Exception('Could not Resolve \'{}\'\n'.format(host_input))
    return output

def verify_port(host_input, silent, exit_on_error):
    try:
        tmp = host_input.split(":")
        if REGEX['single'].match(tmp[0]) and int(tmp[1]):
                return [host_input]
        else:
            raise Exception("Failed to extract port from: \'{}\'\n".format(host_input))
    except Exception as e:
        if not silent:
            stdout.write(str("IPParser Error: {}".format(str(e))))
        if exit_on_error:
            exit(1)