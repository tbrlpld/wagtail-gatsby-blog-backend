# -*- coding: utf-8 -*-

"""Defines BlogPage model."""

from django.db import models as djm  # type: ignore
import graphene  # type: ignore
from grapple import helpers as gph  # type: ignore
from grapple import models as gpm
from modelcluster.contrib import taggit as mcctg  # type: ignore
from wagtail.admin import edit_handlers as wtaeh  # type: ignore
from wagtail.core import blocks as wtcb  # type: ignore
from wagtail.core import fields as wtcf
from wagtail.core import models as wtcm
from wagtail.documents import blocks as wtdb  # type: ignore
from wagtail.embeds import blocks as wteb  # type: ignore
from wagtail.images import blocks as wtib  # type: ignore
from wagtail.search import index as wtsi  # type: ignore
from wagtail_headless_preview import models as wthpm  # type: ignore

from headless.models import HeadlessServeMixin


@gph.register_query_field('blogPage', 'blogPages', {
    'id': graphene.ID(),
    'url': graphene.String(),
    'slug': graphene.String(),
})
class BlogPage(HeadlessServeMixin, wthpm.HeadlessPreviewMixin, wtcm.Page):
    """
    Page definition for article content.

    This is only an example page and utilizes almost all available types of
    fields. This is for testing purposes and now how you should really define
    a page.

    """

    parent_page_types = [
        'blog.BlogIndexPage',
    ]
    subpage_types = []  # type: ignore

    author = djm.CharField(max_length=250, blank=True)  # noqa: WPS432
    date = djm.DateField('Post date')
    intro = djm.CharField(max_length=250)  # noqa: WPS432
    body = wtcf.RichTextField(
        blank=True,
        features=[
            'bold',
            'italic',
            'superscript',
            'subscript',
            'strikethrough',
            'ol',
            'ul',
            'link',
            'document-link',
            'h2',
            'h3',
            'h4',
            'h5',
            'h6',
            'blockquote',
            'code',
            'hr',
            # 'image',
            # 'embed',
        ],
    )
    freeformbody = wtcf.StreamField(
        [
            ('heading', wtcb.CharBlock(classname='full title')),
            ('paragraph', wtcb.RichTextBlock()),
            ('image', wtib.ImageChooserBlock()),
            ('text', wtcb.TextBlock()),
            ('email', wtcb.EmailBlock(help_text='Your email goes here.')),
            ('integer', wtcb.IntegerBlock(help_text='Just a number.')),
            ('float', wtcb.FloatBlock(help_text='A floating point number.')),
            ('decimal', wtcb.DecimalBlock(
                help_text='A decimal number.',
                decimal_places=2,
            )),
            ('regex', wtcb.RegexBlock(
                regex=r'^.*stuff.*$',
                help_text='A string with stuff in the middle.',
                error_messages={
                    'invalid': 'You need to have " stuff " in the string.',
                },
            )),
            ('url', wtcb.URLBlock()),
            ('bool', wtcb.BooleanBlock(required=False)),
            ('date', wtcb.DateBlock()),
            ('time', wtcb.TimeBlock()),
            ('datetime', wtcb.DateTimeBlock()),
            ('rawhtml', wtcb.RawHTMLBlock(
                help_text='Here you can show off your HTML skills.',
            )),
            ('blockquote', wtcb.BlockQuoteBlock()),
            ('choice', wtcb.ChoiceBlock(choices=(
                ('yes', 'Yes'),  # noqa: WPS317
                ('no', 'No'),
                ('maybe', 'Maybe'),
            ))),
            # Only in wagtail > 2.8
            # ('multiple_choice', wtcb.MultipleChoiceBlock(
            #     choices=(
            #         ('scotch', 'Scotch'),
            #         ('beer', 'Beer'),
            #         ('bourbon', 'Bourbon'),
            #         ('bubbly', 'Bubbly'),
            #     )
            # )),
            ('page', wtcb.PageChooserBlock()),
            ('doc', wtdb.DocumentChooserBlock()),
            # Requires a snippet class to be passed. I currently have no
            # snippet available.
            # ('snippet', SnippetChooserBlock()),
            ('embed', wteb.EmbedBlock()),
            ('static', wtcb.StaticBlock(
                admin_text='Latest Posts (no configuration needed)',
                help_text=(
                    'If you include this block,'
                    + ' the latest posts will be displayed here.'
                ),
            )),
            ('person', wtcb.StructBlock(
                [
                    ('first_name', wtcb.CharBlock()),
                    ('last_name', wtcb.CharBlock()),
                    ('biography', wtcb.TextBlock()),
                ],
                icon='user',
            )),
            ('list', wtcb.ListBlock(
                wtcb.CharBlock(label='List Item'),
            )),
            # There are open issues with the stream block:
            # https://github.com/GrappleGQL/wagtail-grapple/pull/54
            # These issues make it basically impossible to query meaningful
            # data. Until that is resolved, I should possibly stay clear of of
            # using the SteamBlock.
            ('substream', wtcb.StreamBlock(
                [
                    ('quote', wtcb.BlockQuoteBlock()),
                    ('author', wtcb.CharBlock(min_length=5)),
                ],
            )),
        ],
        blank=True,
    )
    tags = mcctg.ClusterTaggableManager(
        through='blog.BlogPageTag',
        blank=True,
    )
    category = djm.ForeignKey(
        'blog.BlogCategory',
        null=True,
        blank=True,
        on_delete=djm.SET_NULL,
        related_name='blogpages',
    )

    search_fields = wtcm.Page.search_fields + [
        wtsi.SearchField('intro'),
        wtsi.SearchField('body'),
    ]

    content_panels = wtcm.Page.content_panels + [
        wtaeh.MultiFieldPanel(
            [
                wtaeh.FieldPanel('author'),
                wtaeh.FieldPanel('date'),
                wtaeh.FieldPanel('tags'),
                wtaeh.FieldPanel('category'),
            ],
            heading='Blog Post Information',
        ),
        wtaeh.FieldPanel('intro'),
        wtaeh.FieldPanel('body', classname='full'),
        wtaeh.StreamFieldPanel('freeformbody'),
        wtaeh.InlinePanel('gallery_images', label='Gallery Images'),
    ]

    graphql_fields = [
        gpm.GraphQLString('title', required=True),
        gpm.GraphQLString('date'),
        gpm.GraphQLString('author'),
        gpm.GraphQLString('intro'),
        gpm.GraphQLString('body'),
        gpm.GraphQLStreamfield('freeformbody'),
        gpm.GraphQLField(
            'tags',
            'tagging.schema.TagType',
            is_list=True,
        ),
        # The next field is needed so that the connection from
        # BlogPageTag to the BlogPage can be found.
        gpm.GraphQLField(
            'tag_connections',
            'blog.schema.BlogPageTagConnection',
            is_list=True,
        ),
        gpm.GraphQLForeignKey(
            'category',
            'blog.BlogCategory',
        ),
        gpm.GraphQLCollection(
            gpm.GraphQLForeignKey,
            'gallery_images',
            'blog.BlogPageGalleryImage',
            required=False,
        ),
    ]
