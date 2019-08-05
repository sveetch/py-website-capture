# -*- coding: utf-8 -*-
"""
Exceptions
==========

Specific exceptions that py-website-capture code can raise.
"""


class WebsiteCaptureBaseException(Exception):
    """
    Base for py-website-capture exceptions.
    """
    pass


class SettingsInvalidError(WebsiteCaptureBaseException):
    """
    Exception to be raised when a settings is detected as invalid.
    """
    pass


class PageConfigError(SettingsInvalidError):
    """
    Exception to be raised when a page configuration is invalid.
    """
    pass


class InvalidPageSizeError(SettingsInvalidError):
    """
    Exception to be raised when an encountered size is invalid.
    """
    pass


class ProcessorImportError(SettingsInvalidError):
    """
    Exception to be raised when a processor import fails.
    """
    pass
