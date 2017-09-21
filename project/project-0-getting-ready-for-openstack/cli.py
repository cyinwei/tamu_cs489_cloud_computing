#!/usr/bin/env python3

"""
The CLI (command line interface) of aggiescript.  The 'main' function.
"""
from pathlib import Path
import pprint
import click

from aggiestack.config_io import (import_hardware_config, import_image_config,
                                  import_flavor_config)
from aggiestack.utils.io_helpers import load_state
from aggiestack.utils.config_settings import (LOGFILE, HARDWARE_FILE,
                                              IMAGE_FILE, FLAVOR_FILE)

@click.group()
def cli():
    pass

@click.command()
@click.option('--hardware', default='', help='Configure the hardware settings.')
@click.option('--images', default='', help='Configure the OS image settings.')
@click.option('--flavor', default='', help='Configure the flavor (e.g. RAM, number of disks, and number of VCPUs).')
def config(hardware, images, flavor):
    if hardware != '':
        path = Path(hardware).resolve() # get absolute path
        (success, err_msg) = import_hardware_config(path)
        print (success)
        print(err_msg)
        # log output
        cli_input = 'aggiestack config --hardware {}'.format(hardware)
        log_str = None
        if success is True:
            log_str = "Success: " + cli_input + '\n'

        else:
            click.echo(err_msg, err=True)
            log_str = "Failure: " + cli_input + '\n'

        with LOGFILE.open('a+') as log: # + is create file if not exist
                log.write(log_str)

        print('end of function')
    if (images != ''):
        pass
    
    if (flavor != ''):
        pass

@click.command()
@click.option('--hardware', default='', help='')
@click.option('--images', default='', help='')
@click.option('--flavor', default='', help='')
def show(hardware, images, flavor):
    if hardware != '':
        (success, data, err_msg) = load_state(HARDWARE_FILE)
        cli_input = 'aggiestack show --hardware'
        log_str = None
        if not success:
            click.echo(err_msg, err=True)
            log_str = "Failure: " + cli_input
        else:
            # TODO: Need a better printer
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(data)
            log_str = "Success: " + cli_input

        with LOGFILE.open('a+') as log:
            log.write(log_str)
    
cli.add_command(config)
cli.add_command(show)

if __name__ == '__main__':
    cli()