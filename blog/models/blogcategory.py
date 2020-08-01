# -*- coding: utf-8 -*-

"""Defines BlogCategory page model."""

import graphene  # type: ignore
from grapple import helpers as gph  # type: ignore
from grapple import models as gpm  # type: ignore
from wagtail.admin import edit_handlers as wtaeh  # type: ignore
from wagtail.core import fields as wtcf  # type: ignore
from wagtail.core import models as wtcm  # type: ignore
from wagtail_headless_preview import models as wthpm

from headless.models import HeadlessServeMixin


class BlogCategoriesIndex(
    HeadlessServeMixin,
    wthpm.HeadlessPreviewMixin,
    wtcm.Page,
):
    """
    Simple index page to hold the different BlogCategories.

    This index only serves as a container and to fully create pages for
    a complete URL structure.

    """

    parent_page_types = [
        'home.HomePage',
    ]
    subpage_types = [
        'blog.BlogCategory',
    ]
    max_count = 1

    content_panels = [
        wtaeh.HelpPanel(
            'This is only a container page and no content needs to be'
            + ' defined. This page only serves as an organizational element.'
            + ' Create the actual categories as child pages of this page.',
        ),
    ]
    promote_panels = []
    settings_panels = []

    def save(self, clean=True, **kwargs):
        """Set forced values and save page."""
        self.title = 'Categories'
        super().save(**kwargs)


@gph.register_query_field('blogCategory', 'blogCategories', {
    'id': graphene.ID(),
    'url': graphene.String(),
    'slug': graphene.String(),
})
class BlogCategory(
    HeadlessServeMixin,
    wthpm.HeadlessPreviewMixin,
    wtcm.Page,
):
    """
    Simple BlogCategory page model.

    The BlogCategory is defined as a Page model, so that functionality like
    slug and 'show_in_menu' can easily be used.

    """

    parent_page_types = [
        'blog.BlogCategoriesIndex',
    ]
    subpage_types = [
    ]

    intro = wtcf.RichTextField(blank=True)

    content_panels = wtcm.Page.content_panels + [
        wtaeh.FieldPanel('intro', classname='full'),
    ]

    graphql_fields = [
        gpm.GraphQLString('title', required=True),
        gpm.GraphQLString('intro'),
        gpm.GraphQLCollection(
            gpm.GraphQLForeignKey,
            'blogpages',
            'blog.BlogPage',
        ),
    ]
