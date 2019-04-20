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
