# -*- coding: utf-8 -*-
"""
Chrome test focus on specific methods without covering basic interface mechanic
like Firefox has allready done.
"""
import io
import json
import os
from shutil import which

import pytest

from website_capture.logs import init_logger
from website_capture.interfaces.selenium_interface import SeleniumChromeInterface


def test_driver_is_installed():
    """
    Driver binary should be available from system
    """
    assert which("chromedriver") is not None


def test_single_sized_screenshot(caplog, debuglogger, temp_builds_dir,
                                 demo_baseurl):
    """
    Given a single page with a single size for screenshot task, runner should
    return an item and screenshot file should have been created with a non
    null size.
    """
    testdir = "chrome_single_sized_screenshot"
    basedir = temp_builds_dir.join(testdir)
    os.makedirs(basedir)

    interface_instance = SeleniumChromeInterface(basedir=basedir)

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

    NOTE: This suffer from current bug with Chrome report task which get logs
    twice.
    """
    testdir = "chrome_single_report"
    basedir = temp_builds_dir.join(testdir)
    os.makedirs(basedir)

    interface_instance = SeleniumChromeInterface(basedir=basedir)

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

    with io.open(expected, "r") as fp:
        report = json.loads(fp.read())

    assert report["logs"] == [
        ["info", "35:16 \"Before error\""],
        ["error", "36:18 Uncaught ReferenceError: bar is not defined"],
        ["info", "35:16 \"Before error\""],
        ["error", "36:18 Uncaught ReferenceError: bar is not defined"]
    ]
