"""
Implementations for the 'aggiestack server [...]' CLI commands.
"""

from lib.utils.server_helpers import (find_physical_server,
                                      update_physical_server,
                                      server_list_append,
                                      server_list_delete,
                                      shape_server)
from lib.utils.io_helpers import load_state, write_state
from lib.settings import ADMIN_STATE_HARDWARE_FILE, SERVER_FILE


def create_server(name, image, flavor,
                  hardware_state_file=ADMIN_STATE_HARDWARE_FILE,
                  server_list_file=SERVER_FILE):
    """
    Creates/Instantiates a virtual server based on the size (flavor) and OS
    (image).

    Returns (Success, Error Message).
    """
    # First find a physical server to host
    (find_success, hardware_name) = find_physical_server(flavor)
    if not find_success:
        return (False, hardware_name)  # hw_name will be the error msg here

    # Update the current hardware state and the server list
    (hw_success, err_msg_hw) = update_physical_server(flavor, hardware_name,
                                                      True)
    if not hw_success:
        return (False, err_msg_hw)
    (sv_success, err_msg_sv) = server_list_append(shape_server(name,
                                                               image,
                                                               flavor,
                                                               hardware_name))
    if not sv_success:
        return (False, err_msg_sv)

    return (True, 'Successfully created virtual server [{}].'.format(name))


def delete_server(name, server_list_file=SERVER_FILE,
                  hardware_state_file=ADMIN_STATE_HARDWARE_FILE):
    """
    Deletes a virtual server by its instance name.
    """
    (sv_read_success, sv_data) = load_state(server_list_file)
    if sv_read_success is False:
        return (False, sv_data)

    # check if the name exists
    if sv_data.get(name) is None:
        return (False, 'Error: Virtual server [{}] does not exist.'.format(name))

    # grab flavor and hardware data from the server list
    flavor = sv_data[name]['flavor']
    hardware = sv_data[name]['hardware']

    # update the hardware state and server list
    (hw_success, err_msg_hw) = update_physical_server(flavor, hardware, False)
    if hw_success is False:
        return (False, err_msg_hw)
    (sv_success, err_msg_sv) = server_list_delete(name)
    if sv_success is False:
        return (False, err_msg_sv)

    return (True, 'Removed virtual server [{}].'.format(name))


def reset_server_list(server_file=SERVER_FILE):
    """
    Cleans out the server list by resetting the state (JSON file).
    """
    return write_state({}, server_file)