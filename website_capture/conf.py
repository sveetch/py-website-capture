# -*- coding: utf-8 -*-
import json
import logging

from website_capture.exceptions import SettingsInvalidError

ALLOWED_SCREENSHOT_METHODS = ["body", "window"]


def get_project_configuration(fileobject):
    """
    Load and validate given JSON config file.

    Arguments:
        fileobject (object): A file object to read for JSON content, you have
            to close file object once method has finished. Instead of real file
            object it can be a in-memory stream for text I/O but since stream
            has no ``name`` attribute, debug log will print out stream object
            representation.

    Return:
        dict: Configuration items in a dict.
    """
    logger = logging.getLogger("py-website-capture")

    msg = "Opening JSON configuration file: {}"
    filename = getattr(fileobject, "name", fileobject.__repr__())
    logger.debug(msg.format(filename))

    try:
        config = json.load(fileobject)
    except json.decoder.JSONDecodeError as e:
        msg = "Invalid JSON configuration file"
        logger.critical(msg)
        raise e

    if "output_dir" not in config:
        msg = ("Your configuration must contains a directory path where to "
               "create files in a 'output_dir' item.")
        raise SettingsInvalidError(msg)

    if "pages" not in config:
        msg = ("Your configuration must contains a list of pages in a "
               "'pages' item.")
        raise SettingsInvalidError(msg)

    if ("screenshot_method" in config
        and config["screenshot_method"] not in ALLOWED_SCREENSHOT_METHODS):
        msg = ("Unknowed screenshot method '{}', it must be one of allowed "
               "methods: {}".format(
                   config["screenshot_method"],
                   ", ".joint(ALLOWED_SCREENSHOT_METHODS)
                ))
        raise SettingsInvalidError(msg)

    for page in config["pages"]:
        # Page sizes have to be a tuple so it's hashable for ordering
        if "sizes" in page:
            page["sizes"] = [tuple(size) for size in page["sizes"]]

    return config
