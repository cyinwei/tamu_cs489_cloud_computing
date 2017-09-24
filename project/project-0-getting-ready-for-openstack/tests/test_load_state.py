"""
Tests our load and save state functions from Aggiestack.lib.utils.io_helpers.
"""
from Aggiestack.lib.utils.io_helpers import load_state, write_state
from tests import FLAVOR_JSON, TEST_JSON
from tests.fixtures.fixtures import IMAGES_DICT

def test_load_state(path=FLAVOR_JSON):
    """
    Tests if the file we just loaded is a dict and has the correct data.
    """
    (success, data, err_msg) = load_state(path)
    print(err_msg)

    assert success is True
    # just test one value to ensure we loaded the json
    assert data['large']['vcpu'] == 4

def test_write_state(data=None, testpath=TEST_JSON):
    """
    Tests we can write a JSON file out, read it in, and see if it's the same.
    """
    if data is None:
        data = IMAGES_DICT

    (w_success, w_err_msg) = write_state(data, testpath)
    print(w_err_msg)
    assert w_success is True

    (r_success, r_data, r_err_msg) = load_state(testpath)
    print(r_err_msg)
    assert r_success is True

    assert data == r_data
