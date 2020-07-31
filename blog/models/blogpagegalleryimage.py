# -*- coding: utf-8 -*-

"""Defines BlogPageGalleryImage."""

from django.db import models as djm  # type: ignore
from grapple import models as gpm  # type: ignore
from modelcluster import fields as mcf  # type: ignore
from wagtail.admin import edit_handlers as wtaeh  # type: ignore
from wagtail.core import fields as wtcf  # type: ignore
from wagtail.core import models as wtcm  # type: ignore
from wagtail.images import edit_handlers as wtieh  # type: ignore


class BlogPageGalleryImage(wtcm.Orderable):
    """Create relationship between a BlogPage and multiple images."""

    # Associate with blog page.
    page = mcf.ParentalKey(
        'blog.BlogPage',
        on_delete=djm.CASCADE,
        related_name='gallery_images',
    )

    # Relation to image storage
    image = djm.ForeignKey(
        'wagtailimages.Image',
        on_delete=djm.CASCADE,
        related_name='+',
    )

    caption = djm.CharField(
        blank=True,
        max_length=250,  # noqa: WPS432
    )

    panels = [
        wtieh.ImageChooserPanel('image'),
        wtaeh.FieldPanel('caption'),
    ]

    graphql_fields = [
        gpm.GraphQLImage(
            'image',
            required=True,
        ),
    ]
