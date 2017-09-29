#!/usr/bin/env python3

"""
The CLI (command line interface) of aggiescript.  The 'main' function.
"""
from pathlib import Path
import click

from lib.config_io import (import_hardware_config, import_image_config,
                           import_flavor_config, create_admin_hardware_state)
from lib.display import display
from lib.settings import (LOGFILE, ADMIN_HARDWARE_FILE, HARDWARE_FILE,
                          IMAGE_FILE, FLAVOR_FILE, HARDWARE_KEYS, IMAGE_KEYS,
                          FLAVOR_KEYS)

def _log(success, command):
    log_str = None
    if success is True:
        log_str = 'Success: ' + command + '\n'
    else:
        log_str = 'Failure: ' + command + '\n'
    with LOGFILE.open('a+') as log: # + is create file if not exist
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
@click.pass_context
@click.option('--hardware', default='', help='Configure the hardware settings.')
@click.option('--images', default='', help='Configure the OS image settings.')
@click.option('--flavors', default='', help='Configure the flavor sizes.')
def config(ctx, hardware, images, flavors):
    """
    Import a configuration file.
    """
    cli_input_base = "{} {} ".format(ctx.parent.info_name,
                                     ctx.info_name)
    if hardware != '':
        cli_input = cli_input_base + "-- hardware {}".format(hardware)
        path = Path(hardware)
        (success, err_msg) = import_hardware_config(path)
        if success is True:
            # don't print anything, just log
            _log(True, cli_input)
        else:
            click.echo("Error: couldn't import hardware settings.  Reasons:")
            click.echo(err_msg)
            _log(False, cli_input)

    if images != '':
        cli_input = cli_input_base + "-- images {}".format(hardware)
        path = Path(images)
        (success, err_msg) = import_image_config(path)
        if success is True:
            # don't print anything, just log
            _log(True, cli_input)
        else:
            click.echo("Error: couldn't import images settings.  Reasons:")
            click.echo(err_msg)
            _log(False, cli_input)

    if flavors != '':
        cli_input = cli_input_base + "-- flavors {}".format(hardware)
        path = Path(flavors)
        (success, err_msg) = import_flavor_config(path)
        if success is True:
            # don't print anything, just log
            _log(True, cli_input)
        else:
            click.echo("Error: couldn't import flavors settings.  Reasons:")
            click.echo(err_msg)
            _log(False, cli_input)

@click.group()
def show():
    """
    Show the current configuration.
    """

@click.command('hardware')
@click.pass_context
def show_hardware(ctx):
    """
    Displays the available hardware configurations.
    """
    # switch on the context
    cli_input = None
    table_info = None
    success = None
    data = None
    if ctx.parent.parent.info_name == 'admin':
        cli_input = "{} {} {} {}".format(ctx.parent.parent.parent.info_name,
                                         ctx.parent.parent.info_name,
                                         ctx.parent.info_name,
                                         ctx.info_name)
        table_info = 'Available current (admin) hardware configurations:'
        (success, data) = display(ADMIN_HARDWARE_FILE, HARDWARE_KEYS)
    else:
        cli_input = "{} {} {}".format(ctx.parent.parent.info_name,
                                      ctx.parent.info_name,
                                      ctx.info_name)
        table_info = 'Available default hardware configurations:'
        (success, data) = display(HARDWARE_FILE, HARDWARE_KEYS)
    # display data and log
    if success is True:
        click.echo(table_info)
        click.echo(data)
    else:
        click.echo('Error: Could not display configurations for hardware.  Reasons:')
        click.echo(data)
    _log(success, cli_input)
   
@click.command('images')
@click.pass_context
def show_images(ctx):
    """
    Displays the available image configurations.
    """
    cli_input = "{} {} {}".format(ctx.parent.parent.info_name,
                                  ctx.parent.info_name,
                                  ctx.info_name)
    (success, data) = display(IMAGE_FILE, IMAGE_KEYS)
    # display data and log
    if success is True:
        click.echo('Available base images configurations:')
        click.echo(data)
    else:
        click.echo('Error: Could not display configurations for images.  Reasons:')
        click.echo(data)
    _log(success, cli_input)

@click.command('flavors')
@click.pass_context
def show_flavors(ctx):
    """
    Displays the available flavor configurations.
    """
    cli_input = "{} {} {}".format(ctx.parent.parent.info_name,
                                  ctx.parent.info_name,
                                  ctx.info_name)
    (success, data) = display(FLAVOR_FILE, FLAVOR_KEYS)
    # display data and log
    if success is True:
        click.echo('Available base flavor configurations:')
        click.echo(data)
    else:
        click.echo('Error: Could not display configurations for flavors.  Reasons:')
        click.echo(data)
    _log(success, cli_input)

@click.command('all')
@click.pass_context
def show_all(ctx):
    """
    Displays all the available configurations.
    """
    cli_input = "{} {} {}".format(ctx.parent.parent.info_name,
                                  ctx.parent.info_name,
                                  ctx.info_name)
    (hw_success, hw_data) = display(HARDWARE_FILE, HARDWARE_KEYS)
    (im_success, im_data) = display(IMAGE_FILE, IMAGE_KEYS)
    (fl_success, fl_data) = display(FLAVOR_FILE, FLAVOR_KEYS)

    success = hw_success and im_success and fl_success
    # display errors first, then data
    if success is True:
        click.echo("Available configurations:")
        click.echo("Hardware:")
        click.echo(hw_data)
        click.echo("Images")

    else:
        click.echo('Error in displaying all configs:')
        if hw_success is False:
            click.echo('Error: when displaying hardware config:')
            click.echo(hw_data)
        if im_success is False:
            click.echo('Error: when displaying images config')
            click.echo(im_data)
        if fl_success is False:
            click.echo('Error: when displaying flavors config:')
            click.echo(fl_data)

    _log(success, cli_input)

cli.add_command(config)
cli.add_command(show)

show.add_command(show_hardware)
show.add_command(show_images)
show.add_command(show_flavors)
show.add_command(show_all)

if __name__ == '__main__':
    cli()
