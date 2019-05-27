# -*- coding: utf-8 -*-
import json
import os

from slugify import slugify

from optimus.pages.views.base import PageViewBase
from optimus.conf.registry import settings


class Index(PageViewBase):
    """
    Default index page
    """
    title = "Index"
    template_name = "index.html"
    destination = "index.html"
    pages = []

    def get_context(self):
        super().get_context()

        pages_map = []
        for page in self.pages:
            pages_map.append({
                "title": page.title,
                "destination": page.destination,
            })

        self.context.update({
            "DEFAULT_LANGUAGE": settings.LANGUAGE_CODE,
            "LANGUAGES": settings.LANGUAGES,
            "pages": pages_map,
        })

        return self.context


class JsonIndex(Index):
    """
    JSON page configuration for py-website-capture
    """
    title = "Index"
    template_name = "index.json" # Unused
    destination = "index.json"

    def render(self, env):
        """
        Build JSON config content
        """
        self.env = env

        sizes = [
            [320, 768],
            [1440, 768],
        ]

        pages_map = []
        for page in self.pages:
            pages_map.append({
                "name": slugify(page.title),
                "url": os.path.join(self.env.globals["SITE"]["web_url"],
                                    page.destination),
                "sizes": sizes,
                "tasks": ["screenshot", "logs"]
            })

        content = {
            "output_dir": "./outputs/page-tests/",
            "size_dir": True,
            "headless": True,
            "pages": pages_map,
        }

        return json.dumps(content, indent=4)

