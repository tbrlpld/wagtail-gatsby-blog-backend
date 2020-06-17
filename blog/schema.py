# -*- coding: utf-8 -*-

"""
Custom GraphQL schema types that are not supported natively by Grapple.

"""

import graphene
import graphene_django
from graphene_django.converter import convert_django_field
import grapple.models as gpm
import modelcluster.contrib.taggit as mct
import taggit.models as tgt



class TagType(graphene_django.DjangoObjectType):
    class Meta:
        model = tgt.Tag

    tagged_items = graphene.List("grapple.types.images.ImageObjectType")
    # tagged_items = graphene.Field(TaggedItemType)

    def resolve_tagged_items(self, _):
        tagged_items = self.taggit_taggeditem_items.all()
        native_items = []
        for tagged_item in tagged_items:
            item_class = tagged_item.content_type.model_class()
            native_item = item_class.objects.get(pk=tagged_item.pk)
            native_items.append(native_item)
        return native_items
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
