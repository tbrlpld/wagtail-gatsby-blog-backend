from django.db import models

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


class BlogIndexPage(Page):
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
    def get_context(self, request):
        context = super().get_context(request)

        tag = request.GET.get('tag')
        blogposts = BlogPage.objects.filter(tags__name=tag)

        context['blogposts'] = blogposts
        return context


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )


class BlogPage(Page):
    author = models.CharField(max_length=250, blank=True)
    date = models.DateField('Post date')
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    freeformbody = StreamField(
        [
            ("heading", blocks.CharBlock(classname="full title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
        ],
        blank=True
    )
    tags = ClusterTaggableManager(
        through=BlogPageTag,
        blank=True,
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
            ],
            heading='Blog Post Information',
        ),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        StreamFieldPanel('freeformbody'),
        InlinePanel('gallery_images', label='Gallery Images'),
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
