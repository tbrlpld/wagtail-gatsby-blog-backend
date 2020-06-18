# -*- coding: utf-8 -*-

"""
Custom GraphQL schema types that are not supported natively by Grapple.

"""

import graphene
from graphene.types.structures import Structure
import graphene_django
from graphene_django.converter import convert_django_field
import grapple.models as gpm
import modelcluster.contrib.taggit as mct
import taggit.models as tgt



class TagType(graphene_django.DjangoObjectType):
    class Meta:
        model = tgt.Tag

    # Importing the grapple types does not work, because they depend on the
    # apps being registered.
    # from grapple.types.images import ImageObjectType
    # -> django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.

    # graphene.Union fails. It can not work with the string identified types.

    tagged_images = graphene.List("grapple.types.images.ImageObjectType")
    # tagged_items = graphene.List("grapple.types.images.ImageObjectType")
    # tagged_items = graphene.Field(TaggedItemType)

    def resolve_tagged_images(self, _):
        from wagtail.images.models import Image

        tagged_items = self.taggit_taggeditem_items.all()
        image_pks = []
        for ti in tagged_items:
            ti_class = ti.content_type.model_class()
            if ti_class == Image:
                image_pks.append(ti.pk)

        # TODO: filter image query set for the found image_pks.
        return Image.objects.filter(pk__in=image_pks)
        # return self.taggit_taggeditem_items.first().content_type.model_class().objects.all()


class TagQuery(graphene.ObjectType):
    """Queries for the TagType."""

    tag = graphene.Field(TagType, id=graphene.ID())
    tags = graphene.List(TagType)

    def resolve_tag(self, _, id):  # noqa: D102
        return tgt.Tag.objects.get(pk=id)

    def resolve_tags(self, _):  # noqa: D102
        return tgt.Tag.objects.all().order_by('pk')


@convert_django_field.register(mct.ClusterTaggableManager)
def convert_tag_manager_to_string(field, registry=None):
    """Define converter type for ClusterTaggableManager."""
    return TagType()


def GraphQLTags(field_name: str, **kwargs):  # noqa: N802
    """Custom grapple wrapper function for the TagType."""
    def Mixin():
        return gpm.GraphQLField(field_name, TagType, is_list=True, **kwargs)

    return Mixin
