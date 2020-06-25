import graphene
import graphene_django

from blog.models import BlogPageTag, BlogPageGalleryImage


class BlogPageTagConnection(graphene_django.DjangoObjectType):
    class Meta:
        model = BlogPageTag

    tag = graphene.Field('tagging.schema.TagType', required=True)


class BlogPageGalleryImageType(graphene_django.DjangoObjectType):
    class Meta:
        model = BlogPageGalleryImage
