from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / 'fixtures'

def read_file(path):
    lines = []
    with path.open() as f:
        lines = f.readlines()
    
    return lines