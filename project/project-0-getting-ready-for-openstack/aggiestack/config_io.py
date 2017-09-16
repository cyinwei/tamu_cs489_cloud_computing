"""
config_io.py

This module handles the I/O of the aggiestack CLI.  It reads files given by the
CLI, parses it, and stores it in a JSON state file.

In this implementation of aggiestack, the CLI loads a set of state files in
order to store its configuration settings.  The state files are JSON files which
correspond to the *machines*, *images*, and *flavors* managed by the CLI.  This
way, aggiestack will remember the configuration settings after the initial
setup.

The  default 
"""

import os
import ipaddress
import json

_MACHINE_CONFIG_TERM_AMOUNT = 5

# Use python3 to help us check valid IP addresses and numbers
def _check_num(num_as_str):
    try:
        return bool(int(num_as_str) >= 0)
    except ValueError:
        return False

def _check_ip_addr(ip_as_str):
    try:
        ipaddress.ip_address(ip_as_str)
        return True
    except ValueError:
        return False

# Check if the file formats for the different configs are valid
def _check_hardware_config_file_format(file_lines):
    if len(file_lines) == 0:
        return (False, "Empty File.\n")

    # the first line tells us how many machine configs we have
    if _check_num(file_lines[0]) is False:
        return (False, "First line (number of machine configs) is NaN.\n")

    num_machines = int(file_lines[0])

    # do the number of machines match up?
    machines = file_lines[1:]
    if len(machines) != num_machines:
        error_message = ("First line (number of machine configs) does not",
                         "match the length of the file (machine configs).\n")
        return (False, error_message)

    # check each machine config line
    for line, machine in enumerate(machines): # line is line number - 2
        config = machine.split() # split by whitespace

        # does the individual machine config have the right number of terms?
        if (len(config) != _MACHINE_CONFIG_TERM_AMOUNT):
            error_message = ("In line {}:\n".format(line + 2),
                             "Invalid number of terms.",
                             "Expected {} terms.\n".format(_MACHINE_CONFIG_TERM_AMOUNT))
            return (False, error_message)

        # does each term have the right format?
        # 0th term is a string (name of machine)
        # 1st term is an IP address
        if _check_ip_addr(config[1]) is False:
            error_message = ("In line {}:\n".format(line + 2),
                             "Invalid IP address: [{}].\n".format(config[1]))
            return (False, error_message)

        # 2nd term is an int (RAM size in GB)
        if _check_num(config[2]) is False:
            error_message = ("In line {}:\n".format(line + 2),
                             "Invalid postive num (RAM): ",
                             "[{}].\n".format(config[2]))
            return (False, error_message)
        
        # 3rd term is an int (number of disks)
        if _check_num(config[3]) is False:
            error_message = ("In line {}:\n".format(line + 2),
                             "Invalid postive num (disks): ",
                             "[{}].\n".format(config[3]))
            return (False, error_message)
 
        # 4th term is an int (number of VCPUs)
        if _check_num(config[4]) is False:
            error_message = ("In line {}:\n".format(line + 2),
                             "Invalid postive num (VCPUs): ",
                             "[{}].\n".format(config[4]))
            return (False, error_message)

    return (True, "File successfully parsed.")
 
def _check_image_config_file_format(file_lines):
    pass

def _check_flavor_config_file_format(file_lines):
    pass
