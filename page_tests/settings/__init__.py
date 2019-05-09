# -*- coding: utf-8 -*-
"""
Base settings for Page tests
"""
import os
from webassets import Bundle

# Register custom webasset filter for RCssMin minifier
from webassets.filter import register_filter
from .webassets_filters import RCSSMin
register_filter(RCSSMin)

DEBUG = True

PROJECT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
    )
)

# Common site name and domain to use available in templates
SITE_NAME = 'Page tests'
SITE_DOMAIN = 'localhost:8001'

# Sources directory where the assets will be searched
SOURCES_DIR = os.path.join(PROJECT_DIR, 'sources')
# Templates directory
TEMPLATES_DIR = os.path.join(SOURCES_DIR, 'templates')
# Directory where all stuff will be builded
PUBLISH_DIR = os.path.join(PROJECT_DIR, '_build/dev')
# Path where will be moved all the static files, usually this is a directory in
# the ``PUBLISH_DIR``
STATIC_DIR = os.path.join(PROJECT_DIR, PUBLISH_DIR, 'static')
# Path to the i18n messages catalog directory
LOCALES_DIR = os.path.join(PROJECT_DIR, 'locale')

# Locale name for default language to use for Pages
LANGUAGE_CODE = "en_US"

# A list of locale name for all available languages to manage with PO files
LANGUAGES = (LANGUAGE_CODE,)

# The static url to use in templates and with webassets
# This can be a full URL like http://, a relative path or an absolute path
STATIC_URL = 'static/'

# Extra or custom bundles
BUNDLES = {
    'main_css': Bundle(
        'css/main.css',
        filters='rcssmin',
        output='css/main.min.css'
    ),
    'main_js': Bundle(
        "js/foundation/vendor.js",
        "js/foundation/plugins/foundation.core.js",
        "js/foundation/plugins/foundation.util.box.js",
        "js/foundation/plugins/foundation.util.imageLoader.js",
        "js/foundation/plugins/foundation.util.keyboard.js",
        "js/foundation/plugins/foundation.util.mediaQuery.js",
        "js/foundation/plugins/foundation.util.motion.js",
        "js/foundation/plugins/foundation.util.nest.js",
        "js/foundation/plugins/foundation.util.timer.js",
        "js/foundation/plugins/foundation.util.touch.js",
        "js/foundation/plugins/foundation.util.triggers.js",
        "js/foundation/plugins/foundation.abide.js",
        "js/foundation/plugins/foundation.accordion.js",
        "js/foundation/plugins/foundation.accordionMenu.js",
        "js/foundation/plugins/foundation.drilldown.js",
        "js/foundation/plugins/foundation.dropdown.js",
        "js/foundation/plugins/foundation.dropdownMenu.js",
        "js/foundation/plugins/foundation.equalizer.js",
        "js/foundation/plugins/foundation.interchange.js",
        "js/foundation/plugins/foundation.smoothScroll.js",
        "js/foundation/plugins/foundation.magellan.js",
        "js/foundation/plugins/foundation.offcanvas.js",
        "js/foundation/plugins/foundation.orbit.js",
        "js/foundation/plugins/foundation.responsiveMenu.js",
        "js/foundation/plugins/foundation.responsiveToggle.js",
        "js/foundation/plugins/foundation.reveal.js",
        "js/foundation/plugins/foundation.slider.js",
        "js/foundation/plugins/foundation.sticky.js",
        "js/foundation/plugins/foundation.tabs.js",
        "js/foundation/plugins/foundation.toggler.js",
        "js/foundation/plugins/foundation.tooltip.js",
        "js/foundation/plugins/foundation.responsiveAccordionTabs.js",
        "js/main.js",
        filters='rjsmin',
        output='js/main.min.js'
    ),
}

# Sources files or directory to synchronize within the static directory
FILES_TO_SYNC = (
    #'images',
    #'fonts',
    'css',
)
