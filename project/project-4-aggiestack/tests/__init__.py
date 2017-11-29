"""
Our testing module for Aggiestack (project 0).
"""
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / 'fixtures'
FLAVOR_JSON = FIXTURES_DIR / 'success' / 'flavor-config.json'
ADMIN_JSON = FIXTURES_DIR / 'success' / 'hardware.json'
FLAVOR_TXT = FIXTURES_DIR / 'success' / 'flavor-config.txt'
TEST_JSON = Path(__file__).parent / 'test.json'

def read_file(path):
    """
    loads a file from a pathlib.Path and returns the lines of the file.
    """
    lines = []
    with path.open() as read_only_file:
        lines = read_only_file.readlines()

    return lines
