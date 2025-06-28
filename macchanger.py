#!/usr/bin/env python3

import subprocess as sub
import optparse as opt
import re
import random

def inputs():
    """
    Gets the interface and MAC address parameters from the command line.
    """
    opt_object = opt.OptionParser()
    opt_object.add_option("-i", "--interface", dest="interface")
    opt_object.add_option("-m", "--mac", dest="mac_address")
    return opt_object.parse_args()

def random_mac():
    """
    Generates and returns a random MAC address.
    """
    mac = [random.randint(0x00, 0xff) for i in range(6)]
    return ':'.join(f"{octet:02x}" for octet in mac)

def changer(user_interface, mac_address):
    """
    Changes the MAC address of the given interface.
    First brings the interface down, changes the MAC, then brings it up.
    """
    sub.call(["ifconfig", user_interface, "down"])
    sub.call(["ifconfig", user_interface, "hw", "ether", mac_address])
    sub.call(["ifconfig", user_interface, "up"])

def controller(interface):
    """
    Returns the current MAC address of the given interface.
    """
    ifconfig = sub.check_output(["ifconfig", interface])
    new_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig))
    if new_mac:
        return new_mac.group(0)
    else:
        return None

def main():
    """
    Main function of the program. Gets parameters from the user,
    generates a random MAC address if needed, and applies the change.
    """
    while True:
        (options, args) = inputs()
        # If interface is not specified, use eth0 by default
        if not options.interface:
            options.interface = "eth0"
        # If MAC address is not specified, generate a random one
        if options.mac_address is None:
            options.mac_address = random_mac()
            print(f"New MAC Address : {options.mac_address}")
        # Change the MAC address
        changer(options.interface, options.mac_address)
        # Check if the change was successful
        finalized_mac = controller(options.interface)
        if finalized_mac and finalized_mac.lower() == options.mac_address.lower():
            break
        else:
            pass

if __name__ == "__main__":
    main()
