
from pathlib import Path
import pytest

from aggiestack.utils.check_config_io import (check_hardware_config_file,
    check_image_config_file, check_flavor_config_file) 

from tests import FIXTURES_DIR, read_file


# test hardware configs
def test_correct_hardware_config():
    filepath = FIXTURES_DIR / 'success' / 'hardware-config.txt'
    lines = read_file(filepath)
    (check, err_msg) = check_hardware_config_file(lines)
    print(err_msg)
    assert check is True

def test_default_hardware_config():
    filepath = FIXTURES_DIR / 'default' / 'hardware-config.txt'
    lines = read_file(filepath)
    (check, err_msg) = check_hardware_config_file(lines)
    print(err_msg)
    assert check is False

def test_ip_hardware_config():
    filepath = FIXTURES_DIR / 'fail' / 'hardware' / 'bad-ip.txt'
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
