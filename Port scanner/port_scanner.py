#!/usr/bin/env python3

import socket
import argparse
import sys
from termcolor import colored

def get_arguments():
    parser = argparse.ArgumentParser(description="Fast TCP Port Scanner")
    parser.add_argument("-t", "--target", dest="target", help="Victim target to scan (Ex: -t 192.168.1.1)")
    parser.add_argument("-p", "--port", dest="port", help="Port range to scan (Ex: -p 1-100)")
    options = parser.parse_args()

    if options.target is None or options.port is None:
        parser.print_help()
        sys.exit(1)

    return options.target, options.port

def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    return s

def port_scanner(port, host, s):
    try:
        s.connect((host, port))
        print(colored(f"\n[+] El puerto {port} está abierto", "red"))
        s.close()

    except (socket.timeout, ConnectionRefusedError):
        s.close()

def main():

    target, port = get_arguments()

    if "-" in port:
        ports = port.split("-")

        for port in range(int(ports[0]), int(ports[1])):
            s = create_socket()
            port_scanner(port, target, s)

    elif "," in port:
        ports = port.split(",")

        for port in ports:
            s = create_socket()
            port_scanner(int(port), target, s)

if __name__ == "__main__":
    main()
