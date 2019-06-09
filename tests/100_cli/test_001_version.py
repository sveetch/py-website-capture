# -*- coding: utf-8 -*-
import os

import pytest

import click
from click.testing import CliRunner

from website_capture.cli.console_script import cli_frontend


def test_version_output(caplog):
    """
    Very basic test just for checking command health
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        # Default verbosity
        result = runner.invoke(cli_frontend, ['version'])

        assert caplog.record_tuples == []


        assert result.output.startswith('py-website-capture') == True
        assert result.exit_code == 0
