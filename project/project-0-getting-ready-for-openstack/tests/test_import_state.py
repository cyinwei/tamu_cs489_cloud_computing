"""
Tests our import state function, which reads in a file, parses it, and writes it
to our state file.
"""
from lib.config_io import (import_hardware_config,
                           import_image_config,
                           import_flavor_config)
from lib.utils.io_helpers import load_state, read_config_file
from lib.utils.check_config_inputs import (check_hardware_config_file,
                                           check_image_config_file,
                                           check_flavor_config_file)
from lib.settings import HARDWARE_KEYS, IMAGE_KEYS, FLAVOR_KEYS
from tests import FIXTURES_DIR, TEST_JSON

def test_import_hardware():
    """
    Tests if we can import a hardware config file to TEST_JSON.
    """
    input_path = FIXTURES_DIR / 'success' / 'hardware-config.txt'
    # import the file
    (i_success, i_err_msg) = import_hardware_config(input_path, TEST_JSON)
    print(('import err_msg: ', i_err_msg))
    assert i_success is True

    # load the test state file
    (l_success, data, l_err_msg) = load_state(TEST_JSON)
    print(('load err_msg: ', l_err_msg))
    assert l_success is True

    # parse the input file again and check the data is the same
    (r_success, r_data, r_err_msg) = read_config_file(input_path, HARDWARE_KEYS,
                                                      check_hardware_config_file)
    print(('read config err_msg: ', r_err_msg))
    assert r_success is True

    # check if our parsed config file is the same as our stored state
    assert data == r_data

def test_import_image():
    """
    Tests if we can import an image config file to TEST_JSON.
    """
    input_path = FIXTURES_DIR / 'success' / 'images-config.txt'
    # import the file
    (i_success, i_err_msg) = import_image_config(input_path, TEST_JSON)
    print(('import err_msg: ', i_err_msg))
    assert i_success is True

    # load the test state file
    (l_success, data, l_err_msg) = load_state(TEST_JSON)
    print(('load err_msg: ', l_err_msg))
    assert l_success is True

    # parse the input file again and check the data is the same
    (r_success, r_data, r_err_msg) = read_config_file(input_path, IMAGE_KEYS,
                                                    check_image_config_file)
    print(('read config err_msg: ', r_err_msg))
    assert r_success is True

    # check if our parsed config file is the same as our stored state
    assert data == r_data

def test_import_flavor():
    """
    Tests if we can import a flavor config file to TEST_JSON.
    """
    input_path = FIXTURES_DIR / 'success' / 'flavor-config.txt'
    # import the file
    (i_success, i_err_msg) = import_flavor_config(input_path, TEST_JSON)
    print(('import err_msg: ', i_err_msg))
    assert i_success is True

    # load the test state file
    (l_success, data, l_err_msg) = load_state(TEST_JSON)
    print(('load err_msg: ', l_err_msg))
    assert l_success is True

    # parse the input file again and check the data is the same
    (r_success, r_data, r_err_msg) = read_config_file(input_path, FLAVOR_KEYS,
                                                      check_flavor_config_file)
    print(('read config err_msg: ', r_err_msg))
    assert r_success is True

    # check if our parsed config file is the same as our stored state
    assert data == r_data