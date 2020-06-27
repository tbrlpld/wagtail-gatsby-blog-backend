from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

from grapple import models as gpm


class HomePage(Page):
    parent_page_types = [
        'wagtailcore.Page',
    ]

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full'),
    ]

    graphql_fields = [
        gpm.GraphQLString('title'),
        gpm.GraphQLString('body'),
    ]
