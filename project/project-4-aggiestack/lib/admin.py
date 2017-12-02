"""
Implements the functionality we expect from the 'aggiestack admin ' command.
"""
from lib.settings import (
    ADMIN_STATE_HARDWARE_FILE,
    HARDWARE_FILE,
    FLAVOR_FILE,
    SERVER_FILE
)
from lib.utils.io_helpers import load_state
from lib.utils.server_helpers import server_list_delete


def can_hardware_handle_flavor(machine_name, flavor_name,
                               hw_file=ADMIN_STATE_HARDWARE_FILE,
                               fl_file=FLAVOR_FILE):
    """
    Checks if a given hardware config can handle a flavor size.
    Returns (success (I/O errors), can_handle, msg).
    """
    # load states and check if everything is valid
    (success, hw_data) = load_state(hw_file)
    if success is False:
        error_msg = ("In can_hardware_handle_flavor(): "
                     "Cannot find admin hardware state.")
        error_msg += ('\n' + hw_data)
        return (False, False, error_msg)
    machines = hw_data['machines']
    if machine_name not in machines:
        error_msg = ("In can_hardware_handle_flavor(): "
                     "[{}] isn't a valid config.".format(machine_name))
        return (False, False, error_msg)

    (success, fl_data) = load_state(fl_file)
    if success is False:
        error_msg = ("In can_hardware_handle_flavor(): "
                     "Cannot find flavor state: ")
        error_msg += fl_data
        return (False, False, fl_data)
    if flavor_name not in fl_data:
        error_msg = ("In can_hardware_handle_flavor(): "
                     "[{}] isn't a valid config.".format(flavor_name))
        return (False, False, error_msg)

    machine = machines[machine_name]
    flavor = fl_data[flavor_name]
    keys = list(flavor)  # flavor keys are in hardware keys
    fail_msg_template = "machine [{}] can't run flavor [{}] because of insufficient [{}]."
    for key in keys:
        if machine[key] < flavor[key]:
            return (True, False, fail_msg_template.format(machine_name,
                                                          flavor_name, key))

    success_msg = "machine: [{}] can run flavor [{}]".format(machine_name,
                                                             flavor_name)
    return (True, True, success_msg)


def remove_machine(machine_name,
                   admin_file=ADMIN_STATE_HARDWARE_FILE,
                   hardware_file=HARDWARE_FILE,
                   server_file=SERVER_FILE):
    """
    Removes a machine from the configuration and its associated virtual
    servers.
    """
    # Load states
    (r_success_hw_d, default_state) = load_state(hardware_file)
    if not r_success_hw_d:
        return (False, default_state)
    (r_success_hw_a, current_state) = load_state(admin_file)
    if not r_success_hw_a:
        return (False, default_state)
    (r_success_sv, servers) = load_state(server_file)
    if not r_success_sv:
        return (False, r_success_sv)

    default_machines = default_state['machines']
    current_machines = current_state['machines']

    # Verify the machine currently exists in both states
    if (machine_name not in default_machines and
       machine_name not in current_machines):
        return (False, 'Error: machine: [{}] '
                'cannot be found.'.format(machine_name))
    elif (machine_name not in default_machines or
          machine_name not in current_machines):  # have a mismatch here
        return (False, 'Error!!: States (admin vs hardware) are mismatched '
                'for machine [{}]'.format(machine_name))

    # Remove any virtual servers on the machine
    server_names = [server_name for server_name in servers
                    if servers[server_name]['hardware'] == machine_name]

    for server_name in server_names:
        (success, msg) = server_list_delete(server_name, server_file)
        if not success:
            return (False, 'Error: When removing machine '
                           '[{}], '.format(server_name) + msg)

    # Remove the machines from the current (admin) state and default state
    default_machine = default_machines.pop(machine_name, None)
    current_machine = current_machines.pop(machine_name, None)

    if default_machine is None or current_machine is None:
        return (False, 'ERROR!!: SHOULD NEVER BE HERE, SOME OTHER THREAD '
                       'REMOVED IT ALREADY')
    
    msg = 'Successfully removed machine [{}]'.format(machine_name)
    if server_names:  # non empty list
        msg += ('\nAlso removed virtuals servers [{}], which depend on the '
                'machine'.format(server_names.join(' ,')))
    
    return (True, msg)
    