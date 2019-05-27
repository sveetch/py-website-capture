"""
Some fixture methods
"""
import os

import pytest


@pytest.fixture(scope='session')
def temp_builds_dir(tmpdir_factory):
    """
    Prepare a temporary build directory
    """
    fn = tmpdir_factory.mktemp('builds')
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
