"""
Some fixture methods
"""
import os

import pytest

from website_capture.logs import init_logger


@pytest.fixture(scope='session')
def demo_baseurl(tmpdir_factory):
    """
    Return base URL for expected demo server
    """
    return "http://localhost:8001"


@pytest.fixture(scope='function')
def debuglogger(tmpdir_factory):
    """
    Initialize logger object without printout enabled and debug level
    """
    return init_logger("py-website-capture", "DEBUG", printout=True)


@pytest.fixture(scope='session')
def temp_builds_dir(tmpdir_factory):
    """
    Prepare a temporary build directory
    """
    fn = tmpdir_factory.mktemp('builds_selenium')
    return fn


@pytest.fixture(scope='session')
def insert_basedir():
    """
    Prepend basedir to enabled payload fields

    This return a function which will perform this.
    """
    def curry_func(basedir, payload, fields=["logs", "screenshot"]):
        for item in fields:
            if item in payload and isinstance(payload[item], str):
                payload[item] = os.path.join(basedir, payload[item])
        return payload

    return curry_func
