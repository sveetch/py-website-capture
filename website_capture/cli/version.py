# -*- coding: utf-8 -*-
from shutil import which

import click

from website_capture import __version__
from selenium import __version__ as selenium_version

@click.command()
@click.pass_context
def version_command(context):
    """
    Print out version information.
    """
    click.echo(f"py-website-capture {__version__}")

    geckodriver = which("geckodriver")
    if geckodriver:
        click.echo(f"├── Firefox WebDriver found at: {geckodriver}")

    chromedriver = which("chromedriver")
    if chromedriver:
        click.echo(f"├── Chrome WebDriver found at: {chromedriver}")

    safaridriver = which("safaridriver")
    if safaridriver:
        click.echo(f"├── Safari WebDriver found at: {safaridriver}")

    click.echo(f"└── Selenium version {selenium_version}")
