
"""
Tests that our config checkers (see if a config text file is syntactically
correct) work.
"""


from lib.utils.check_config_inputs import (
    check_hardware_config_file,
    check_image_config_file,
    check_flavor_config_file
) 
from tests import (read_file,
                   HARDWARE_CONFIG_TXT,
                   FLAVOR_CONFIG_TXT,
                   IMAGE_CONFIG_TT,
                   
)


# test hardware configs
def test_correct_hardware_config():
    filepath = HARDWARE_CONFIG_TXT
    lines = read_file(filepath)
    (check, err_msg) = check_hardware_config_file(lines)
    print(err_msg)
    assert check is True


def test_default_hardware_config():
    filepath = HARDWARE_CONFIG_TXT
    lines = read_file(filepath)
    (check, err_msg) = check_hardware_config_file(lines)
    print(err_msg)
    assert check is False


def test_ip_hardware_config():
    filepath = HARDWARE_CONFIG_TXT
    lines = read_file(filepath)
    (check, err_msg) = check_hardware_config_file(lines)
    print(err_msg)
    assert check is False


def test_mem_hardware_config():
    filepath = FIXTURES_DIR / 'fail' / 'hardware' / 'bad-mem.txt'
    lines = read_file(filepath)
    (check, err_msg) = check_hardware_config_file(lines)
    print(err_msg)
    assert check is False


def test_disk_hardware_config():
    filepath = FIXTURES_DIR / 'fail' / 'hardware' / 'bad-disk.txt'
    lines = read_file(filepath)
    (check, err_msg) = check_hardware_config_file(lines)
    print(err_msg)
    assert check is False


def test_vcpu_hardware_config():
    filepath = FIXTURES_DIR / 'fail' / 'hardware' / 'bad-vcpu.txt'
    lines = read_file(filepath)
    (check, err_msg) = check_hardware_config_file(lines)
    print(err_msg)
    assert check is False


# test if we can check images correctly
def test_success_image_config():
    filepath = IMAGE_CONFIG_TXT
    lines = read_file(filepath)
    (check, err_msg) = check_image_config_file(lines)
    print(err_msg)
    assert check is True


# test if we check flavors correctly
def test_success_flavor_config():
    filepath = FLAVOR_CONFIG_TXT
    lines = read_file(filepath)
    (check, err_msg) = check_flavor_config_file(lines)
    print(err_msg)
    assert check is True
