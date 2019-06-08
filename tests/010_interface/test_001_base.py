# -*- coding: utf-8 -*-
import io
import json

import pytest

from website_capture.interfaces.base import BaseInterface
from website_capture.exceptions import InvalidPageSizeError, PageConfigError


@pytest.mark.parametrize("pages,expected", [
    # Empty or no sizes provided, return at least the default size
    (
        [{"sizes": []}],
        [BaseInterface._default_size_value]
    ),
    (
        [{}],
        [BaseInterface._default_size_value]
    ),
    # Single
    (
        [
            {"sizes": [(1, 42)]}
        ],
        [
            BaseInterface._default_size_value,
            (1, 42),
        ]
    ),
    # Multiple same size is stored only once
    (
        [
            {
                "sizes": [
                    (1, 42),
                ],
            },
            {
                "sizes": [
                    (1, 42),
                ],
            },
            {
                "sizes": [
                    (1, 42),
                ],
            },
        ],
        [
            BaseInterface._default_size_value,
            (1, 42),
        ]
    ),
    # Various sizes
    (
        [
            {
                "sizes": [
                    (42, 42),
                ],
            },
            {
                "sizes": [
                    (1, 42),
                    (300, 1444),
                ],
            },
            {
                "sizes": [
                    (1, 42),
                ],
            },
            {
                "sizes": [
                    (42, 42),
                    (300, 1444),
                    (1397, 22),
                    (1, 42),
                ],
            },
        ],
        [
            BaseInterface._default_size_value,
            (1, 42),
            (42, 42),
            (300, 1444),
            (1397, 22),
        ]
    ),
])
def test_get_available_sizes(pages, expected):
    """
    All defined sizes through every pages should be registered
    """
    interface = BaseInterface()

    assert interface.get_available_sizes(pages) == expected


@pytest.mark.parametrize("pages", [
    [{"sizes": ["nope"]}],
    [{"sizes": ["20x42"]}],
    [{"sizes": [(1, 42), "20x42"]}],
    [{"sizes": [(1, 42, 41)]}],
])
def test_get_available_sizes_invalid(pages):
    """
    Size is always an iterable of two items, every other size kind should
    raise an exception
    """
    interface = BaseInterface()

    with pytest.raises(InvalidPageSizeError):
        interface.get_available_sizes(pages)


@pytest.mark.parametrize("width,height,expected", [
    (
        BaseInterface._default_size_value[0],
        BaseInterface._default_size_value[1],
        "Default"
    ),
    (1, 42, "1x42"),
    (10, 42, "10x42"),
    (1200, 420, "1200x420"),
])
def test_get_size_repr(width, height, expected):
    """
    Size representation from given width and height is always a string like
    ``WIDTHxHEIGHT``. Default size value is always representated as "Default"
    """
    interface = BaseInterface()

    assert interface.get_size_repr(width, height) == expected


@pytest.mark.parametrize("size,size_dir,expected", [
    (BaseInterface._default_size_value, True, "/basedir/Default"),
    ((1, 42), True, "/basedir/1x42"),
    ((1, 42), False, "/basedir"),
])
def test_get_destination_dir(size, size_dir, expected):
    interface = BaseInterface("/basedir", size_dir=size_dir)

    assert interface.get_destination_dir(size) == expected


@pytest.mark.parametrize("config,size_dir,expected", [
    (
        {
            "filename": "foo.png",
            "size": BaseInterface._default_size_value,
        },
        True,
        "/basedir/Default/foo.png"
    ),
    (
        {
            "filename": "foo.png",
            "size": (1, 42),
        },
        True,
        "/basedir/1x42/foo.png"
    ),
    (
        {
            "filename": "foo.png",
            "size": (1, 42),
        },
        False,
        "/basedir/foo.png"
    ),
])
def test_get_file_destination(config, size_dir, expected):
    interface = BaseInterface("/basedir", size_dir=size_dir)

    assert interface.get_file_destination(config) == expected


