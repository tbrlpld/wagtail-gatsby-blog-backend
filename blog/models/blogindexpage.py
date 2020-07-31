# -*- coding: utf-8 -*-

"""
Defines BlogIndexPage.

The BlogIndexPage is the parent page for the BlogPage model and its purpose is
to list links to all the available BlogPages.

"""

from wagtail.admin import edit_handlers as wtaeh  # type: ignore
from wagtail.core import fields as wtcf  # type: ignore
from wagtail.core import models as wtcm  # type: ignore

from headless.models import HeadlessServeMixin


class BlogIndexPage(HeadlessServeMixin, wtcm.Page):
    """
    Parent to the BlogPage model.

    Should list all links to all BlogPages.

    """

    parent_page_types = [
        'home.HomePage',
    ]
    subpage_types = [
        'blog.BlogPage',
    ]

    intro = wtcf.RichTextField(blank=True)

    content_panels = wtcm.Page.content_panels + [
        wtaeh.FieldPanel('intro', classname='full'),
    ]
