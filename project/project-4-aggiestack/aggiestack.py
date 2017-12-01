#!/usr/bin/env python3

"""
The CLI (command line interface) of aggiescript.  The 'main' function.
"""
from pathlib import Path
import click

from lib.config_io import (import_hardware_config, import_image_config,
                           import_flavor_config, create_admin_hardware_state)
from lib.display import display
from lib.admin import can_hardware_handle_flavor
from lib.server import create_server, delete_server
from lib.settings import (LOGFILE, ADMIN_STATE_HARDWARE_FILE, HARDWARE_FILE,
                          IMAGE_FILE, FLAVOR_FILE, HARDWARE_KEYS, IMAGE_KEYS,
                          FLAVOR_KEYS, SERVER_FILE, SERVER_KEYS)


def _log(success, command):
    log_str = None
    if success is True:
        log_str = 'SUCCESS: ' + command + '\n'
    else:
        log_str = 'FAILURE: ' + command + '\n'
    with LOGFILE.open('a+') as log:  # + is create file if not exist
        log.write(log_str)

def _log_plus(success, context):
    pass

@click.group()
def cli():
    """
    Our command line interface (CLI) implemented in click.
    """
    pass


@click.command()
@click.pass_context
@click.option('--hardware', default='', help='Configure the hardware settings.')
@click.option('--images', default='', help='Configure the OS image settings.')
@click.option('--flavors', default='', help='Configure the flavor sizes.')
def config(ctx, hardware, images, flavors):
    """
    Import a configuration file.  NOTE: Importing a hardware file also resets
    the admin hardware file.
    """
    cli_input_base = "{} {} ".format(ctx.parent.info_name,
                                     ctx.info_name)
    if hardware != '':
        cli_input = cli_input_base + "-- hardware {}".format(hardware)
        path = Path(hardware)
        (success, err_msg) = import_hardware_config(path)
        if success is True:
            # don't print anything, just log
            (ad_s, ad_err_msg) = create_admin_hardware_state(HARDWARE_FILE,
                                                             ADMIN_STATE_HARDWARE_FILE)
            if ad_s is False:
                click.echo("Error: Couldn't create admin state... Reason:")
                click.echo(ad_err_msg)
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
        (success, data) = display(ADMIN_STATE_HARDWARE_FILE, HARDWARE_KEYS)
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
        click.echo("Available configurations:\n")
        click.echo("Hardware:")
        click.echo(hw_data + '\n')
        click.echo("Images")
        click.echo(im_data + '\n')
        click.echo("Flavors")
        click.echo(fl_data)

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


@click.group()
def admin():
    """
    Check if we can allocate hardware resources.
    """
    pass


@click.group('show')
def admin_show():
    """
    Displays admin configurations [just hardware right now].
    """
    pass


@click.command()
@click.argument('names', nargs=2)
@click.pass_context
def can_host(ctx, names):
    """
    Check to see if [machine name] can host a [flavor] configuration.
    """
    (machine_name, flavor) = names
    cli_input = "{} {} {} {} {}".format(ctx.parent.parent.info_name,
                                        ctx.parent.info_name,
                                        ctx.info_name,
                                        machine_name,
                                        flavor)
    (success, can_handle, msg) = can_hardware_handle_flavor(machine_name, flavor)
    if success is True:
        # the msg already has our contents
        click.echo(str(can_handle) + ': ' + msg)
    else:
        click.echo("Error: Cannot check if hardware can host flavor.  Reason:")
        click.echo(msg)
    _log(success, cli_input)


@click.group('server')
def server():
    """
    Create or delete virtual servers based on the available hardware.
    """
    pass


@click.command('create')
@click.pass_context
@click.option('--image', default='',
              help='The image (OS version) the virtual instance uses.')
@click.option('--flavor', default='',
              help='The hardware flavor the virtual instance loads on.')
@click.argument('name')
def server_create(ctx, image, flavor, name):
    """
    Create a virtual server based on the image and flavor.
    """
    # Logging
    success = None
    cli_input = "{} {} {}".format(ctx.parent.parent.info_name,
                                  ctx.parent.info_name,
                                  ctx.info_name)

    if image != '' and flavor != '':
        (success, err_msg) = create_server(name, image, flavor)
        if success is False:
            click.echo('Error: {}'.format(err_msg))
        else:
            click.echo(err_msg)  # success
    else:
        click.echo('Error, need non-empty --image and --flavor options.')
        success = False

    _log(success, cli_input)


@click.command('list')
@click.pass_context
def server_list(ctx):
    """
    Lists the currently active virtual servers.
    """
    cli_input = "{} {} {}".format(ctx.parent.parent.info_name,
                                  ctx.parent.info_name,
                                  ctx.info_name)
    (success, data) = display(SERVER_FILE, SERVER_KEYS)
    # display data and log
    if success is True:
        click.echo('Currently active virtual servers:')
        click.echo(data)
    else:
        click.echo('Error: Could not list virtual servers.  '
                   'Reasons:')
        click.echo(data)
    _log(success, cli_input)
    

@click.command('delete')
@click.pass_context
@click.argument('instance')
def server_delete(ctx, instance):
    """
    Removes the INSTANCE from the active virtual server list.
    """
    cli_input = "{} {} {}".format(ctx.parent.parent.info_name,
                                  ctx.parent.info_name,
                                  ctx.info_name)
    (success, msg) = delete_server(instance)
    click.echo(msg)
    _log(success, cli_input)


cli.add_command(config)
cli.add_command(show)
cli.add_command(admin)
cli.add_command(server)

admin_show.add_command(show_hardware)

admin.add_command(admin_show)
admin.add_command(can_host)

show.add_command(show_hardware)
show.add_command(show_images)
show.add_command(show_flavors)
show.add_command(show_all)

server.add_command(server_create)
server.add_command(server_list)
server.add_command(server_delete)

if __name__ == '__main__':
    cli()
