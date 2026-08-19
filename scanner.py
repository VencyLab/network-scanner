import argparse
import socket
import ipaddress

services = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    21: "FTP",
    3306: "MySQL",
}

parser = argparse.ArgumentParser()
parser.add_argument("--host", help="Target IP address")
parser.add_argument("--ports", help="Port range, e.g. 1-1024")
parser.add_argument("--network", help="IP/Network")
args = parser.parse_args()

def is_host_up(ip):
        for port in services:
            sock = socket.socket()
            sock.settimeout(1)
            result = sock.connect_ex((str(ip), port))
            sock.close()
            if result == 0:
                return True
        return False

if args.host and args.ports:
    ip = str(args.host)
    port = str(args.ports)
    print(f"Scanning {ip} ports {port}")

    if "-" in args.ports:
        position = port.find("-")
        start = int(port[:position])
        end = int(port[position+1:])
        count = 0
        for x in range(start, end+1):
            systemPort = services.get(x, "Unknown")
            sock = socket.socket()
            sock.settimeout(1)
            result = sock.connect_ex((ip, x))
            if result == 0:
                print(f"Port {systemPort} : {x} Open")
                count += 1
            sock.close()
        print(f"\nScan complete. {count} open ports found.")

    else:
        systemPort = services.get(int(port), "Unknown")
        sock = socket.socket()
        sock.settimeout(1)
        result = sock.connect_ex((ip, int(port)))
        if result == 0:
            print(f"Port {systemPort} : {args.ports} Open")
            count = 1
        else:
            print(f"Port {systemPort} : {args.ports} Close")
            count = 0
        print(f"\nScan complete. {count} open ports found.")
        sock.close()
elif args.network:
    network = ipaddress.ip_network(args.network)
    count = 0
    for ip in network.hosts():
        if is_host_up(ip):
            print(f"Host {ip} is UP!")
            count += 1
    print(f"\nScan complete. {count} hosts found.")
else:
    print("Unknown")