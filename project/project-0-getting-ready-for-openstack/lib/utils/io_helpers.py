"""
Does the I/O (read file -> state), write the state to a file.
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
        if key == 'mem' or key == 'disk' or key == 'vcpu':
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
        with path.open('r') as json_file:
            lines = json_file.readlines()
    except IOError as io_e:
        err_msg = "IOError: [{}], {}".format(io_e.errno, io_e.strerror)
        return (False, {}, err_msg)

    # check if the file format is good
    (success, check_error_msg) = check_fn(lines)
    if not success:
        err_msg = "Error: In file [{}]: ".format(path) + '\n'+ check_error_msg
        return (False, {}, err_msg)

    # read the file
    config = {}
    for line in lines[1:]: # 1st line is the number of configs
        (name, line_config) = parse_config_line(line, config_keys)
        config[name] = line_config

    return (True, config, 'Success.')

def write_state(data, output_path):
    """
    Writes a dict (data) as a JSON file with pathlib.Path (output)
    """
    # wipes old state if it exists
    if output_path.exists() is True:
        if output_path.is_dir():
            err_msg = "Error: {} is a directory, can't overwrite it".format(output_path)
            return (False, err_msg)
        output_path.unlink()

    # write new state
    try:
        # create file if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.touch(exist_ok=True)

        with output_path.open('w+') as out:
            json.dump(data, out)
    except IOError as io_e:
        err_msg = "In write_state(): IOError: [{}], {}".format(io_e.errno, io_e.strerror)
        return (False, err_msg)

    return (True, 'success')

def load_state(input_path):
    """
    Loads a JSON file from pathlib.Path (inpu_path) as a dict.
    """
    try:
        with input_path.open('r') as json_file:
            data = json.load(json_file)
            return (True, data, 'success')
    except IOError as io_e:
        err_msg = "In load_state(): IOError: [{}], {}".format(io_e.errno, io_e.strerror)
        return (False, {}, err_msg)
        