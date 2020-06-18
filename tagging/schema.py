# -*- coding: utf-8 -*-

"""
Custom GraphQL schema types that are not supported natively by Grapple.

"""

import django.db.models as djm
import graphene
import graphene_django
from graphene_django.converter import convert_django_field
import grapple.models as gpm
import modelcluster.contrib.taggit as mct
import taggit.models as tgt

from wagtail.documents.models import get_document_model
from wagtail.images import get_image_model


# Importing the grapple types does not work, because they depend on the
# apps being registered.
# from grapple.types.images import ImageObjectType  # noqa: E800
# -> django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.

# graphene.Union fails. It can not work with the string identified types.


def convert_tagged_items_to_model_queryset(
    tag: tgt.Tag,
    target_model: djm.Model,
):
    """
    Convert the items tagged by a Tag into a query set of a given class.

    This conversion is only performed if the tagged items is actually of
    the given type.

    Parameters
    ----------
    tag_item: tgt.Tag
        Tag for which the tagged items of a given class shall be extracted.
    target_model: djm.Model
        Django model that the items should be checked against.

    Returns
    -------
    djm.query.QuerySet
        QuerySet of the the `target_class` containing only the item tagged
        with the given `tag`.

    """

    tagged_items = tag.taggit_taggeditem_items.all()
    tagged_item_pks = []
    for ti in tagged_items:
        # Check if the tagged items class matches the target class
        ti_class = ti.content_type.model_class()
        if ti_class == target_model:
            # Store object id of the item if its class matches the
            # target class
            tagged_item_pks.append(ti.object_id)

    return target_model.objects.filter(pk__in=tagged_item_pks)


class TagType(graphene_django.DjangoObjectType):
    class Meta:
        model = tgt.Tag


class ImageTagType(graphene_django.DjangoObjectType):
    class Meta:
        model = tgt.Tag

    tagged_images = graphene.List("grapple.types.images.ImageObjectType")

    def resolve_tagged_images(self, _):
        image_model = get_image_model()

        return convert_tagged_items_to_model_queryset(self, image_model)


class DocumentTagType(graphene_django.DjangoObjectType):
    class Meta:
        model = tgt.Tag

    tagged_documents = graphene.List("grapple.types.documents.DocumentObjectType")

    def resolve_tagged_documents(self, _):
        document_model = get_document_model()

        return convert_tagged_items_to_model_queryset(self, document_model)


class TaggingQueries(graphene.ObjectType):
    """Queries for the TagType."""

    tag = graphene.Field(TagType, id=graphene.ID())
    tags = graphene.List(TagType)

    image_tag = graphene.Field(ImageTagType, id=graphene.ID())
    image_tags = graphene.List(ImageTagType)

    document_tag = graphene.Field(DocumentTagType, id=graphene.ID())
    document_tags = graphene.List(DocumentTagType)

    def resolve_tag(self, _, id):  # noqa: D102
        return tgt.Tag.objects.get(pk=id)

    def resolve_tags(self, _):  # noqa: D102
        return tgt.Tag.objects.all().order_by('pk')

    def resolve_image_tag(self, _, id):
        return tgt.Tag.objects.filter(
            taggit_taggeditem_items__content_type__model='image',
        ).get(
            pk=id,
        )

    def resolve_image_tags(self, _):
        return tgt.Tag.objects.filter(
            taggit_taggeditem_items__content_type__model='image',
        )

    def resolve_document_tag(self, _, id):
        return tgt.Tag.objects.filter(
            taggit_taggeditem_items__content_type__model='document',
        ).get(
            pk=id,
        )

    def resolve_document_tags(self, _):
        return tgt.Tag.objects.filter(
            taggit_taggeditem_items__content_type__model='document',
        )


@convert_django_field.register(mct.ClusterTaggableManager)
def convert_tag_manager_to_string(field, registry=None):
    """Define converter type for ClusterTaggableManager."""
    return TagType()


def GraphQLTag(field_name: str, **kwargs):  # noqa: N802
    """Custom grapple wrapper function for the TagType."""
    def Mixin():
        return gpm.GraphQLField(field_name, TagType, is_list=False, **kwargs)

    return Mixin


def GraphQLTags(field_name: str, **kwargs):  # noqa: N802
    """Custom grapple wrapper function for the TagType."""
    def Mixin():
        return gpm.GraphQLField(field_name, TagType, is_list=True, **kwargs)

    return Mixin
