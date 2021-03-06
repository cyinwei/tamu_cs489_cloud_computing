"""
Handles the configuration I/O (aggiestack config --?) logic.
"""
from lib.settings import (HARDWARE_KEYS, IMAGE_KEYS,
                          FLAVOR_KEYS, HARDWARE_FILE,
                          IMAGE_FILE, FLAVOR_FILE, ADMIN_HARDWARE_FILE)
from lib.utils.io_helpers import (read_config_file, load_state, write_state)
from lib.utils.check_config_inputs import (check_hardware_config_file,
                                           check_image_config_file,
                                           check_flavor_config_file)

def import_hardware_config(input_path, output_path=HARDWARE_FILE):
    """
    Reads and saves a hardware config file as a JSON file.
    """
    (success, data, err_msg) = read_config_file(input_path, HARDWARE_KEYS,
                                                check_hardware_config_file)
    if success is False:
        return (False, err_msg)

    return write_state(data, output_path)

def import_image_config(input_path, output_path=IMAGE_FILE):
    """
    Reads and saves a image config file as a JSON file.
     """
    (success, data, err_msg) = read_config_file(input_path, IMAGE_KEYS,
                                                check_image_config_file)
    if success is False:
        return (False, err_msg)
    return write_state(data, output_path)

def import_flavor_config(input_path, output_path=FLAVOR_FILE):
    """
    Reads and saves a flavor config file as a JSON file.
    """
    (success, data, err_msg) = read_config_file(input_path, FLAVOR_KEYS,
                                                check_flavor_config_file)
    if success is False:
        return (False, err_msg)
    return write_state(data, output_path)

def create_admin_hardware_state(input_p=HARDWARE_FILE,
                                output_p=ADMIN_HARDWARE_FILE):
    """
    Given a config --hardware HARDWARE_FILE state, we make a copy of it and
    place the state in output_p.
    """
    (r_success, data, err_msg) = load_state(input_p)
    if r_success is False:
        return (False, 'Error in creating admin hardware state:: ' + err_msg)
    (w_success, err_msg) = write_state(data, output_p)
    if w_success is False:
        return (False, 'Error in creating admin hardware state: ' + err_msg)
    return (True, 'Success in creating admin hardware state')
