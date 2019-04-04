# IPParser

The IPParser Python module was created to simplify accepting IPv4 addresses, DNS names, and target / host information when creating other security or network tools. User inputs are taken and parsed to provide a list of IPv4 addresses or DNS names that can be used for iteration. If called with ```resolve=True```, ipparser will attempt to perform "A" record lookups and returns all IP addresses found for the host.

#### Inputs:
IPParser currently accepts the following user inputs:
* Single IP (192.168.1.10)
* IP ranges (192.168.1.1-55)
* Multiple IP's (192.168.1.3,192.168.1.7,m8r0wn.com)
* CIDR /24, /16, /8 (192.168.1.0/24)
* DNS Names (m8r0wn.com)
* .txt files (Containing any of the items listed)

## Install
```bash
git clone https://github.com/m8r0wn/ipparser
cd ipparser
python3 setup.py install
```

## Usage
```python
>>> from ipparser import ipparser
>>> ipparser('192.168.1.3-5')
['192.168.1.3', '192.168.1.4', '192.168.1.5']

>>> ipparser('yahoo.com',resolve=True)
['98.138.219.232', '98.138.219.231', '72.30.35.9', '72.30.35.10', '98.137.246.7', '98.137.246.8']

>>> ipparser('example', resolve=True, verbose=True)
"IPParser Error: Invalid or unsupported input provided : 'example'"

>>> ipparser('192.168.1.1,yahoo.com')
['192.168.1.1', 'yahoo.com']

>>> ipparser('192.168.1.1,yahoo.com,example', resolve=True, verbose=True)
IPParser Error: 'example'
['192.168.1.1', '98.137.246.7', '72.30.35.10', '98.137.246.8', '98.138.219.231', '98.138.219.232', '72.30.35.9']

>>> ipparser('192.168.1.1,yahoo.com,example', resolve=True)
['192.168.1.1', '72.30.35.10', '98.138.219.231', '98.137.246.7', '98.137.246.8', '72.30.35.9', '98.138.219.232']
```

## Argparse Integration
* Standard Argument:
```python
from ipparser import ipparser
from argparse import ArgumentParser

args = ArgumentParser(description='ipparser Integration with argparse')
args.add_argument('-host', dest='host', default=False, type=lambda x: ipparser(x, resolve=True), help='Host Input')
args = args.parse_args()
```

* Positional Argument:
```python
from ipparser import ipparser
from argparse import ArgumentParser

args = ArgumentParser(description='ipparser Integration with argparse')
args.add_argument(dest='positional_host', nargs='+', type=lambda x: ipparser(x, resolve=False, verbose=True), help='Host Input')
args = args.parse_args()
```
