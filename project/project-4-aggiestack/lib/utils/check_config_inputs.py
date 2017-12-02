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


def _check_rack(rack_name, RACK_TYPES=None):
    if RACK_TYPES is None:
        return False  # Nothing to compare to

    if rack_name in RACK_TYPES:
        return True
    return False


# Helper functions to check for certain terms
class TermType(Enum):
    """ Number of term Python object types (the configuration values). """
    STRING = 0
    NUM = 1
    IP_ADDR = 2
    RACK = 3


def _generate_rack_types(lines):
    """
    Given a list of lines (from .txt), generate a list of the valid rack names.

    NOTE: No error checking.  Use _check_file_structure() to do checking.
    """
    rack_types = []
    for name in lines[1:]:
        rack_types.append(name.strip())
    return rack_types


def _check_file_structure(lines):
    """
    Checks the configuration file format.

    All three (hardware, image, flavor) configuration file types share similar
    structures.  The first line contains the number of configurations.  Each
    following line represents one configuration.

    NOTE: Hardware is a bit different by adding a number of racks before the
    exact number of configurations.
    """

    if not lines:
        return (False, "Empty File.\n")

    # the first line tells us how many machine configs we have
    if _check_num(lines[0]) is False:
        return (False, "First line (number of configs) is NaN.\n")

    # do the number of machines match up?
    num_machines = int(lines[0])
    if len(lines)-1 != num_machines:
        error_message = ("First line (number of configs) does not "
                         "match the length of the file.\n")
        return (False, error_message)

    return (True, "No errors in the file structure.")


def _check_term_types(line, term_schema, RACK_TYPES=None):
    """
    Checks that the individual configuration (a line in the config file) is
    correct syntactially.

    Each configuration contains a name, followed by the configuration values,
    which are named 'terms'.  Different config files (hardware, images, flavor)
    have different configuration lists, which we pass into as a term_schema.

    NOTE: We just check for syntax; e.g. check the IP is syntactally valid or
    that a number is actually a positive number.  We do not check if a file
    path exists, or the numbers are obviously wrong, or if we can connect to 
    the IP, etc.

    NOTE: For the RACK TermType, we need a list of valid STRINGs to match.
    """
    terms = line.split()  # split by whitespace

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
        elif term_schema[index] == TermType.IP_ADDR:
            if _check_ip_addr(term) is False:
                error_message = "Invalid IP address: [{}].\n".format(term)
                return (False, error_message)
        else:  # term_schema[index] == TermType.RACK:
            if _check_rack(term, RACK_TYPES) is False:
                error_message = ("Invalid Rack name: [{}].  Imported Rack "
                                 "names are [{}].\n".format(term, RACK_TYPES))

    return (True, 'No errors in the single configuration.')


def check_hardware_config_file(file_lines):
    """
    Checks that the hardware configuration file is valid.

    NOTE: Just check for format and syntax.  We don't verify, for example, that
    we can connect to the IP address of the a machine, or that it actually has
    that much memory.

    NOTE: We split the config file into two parts: the rack and then machines
    part.
    """
    rack_line_nums = int(file_lines[0])
    if rack_line_nums == len(file_lines) - 1:
        return (False, 'Need both rack and machine configurations.')

    rack_lines = file_lines[:rack_line_nums+1]
    machine_lines = file_lines[rack_line_nums+1:]

    # check that the file structure is valid
    (valid_file_rack, err_msg) = _check_file_structure(rack_lines)
    if valid_file_rack is False:
        return (False, err_msg)
    (valid_file_machine, err_msg) = _check_file_structure(machine_lines)
    if valid_file_machine is False:
        return (False, err_msg)

    # check each rack config line
    racks = rack_lines[1:]
    rack_term_types = [TermType.STRING,  # name of rack
                       TermType.NUM]     # size of rack cache
    for line, rack in enumerate(racks):
        (is_term, err_msg) = _check_term_types(rack, rack_term_types)
        if is_term is False:
            error_message = ("Syntax Error: In line {}:\n".format(line + 2) +
                             err_msg)
            return (False, error_message) 

    # check each machine config line
    machines = machine_lines[1:]
    hardware_term_types = [TermType.STRING,   # name of machine,
                           TermType.RACK,     # rack name
                           TermType.IP_ADDR,  # IP address
                           TermType.NUM,      # RAM in GB
                           TermType.NUM,      # Number of virtual disks
                           TermType.NUM]      # Number of virtual cores (VCPUs)
    for line, machine in enumerate(machines):  # line is line number - 2
        (is_term, err_msg) = _check_term_types(machine, hardware_term_types)
        if is_term is False:
            error_message = ("Syntax Error: In line {}:\n".format(line + 2) +
                             err_msg)
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
    image_term_types = [TermType.STRING,  # name of image
                        TermType.NUM,     # image size
                        TermType.STRING]  # image file path

    for line, machine in enumerate(machines):  # line is line number - 2
        (is_term, err_msg) = _check_term_types(machine, image_term_types)
        if is_term is False:
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
