"""
Contains the configuration settings for using pymongo in query.py
"""
from pathlib import Path
import json

HOST = "34.233.78.56"
DB = "fitness_721008432"
COLLECTION = "fitness_721008432"
TEST_COLLECTION = "test"

DUMMY_FITNESS_FILE = Path('data/dummy-fitness.json')
USER_1001_FILE = Path('data/user1001-new.json')

with DUMMY_FITNESS_FILE.open('r') as f:
    DUMMY_FITNESS_DATA = json.load(f)
with USER_1001_FILE.open('r') as f:
    USER_1001_DATA = json.load(f)

