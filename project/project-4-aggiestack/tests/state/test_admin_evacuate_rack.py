"""
Tests the function evacuate_rack(), which is used in
'aggiestack admin evacuate RACK'. 
"""
import shutil
from lib.admin import evacuate_rack
from tests import (
    FIXTURES_DIR
    ADMIN_JSON,
    HARDWARE_JSON,
    FLAVOR_JSON,
    IMAGE_JSON,
    SERVER_JSON
)


FIXTURES_DIR_TMP = FIXTURES_DIR / 'tmp'
ADMIN_JSON_TMP = FIXTURES_DIR_TMP / 'admin.json'
HARDWARE_JSON_TMP = FIXTURES_DIR_TMP / 'hardware.json'
FLAVOR_JSON_TMP = FIXTURES_DIR_TMP / 'flavor.json'
IMAGE_JSON_TMP = FIXTURES_DIR_TMP / 'image.json'
SERVER_JSON_TMP = FIXTURES_DIR_TMP / 'server.json'


def _set_up_tmp_files():
    shutil.copyfile(str(ADMIN_JSON), str(ADMIN_JSON_TMP))
    shutil.copyfile(str(HARDWARE_JSON), str(HARDWARE_JSON_TMP))
    shutil.copyfile(str(FLAVOR_JSON), str(FLAVOR_JSON_TMP))
    shutil.copyfile(str(IMAGE_JSON), str(IMAGE_JSON_TMP))
    shutil.copyfile(str(SERVER_JSON), str(SERVER_JSON_TMP))


def _delete_tmp_files():
    ADMIN_JSON_TMP.unlink()
    HARDWARE_JSON_TMP.unlink()
    FLAVOR_JSON_TMP.unlink()
    IMAGE_JSON_TMP.unlink()
    SERVER_JSON_TMP.unlink()


