import argparse
import socket
import ipaddress
import threading

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

count = 0
lock = threading.Lock()

def is_host_up(ip):
        global count
        for port in services:
            sock = socket.socket()
            sock.settimeout(1)
            result = sock.connect_ex((str(ip), port))
            sock.close()
            if result == 0:
                print(f"Host {ip} is UP!")
                with lock:
                    count += 1
                return
        return False

if args.host and args.ports:
    ip = str(args.host)
    port = str(args.ports)
    print(f"Scanning {ip} ports {port}")

    if "-" in args.ports:
        position = port.find("-")
        start = int(port[:position])
        end = int(port[position+1:])
        for x in range(start, end+1):
            systemPort = services.get(x, "Unknown")
            sock = socket.socket()
            sock.settimeout(1)
            result = sock.connect_ex((ip, x))
            if result == 0:
                print(f"Port {systemPort} : {x} Open")
                count += 1
            sock.close()

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
        sock.close()
        
    print(f"\nScan complete. {count} open ports found.")

elif args.network:
    network = ipaddress.ip_network(args.network)
    threads = []
    for ip in network.hosts():
        t = threading.Thread(target=is_host_up, args=(ip,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    print(f"\nScan complete. {count} hosts found.")
else:
    print("Unknown")