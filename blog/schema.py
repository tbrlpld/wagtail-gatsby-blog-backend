# -*- coding: utf-8 -*-

"""
Custom GraphQL schema types that are not supported natively by Grapple.

"""

import graphene
from graphene_django.converter import convert_django_field
import grapple.models as gpl
import modelcluster.contrib.taggit as mct
import taggit.models as tgt


@convert_django_field.register(mct.ClusterTaggableManager)
def convert_tag_manager_to_string(field, registry=None):
    """Define converter type for ClusterTaggableManager."""
    return TagType()


class TagType(graphene.ObjectType):
    """Tag GraphQL Type."""

    tag_id = graphene.Int(name='id')
    name = graphene.String()
    slug = graphene.String()

    def resolve_tag_id(self, _):  # noqa: D102
        return self.id

    def resolve_name(self, _):  # noqa: D102
        return self.name

    def resolve_slug(self, _):  # noqa: D102
        return self.slug



class TagQuery(graphene.ObjectType):
    """Queries for the TagType."""

    tag = graphene.Field(TagType, id=graphene.Int())
    tags = graphene.List(TagType)

    def resolve_tag(self, _, id):  # noqa: D102
        return tgt.Tag.objects.get(pk=id)

    def resolve_tags(self, _):  # noqa: D102
        return tgt.Tag.objects.all().order_by('pk')


def GraphQLTags(field_name: str, **kwargs):  # noqa: N802
    """Custom grapple wrapper function for the TagType."""
    def Mixin():
        return gpl.GraphQLField(field_name, TagType, is_list=True, **kwargs)

    return Mixin
