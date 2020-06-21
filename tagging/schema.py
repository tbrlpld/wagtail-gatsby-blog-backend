# -*- coding: utf-8 -*-

"""
Custom GraphQL schema types that are not supported natively by Grapple.

Importing the grapple types does not work, because they depend on the
apps being registered.

```python
from grapple.types.images import ImageObjectType  # noqa: E800
# -> django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
```

graphene.Union fails. It can not work with the string identified types
the way that graphene.List does.
Therefore, I can not return all tagged items in one type. The different
returned elements need to have their own tag type each.

"""
from wagtail.documents.models import get_document_model   # type: ignore
from wagtail.images import get_image_model   # type: ignore

from taggit import models as tgm   # type: ignore

import graphene  # type: ignore
import graphene_django  # type: ignore


class TagType(graphene_django.DjangoObjectType):
    class Meta:
        model = tgm.Tag
        description="Type for a general taggit.Tag"


class ImageTagType(graphene_django.DjangoObjectType):
    class Meta:
        model = tgm.Tag
        exclude = ('blog_blogpagetag_items',)
        description="Tag used on images."

    tagged_images = graphene.List("grapple.types.images.ImageObjectType")

    def resolve_tagged_images(self, _):
        image_model = get_image_model()

        return image_model.objects.filter(tags__id=self.id)


class DocumentTagType(graphene_django.DjangoObjectType):
    class Meta:
        model = tgm.Tag
        exclude = ('blog_blogpagetag_items',)
        description="Tag used on documents."

    tagged_documents = graphene.List("grapple.types.documents.DocumentObjectType")

    def resolve_tagged_documents(self, _):
        document_model = get_document_model()

        return document_model.objects.filter(tags__id=self.id)

class Query(graphene.ObjectType):
    """Queries for the TagType."""

    tag = graphene.Field(
        TagType,
        id_=graphene.ID(name='id'),
        name=graphene.String(),
    )
    tags = graphene.List(TagType)

    def resolve_tag(self, _, id_=None, name=None):
        if id_ is not None:
            return tgm.Tag.objects.get(pk=id_)
        if name is not None:
            return tgm.Tag.objects.get(name=name)
        return None

    def resolve_tags(self, _):  # noqa: D102
        return tgm.Tag.objects.all().order_by('pk')

    image_tag = graphene.Field(
        ImageTagType,
        id_=graphene.ID(name='id'),
        name=graphene.String(),
    )
    image_tags = graphene.List(ImageTagType)

    tags_of_image = graphene.List(
        ImageTagType,
        image_id=graphene.ID(required=True),
    )

    @staticmethod
    def get_image_tags():
        return tgm.Tag.objects.filter(
            taggit_taggeditem_items__content_type__model='image',
        )

    def resolve_image_tag(self, _, id_=None, name=None):
        image_tags = Query.get_image_tags()
        if id_ is not None:
            return image_tags.get(pk=id_)
        if name is not None:
            return image_tags.get(name=name)
        return None

    def resolve_image_tags(self, _):
        return Query.get_image_tags()

    def resolve_tags_of_image(self, _, image_id):
        Image = get_image_model()
        image = Image.objects.get(pk=image_id)
        return image.tags.all()

    document_tag = graphene.Field(DocumentTagType, id=graphene.ID())
    document_tags = graphene.List(DocumentTagType)

    @staticmethod
    def get_document_tags():
        return tgm.Tag.objects.filter(
            taggit_taggeditem_items__content_type__model='document',
        )

    def resolve_document_tag(self, _, id):
        return Query.get_document_tags().get(pk=id)

    def resolve_document_tags(self, _):
        return Query.get_document_tags()
