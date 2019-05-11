# -*- coding: utf-8 -*-
import io
import json
import os

import pytest

from website_capture.interfaces.dummy import DummyInterface, DummyScreenshot


def test_get_interface_class():
    engine = DummyScreenshot()

    assert engine.get_interface_class() == DummyInterface


def test_get_interface_instance():
    engine = DummyScreenshot()

    assert isinstance(engine.get_interface_instance({}),
                      DummyInterface) == True


@pytest.mark.parametrize("page,size,size_dir,expected", [
    (
        {
            "name": "foo",
            "url": "some_url",
        },
        (1, 42),
        True,
        "/basedir/1x42/foo_test.png",
    ),
])
def test_capture(page, size, size_dir, expected):
    engine = DummyScreenshot("/basedir", size_dir=size_dir)
    engine.DESTINATION_FILEPATH = "{name}_test.png"

    config = engine.get_page_config(page, size)
    options = engine.get_interface_options(config)
    interface = engine.get_interface_instance(options)

    assert engine.capture(engine, config) == expected


@pytest.mark.parametrize("pages,size_dir,expected_dirs,expected_screens", [
    # Expected paths are relative to their future base directory which will
    # be appended during assertions
    (
        [
            {
                "name": "foo",
                "url": "some_url",
                "sizes": [(1, 42)],
            },
            {
                "name": "ping",
                "url": "some_ping",
                "sizes": [(1, 42), (30, 30)],
            },
        ],
        True,
        ["Default", "1x42", "30x30"],
        [
            "1x42/foo_test.png",
            "1x42/ping_test.png",
            "30x30/ping_test.png",
        ],
    ),
])
def test_run(temp_builds_dir, pages, size_dir, expected_dirs, expected_screens):
    basedir = temp_builds_dir.join('interface_dummy_run')

    engine = DummyScreenshot(basedir, size_dir=size_dir)
    engine.DESTINATION_FILEPATH = "{name}_test.png"

    assert engine.run(pages) == [os.path.join(basedir, item) \
                                 for item in expected_screens]

    assert os.listdir(basedir) == expected_dirs
