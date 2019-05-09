# -*- coding: utf-8 -*-
import io
import json

import pytest

from website_capture.interfaces.base import BaseScreenshot
from website_capture.exceptions import InvalidPageSizeError, PageConfigError


@pytest.mark.parametrize("pages,expected", [
    # Empty or no sizes provided, return at least the default size
    (
        [{"sizes": []}],
        [BaseScreenshot._default_size_value]
    ),
    (
        [{}],
        [BaseScreenshot._default_size_value]
    ),
    # Single
    (
        [
            {"sizes": [(1, 42)]}
        ],
        [
            BaseScreenshot._default_size_value,
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
            BaseScreenshot._default_size_value,
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
            BaseScreenshot._default_size_value,
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
    interface = BaseScreenshot()

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
    interface = BaseScreenshot()

    with pytest.raises(InvalidPageSizeError):
        interface.get_available_sizes(pages)


@pytest.mark.parametrize("width,height,expected", [
    (
        BaseScreenshot._default_size_value[0],
        BaseScreenshot._default_size_value[1],
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
    interface = BaseScreenshot()

    assert interface.get_size_repr(width, height) == expected


@pytest.mark.parametrize("size,size_dir,expected", [
    (BaseScreenshot._default_size_value, True, "/basedir/Default"),
    ((1, 42), True, "/basedir/1x42"),
    ((1, 42), False, "/basedir"),
])
def test_get_destination_dir(size, size_dir, expected):
    interface = BaseScreenshot("/basedir", size_dir=size_dir)

    assert interface.get_destination_dir(size) == expected


@pytest.mark.parametrize("config,size_dir,expected", [
    (
        {
            "filename": "foo.png",
            "size": BaseScreenshot._default_size_value,
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
    interface = BaseScreenshot("/basedir", size_dir=size_dir)

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
    interface = BaseScreenshot()

    with pytest.raises(PageConfigError):
        assert interface.get_page_config(page, (1, 42))


@pytest.mark.parametrize("page,size,size_dir,expected", [
    (
        {
            "name": "foo.png",
            "url": "some_url",
        },
        (1, 42),
        True,
        {
            "name": "foo.png",
            "url": "some_url",
            "size": (1, 42),
            "destination": "/basedir/1x42/foo.png_base.png",
            "log_path": "/basedir/1x42/foo.png_base.png.driver.log",
        }
    ),
    (
        {
            "name": "foo.png",
            "filename": "bar.png",
            "url": "some_url",
        },
        (1, 42),
        True,
        {
            "name": "foo.png",
            "url": "some_url",
            "size": (1, 42),
            "destination": "/basedir/1x42/bar.png_base.png",
            "log_path": "/basedir/1x42/bar.png_base.png.driver.log",
        }
    ),
])
def test_get_page_config(page, size, size_dir, expected):
    interface = BaseScreenshot("/basedir", size_dir=size_dir)
    print(interface.get_page_config(page, size))
    assert interface.get_page_config(page, size) == expected
