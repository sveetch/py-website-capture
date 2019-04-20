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

from website_capture.settings import *

@click.command()
@click.option('--interface',
              type=click.Choice(['dummy', 'selenium', 'splinter']),
              help='Interface engine to perform tasks',
              default="dummy")
@click.pass_context
def screenshot_command(context, interface):
    """
    Screenshot pages

    Actually just for development debugging
    """
    logger = logging.getLogger("py-website-capture")

    if interface == "dummy":
        logger.info("🤖 DummyScreenshot")
        screenshoter = DummyScreenshot(basedir=DUMPS_PATH)
        screenshoter.run(pages=PAGES)

    if interface == "selenium":
        logger.info("🤖 SeleniumFirefoxScreenshot")
        screenshoter = SeleniumFirefoxScreenshot(
            basedir=DUMPS_PATH,
        )
        screenshoter.run(pages=PAGES)

        logger.info("🤖 SeleniumChromeScreenshot")
        screenshoter = SeleniumChromeScreenshot(
            basedir=DUMPS_PATH,
        )
        screenshoter.run(pages=PAGES)

    if interface == "splinter":
        logger.info("🤖 SplinterFirefoxScreenshot")
        screenshoter = SplinterFirefoxScreenshot(
            basedir=DUMPS_PATH,
        )
        screenshoter.run(pages=PAGES)

        logger.info("🤖 SplinterChromeScreenshot")
        screenshoter = SplinterChromeScreenshot(
            basedir=DUMPS_PATH,
        )
        screenshoter.run(pages=PAGES)
