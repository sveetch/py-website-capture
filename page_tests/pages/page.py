# -*- coding: utf-8 -*-
from optimus.pages.views.base import PageViewBase
from optimus.conf.registry import settings


class BasicPage(PageViewBase):
    """
    Basic page
    """
    title = "Basic page"
    template_name = "page.html"
    destination = "page.html"

    def get_context(self):
        super().get_context()

        self.context.update({
            'DEFAULT_LANGUAGE': settings.LANGUAGE_CODE,
            'LANGUAGES': settings.LANGUAGES,
        })

        return self.context
