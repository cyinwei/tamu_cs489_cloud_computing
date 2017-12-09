"""
Test the admin can_host() logic.
"""

from lib.admin import can_hardware_handle_flavor
from tests import ADMIN_JSON, FLAVOR_JSON


def test_admin_yes_handle():
    """
    Tests the admin logic, everything is good.
    """

    machine_name = 'calvin'
    flavor = 'small'
    (success, can_handle, msg) = can_hardware_handle_flavor(machine_name,
                                                            flavor,
                                                            ADMIN_JSON,
                                                            FLAVOR_JSON)
    print(msg)
    assert success is True
    assert can_handle is True


def test_admin_no_handle():
    """
    Tests the admin logic, machine name can't handle flavor.
    """

    machine_name = 'calvin'
    flavor = 'xlarge'
    (success, can_handle, msg) = can_hardware_handle_flavor(machine_name,
                                                            flavor,
                                                            ADMIN_JSON,
                                                            FLAVOR_JSON)
    print(msg)
    assert success is True
    assert can_handle is False


def test_admin_bad_machine_name():
    """
    Tests the admin logic, machine name doesn't exist.
    """
    bad_machine_name = 'calvins'
    flavor = 'xlarge'
    (success, can_handle, msg) = can_hardware_handle_flavor(bad_machine_name,
                                                            flavor,
                                                            ADMIN_JSON,
                                                            FLAVOR_JSON)
    print(msg)
    assert success is False
    assert can_handle is False


def test_admin_bad_flavor_name():
    """
    Tests the admin logic, flavor name doesn't exist.
    """
    machine_name = 'calvin'
    bad_flavor = 'xlarges'
    (success, can_handle, msg) = can_hardware_handle_flavor(machine_name,
                                                            bad_flavor,
                                                            ADMIN_JSON,
                                                            FLAVOR_JSON)
    print(msg)
    assert success is False
    assert can_handle is False
