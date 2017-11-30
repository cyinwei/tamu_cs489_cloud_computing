"""
Tests that our fcfs algorithm to find a physical server works.
"""
from lib.server import find_physical_server
from lib.server import _fcfs
from tests import ADMIN_JSON, FLAVOR_JSON


def test_find_physical_server_fcfs_xlarge():
    (query, hw_name) = find_physical_server('xlarge', _fcfs, ADMIN_JSON,
                                            FLAVOR_JSON)
    assert query is True
    assert hw_name == 'dora'


def test_find_physical_server_fcfs_small():
    (query, hw_name) = find_physical_server('small', _fcfs, ADMIN_JSON,
                                            FLAVOR_JSON)
    assert query is True
    assert hw_name == 'm1'