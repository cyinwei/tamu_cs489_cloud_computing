"""
Implementations for the 'aggiestack server [...]' CLI commands.
"""

from lib.utils.server_helpers import (find_physical_server,
                                      update_physical_server,
                                      server_list_append,
                                      server_list_delete,
                                      shape_server)
from lib.settings import ADMIN_STATE_HARDWARE_FILE, SERVER_FILE


def create_server(name, image, flavor,
                  hardware_state=ADMIN_STATE_HARDWARE_FILE,
                  server_state=SERVER_FILE):
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
    update_physical_server(flavor, hardware_name)
    server_list_append(shape_server(name, image, flavor, hardware_name))

    return (True, 'Successfully created virtual server {}.'.format(name))


def delete_server(name):
    return server_list_delete(name)