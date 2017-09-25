#!/usr/bin/env python3

"""
The CLI (command line interface) of aggiescript.  The 'main' function.
"""
from pathlib import Path
import click

from lib.config_io import (import_hardware_config, import_image_config,
                           import_flavor_config)
from lib.display import (display_flavor, display_hardware, display_image)
from lib.settings import LOGFILE

def _config(path_str, option):
    # switch based on the type of config. (option)
    import_fn = None
    cli_input = None
    if option == 'hardware':
        import_fn = import_hardware_config
        cli_input = 'aggiestack config --hardware {}'.format(path_str)
    elif option == 'images':
        import_fn = import_image_config
        cli_input = 'aggiestack config --images {}'.format(path_str)
    elif option == 'flavor':
        import_fn = import_flavor_config
        cli_input = 'aggiestack config --flavor {}'.format(path_str)
    else:
        click.echo('Error in _config(): bad option input (NEVER SHOULD BE HERE')
        return
    # import our file and log it
    path = Path(path_str)
    (success, err_msg) = import_fn(path)
    if success is True:
        log_str = "Success: " + cli_input + '\n'
    else:
        click.echo('Error importing... :' + err_msg, err=True)
        log_str = "Failure: " + cli_input + '\n'

    with LOGFILE.open('a+') as log: # + is create file if not exist
        log.write(log_str)

def _show(option):
    # switch based on the type of config. (option)
    display_fn = None
    cli_input = None
    display_str = ' configurations are:'
    if option == 'hardware':
        display_fn = display_hardware
        cli_input = 'aggiestack show --hardware'
        display_str = 'Hardware' + display_str
    elif option == 'images':
        display_fn = display_image
        cli_input = 'aggiestack show --images'
        display_str = 'Images' + display_str
    elif option == 'flavor':
        display_fn = display_flavor
        cli_input = 'aggiestack show --flavor'
        display_str = 'Flavor' + display_str
    else:
        click.echo('Error in _config(): bad option input (NEVER SHOULD BE HERE')
        return
    # load our state and display it
    (success, table) = display_fn()
    if success is True:
        log_str = 'Success: ' + cli_input
        click.echo(display_str)
        click.echo(table)
    else:
        err_msg = 'Error: no hardware configuration found.'
        click.echo(err_msg, err=True)
        log_str = 'Failure: ' + cli_input

    with LOGFILE.open('a+') as log:
        log.write(log_str)

@click.group()
def cli():
    """
    Our command line interface (CLI) implemented in click.
    NOTE: aggiestack doesn't any default configs without commands, so this is
    empty.
    """
    pass

@click.command()
@click.option('--hardware', default='', help='Configure the hardware settings.')
@click.option('--images', default='', help='Configure the OS image settings.')
@click.option('--flavor', default='', help='Configure the flavor sizes.')
def config(hardware, images, flavor):
    """
    Handles the 'aggiestack config ' CLI command.
    """
    if hardware != '':
        _config(hardware, 'hardware')

    if images != '':
        _config(images, 'images')

    if flavor != '':
        _config(flavor, 'flavor')

@click.command()
@click.option('--hardware', is_flag=True, help='Display the config for hardware.')
@click.option('--images', is_flag=True, help='Display the config for images.')
@click.option('--flavor', is_flag=True, help='Display the config for flavors.')
def show(hardware, images, flavor):
    """
    Handles the 'aggiestack show ' CLI command.
    """
    if hardware is True:
        _show('hardware')

    if images is True:
        _show('images')

    if flavor is True:
        _show('flavor')

cli.add_command(config)
cli.add_command(show)

if __name__ == '__main__':
    cli()
