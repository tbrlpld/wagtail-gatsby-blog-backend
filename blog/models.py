from django.db import models

# Create your models here.
from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
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


class BlogPage(Page):
    date = models.DateField('Post date')
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
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
