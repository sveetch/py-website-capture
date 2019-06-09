# -*- coding: utf-8 -*-
import click
import logging
from collections import OrderedDict

from website_capture.exceptions import SettingsInvalidError
from website_capture.interfaces.dummy import DummyInterface

from website_capture.interfaces.selenium_interface import (
    SeleniumFirefoxInterface,
    SeleniumChromeInterface
)

from website_capture.conf import get_project_configuration


INTERFACES = OrderedDict((
    ("dummy", DummyInterface),
    ("firefox", SeleniumFirefoxInterface),
    ("chrome", SeleniumChromeInterface),
))

DEFAULT_INTERFACE = "dummy"

@click.command()
@click.option("--interface",
              type=click.Choice(INTERFACES.keys()),
              help=("Interface engine to perform browser tasks. If argument is "
                    "empty the default interface "
                    "'{}' is used.".format(DEFAULT_INTERFACE)),
              multiple=True)
@click.option("--config", default=None, metavar="PATH",
              help="Path to config file",
              type=click.File("rb"),
              required=True)
@click.pass_context
def capture_command(context, interface, config):
    """
    Perform page capture(s) from a job configuration file with required
    interface(s).
    """
    logger = logging.getLogger("py-website-capture")

    try:
        json_config = get_project_configuration(config)
    except SettingsInvalidError as e:
        logger.critical(e)
        raise click.Abort()


    interface_config = {
        "basedir": json_config["output_dir"],
        "size_dir": json_config.get("size_dir", True),
        "headless": json_config.get("headless", True),
    }

    if len(interface) == 0:
        logger.warning(
            ("No interface was chosen, using default "
             "'{}' interface").format(DEFAULT_INTERFACE)
        )
        interface = (DEFAULT_INTERFACE,)

    for item in interface:
        klass = INTERFACES[item]
        logger.info("🤖 {}".format(klass.__name__))
        interface_instance = klass(**interface_config)
        interface_instance.run(json_config["pages"])
