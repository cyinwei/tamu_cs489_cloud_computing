"""
Implements the functionality we expect from the 'aggiestack admin ' command.
"""
from lib.settings import ADMIN_HARDWARE_FILE, FLAVOR_FILE
from lib.utils.io_helpers import load_state

def can_hardware_handle_flavor(machine_name, flavor_name,
                               hw_file=ADMIN_HARDWARE_FILE,
                               fl_file=FLAVOR_FILE):
    """
    Checks if a given hardware config can handle a flavor size.
    Returns (success (I/O errors), can_handle, msg).
    """
    # load states and check if everything is valid
    (success, hw_data, err_msg) = load_state(hw_file)
    if success is False:
        error_msg = ("In can_hardware_handle_flavor(): "
                     "Cannot find admin hardware state: \n")
        error_msg += err_msg
        return (False, False, error_msg)
    if machine_name not in hw_data:
        error_msg = ("In can_hardware_handle_flavor(): "
                     "{} isn't a valid config.\n".format(machine_name))
        return (False, False, error_msg)

    (success, fl_data, err_msg) = load_state(fl_file)
    if success is False:
        error_msg = ("In can_hardware_handle_flavor(): "
                     "Cannot find flavor state: \n")
        error_msg += err_msg
        return (False, False, error_msg)
    if flavor_name not in fl_data:
        error_msg = ("In can_hardware_handle_flavor(): "
                     "{} isn't a valid config.\n".format(machine_name))
        return (False, False, error_msg)

    machine = hw_data[machine_name]
    flavor = fl_data[flavor_name]
    keys = list(flavor) # flavor keys are in hardware keys
    fail_msg_template = "No, machine {} can't run flavor {} because of {}"
    for key in keys:
        if machine[key] < flavor[key]:
            return (True, False, fail_msg_template.format(machine_name,
                                                          flavor_name, key))

    success_msg = "Yes, machine: {} can run flavor {}".format(machine_name,
                                                              flavor_name)
    return (True, False, success_msg)
