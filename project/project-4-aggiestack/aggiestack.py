#!/usr/bin/env python3

"""
The CLI (command line interface) of aggiescript.  The 'main' function.
"""
from pathlib import Path
import click

from lib.utils.io_helpers import load_state
from lib.config_io import (import_hardware_config, import_image_config,
                           import_flavor_config, create_admin_hardware_state)
from lib.display import display, get_table
from lib.admin import (
    can_hardware_handle_flavor,
    evacuate_rack,
    add_machine,
    remove_machine
)
from lib.server import create_server, delete_server, reset_server_list
from lib.settings import (LOGFILE, ADMIN_STATE_HARDWARE_FILE, HARDWARE_FILE,
                          IMAGE_FILE, FLAVOR_FILE, RACK_KEYS, HARDWARE_KEYS,
                          IMAGE_KEYS, FLAVOR_KEYS, SERVER_FILE, SERVER_KEYS,
                          INSTANCE_KEYS)


def _log(success, command):
    log_str = None
    if success is True:
        log_str = 'SUCCESS: ' + command + '\n'
    else:
        log_str = 'FAILURE: ' + command + '\n'
    with LOGFILE.open('a+') as log:  # + is create file if not exist
        log.write(log_str)


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
    if ((hardware != '' and images != '') or (hardware != '' and flavors != '')
       or (images != '' and flavors != '')):
        cli_input = cli_input_base
        if hardware != '':
            cli_input += '--hardware {} '.format(hardware)
        if images != '':
            cli_input += '--images {} '.format(images)
        if flavors != '':
            cli_input += '--flavors {}'.format(flavors)

        click.echo('Error: Can only accept ONE option [hardware, flavor, '
                   'image] at a time.')
        _log(False, cli_input)

    elif hardware != '':
        cli_input = cli_input_base + "--hardware {}".format(hardware)
        path = Path(hardware)
        (success, err_msg) = import_hardware_config(path)
        if success is True:
            # don't print anything, just log
            (ad_s, ad_err_msg) = create_admin_hardware_state(HARDWARE_FILE,
                                                             ADMIN_STATE_HARDWARE_FILE)
            SERVER_FILE.unlink()  # new hardware, reset the server list
            if ad_s is False:
                click.echo("Error: Couldn't create admin state... Reason:")
                click.echo(ad_err_msg)
            (sv_s, sv_err_msg) = reset_server_list()
            if sv_s is False:
                click.echo("Error: Couldn't create admin state... Reason:")
                click.echo(sv_err_msg)
            click.echo('Reset server list after configuration.')
            click.echo('Successfully configured hardware with [{}].'.format(hardware))
            _log(True, cli_input)
        else:
            click.echo("Error: couldn't import hardware settings.  Reasons:")
            click.echo(err_msg)
            _log(False, cli_input)

    elif images != '':
        cli_input = cli_input_base + "--images {}".format(hardware)
        path = Path(images)
        (success, err_msg) = import_image_config(path)
        if success is True:
            (sv_s, sv_err_msg) = reset_server_list()
            if sv_s is False:
                click.echo("Error: Couldn't create admin state... Reason:")
                click.echo(sv_err_msg)
            click.echo('Reset server list after configuration.')
            click.echo('Successfully configured images with [{}].'.format(images))
            _log(True, cli_input)
        else:
            click.echo("Error: couldn't import images settings.  Reasons:")
            click.echo(err_msg)
            _log(False, cli_input)

    elif flavors != '':
        cli_input = cli_input_base + "-- flavors{}".format(hardware)
        path = Path(flavors)
        (success, err_msg) = import_flavor_config(path)
        if success is True:
            (sv_s, sv_err_msg) = reset_server_list()
            if sv_s is False:
                click.echo("Error: Couldn't create admin state... Reason:")
                click.echo(sv_err_msg)
            click.echo('Reset server list after configuration.')
            click.echo('Successfully configured flavors with [{}].'.format(flavors))
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
        (success, state) = load_state(ADMIN_STATE_HARDWARE_FILE)
        if success is True:
            data = 'Racks:\n' + get_table(state['racks'], RACK_KEYS)
            data += ('\n\nMachines:\n' + get_table(state['machines'], HARDWARE_KEYS))
    else:
        cli_input = "{} {} {}".format(ctx.parent.parent.info_name,
                                      ctx.parent.info_name,
                                      ctx.info_name)
        table_info = 'Available default hardware configurations:'
        (success, state) = load_state(HARDWARE_FILE)
        if success is True:
            data = 'Racks:\n' + get_table(state['racks'], RACK_KEYS)
            data += ('\n\nMachines:\n' + get_table(state['machines'], HARDWARE_KEYS))
    # display data and log
    if success is True:
        click.echo(table_info)
        click.echo(data)
    else:
        click.echo('Error: Could not display configurations for hardware. '
                   'Reasons:')
        click.echo(data)
    _log(success, cli_input)


