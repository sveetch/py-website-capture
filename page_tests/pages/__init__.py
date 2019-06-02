# -*- coding: utf-8 -*-
"""
The project pages map for Page tests
"""
from optimus.pages.views.base import PageViewBase
from optimus.conf.registry import settings

from .index import Index, JsonIndex, JsonDemoMarker
from .page import BasicPage


# Available pages
SAMPLE_PAGES = [
    BasicPage(
        title="Basic console log info",
        template_name="console-log.basic.html",
        destination="console-log.basic.html",
    ),
    BasicPage(
        title="Basic Javascript error",
        template_name="javascript-error.basic.html",
        destination="javascript-error.basic.html",
    ),
    BasicPage(
        title="Every error cases",
        template_name="every-logs.basic.html",
        destination="every-logs.basic.html",
    ),
    BasicPage(
        title="Basic lorem ipsum",
        template_name="lorem-ipsum.basic.html",
        destination="lorem-ipsum.basic.html",
    ),
]

# Enabled pages to build
PAGES = SAMPLE_PAGES + [
    Index(pages=SAMPLE_PAGES),
    JsonIndex(pages=SAMPLE_PAGES),
    JsonDemoMarker(),
]
