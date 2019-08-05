# -*- coding: utf-8 -*-
import io
import json

import pytest

from website_capture.exceptions import ProcessorImportError
from website_capture.interfaces.base import (BaseInterface,
                                             ProcessorManagerMixin)


@pytest.mark.parametrize("path", [
    42,
    ["foo"],
])
def test_split_processor_path_invalid_type(path):
    """
    An exception should be raised when path is not a string.
    """
    manager = ProcessorManagerMixin()

    with pytest.raises(ProcessorImportError):
        manager.split_processor_path(path)


@pytest.mark.parametrize("path", [
    "foo",
    "foobar",
])
def test_split_processor_path_invalid_path(path):
    """
    An exception should be raised when Python path is too short (require at
    least a module then object name).
    """
    manager = ProcessorManagerMixin()

    with pytest.raises(ProcessorImportError):
        manager.split_processor_path(path)


@pytest.mark.parametrize("path,expected", [
    (
        "module.object",
        ("module", "object"),
    ),
    (
        "module.submodule.object",
        ("module.submodule", "object"),
    ),
    (
        "foo.bar.ping.Pong",
        ("foo.bar.ping", "Pong"),
    ),
])
def test_split_processor_path_success(path, expected):
    """
    Return splitted path should return separated module and object.
    """
    manager = ProcessorManagerMixin()

    assert expected == manager.split_processor_path(path)


@pytest.mark.parametrize("paths,expected", [
    (
        ["foo.bar.ping"],
        "Unable to import module 'foo.bar'",
    ),
    (
        ["website_capture.processors.ProcessorBase", "foo.bar.ping"],
        "Unable to import module 'foo.bar'",
    ),
    (
        ["json.nope"],
        "Unable to get object 'nope' from module 'json'",
    ),
    (
        ["nope"],
        "Invalid processor path: nope",
    ),
    (
        "nope",
        "Invalid processor path: n",
    ),
])
def test_import_processors_invalid(paths, expected):
    """
    An exception should be raised once an error occurs on importing module or
    reaching object from given paths.
    """
    manager = ProcessorManagerMixin()

    with pytest.raises(ProcessorImportError) as excinfo:
        manager.get_processors_objects(paths)

    assert expected == str(excinfo.value)


@pytest.mark.parametrize("paths", [
    [
        "website_capture.processors.ProcessorBase",
    ],
    [
        "website_capture.processors.base.ProcessorBase",
        "website_capture.processors.DummyProcessor",
    ],
])
def test_import_processors_success(paths):
    """
    Every processor objects should be returned from every given paths.
    """
    manager = ProcessorManagerMixin()

    objects = manager.get_processors_objects(paths)

    assert len(paths) == len(objects)

    for item in objects:
        assert hasattr(item, "run")


@pytest.mark.parametrize("paths,expected", [
    (
        [
            "website_capture.processors.ProcessorBase",
        ],
        [
            ("basic", None),
        ],
    ),
    (
        [
            "website_capture.processors.DummyProcessor",
            "website_capture.processors.ProcessorBase",
        ],
        [
            ("dummy", "Dummy report"),
            ("basic", None),
        ],
    ),
])
def test_task_processing(paths, expected):
    """
    Processors should be runned right and return a report.
    """
    manager = ProcessorManagerMixin()

    driver = object()
    response = object()

    config = {
        "processors": paths,
    }

    report = manager.task_processing(driver, config, response)

    assert expected == report
