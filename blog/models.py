from django.db import models
import graphene
from grapple import helpers as gph
from grapple import models as gpm
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
)
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail_headless_preview.models import HeadlessPreviewMixin


class BlogIndexPage(Page):
    parent_page_types = [
        'home.HomePage',
    ]
    subpage_types = [
        'blog.BlogPage',
    ]

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
    ]


@gph.register_query_field('blogCategory', 'blogCategories', {
    'id': graphene.ID(),
    'url': graphene.String(),
    'slug': graphene.String(),
})
class BlogCategory(Page):
    parent_page_types = [
        'home.HomePage',
    ]
    subpage_types = [
    ]

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
    ]

    graphql_fields = [
        gpm.GraphQLString('title'),
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


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tag_connections',
        on_delete=models.CASCADE,
    )


@gph.register_query_field('blogPage', 'blogPages', {
    'id': graphene.ID(),
    'url': graphene.String(),
    'slug': graphene.String(),
})
class BlogPage(HeadlessPreviewMixin, Page):
    parent_page_types = [
        BlogIndexPage,
    ]
    subpage_types = []

    author = models.CharField(max_length=250, blank=True)
    date = models.DateField('Post date')
    intro = models.CharField(max_length=250)
    body = RichTextField(
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
        ]
    )
    freeformbody = StreamField(
        [
            ('heading', blocks.CharBlock(classname='full title')),
            ('paragraph', blocks.RichTextBlock()),
            ('image', ImageChooserBlock()),
            ('text', blocks.TextBlock()),
            ('email', blocks.EmailBlock(help_text='Your email goes here.')),
            ('integer', blocks.IntegerBlock(help_text='Just a number.')),
            ('float', blocks.FloatBlock(help_text='A floating point number.')),
            ('decimal', blocks.DecimalBlock(
                help_text='A decimal number.',
                decimal_places=2,
            )),
            ('regex', blocks.RegexBlock(
                regex=r'^.*stuff.*$',
                help_text='A string with stuff in the middle.',
                error_messages={
                    'invalid': 'You need to have " stuff " in the string.',
                },
            )),
            ('url', blocks.URLBlock()),
            ('bool', blocks.BooleanBlock(required=False)),
            ('date', blocks.DateBlock()),
            ('time', blocks.TimeBlock()),
            ('datetime', blocks.DateTimeBlock()),
            ('rawhtml', blocks.RawHTMLBlock(
                help_text='Here you can show off your HTML skills.')),
            ('blockquote', blocks.BlockQuoteBlock()),
            ('choice', blocks.ChoiceBlock(
                choices=(
                    ('yes', 'Yes'),
                    ('no', 'No'),
                    ('maybe', 'Maybe'),
                ),
            )),
            # Only in wagtail > 2.8
            # ('multiple_choice', blocks.MultipleChoiceBlock(
            #     choices=(
            #         ('scotch', 'Scotch'),
            #         ('beer', 'Beer'),
            #         ('bourbon', 'Bourbon'),
            #         ('bubbly', 'Bubbly'),
            #     )
            # )),
            ('page', blocks.PageChooserBlock()),
            ('doc', DocumentChooserBlock()),
            # Requires a snippet class to be passed. I currently have no
            # snippet available.
            # ('snippet', SnippetChooserBlock()),
            ('embed', EmbedBlock()),
            ('static', blocks.StaticBlock(
                admin_text='Latest Posts (no configuration needed)',
                help_text='If you include this block, the latest posts will be displayed here.'
            )),
            ('person', blocks.StructBlock([
                ('first_name', blocks.CharBlock()),
                ('last_name', blocks.CharBlock()),
                ('photo', ImageChooserBlock(required=False)),
                ('biography', blocks.TextBlock()),
            ], icon='user')),
            ('list', blocks.ListBlock(
                blocks.CharBlock(label='List Item')
            )),
            ('substream', blocks.StreamBlock([
                ('image', ImageChooserBlock()),
                ('quote', blocks.BlockQuoteBlock()),
                ('author', blocks.CharBlock(min_length=5)),
            ])),
        ],
        blank=True,
    )
    tags = ClusterTaggableManager(
        through=BlogPageTag,
        blank=True,
    )
    category = models.ForeignKey(
        'blog.BlogCategory',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='blogpages',
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('author'),
                FieldPanel('date'),
                FieldPanel('tags'),
                FieldPanel('category'),
            ],
            heading='Blog Post Information',
        ),
        FieldPanel('intro'),
        FieldPanel('body', classname='full'),
        StreamFieldPanel('freeformbody'),
        InlinePanel('gallery_images', label='Gallery Images'),
    ]

    graphql_fields = [
        gpm.GraphQLString('title'),
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
        gpm.GraphQLField(
            'gallery_images',
            'blog.schema.BlogPageGalleryImageType',
            is_list=True,
        ),
    ]


class BlogPageGalleryImage(Orderable):
    # Associate with blog page.
    page = ParentalKey(
        BlogPage,
        on_delete=models.CASCADE,
        related_name='gallery_images',
    )

    # Relation to image storage
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.CASCADE,
        related_name='+',
    )

    caption = models.CharField(
        blank=True,
        max_length=250,
    )

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
