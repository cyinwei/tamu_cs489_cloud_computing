"""
Implements the 'aggiestack server' commands, which create and delete virtual
servers.
"""


from lib.settings import (ADMIN_STATE_HARDWARE_FILE, IMAGE_FILE, FLAVOR_FILE,
                          FLAVOR_KEYS, SERVER_FILE)
from lib.admin import can_hardware_handle_flavor
from lib.utils.io_helpers import load_state, write_state


def shape_server(name, image, flavor, hardware):
    return {name: {'image': image, 'flavor': flavor, 'hardware': hardware}}


def server_list_append(server, servers_p=SERVER_FILE):
    """
    Given a server (a dictionary), add it to the server list state (JSON file).
    """
    data = None
    if servers_p.exists() is True:
        (r_success, data) = load_state(servers_p)
        if r_success is False:
            return (False, data)
    else:
        data = {}

    # Check for same name collisions
    for name in server:
        if data.get(name) is not None:
            return (False, 'Could not create server [{}], since there is '
                    'another virtual server with the same name'.format(name))

    data.update(server)
    (w_success, err_msg) = write_state(data, servers_p)
    if w_success is False:
        return (False, 'Could not create server state.  Reason:\n'
                + err_msg)
    return (True, 'Success in appending to the server state')


def server_list_delete(server_name, servers_p=SERVER_FILE):
    """
    Delete a server (by name) from the server list.  Pure delete; will return
    true if the name doesn't exist.
    """
    if servers_p.exists() is False:
        return (False, 'Error: Virtual server state file: {} '
                'does not exist.'.format(str(servers_p)))
    (r_success, data) = load_state(servers_p)
    if r_success is False:
        return (False, 'Could not delete server.  Reason\n' + data)

    data.pop(server_name, None)
    write_state(data, SERVER_FILE)
    return (True, 'Deleted {} from the server list.'.format(server_name))


def _fcfs(flavor, machines):
    """
    The brute force algorithm.  Finds the 'first' available physical server
    that can run the flavor.

    Returns if the search was successful, and the name of the hardware or error
    message.
    """

    found_machine = 0  # increment 1 for every 'match'
    for name, settings in machines.items():
        for key in FLAVOR_KEYS:
            if settings[key] >= flavor[key]:
                found_machine += 1
        if found_machine == len(FLAVOR_KEYS):  # if all the keys are good
            return (True, name)
        else:
            found_machine = 0  # reset

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
    (query_hw, hardware) = load_state(hardware_state)
    if query_hw is False:
        return (False, hardware)
    (query_flavor, flavors) = load_state(flavors)
    if query_flavor is False:
        return (False, flavors)
    flavor_config = flavors[flavor_name]

    # Run the algorithm
    (found, hw_name) = algorithm(flavor_config, hardware['machines'])

    if found is False:
        return (False, ('Error: No suitable physical server '
                        '(hardware) for flavor: {}'.format(flavor_name)))

    return (True, hw_name)


def update_physical_server(flavor_name, phys_server_name,
                           subtract=True,
                           flavor_state=FLAVOR_FILE,
                           flavor_keys=FLAVOR_KEYS,
                           hardware_state=ADMIN_STATE_HARDWARE_FILE):
    """
    Update the physical servers / hardwares state, substracting the flavor
    usage from the physical server (hardware).

    Returns if the attempt is successful or not. (True/False, Error Message)
    """
    (r_success_flavor, flavors) = load_state(flavor_state)
    if r_success_flavor is False:
        return (False, flavors)
    (r_success_hw, hardwares) = load_state(hardware_state)
    if r_success_hw is False:
        return (False, hardwares)
    
    flavor = flavors[flavor_name]
    phys_server = hardwares['machines'][phys_server_name]

    # check if can 'subtract' and end up with nonnegative resources
    if subtract:
        matches = 0
        for key in flavor_keys:
            if phys_server[key] >= flavor[key]:
                matches += 1
        if matches != len(flavor_keys):
            return (False, 'Error: Cannot update hardware state:\n'
                    'One or more fields in the hardware is less than the '
                    'flavor requirements')

    for key in flavor_keys:
        if subtract:
            phys_server[key] -= flavor[key]
        else:
            phys_server[key] += flavor[key]

    phys_server_entry = {phys_server_name: phys_server}
    hardwares['machines'].update(phys_server_entry)
    (w_success_hw, err_msg_write_hw) = write_state(hardwares,
                                                   ADMIN_STATE_HARDWARE_FILE)
    if w_success_hw is False:
        return (False, 'Error: Failed when writing to state in update_server()'
                       '. Reason:\n' + err_msg_write_hw)

    return (True, 'Successfully updated physical server.')
