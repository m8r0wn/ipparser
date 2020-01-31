from os import path
from re import compile
from sys import stdout, exit
from dns.resolver import Resolver
from ipparser.cidr import parse_cidr
from ipparser.nmap import parse_nmap

REGEX = {
    'single': compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"),
    'range' : compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}-\d{1,3}$"),
    'cidr' : compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$"),
    'dns'   : compile("^.+\.[a-z|A-Z]{2,}$")
}

def ipparser(host_input, resolve=False, open_ports=False, silent=False, exit_on_error=True, debug=False):
    '''
    :param host_input: User Input
    :param resolve: Resolve DNS names
    :param open_ports: Return IP:Port notation for all open ports found (Nmap XML only)
    :param silent: Show error messages during parsing
    :param exit_on_error: Exit when error found
    :param debug: Show debug messages/input classifications
    '''
    host_input = str(host_input).strip()
    output = []
    try:
        # TXT File
        if host_input.lower().endswith('.txt'):
            if debug:
                stdout.write("[-->] IPParser: {} :: TXT File\n".format(host_input))
            if path.exists(host_input):
                output = parse_txt(host_input, resolve, silent,exit_on_error, debug)
            else:
                raise Exception('Input file: \'{}\' not found\n'.format(host_input))

        # Nmap XML File
        elif host_input.lower().endswith('.xml'):
            if debug:
                stdout.write("[-->] IPParser: {} :: XML File\n".format(host_input))
            if path.exists(host_input):
                output = parse_nmap(host_input, open_ports)
            else:
                raise Exception('Input file: \'{}\' not found\n'.format(host_input))

        # Multiple (handle single IP & DNS names)
        elif "," in host_input:
            if debug:
                stdout.write("[-->] IPParser: {} :: Multi\n".format(host_input))
            output = parse_multi(host_input, resolve, silent, exit_on_error, debug)

        # DNS Name
        elif REGEX['dns'].match(host_input) and "," not in host_input:
            if debug:
                stdout.write("[-->] IPParser: {} :: DNS\n".format(host_input))
            if resolve:
                output = parse_dnsname(host_input)
            else:
                output = [host_input]

        # CIDR
        elif REGEX['cidr'].match(host_input):
            if debug:
                stdout.write("[-->] IPParser: {} :: CIDR\n".format(host_input))
            cidr = int(host_input.split("/")[1])
            if cidr < 8 or cidr > 32:
                raise Exception('Invalid CIDR detected: \'{}\'\n'.format(host_input))
            output = parse_cidr(host_input)

        # IP Range
        elif REGEX['range'].match(host_input):
            if debug:
                stdout.write("[-->] IPParser: {} :: IP Range\n".format(host_input))
            output = parse_iprange(host_input)

        else:
            # Single IP - 127.0.0.1, URL - http://, Port - 127.0.0.1:8080
            if debug:
                stdout.write("[-->] IPParser: {} :: Other\n".format(host_input))
            output = [host_input]

    except KeyboardInterrupt:
        exit(0)
    except Exception as e:
        if not silent:
            stdout.write(str("IPParser Error: {}".format(str(e))))
        if exit_on_error:
            exit(1)
    return output

def parse_txt(host_input, resolve, silent, exit_on_error, debug):
    output = []
    tmp_file = [line.strip() for line in open(host_input)]
    for item in tmp_file:
        try:
            tmp = ipparser(str(item).strip(), resolve, silent, exit_on_error, debug)
            if type(tmp) is list:
                output = output + tmp
        except Exception as e:
            if not silent:
                stdout.write(str("IPParser Error: {}\n".format(str(e))))
            if exit_on_error:
                exit(1)
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

def parse_multi(host_input, resolve, silent, exit_on_error, debug):
    output = []
    for item in host_input.split(","):
        try:
            tmp = ipparser(str(item).strip(), resolve, silent, exit_on_error, debug)
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