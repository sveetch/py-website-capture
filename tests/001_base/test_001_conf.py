# -*- coding: utf-8 -*-
import io
import json

import pytest

from website_capture.exceptions import SettingsInvalidError
from website_capture.conf import get_project_configuration


def test_invalid_json():
    """
    JSON exception should be raised when file is invalid JSON
    """
    source = "This is not JSON"

    with io.StringIO(source) as fp:
        with pytest.raises(json.decoder.JSONDecodeError):
            get_project_configuration(fp)


@pytest.mark.parametrize("source", [
    # Just empty JSON
    {},
    # Only "output_dir" field
    {
        "output_dir": "/nope"
    },
    # Only "pages" field
    {
        "pages": []
    },
])
def test_required_fields(source):
    """
    Config parser should raise exception when config miss some required fields
    """
    with io.StringIO(json.dumps(source)) as fp:
        with pytest.raises(SettingsInvalidError):
            get_project_configuration(fp)


@pytest.mark.parametrize("source, expected", [
    # Almost empty but valid
    (
        {
            "output_dir": "/nope",
            "pages": [],
        },
        {
            "output_dir": "/nope",
            "pages": [],
        },
    ),
    # Don"t really bother about (almost) any page options
    (
        {
            "output_dir": "/nope",
            "pages": [
                {
                    "name": "foo",
                    "ping": "pong",
                }
            ],
        },
        {
            "output_dir": "/nope",
            "pages": [
                {
                    "name": "foo",
                    "ping": "pong",
                }
            ],
        },
    ),
    # ..Except for page "sizes" option which should always be turned to tuples
    (
        {
            "output_dir": "/nope",
            "pages": [
                {
                    "name": "foo",
                    "sizes": [
                        (1, 42),
                        [2, 6],
                    ],
                }
            ],
        },
        {
            "output_dir": "/nope",
            "pages": [
                {
                    "name": "foo",
                    "sizes": [
                        (1, 42),
                        (2, 6),
                    ],
                }
            ],
        },
    ),
])
def test_required_page_options(source, expected):
    """
    Config parser should raise exception when a page config miss some required options
    """
    with io.StringIO(json.dumps(source)) as fp:
        conf = get_project_configuration(fp)

    assert conf == expected
