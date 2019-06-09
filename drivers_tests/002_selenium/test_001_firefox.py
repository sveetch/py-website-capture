# -*- coding: utf-8 -*-
import io
import json
import os
from shutil import which

import pytest

import click
from click.testing import CliRunner

from website_capture.cli.console_script import cli_frontend
from website_capture.logs import init_logger
from website_capture.interfaces.selenium_interface import SeleniumFirefoxInterface


def test_driver_is_installed():
    """
    Driver binary should be available from system
    """
    assert which("geckodriver") is not None


def test_notask(caplog, debuglogger, temp_builds_dir, demo_baseurl):
    """
    Page job without any tasks should run without failing but won't produce
    anything
    """
    testdir = "firefox_notask"
    basedir = temp_builds_dir.join(testdir)
    os.makedirs(basedir)

    interface_instance = SeleniumFirefoxInterface(basedir=basedir)

    built, error_logs = interface_instance.run([
        {
            "name": "lorem-ipsum-nofield",
            "url": "{}/lorem-ipsum.basic.html".format(demo_baseurl),
            "sizes": [(1440, 768)],
        },
        {
            "name": "lorem-ipsum-empty",
            "url": "{}/lorem-ipsum.basic.html".format(demo_baseurl),
            "sizes": [(1440, 768)],
            "tasks": [],
        },
    ])

    assert len(built) == 0


def test_nosize(caplog, debuglogger, temp_builds_dir, demo_baseurl):
    """
    Given pages with no defined size for a task, runner should
    return perform task and related task file should have been created with a
    non null size.
    """
    testdir = "firefox_single_nosize_screenshot"
    basedir = temp_builds_dir.join(testdir)
    os.makedirs(basedir)

    interface_instance = SeleniumFirefoxInterface(basedir=basedir)

    built, error_logs = interface_instance.run([
        {
            "name": "lorem-ipsum-nofield",
            "url": "{}/lorem-ipsum.basic.html".format(demo_baseurl),
            "tasks": ["screenshot"],
        },
        {
            "name": "lorem-ipsum-empty",
            "url": "{}/lorem-ipsum.basic.html".format(demo_baseurl),
            "sizes": [],
            "tasks": ["screenshot"],
        },
    ])

    assert len(built) == 2

    for item in built:
        assert os.path.exists(item["screenshot"]) == True
        assert os.stat(item["screenshot"]).st_size > 0


def test_single_sized_screenshot(caplog, debuglogger, temp_builds_dir,
                                 demo_baseurl):
    """
    Given a single page with a single size for screenshot task, runner should
    return an item and screenshot file should have been created with a non
    null size.
    """
    testdir = "firefox_single_sized_screenshot"
    basedir = temp_builds_dir.join(testdir)
    os.makedirs(basedir)

    interface_instance = SeleniumFirefoxInterface(basedir=basedir)

    built, error_logs = interface_instance.run([{
        "name": "lorem-ipsum",
        "url": "{}/lorem-ipsum.basic.html".format(demo_baseurl),
        "sizes": [(1440, 768)],
        "tasks": ["screenshot"],
    }])

    assert len(built) == 1

    expected = built[0]["screenshot"]
    assert os.path.exists(expected) == True
    assert os.stat(expected).st_size > 0


def test_single_report(caplog, debuglogger, temp_builds_dir, demo_baseurl):
    """
    Given a single page with a single size for report task, runner should
    return an item and report file should have been created with expected logs.
    """
    testdir = "firefox_single_report"
    basedir = temp_builds_dir.join(testdir)
    os.makedirs(basedir)

    interface_instance = SeleniumFirefoxInterface(basedir=basedir)

    built, error_logs = interface_instance.run([{
        "name": "every-logs",
        "url": "{}/every-logs.basic.html".format(demo_baseurl),
        "sizes": [(1440, 768)],
        "tasks": ["report"],
    }])

    assert len(built) == 1
    assert "report" in built[0]

    expected = built[0]["report"]
    assert os.path.exists(expected) == True
    assert os.stat(expected).st_size > 0

    # Open create report to check it
    with io.open(expected, "r") as fp:
        report = json.loads(fp.read())

    assert report["interface"] == "SeleniumFirefoxInterface"
    assert report["elapsed_time"] > 0

    assert report["logs"] == [
        [
            "error",
            "line 37: ReferenceError: bar is not defined"
        ]
    ]


def test_cli_screenshot(caplog):
    """
    Driver screenshot usage on simple demo page with custom base filename and
    without size directory.
    """
    runner = CliRunner()

    config = {
        "output_dir": ".",
        "size_dir": False,
        "pages": [
            {
                "name": "basic-lorem-ipsum",
                "url": "http://localhost:8001/lorem-ipsum.basic.html",
                "filename": "sample_{size}",
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
            "--interface",
            "firefox",
        ])

        #print("exit_code:", result.exit_code)
        #print(result.output)
        #print(caplog.record_tuples)

        assert caplog.record_tuples == [
            ("py-website-capture", 20,
             "🤖 SeleniumFirefoxInterface"),
            ("py-website-capture", 20,
             "🔹 Getting page for: basic-lorem-ipsum (Default)")
        ]

        assert sorted(os.listdir(test_cwd)) == sorted([
            "sample_Default.png",
            "foo.json",
        ])

        expected = os.path.join(test_cwd, "sample_Default.png")
        assert os.stat(expected).st_size > 0

        assert result.exit_code == 0
