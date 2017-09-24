"""
Handles the configuration I/O (aggiestack config --?) logic.
"""
from Aggiestack.lib.settings import (HARDWARE_KEYS, IMAGE_KEYS,
                                     FLAVOR_KEYS, HARDWARE_FILE,
                                     IMAGE_FILE, FLAVOR_FILE)
from Aggiestack.lib.utils.io_helpers import (read_config_file, write_state)
from Aggiestack.lib.utils.check_config_inputs import (check_hardware_config_file,
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
