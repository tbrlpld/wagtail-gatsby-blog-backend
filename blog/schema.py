import graphene
import graphene_django

from tagging.schema import TagType

from blog.models import BlogPageTag


class BlogPageTagType(graphene_django.DjangoObjectType):
    class Meta:
        model = BlogPageTag

    tag = graphene.Field(TagType, required=True)


class Query(graphene.ObjectType):
    blog_page_tag = graphene.Field(
        BlogPageTagType,
        blog_page_tag_id=graphene.ID(required=True),
    )
    blog_page_tags = graphene.List(
        BlogPageTagType,
        tag=graphene.String(),
    )

    def resolve_blog_page_tag(self, info, blog_page_tag_id=None):
        return BlogPageTag.objects.get(pk=blog_page_tag_id)

    def resolve_blog_page_tags(self, info, tag=None):
        if tag is not None:
            return BlogPageTag.objects.filter(tag__name=tag)
        return BlogPageTag.objects.all()


