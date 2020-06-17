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

from grapple.models import (
    GraphQLField,
    GraphQLInt,
    GraphQLString,
    GraphQLStreamfield,
    GraphQLCollection,
    GraphQLForeignKey,
)
from grapple.helpers import register_query_field


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


@register_query_field('blogpagetag')
class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )

    graphql_fields = [
        GraphQLInt('id'),
        GraphQLInt('tag_id'),
        GraphQLString('tag'),
        GraphQLForeignKey('content_object', 'blog.BlogPage'),
    ]


from graphene_django.converter import convert_django_field
import graphene


# @convert_django_field.register(ClusterTaggableManager)
# def convert_tag_manager_to_string(field, registry=None):
#     return graphene.String(description=field.help_text, required=not field.null)

@convert_django_field.register(ClusterTaggableManager)
def convert_tag_manager_to_string(field, registry=None):
    return TagType()


class TagType(graphene.ObjectType):
    tag_id = graphene.Int()
    name = graphene.String()

    def resolve_tag_id(self, info):
        return self.id

    def resolve_name(self, info):
        return self.name


class TagQuery(graphene.ObjectType):
    tag = graphene.Field(TagType, tag_id=graphene.Int())

    def resolve_tag(self, info, tag_id):
        return BlogPage.tags.get(pk=tag_id)


def GraphQLTag(field_name: str, **kwargs):
    def Mixin():
        return GraphQLField(field_name, TagType, is_list=True, **kwargs)

    return Mixin


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
        blank=True,
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

    graphql_fields = [
        GraphQLString("title"),
        GraphQLString("date"),
        GraphQLString("author"),
        GraphQLString("intro"),
        GraphQLString("body"),
        GraphQLTag("tags"),
        GraphQLStreamfield("freeformbody"),
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
