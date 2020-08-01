from django.db import models
from grapple import models as gpm
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail_headless_preview import models as wthpm

from headless.models import HeadlessServeMixin


class HomePage(
    HeadlessServeMixin,
    wthpm.HeadlessPreviewMixin,
    Page,
):
    parent_page_types = [
        'wagtailcore.Page',
    ]

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full'),
    ]

    graphql_fields = [
        gpm.GraphQLString('title', required=True),
        gpm.GraphQLString('body'),
    ]
