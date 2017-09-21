"""
Handles the configuration I/O (aggiestack config --?) logic.
"""
from aggiestack.utils.config_settings import (HARDWARE_KEYS, IMAGE_KEYS,
                                              FLAVOR_KEYS, HARDWARE_FILE,
                                              IMAGE_FILE, FLAVOR_FILE)
from aggiestack.utils.io_helpers import (read_config_file, write_state,
                                         load_state)
from aggiestack.utils.check_config_inputs import (check_hardware_config_file,
                                                  check_image_config_file,
                                                  check_flavor_config_file)

def read_hardware_config_file(input_file):
    """
    Reads a hardware config file as a dict.
    """
    return read_config_file(input_file, HARDWARE_KEYS,
                            check_hardware_config_file)

def read_image_config_file(input_file):
    """
    Reads a image config file as a dict.
    """
    return read_config_file(input_file, IMAGE_KEYS,
                            check_image_config_file)

def read_flavor_config_file(input_file):
    """
    Reads a flavor config file as a dict.
    """
    return read_config_file(input_file, FLAVOR_KEYS,
                            check_flavor_config_file)

def import_hardware_config(input_file, output_file=HARDWARE_FILE):
    """
    Reads and saves a hardware config file as a JSON file.
    """
    (status, data, err_msg) = read_hardware_config_file(input_file)
    print('status')
    print(status)
    if status is False:
        return (False, err_msg)
    print('yay')
    return write_state(data, output_file)

def import_image_config(input_file, output_file=IMAGE_FILE):
    """
    Reads and saves a image config file as a JSON file.
    """
    (status, data, err_msg) = read_image_config_file(input_file)
    if status is False:
        return (False, err_msg)

    return write_state(data, output_file)

def import_flavor_config(input_file, output_file=FLAVOR_FILE):
    """
    Reads and saves a flavor config file as a JSON file.
    """
    (status, data, err_msg) = read_flavor_config_file(input_file)
    if status is False:
        return (False, err_msg)

    return write_state(data, output_file)

def load_hardware_config(state_file=HARDWARE_FILE):
    """
    Loads a JSON file (state_file) as a dict.
    """
    return load_state(state_file)

def load_image_config(state_file=IMAGE_FILE):
    """
    Loads a JSON file (state_file) as a dict.
    """
    return load_state(state_file)

def load_flavor_config(state_file=FLAVOR_FILE):
    """
    Loads a JSON file (state_file) as a dict.
    """
    return load_state(state_file)
