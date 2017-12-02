"""
Displays the state of a configuration (hardware, image, flavor) based on the
stored state.
"""
from lib.utils.io_helpers import load_state


def _generate_body(data, keys):
    """
    Generate the body (all the rows after the column names) as a list of
    lines.  Each line is a list of row elements to be formatted.
    """
    body = []

     # loop over the data to create the lines
    lines = list(data)
    for line in lines:
        row = [line] # first row elem, the name of the config
        terms_dict = data[line] # rest of the row elems
        for term_key in keys:
            term = terms_dict[term_key]
            row.append(term)

        body.append(row)

    return body


def _find_maxwidths(header, body):
    """
    Finds the max width of each column in the output table by looking at the
    widths of each elem in the table.
    """

    maxwidths = []
    for column_name in header:
        maxwidths.append(len(column_name))

    for row in body:
        for i, elem in enumerate(row):
            if (maxwidths[i] < len(str(elem))):
                maxwidths[i] = len(str(elem))

    return maxwidths


def get_table(data, keys, translations=None):
    """
    Given a state (data) and the data type (keys), print a table out (columns
    are the keys, worded nicer with a translation dict).
    """

    # First get the data into a list of rows to print
    if data is None:
        return 'NONE.'
    if not data:  # empty {} evaluates to False
        return 'NONE.'

    # get the column names, which is the first row / header
    keynames = None
    if translations is None:
        keynames = keys
    else:
        keynames = [translations[key] for key in keys]

    header = ("name", ) + keynames  # Name is the first column
    body = _generate_body(data, keys)

    # Then format our list of lines (header + body)

    maxwidths = _find_maxwidths(header, body)

    # format our lines with a template string
    row_formatted = "|"
    line_under_header = "|"
    for width in maxwidths:
        row_formatted += "{:<" + str(width) + "}|"
        line_under_header += (('-' * width) + '|')

    # generate the header
    formatted_lines = []

    header_str = row_formatted.format(*header)
    formatted_lines.append(header_str)
    formatted_lines.append(line_under_header)
    # generate the body of the table
    for row in body:
        formatted_lines.append(row_formatted.format(*row))

    return '\n'.join(formatted_lines)


def display(state_path, keys):
    (success, data) = load_state(state_path)

    if success is False:
        return (False, data)

    else:
        return (True, get_table(data, keys))


def display_state(data, keys):
    return (True, get_table(data, keys))
