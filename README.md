# network-scanner

A command-line network scanner written in Python.
Built from scratch using only Python standard libraries.

> This tool is intended for use on your own network only.
> Scanning networks without permission is illegal.

## Requirements

Python 3.x - no external libraries needed.

## Usage

'''bash
# Scan ports on a specific host
python scanner.py --host <ip> --ports <range>

# Discover active hosts on a network
python scanner.py --network <cidr>
'''

## Example

'''bash
$ python scanner.py --host 192.168.1.1 --ports 1-1024
Scanning 192.168.1.1 ports 1-1024
port HTTP : 80 Open
port HTTPS : 443 Open

Scan complete. 2 open ports found.

$ python scanner.py --network 192.168.1.0/24
Host 192.168.1.1 is UP!
Host 192.168.1.5 is UP!

Scan complete. 2 hosts found.
'''