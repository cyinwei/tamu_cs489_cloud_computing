"""
check_config_io.py

This module does syntax error checking for the input options on the CLI.

This module handles the I/O of the aggiestack CLI.  It reads files given by the
CLI, parses it, and stores it in a JSON state file.

In this implementation of aggiestack, the CLI loads a set of state files in
order to store its configuration settings.  The state files are JSON files which
correspond to the *machines*, *images*, and *flavors* managed by the CLI.  This
way, aggiestack will remember the configuration settings after the initial
setup.
"""

import ipaddress
from enum import Enum

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

# Helper functions to check for certain terms
class TermType(Enum):
    """ Number of term Python object types (the configuration values). """
    STRING = 0
    NUM = 1
    IP_ADDR = 2

def _check_file_structure(lines):
    """
    Checks the configuration file format.

    All three (hardware, image, flavor) configuration file types share the same
    structure.  The first line contains the number of configurations.  Each
    following line represents one configuration.
    """

    if not lines:
        return (False, "Empty File.\n")

    # the first line tells us how many machine configs we have
    if _check_num(lines[0]) is False:
        return (False, "First line (number of machine configs) is NaN.\n")

    # do the number of machines match up?
    num_machines = int(lines[0])
    if len(lines)-1 != num_machines:
        error_message = ("First line (number of machine configs) does not "
                         "match the length of the file (machine configs).\n")
        return (False, error_message)

    return (True, "No errors in the file structure.")

def _check_term_types(line, term_schema):
    """
    Checks that the individual configuration (a line in the config file) is
    correct syntactially.

    Each configuration contains a name, followed by the configuration values,
    which are named 'terms'.  Different config files (hardware, images, flavor)
    have different configuration lists, which we pass into as a term_schema.

    NOTE: We just check for syntax; e.g. check the IP is syntactally valid or
    that a number is actually a positive number.  We do not check if a file
    path exists, or the numbers are obviously wrong, or if we can connect to the
    IP, etc.
    """
    terms = line.split() # split by whitespace

    if len(terms) != len(term_schema):
        error_message = ("Invalid number of terms [{}].  ".format(len(terms))
                         + "Expected [{}] terms.".format(len(term_schema)))
        return (False, error_message)

    for index, term in enumerate(terms):
        if term_schema[index] == TermType.STRING:
            pass
        elif term_schema[index] == TermType.NUM:
            if _check_num(term) is False:
                error_message = "Invalid postive num : [{}].\n".format(term)
                return (False, error_message)
        else: # term_schema[index] == TermType.IP:
            if _check_ip_addr(term) is False:
                error_message = "Invalid IP address: [{}].\n".format(term)
                return (False, error_message)

    return (True, 'No errors in the single configuration.')

def check_hardware_config_file(file_lines):
    """
    Checks that the hardware configuration file is valid.

    NOTE: Just check for format and syntax.  We don't verify, for example, that
    we can connect to the IP address of the a machine, or that it actually has
    that much memory.
    """
    # check that the file structure is valid
    (valid_file, err_msg) = _check_file_structure(file_lines)
    if valid_file is False:
        return (False, err_msg)

    # check each machine config line
    machines = file_lines[1:]
    hardware_term_types = [TermType.STRING,  # name of machine
                           TermType.IP_ADDR, # IP address
                           TermType.NUM,     # RAM in GB
                           TermType.NUM,     # Number of virtual disks
                           TermType.NUM]     # Number of virtual cores (VCPUs)

    for line, machine in enumerate(machines): # line is line number - 2
        (is_term, err_msg) = _check_term_types(machine, hardware_term_types)
        if is_term is False:
            error_message = "In line {}:\n".format(line + 2) + err_msg
            return (False, error_message)

    return (True, "Hardware configuration file successfully parsed.")

def check_image_config_file(file_lines):
    """
    Checks that the image configuration file is valid.

    NOTE: Just check for format and syntax.  We don't verify, for example, that
    the image file actually exists, or even if the path exists.
    """
    # check that the file structure is valid
    (is_valid, err_msg) = _check_file_structure(file_lines)
    if is_valid is False:
        return (False, err_msg)

    # check each machine config line
    machines = file_lines[1:]
    image_term_types = [TermType.STRING, # name of image
                        TermType.STRING] # image file path

    for line, machine in enumerate(machines): # line is line number - 2
        (is_term, err_msg) = _check_term_types(machine, image_term_types)
        if is_term is False:
            print(type(err_msg))
            print(err_msg)
            error_message = "In line {}:\n".format(line + 2) + err_msg
            return (False, error_message)

    return (True, "Image configuration file successfully parsed.")

def check_flavor_config_file(file_lines):
    """
    Checks that the flavor configuration file is valid.

    NOTE: Just check for format and syntax.  We don't verify, for example, that
    the image file actually exists, or even if the path exists.
    """
    # check that the file structure is valid
    (is_valid, err_msg) = _check_file_structure(file_lines)
    if is_valid is False:
        return (False, err_msg)

    # check each machine config line
    machines = file_lines[1:]
    image_term_types = [TermType.STRING, # name of flavor
                        TermType.NUM,    # amount of RAM in GB
                        TermType.NUM,    # number of virtual disks
                        TermType.NUM]    # number of virtual cores (VCPUs)

    for line, machine in enumerate(machines): # line is line number - 2
        (is_term, err_msg) = _check_term_types(machine, image_term_types)
        if is_term is False:
            error_message = "In line {}:\n".format(line + 2) + err_msg
            return (False, error_message)

    return (True, "Flavor configuration file successfully parsed.")
