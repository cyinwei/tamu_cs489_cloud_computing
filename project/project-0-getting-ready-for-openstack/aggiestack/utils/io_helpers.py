"""
Handles the configuration I/O (aggiestack config --?) logic. 
"""
import json

def parse_config_line(line, keys):
    """
    Given a single configuration (line), add a key to dict with key: name and
    value: dict with keys corresponding to the configurations.
    """
    terms = line.split() # by whitespace
    name = terms[0]
    values = terms[1:]

    config = {}
    for i, key in enumerate(keys):
        value = None

        # certain keys (below) are definitely numbers
        if key == 'mem' or key == 'disks' or key == 'vcpus':
            value = int(values[i])
        else:
            value = values[i]

        config[key] = value

    return (name, config)

def read_config_file(path, config_keys, check_fn):
    """
    Reads in a config file (path) as a dict.  The config_keys determines what 
    type of file we're reading in.  Use the check_fn to see if its a valid 
    config file.
    """
    lines = []
    try:
        with path.open('r') as f:
            lines = f.readlines()
    except IOError as io_e:
        err_msg = "IOError: [{}], {}".format(io_e.errno, io_e.strerror)
        return (False, {}, err_msg)

    # check if the file format is good
    (success, check_error_msg) = check_fn(lines)
    if not success:
        err_msg = "Error: In file [{}]: ".format(path) + check_error_msg
        return (False, {}, err_msg)

    # read the file
    config = {}
    for line in lines[1:]: # 1st line is the number of configs
        (name, line_config) = parse_config_line(line, config_keys)
        config[name] = line_config

    return (True, config, 'Success.')

def write_state(data, output):
    """
    Writes a dict (data) as a JSON file with Path (output)
    """
    # wipes old state if it exists
    if output.exists():
        if output.is_dir():
            err_msg = "Error: {} is a directory, can't overwrite it".format(output)
            return (False, err_msg)
        output.unlink()

    # write new state
    try:
        print (output)
        with output.open('w+') as out:
            json.dump(data, out)
    except IOError as io_e:
        err_msg = "IOError: [{}], {}".format(io_e.errno, io_e.strerror)
        return (False, err_msg)

    return (True, 'success')

def load_state(input_path):
    """
    Loads a JSON file (input_path) as a dict
    """
    try:
        with input_path.open('r') as json_file:
            data = json.load(json_file)
            return (True, data, 'success')
    except IOError as io_e:
        err_msg = "IOError: [{}], {}".format(io_e.errno, io_e.strerror)
        return (False, {}, err_msg)
        