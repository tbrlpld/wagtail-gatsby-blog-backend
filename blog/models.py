from django.db import models as djm

# Create your models here.
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index
from wagtail.snippets import models as wtsnip

from grapple import models as gpm


@wtsnip.register_snippet
class BlogCategory(djm.Model):
    name = djm.CharField(max_length=255)
    icon = djm.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=djm.SET_NULL,
        related_name='+',
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'blog categories'


class BlogIndexPage(Page):
    parent_page_types = [
        "home.HomePage",
    ]
    subpage_types = [
        "blog.BlogPage",
    ]

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        blogposts = self.get_children().live().order_by('-first_published_at')

        context['blogposts'] = blogposts
        return context


class BlogTagIndexPage(Page):
    parent_page_types = [
        "home.HomePage",
    ]
    subpage_types = [
        "blog.BlogPage",
    ]

    def get_context(self, request):
        context = super().get_context(request)

        tag = request.GET.get('tag')
        blogposts = BlogPage.objects.filter(tags__name=tag)

        context['blogposts'] = blogposts
        return context


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tag_connections',
        on_delete=djm.CASCADE,
    )


class BlogPage(Page):
    parent_page_types = [
        BlogIndexPage,
    ]
    subpage_types = []

    author = djm.CharField(max_length=250, blank=True)
    date = djm.DateField('Post date')
    intro = djm.CharField(max_length=250)
    body = RichTextField(blank=True)
    freeformbody = StreamField(
        [
            ("heading", blocks.CharBlock(classname="full title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
        ],
        blank=True,
    )
    tags = ClusterTaggableManager(
        through=BlogPageTag,
        blank=True,
    )
    category = djm.ForeignKey(
        'blog.BlogCategory',
        null=True,
        blank=True,
        on_delete=djm.SET_NULL,
        related_name='+',
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
        FieldPanel('body', classname="full"),
        StreamFieldPanel('freeformbody'),
        InlinePanel('gallery_images', label='Gallery Images'),
    ]

    graphql_fields = [
        gpm.GraphQLString("title"),
        gpm.GraphQLString("date"),
        gpm.GraphQLString("author"),
        gpm.GraphQLString("intro"),
        gpm.GraphQLString("body"),
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
        gpm.GraphQLStreamfield("freeformbody"),
    ]


class BlogPageGalleryImage(Orderable):
    # Associate with blog page.
    page = ParentalKey(
        BlogPage,
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
        max_length=250,
    )

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
