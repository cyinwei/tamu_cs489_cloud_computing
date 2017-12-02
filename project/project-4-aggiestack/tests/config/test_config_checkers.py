"""
Tests that our config checkers (see if a config text file is syntactically
correct) work.
"""


from lib.utils.check_config_inputs import (
    check_hardware_config_file,
    check_image_config_file,
    check_flavor_config_file
)
from tests import (
    read_file,
    HARDWARE_CONFIG_TXT,
    FLAVOR_CONFIG_TXT,
    IMAGE_CONFIG_TXT,
    BAD_DISK_HARDWARE_TXT_NAN,
    BAD_DISK_HARDWARE_TXT_NEG,
    BAD_IP_HARDWARE_TXT_DECIMALS,
    BAD_IP_HARDWARE_TXT_LOGIC,
    BAD_IP_HARDWARE_TXT_NUM,
    BAD_IP_HARDWARE_TXT_STR,
    BAD_MEM_HARDWARE_TXT_NAN,
    BAD_MEM_HARDWARE_TXT_NEG,
    BAD_RACK_HARDWARE_TXT_M,
    BAD_RACK_HARDWARE_TXT_M2,
    BAD_RACK_HARDWARE_TXT_NAN,
    BAD_RACK_HARDWARE_TXT_NEG,
    BAD_VCPU_HARDWARE_TXT_NAN,
    BAD_VCPU_HARDWARE_TXT_NEG
)


# test hardware configs
def test_correct_hardware_config():
    filepath = HARDWARE_CONFIG_TXT
    lines = read_file(filepath)
    (check, err_msg) = check_hardware_config_file(lines)
    print(err_msg)
    assert check is True


def test_bad_ip_hardware_config():
    paths = [BAD_IP_HARDWARE_TXT_DECIMALS, BAD_IP_HARDWARE_TXT_LOGIC,
             BAD_IP_HARDWARE_TXT_NUM, BAD_IP_HARDWARE_TXT_STR]
    for path in paths:
        lines = read_file(path)
        (check, err_msg) = check_hardware_config_file(lines)
        print(err_msg)
        assert check is False


def test_bad_mem_hardware_config():
    paths = [BAD_MEM_HARDWARE_TXT_NAN, BAD_MEM_HARDWARE_TXT_NEG]
    for path in paths:
        lines = read_file(path)
        (check, err_msg) = check_hardware_config_file(lines)
        print(err_msg)
        assert check is False


def test_bad_disk_hardware_config():
    paths = [BAD_DISK_HARDWARE_TXT_NAN, BAD_DISK_HARDWARE_TXT_NEG]
    for path in paths:
        lines = read_file(path)
        (check, err_msg) = check_hardware_config_file(lines)
        print(err_msg)
        assert check is False


def test_bad_vcpu_hardware_config():
    paths = [BAD_VCPU_HARDWARE_TXT_NAN, BAD_VCPU_HARDWARE_TXT_NEG]
    for path in paths:
        lines = read_file(path)
        (check, err_msg) = check_hardware_config_file(lines)
        print(err_msg)
        assert check is False


def test_bad_rack_hardware_config():
    paths = [BAD_RACK_HARDWARE_TXT_M, BAD_RACK_HARDWARE_TXT_M2,
             BAD_RACK_HARDWARE_TXT_NAN, BAD_RACK_HARDWARE_TXT_NEG]
    for path in paths:
        lines = read_file(path)
        (check, err_msg) = check_hardware_config_file(lines)
        print(str(path))
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
