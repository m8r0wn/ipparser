# IPParser

The IPParser Python module was created to simplify accepting IPv4 addresses, DNS names, and target / host information when creating other security or network tools. User inputs are taken and parsed to provide a list of IPv4 addresses or DNS names that can be used for iteration. If called with ```resolve=True```, ipparser will attempt to perform "A" record lookups and returns all IP addresses found for the host.

#### Inputs:
IPParser currently accepts the following user inputs:
* Single IP (192.168.1.10)
* IP ranges (192.168.1.1-55)
* Multiple IP's (192.168.1.3,192.168.1.7,m8r0wn.com)
* CIDR Ranges /8-/32 (192.168.1.0/24)
* URL's (https://m8r0wn.com/demo)
* IP:Port (192.168.1.1:8080)
* DNS Names (m8r0wn.com)
* TXT files (Containing any of the items listed)

## Install
```bash
pip3 install ipparser
```
OR 
```bash
git clone https://github.com/m8r0wn/ipparser
cd ipparser
python3 setup.py install
```

## Usage:
The IPParser function can be called with the following arguments (shown with their default values):
* ```resolve=False``` - Resolve any DNS names identified, to IPv4 addresses, and append to output.
* ```silent=False``` - Do not show errors while parsing.
* ```exit_on_error=True``` - Exit on errors found while parsing user input.
* ```debug=False``` - Show input classification for debugging.

## Examples
```python
>>> from ipparser import ipparser
>>> ipparser('192.168.1.3-5')
['192.168.1.3', '192.168.1.4', '192.168.1.5']

>>> ipparser('yahoo.com',resolve=True)
['98.138.219.232', '98.138.219.231', '72.30.35.9', '72.30.35.10', '98.137.246.7', '98.137.246.8']

>>> ipparser('example', resolve=True, exit_on_error=False)
IPParser Error: Invalid or unsupported input provided 'example'

>>> ipparser('192.168.1.1,yahoo.com')
['192.168.1.1', 'yahoo.com']

ipparser('192.168.1.1,yahoo.com,example', resolve=True, exit_on_error=False)
IPParser Error: Invalid or unsupported input provided 'example'
['192.168.1.1', '98.138.219.231', '98.137.246.8', '98.137.246.7', '72.30.35.9', '98.138.219.232', '72.30.35.10']

>>> ipparser('192.168.1.1,yahoo.com,example', resolve=True, silent=True)
['192.168.1.1', '72.30.35.10', '98.138.219.231', '98.137.246.7', '98.137.246.8', '72.30.35.9', '98.138.219.232']
```

## Argparse Integration
* Standard Argument:
```python
from ipparser import ipparser
from argparse import ArgumentParser

args = ArgumentParser(description='ipparser integration with argparse')
args.add_argument('-host', dest='host', default=False, type=lambda x: ipparser(x), help='Host Input')
args = args.parse_args()
```
```
Namespace(host=['192.168.1.1'])
```

* Required Positional Argument (Method 1):
```python
from ipparser import ipparser
from argparse import ArgumentParser

args = ArgumentParser(description='ipparser integration with argparse')
args.add_argument(dest='positional_host', nargs='+', type=lambda x: ipparser(x, resolve=False), help='Host Input')
args = args.parse_args()
```
```
Namespace(positional_host=[['192.168.1.1']])
```

* Required Positional Argument (Method 2):
```python
from ipparser import ipparser
from argparse import ArgumentParser

args = ArgumentParser(description='ipparser integration with argparse')
args.add_argument(dest='positional_host', nargs='+', help='Host Input')
args = args.parse_args()
args.positional_host = ipparser(args.positional_host[0]) 
```
```
positional_host=['192.168.1.1'])
```

* Allow user args to determine resolve setting:
```python
from sys import argv
from ipparser import ipparser
from argparse import ArgumentParser

r = False
if "-r" in argv:
    r = True
    
args = ArgumentParser(description='ipparser integration with argparse')
args.add_argument('-r', dest='resolve',action='store_true', help='Resolve input DNS hosts')
args.add_argument(dest='positional_host', nargs='+', type=lambda x: ipparser(x, resolve=r), help='Host Input')
args = args.parse_args()
```

## Sys.argv Usage
* Standard Argument
```python
from sys import argv
from ipparser import ipparser

if "-host" in argv:
    host = ipparser(argv[argv.index("-host") + 1])
```
```
host = ['192.168.1.1']
```

* Positional Argument
```python
from sys import argv
from ipparser import ipparser

host = ipparser(argv[-1])
```
```
host = ['192.168.1.1']
```

## Contributors
* [@darneymartin](https://github.com/darneymartin)
