#!/usr/bin/env python3

import argparse
import subprocess
import sys
from termcolor import colored

def get_arguments():
    parser = argparse.ArgumentParser(description="Herramienta para descubrir hosts activos en una red (ICMP)")
    parser.add_argument("-t", "--target", required=True, dest="target", help="Host o rango de red a escanear")

    args = parser.parse_args()

    return args.target

def parse_target(target_str):
    target_str_splitted = target_str.split(".")
    if len(target_str_splitted) == 4:
        first_three_octets = ".".join(target_str_splitted[:3])
        if "-" in target_str_splitted[3]:
            start, end = target_str_splitted[3].split("-")
            try:
                start = int(start)
                end = int(end)
                return [f"{first_three_octets}.{i}" for i in range(start, end + 1)]
            except ValueError:
                print(colored("\n[!] El rango IP no es válido\n", "red"))
                return None
        else:
            return [target_str]
    else:
        print(colored("\n[!] El formato de IP o rango IP no es válido\n", "red"))
        return None

def host_discovery(targets):
    if targets is None:
        print(colored("[!] No se puede realizar el descubrimiento de hosts debido a un formato de IP incorrecto.", "red"))
        return

    for target in targets:
        try:
            ping = subprocess.run(["ping", "-c", "1", target], timeout=1, stdout=subprocess.DEVNULL)

            if ping.returncode == 0:
                print(colored(f"\t[i] La IP {target} está activa", "green"))
        except:
            pass

def main():
    target_str = get_arguments()
    targets = parse_target(target_str)

    if targets is None:
        sys.exit(1)

    print("\n[+] Hosts activos en la red:\n")
    host_discovery(targets)

if __name__ == "__main__":
    main()
