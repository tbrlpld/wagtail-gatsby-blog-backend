# -*- coding: utf-8 -*-

"""Defines BlogPageTag."""

from django.db import models as djm  # type: ignore
from modelcluster import fields as mcf  # type: ignore
from taggit import models as tgm  # type: ignore


class BlogPageTag(tgm.TaggedItemBase):
    """Create connection between a tag and a BlogPage."""

    content_object = mcf.ParentalKey(
        'blog.BlogPage',
        related_name='tag_connections',
        on_delete=djm.CASCADE,
    )