@pytest.mark.parametrize("page", [
    # Not any mandatory field
    {
        "foo": "bar",
    },
    # Missing "name"
    {
        "url": "bar",
    },
    # Missing "url"
    {
        "name": "bar",
    },
])
def test_get_page_config_invalid(page):
    """
    A config page item require some mandatory fields
    """
    interface = BaseInterface()

    with pytest.raises(PageConfigError):
        assert interface.get_page_config(page, (1, 42))


@pytest.mark.parametrize("page,size,size_dir,expected", [
    # Without 'filename' option the "DESTINATION_FILEPATH" interface attribute
    # should be used to create filenames
    (
        {
            "name": "foo",
            "url": "some_url",
        },
        (1, 42),
        True,
        {
            "destination": "/basedir/1x42/foo_test",
            "screenshot_path": "/basedir/1x42/foo_test.png",
            "driver_log_path": "/basedir/1x42/foo_test.driver.log",
            "browser_log_path": "/basedir/1x42/foo_test.report.json",
            "name": "foo",
            "size": (1, 42),
            "url": "some_url",
        }
    ),
    # When 'filename' option is given, it should be used to create filenames
    # Also, additional options like "filename" and "ping" should be passed to
    # final page config
    (
        {
            "filename": "bar",
            "name": "foo",
            "ping": "pong",
            "url": "some_url",
        },
        (1, 42),
        True,
        {
            "destination": "/basedir/1x42/bar",
            "filename": "bar",
            "screenshot_path": "/basedir/1x42/bar.png",
            "driver_log_path": "/basedir/1x42/bar.driver.log",
            "browser_log_path": "/basedir/1x42/bar.report.json",
            "name": "foo",
            "ping": "pong",
            "size": (1, 42),
            "url": "some_url",
        }
    ),
])
def test_get_page_config(page, size, size_dir, expected):
    interface = BaseInterface("/basedir", size_dir=size_dir)
    interface.DESTINATION_FILEPATH = "{name}_test"
    assert interface.get_page_config(page, size) == expected


def test_get_driver_options():
    """
    Dummy test just for coverage since Base class don't implement nothing
    """
    interface = BaseInterface()
    assert interface.get_driver_options({}) == {}


def test_get_driver_class():
    """
    Dummy test just for coverage since Base class don't implement nothing
    """
    interface = BaseInterface()
    assert interface.get_driver_class() == None


def test_get_driver_instance():
    """
    Dummy test just for coverage since Base class don't implement nothing
    """
    interface = BaseInterface()

    with pytest.raises(NotImplementedError):
        interface.get_driver_instance({}, {})


@pytest.mark.parametrize("page,size,size_dir,expected", [
    (
        {
            "name": "foo",
            "url": "some_url",
        },
        (1, 42),
        True,
        "Pretending to load page: some_url",
    ),
])
def test_load_page(page, size, size_dir, expected):
    interface = BaseInterface("/basedir", size_dir=size_dir)
    # For BaseInterface test we don't need a real driver
    driver = object()

    config = interface.get_page_config(page, size)

    assert interface.load_page(driver, config) == expected


@pytest.mark.parametrize("page,size,size_dir,expected", [
    # No task
    (
        {
            "name": "foo",
            "url": "some_url",
        },
        (1, 42),
        True,
        None,
    ),
    # Single screenshot task
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
        },
    ),
    # Screenshot and report tasks
    (
        {
            "name": "foo",
            "url": "some_url",
            "tasks": ["screenshot", "report"],
        },
        (1, 42),
        True,
        {
            "name": "foo",
            "url": "some_url",
            "size": (1, 42),
            "screenshot": "/basedir/1x42/foo_test.png",
            "report": {},
        },
    ),
])
def test_capture(page, size, size_dir, expected):
    interface = BaseInterface("/basedir", size_dir=size_dir)
    interface.DESTINATION_FILEPATH = "{name}_test"
    # For BaseInterface test we don't need a real driver
    driver = object()

    config = interface.get_page_config(page, size)

    assert interface.capture(driver, config) == expected
