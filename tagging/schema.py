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
from django.db import models as djm  # type: ignore

from wagtail.documents.models import get_document_model   # type: ignore
from wagtail.images import get_image_model   # type: ignore

from taggit import models as tgm   # type: ignore

import graphene  # type: ignore
import graphene_django  # type: ignore


class TagType(graphene_django.DjangoObjectType):
    class Meta:
        model = tgm.Tag


class ImageTagType(graphene_django.DjangoObjectType):
    class Meta:
        model = tgm.Tag
        exclude = ('blog_blogpagetag_items',)

    tagged_images = graphene.List("grapple.types.images.ImageObjectType")

    def resolve_tagged_images(self, _):
        image_model = get_image_model()

        return image_model.objects.filter(tags__id=self.id)


class DocumentTagType(graphene_django.DjangoObjectType):
    class Meta:
        model = tgm.Tag
        exclude = ('blog_blogpagetag_items',)

    tagged_documents = graphene.List("grapple.types.documents.DocumentObjectType")

    def resolve_tagged_documents(self, _):
        document_model = get_document_model()

        return document_model.objects.filter(tags__id=self.id)

class Query(graphene.ObjectType):
    """Queries for the TagType."""

    tag = graphene.Field(TagType, id=graphene.ID())
    tags = graphene.List(TagType)

    image_tag = graphene.Field(ImageTagType, id=graphene.ID())
    image_tags = graphene.List(ImageTagType)

    document_tag = graphene.Field(DocumentTagType, id=graphene.ID())
    document_tags = graphene.List(DocumentTagType)

    def resolve_tag(self, _, id):
        return tgm.Tag.objects.get(pk=id)

    def resolve_tags(self, _):  # noqa: D102
        return tgm.Tag.objects.all().order_by('pk')

    def resolve_image_tag(self, _, id):
        return tgm.Tag.objects.filter(
            taggit_taggeditem_items__content_type__model='image',
        ).get(
            pk=id,
        )

    def resolve_image_tags(self, _):
        return tgm.Tag.objects.filter(
            taggit_taggeditem_items__content_type__model='image',
        )

    def resolve_document_tag(self, _, id):
        return tgm.Tag.objects.filter(
            taggit_taggeditem_items__content_type__model='document',
        ).get(
            pk=id,
        )

    def resolve_document_tags(self, _):
        return tgm.Tag.objects.filter(
            taggit_taggeditem_items__content_type__model='document',
        )
