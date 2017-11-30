"""
Implements the 'aggiestack server' commands, which create and delete virtual
servers.
"""


from .settings import (ADMIN_STATE_HARDWARE_FILE, IMAGE_FILE, FLAVOR_FILE,
                       FLAVOR_KEYS)
from .admin import can_hardware_handle_flavor
from .utils.io_helpers import load_state


def _fcfs(flavor, hardware):
    """
    The brute force algorithm.  Finds the 'first' available physical server
    that can run the flavor.

    Returns if the search was successful, and the name of the hardware or error
    message.
    """

    found_hardware = 0  # increment 1 for every 'match'
    for name, settings in hardware.items():
        for key in FLAVOR_KEYS:
            if settings[key] >= flavor[key]:
                found_hardware += 1
        if found_hardware == len(FLAVOR_KEYS):  # if all the keys are good
            return (True, name)
        else:
            found_hardware = 0  # reset

    return (False, '')


def find_physical_server(flavor_name, algorithm=_fcfs,
                         hardware_state=ADMIN_STATE_HARDWARE_FILE,
                         flavors=FLAVOR_FILE):
    """
    Given a flavor name, pick a physical server (hardware name) based on the
    chosen algorithm (defaults to a brute force first come first serve).

    Returns (Success, Physical Server Name (or error message)).
    """
    # Load data
    (query_hw, hardware, err_msg_hw) = load_state(hardware_state)
    if query_hw is False:
        return (False, err_msg_hw)
    (query_flavor, flavors, err_msg_flavors) = load_state(flavors)
    if query_flavor is False:
        return (False, err_msg_flavors)
    flavor_config = flavors[flavor_name]

    # Run the algorithm
    (found, hw_name) = algorithm(flavor_config, hardware)

    if found is False:
        return (False, ('No suitable physical server'
                        '(hardware) for flavor: {}'.format(flavor_name)))

    return (True, hw_name)


def update_server(flavor, hardware):
    """
    Update the state, substracting the flavor usage from the physical server
    (hardware).

    Returns if the attempt is successful or not. (True/False, Error Message)
    """
    pass 