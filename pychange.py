#!/usr/bin/env python
import re
import subprocess
import argparse


class PyChange():

    def __init__(self):
        print("╔══════════╗")
        print("║ PyChange ║")
        print("╚══════════╝") 

    def get_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--interface", dest="interface", help="Interface to change Mac Address")
        parser.add_argument("-m", "--mac", dest="new_mac", help="New Mac Address")
        args = parser.parse_args()
        if not args.interface:
            parser.error("[-] Specify an interface, use --help for more info!")
        elif not args.new_mac:
            parser.error("[-] Specify a new mac, use --help for more info!")
        return args

    def change_mac(self, interface, new_mac):
        print("[+] Changing MAC address for " + interface + " to " + new_mac)
        subprocess.run(["ifconfig", interface, "down"])
        subprocess.run(["ifconfig", interface, "hw", "ether", new_mac])
        subprocess.run(["ifconfig", interface, "up"])

    def get_mac(self, interface):
        ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode()
        print(">-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-<")
        mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
        if mac_result:
            return mac_result.group(0)
        else:
            print("[-] could not read Mac address")    

if __name__ == "__main__":

    a = PyChange()
    args = a.get_arguments()

    current_mac = a.get_mac(args.interface)
    print("Current MAC = " + str(current_mac))

    a.change_mac(args.interface, args.new_mac)
    current_mac = a.get_mac(args.interface)
    if current_mac == args.new_mac:
        print("[+] MAC addres was succesfully changed to " + current_mac)
    else:
        print("[-] MAC addres didn't get changed")
