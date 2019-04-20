# -*- coding: utf-8 -*-
import click
import logging

from website_capture.interfaces.dummy import DummyScreenshot

from website_capture.interfaces.selenium_interface import (
    SeleniumFirefoxScreenshot,
    SeleniumChromeScreenshot
)

from website_capture.interfaces.splinter_interface import (
    SplinterFirefoxScreenshot,
    SplinterChromeScreenshot
)

from website_capture.conf import get_project_configuration


@click.command()
@click.option("--interface",
              type=click.Choice(["dummy", "selenium", "splinter"]),
              help=("Interface engine to perform browser tasks. Default is "
                    "Dummy interface."),
              default="dummy")
@click.option("--browser",
              type=click.Choice(["firefox", "chrome"]),
              help=("Browser(s) to use with interface engine. This does "
                    "nothing with Dummy interface"),
              multiple=True)
@click.option("--config", default=None, metavar="PATH",
              help="Path to config file",
              type=click.File("rb"),
              required=True)
@click.pass_context
def screenshot_command(context, interface, browser, config):
    """
    Screenshot pages from given configuration file.
    """
    logger = logging.getLogger("py-website-capture")

    json_config = get_project_configuration(config)

    interface_config = {
        "basedir": json_config["output_dir"],
        "size_dir": json_config.get("size_dir", True),
        "headless": json_config.get("headless", True),
    }

    if interface == "dummy":
        logger.info("🤖 DummyScreenshot")
        screenshoter = DummyScreenshot(**interface_config)
        screenshoter.run(pages=json_config["pages"])
    else:
        if len(browser) == 0:
            logger.warning("Interface engine require to choose at least a browser.")
            raise click.Abort()

    if interface == "selenium":
        if "firefox" in browser:
            logger.info("🤖 SeleniumFirefoxScreenshot")
            screenshoter = SeleniumFirefoxScreenshot(**interface_config)
            screenshoter.run(pages=json_config["pages"])

        if "chrome" in browser:
            logger.info("🤖 SeleniumChromeScreenshot")
            screenshoter = SeleniumChromeScreenshot(**interface_config)
            screenshoter.run(pages=json_config["pages"])

    if interface == "splinter":
        if "firefox" in browser:
            logger.info("🤖 SplinterFirefoxScreenshot")
            screenshoter = SplinterFirefoxScreenshot(**interface_config)
            screenshoter.run(pages=json_config["pages"])

        if "chrome" in browser:
            logger.info("🤖 SplinterChromeScreenshot")
            screenshoter = SplinterChromeScreenshot(**interface_config)
            screenshoter.run(pages=json_config["pages"])
