# -*- coding: utf-8 -*-

"""Defines BlogCategory page model."""

import graphene  # type: ignore
from grapple import helpers as gph  # type: ignore
from grapple import models as gpm  # type: ignore
from wagtail.admin import edit_handlers as wtaeh  # type: ignore
from wagtail.core import fields as wtcf  # type: ignore
from wagtail.core import models as wtcm  # type: ignore


@gph.register_query_field('blogCategory', 'blogCategories', {
    'id': graphene.ID(),
    'url': graphene.String(),
    'slug': graphene.String(),
})
class BlogCategory(wtcm.Page):
    """
    Simple BlogCategory page model.

    The BlogCategory is defined as a Page model, so that functionality like
    slug and 'show_in_menu' can easily be used.

    """

    parent_page_types = [
        'home.HomePage',
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

    def get_url_parts(self, request=None):
        site_id, site_root, page_url_raltive_to_site_root = super(
        ).get_url_parts(request)
        # URL typically has leading and trailing slashes. When splitting, an
        # element with empty string remains in the list in the beginning and
        # end. This is useful for joining again (after the alteration).
        urllist = page_url_raltive_to_site_root.split('/')
        # Inserting 'category' after the empty string, before the first
        # real element.
        urllist.insert(1, 'categories')
        page_url_raltive_to_site_root = '/'.join(urllist)
        return (site_id, site_root, page_url_raltive_to_site_root)