@click.command('images')
@click.pass_context
def show_images(ctx):
    """
    Displays the available image configurations.
    """
    (success, data) = display(IMAGE_FILE, IMAGE_KEYS)
    # display data and log
    if success is True:
        click.echo('Available base images configurations:')
        click.echo(data)
    else:
        click.echo('Error: Could not display configurations for images. '
                   'Reasons:')
        click.echo(data)
    cli_input = "{} {} {}".format(ctx.parent.parent.info_name,
                                  ctx.parent.info_name,
                                  ctx.info_name)
    _log(success, cli_input)


@click.command('flavors')
@click.pass_context
def show_flavors(ctx):
    """
    Displays the available flavor configurations.
    """
    (success, data) = display(FLAVOR_FILE, FLAVOR_KEYS)
    # display data and log
    if success is True:
        click.echo('Available base flavor configurations:')
        click.echo(data)
    else:
        click.echo('Error: Could not display configurations for flavors.  Reasons:')
        click.echo(data)
    cli_input = "{} {} {}".format(ctx.parent.parent.info_name,
                                  ctx.parent.info_name,
                                  ctx.info_name)
    _log(success, cli_input)


@click.command('all')
@click.pass_context
def show_all(ctx):
    """
    Displays all the available configurations.
    """
    # hardware
    hw_data = None
    (hw_success, state) = load_state(HARDWARE_FILE)
    if hw_success is True:
        hw_data = get_table(state['racks'], RACK_KEYS)
        hw_data += ('\n\n' + get_table(state['machines'], HARDWARE_KEYS))
    (im_success, im_data) = display(IMAGE_FILE, IMAGE_KEYS)
    (fl_success, fl_data) = display(FLAVOR_FILE, FLAVOR_KEYS)

    success = hw_success and im_success and fl_success
    # display errors first, then data
    if success is True:
        click.echo("Available configurations:\n")
        click.echo("Hardware:")
        click.echo(hw_data + '\n')
        click.echo("Images:")
        click.echo(im_data + '\n')
        click.echo("Flavors:")
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
    cli_input = "{} {} {}".format(ctx.parent.parent.info_name,
                                  ctx.parent.info_name,
                                  ctx.info_name)
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
    Displays admin configurations, or the current usage of servers and
    hardware.
    """
    pass


@click.command('instances')
@click.pass_context
def show_instances(ctx):
    """
    Shows where (hardware) each instance is running on.
    """
    (success, data) = display(SERVER_FILE, INSTANCE_KEYS)
    # display data and log
    if success is True:
        click.echo('Currently active virtual servers and their physical '
                   'server locations (hardware).')
        click.echo(data)
    else:
        click.echo('Error: Could not list virtual servers.  '
                   'Reasons:')
        click.echo(data)
    cli_input = "{} {} {} {}".format(ctx.parent.parent.parent.info_name,
                                     ctx.parent.parent.info_name,
                                     ctx.parent.info_name,
                                     ctx.info_name)
    _log(success, cli_input)


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
    (success, can_handle, msg) = can_hardware_handle_flavor(machine_name,
                                                            flavor)
    if success is True:
        # the msg already has our contents
        click.echo(str(can_handle) + ': ' + msg)
    else:
        click.echo("Error: Cannot check if hardware can host flavor.  Reason:")
        click.echo(msg)
    _log(success, cli_input)


@click.command()
@click.argument('rack_name')
@click.pass_context
def evacuate(ctx, rack_name):
    """
    Removes a rack from the configuration and all it's associated machines.
    """
    (success, msg) = evacuate_rack(rack_name)
    click.echo(msg)
    cli_input = "{} {} {} {}".format(
        ctx.parent.parent.info_name,
        ctx.parent.info_name,
        ctx.info_name,
        rack_name
    )
    _log(success, cli_input)


@click.command()
@click.argument('machine')
@click.pass_context
def remove(ctx, machine):
    """
    Removes a machine from the configuration.
    """
    (success, msg) = remove_machine(machine)
    click.echo(msg)
    cli_input = "{} {} {} {}".format(
        ctx.parent.parent.info_name,
        ctx.parent.info_name,
        ctx.info_name,
        machine
    )
    _log(success, cli_input)


@click.command()
@click.pass_context
@click.argument('machine')
@click.option('-mem', required=True)
@click.option('-disk', required=True)
@click.option('-vcpus', required=True)
@click.option('-ip', required=True)
@click.option('-rack', required=True)
def add(ctx, machine, mem, disk, vcpus, ip, rack):
    """
    Add a machine to the configuration
    """
    (success, msg) = add_machine(machine, mem, disk, vcpus, ip, rack)
    click.echo(msg)
    cli_input = "{} {} {} ".format(ctx.parent.parent.info_name,
                                   ctx.parent.info_name,
                                   ctx.info_name)
    cli_input += (
        '-mem {} -disk {} -vcpus {} -ip {} -rack {} {}'.format(
            mem, disk, vcpus, ip, rack, machine)
        )
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
    base_cli_input = "{} {} {}".format(ctx.parent.parent.info_name,
                                       ctx.parent.info_name,
                                       ctx.info_name)
    if image != '' and flavor != '' and name != '':
        option_cli_input = ' --image {} --flavor {} {}'.format(image,
                                                              flavor,
                                                              name)
        (success, err_msg) = create_server(name, image, flavor)
        click.echo(err_msg)  # err_msg contains the results of the create().
    else:
        click.echo('Error, need non-empty --image and --flavor options, '
                   'along with an unique instance name.')
        success = False
    _log(success, base_cli_input + option_cli_input)


@click.command('list')
@click.pass_context
def server_list(ctx):
    """
    Lists the currently active virtual servers.
    """
    (success, data) = display(SERVER_FILE, SERVER_KEYS)
    # display data and log
    if success is True:
        click.echo('Currently active virtual servers:')
        click.echo(data)
    else:
        click.echo('Error: Could not list virtual servers.  '
                   'Reasons:')
        click.echo(data)
    cli_input = "{} {} {}".format(ctx.parent.parent.info_name,
                                  ctx.parent.info_name,
                                  ctx.info_name) 
    _log(success, cli_input)


@click.command('delete')
@click.pass_context
@click.argument('instance')
def server_delete(ctx, instance):
    """
    Removes the INSTANCE from the active virtual server list.
    """
    cli_input = "{} {} {} {}".format(ctx.parent.parent.info_name,
                                     ctx.parent.info_name,
                                     ctx.info_name,
                                     instance)
    (success, msg) = delete_server(instance)
    click.echo(msg)
    _log(success, cli_input)


cli.add_command(config)
cli.add_command(show)
cli.add_command(admin)
cli.add_command(server)

admin_show.add_command(show_hardware)
admin_show.add_command(show_instances)

admin.add_command(admin_show)
admin.add_command(can_host)
admin.add_command(evacuate)
admin.add_command(add)
admin.add_command(remove)

show.add_command(show_hardware)
show.add_command(show_images)
show.add_command(show_flavors)
show.add_command(show_all)

server.add_command(server_create)
server.add_command(server_list)
server.add_command(server_delete)

if __name__ == '__main__':
    cli()
