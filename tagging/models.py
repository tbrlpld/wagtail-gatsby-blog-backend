from modelcluster.contrib.taggit import ClusterTaggableManager

from graphene_django.converter import convert_django_field


@convert_django_field.register(ClusterTaggableManager)
def convert_tag_manager_to_string(field, registry=None):
    """Define converter type for ClusterTaggableManager."""
    return 'tagging.schema.TagType'
