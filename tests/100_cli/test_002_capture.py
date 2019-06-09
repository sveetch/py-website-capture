# -*- coding: utf-8 -*-
import io
import json
import os

import pytest

import click
from click.testing import CliRunner

from website_capture.cli.console_script import cli_frontend


def test_empty_fail(caplog):
    """
    Just check invoking command without argument fail because of required args.
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        result = runner.invoke(cli_frontend, ["capture"])

        assert caplog.record_tuples == []

        assert result.exit_code == 2


def test_config_fail(caplog):
    """
    Invalid configuration file should output a critical log and abort script
    execution.
    """
    runner = CliRunner()

    config = {
        "pages": [
            {
                "name": "perdu.com",
            },
        ]
    }

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        with io.open("foo.json", 'w') as fp:
            json.dump(config, fp)

        result = runner.invoke(cli_frontend, [
            "capture",
            "--config",
            "foo.json",
        ])

        print(result.output)
        print(caplog.record_tuples)

        assert caplog.record_tuples == [
            (
                'py-website-capture',
                50,
                ("Your configuration must contains a directory path where to "
                 "create files in a 'output_dir' item.")
            )
        ]

        assert 'Aborted!' in result.output
        assert result.exit_code == 1


def test_dummy(caplog):
    """
    Dummy driver usage
    """
    runner = CliRunner()

    config = {
        "output_dir": "./outputs/",
        "pages": [
            {
                "name": "basic-lorem-ipsum",
                "url": "http://localhost:8001/lorem-ipsum.basic.html",
                "tasks": ["screenshot"],
            },
        ]
    }

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        with io.open("foo.json", 'w') as fp:
            json.dump(config, fp)

        result = runner.invoke(cli_frontend, [
            "capture",
            "--config",
            "foo.json",
        ])

        #print("exit_code:", result.exit_code)
        #print(result.output)
        #print(caplog.record_tuples)

        assert caplog.record_tuples == [
            ("py-website-capture", 30,
             "No interface was chosen, using default 'dummy' interface"),
            ("py-website-capture", 20,
             "🤖 DummyInterface"),
            ("py-website-capture", 20,
             "🔹 Getting page for: basic-lorem-ipsum (Default)")
        ]

        assert result.exit_code == 0
