# -*- coding: utf-8 -*-
import io
import json
import os

import pytest

from website_capture.interfaces.base import LogManagerMixin


@pytest.mark.parametrize("page,content,expected", [
    (
        {
            "name": "foo",
            "url": "some_url",
        },
        "",
        []
    ),
])
def test_parse_logs(page, content, expected):
    """
    Basic 'parse_logs' method does not perform any real parsing (yet have to be
    implemented from final interface) and return an empty list.
    """
    manager = LogManagerMixin()

    assert manager.parse_logs({}, page, content) == expected


@pytest.mark.parametrize("page,content,expected", [
    (
        {
            "name": "foo",
            "url": "some_url",
            "size": (1, 42),
            "driver_log_path": "some_path.driver.log",
            "browser_log_path": "some_path.browser.json",
        },
        "Some content",
        {"logs": [], "name": "foo", "size": (1, 42), "url": "some_url"}
    ),
])
def test_task_logs(temp_builds_dir, insert_basedir, page, content, expected):
    """
    'task_logs' method should return browser log filepath
    """
    basedir = temp_builds_dir.join('logmanager_task_logs')
    os.makedirs(basedir)

    page = insert_basedir(basedir, page, fields=["driver_log_path"])

    with io.open(page["driver_log_path"], "w") as fp:
        fp.write(content)

    manager = LogManagerMixin()

    assert manager.task_logs({}, page, content) == expected
