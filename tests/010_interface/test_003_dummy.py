# -*- coding: utf-8 -*-
import io
import json
import os

import pytest

from website_capture.interfaces.dummy import DummyDriver, DummyInterface


def test_get_driver_class():
    engine = DummyInterface()

    assert engine.get_driver_class() == DummyDriver


def test_get_driver_instance():
    engine = DummyInterface()

    assert isinstance(engine.get_driver_instance({}, {}),
                      DummyDriver) == True


@pytest.mark.parametrize("page,size,size_dir,expected", [
    (
        {
            "name": "foo",
            "url": "some_url",
            "tasks": ["screenshot"],
        },
        (1, 42),
        True,
        {
            "name": "foo",
            "url": "some_url",
            "size": (1, 42),
            "screenshot": "/basedir/1x42/foo_test.png",
        }
    ),
])
def test_capture(page, size, size_dir, expected):
    """
    'capture' method should perform tasks for given page
    """
    engine = DummyInterface("/basedir", size_dir=size_dir)
    engine.DESTINATION_FILEPATH = "{name}_test.png"

    config = engine.get_page_config(page, size)
    options = engine.get_driver_options(config)
    driver = engine.get_driver_instance(options, config)

    assert engine.capture(engine, config) == expected


@pytest.mark.parametrize("page,size_dir,expected", [
    (
        {
            "name": "foo",
            "url": "some_url",
            "sizes": [(1, 42)],
            "tasks": ["screenshot"],
        },
        True,
        [
            {
                "name": "foo",
                "url": "some_url",
                "size": (1, 42),
                "screenshot": "1x42/foo_test.png",
            },
        ]
    ),
])
def test_page_job(temp_builds_dir, insert_basedir, page, size_dir, expected):
    """
    page_job should perform capture for given from size 1x42
    """
    required_size = (1, 42)
    basedir = temp_builds_dir.join('interface_dummy_page_job')

    engine = DummyInterface(basedir, size_dir=size_dir)
    engine.DESTINATION_FILEPATH = "{name}_test.png"

    built, error_logs = engine.page_job(required_size, page)

    assert built == [insert_basedir(basedir, item) for item in expected]
    assert error_logs == []


@pytest.mark.parametrize("pages,size_dir,expected_dirs,expected_payload", [
    (
        [
            {
                "name": "foo",
                "url": "some_url",
                "sizes": [(1, 42)],
                "tasks": ["screenshot"],
            },
            {
                "name": "ping",
                "url": "some_ping",
                "sizes": [(1, 42), (30, 30)],
                "tasks": ["screenshot", "report"],
            },
        ],
        True,
        ["1x42"],
        [
            {
                "name": "foo",
                "url": "some_url",
                "size": (1, 42),
                "screenshot": "1x42/foo_test.png",
            },
            {
                "name": "ping",
                "url": "some_ping",
                "size": (1, 42),
                "screenshot": "1x42/ping_test.png",
                "report": {},
            },
        ],
    ),
])
def test_perform_size_pages(temp_builds_dir, insert_basedir, pages, size_dir, expected_dirs,
                            expected_payload):
    """
    perform_size_pages should perform capture for every page for size 1x42
    """
    required_size = (1, 42)
    basedir = temp_builds_dir.join('interface_dummy_perform_size_pages')

    engine = DummyInterface(basedir, size_dir=size_dir)
    engine.DESTINATION_FILEPATH = "{name}_test.png"

    built, error_logs = engine.perform_size_pages(required_size, pages)
    assert built == [insert_basedir(basedir, item) for item in expected_payload]
    assert error_logs == []

    assert os.listdir(basedir) == expected_dirs


@pytest.mark.parametrize("pages,size_dir,expected_dirs,expected_payload", [
    (
        [
            {
                "name": "foo",
                "url": "some_url",
                "sizes": [(1, 42)],
                "tasks": ["screenshot"],
            },
            {
                "name": "ping",
                "url": "some_ping",
                "sizes": [(1, 42), (30, 30)],
                "tasks": ["screenshot"],
            },
        ],
        True,
        ["Default", "1x42", "30x30"],
        [
            {
                "name": "foo",
                "url": "some_url",
                "size": (1, 42),
                "screenshot": "1x42/foo_test.png",
            },
            {
                "name": "ping",
                "url": "some_ping",
                "size": (1, 42),
                "screenshot": "1x42/ping_test.png",
            },
            {
                "name": "ping",
                "url": "some_ping",
                "size": (30, 30),
                "screenshot": "30x30/ping_test.png",
            },
        ],
    ),
])
def test_run(temp_builds_dir, insert_basedir, pages, size_dir, expected_dirs,
             expected_payload):
    """
    run method should perform capture for every pages for every sizes and
    return their payload
    """
    basedir = temp_builds_dir.join('interface_dummy_run')

    engine = DummyInterface(basedir, size_dir=size_dir)
    engine.DESTINATION_FILEPATH = "{name}_test.png"

    built, error_logs = engine.run(pages)
    assert built == [insert_basedir(basedir, item) for item in expected_payload]
    assert error_logs == []

    assert os.listdir(basedir) == expected_dirs
