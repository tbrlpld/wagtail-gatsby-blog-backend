import graphene
import graphene_django

from blog.models import BlogPageTag


class BlogPageTagConnection(graphene_django.DjangoObjectType):
    class Meta:
        model = BlogPageTag

    tag = graphene.Field('tagging.schema.TagType', required=True)


class Query(graphene.ObjectType):
    # blog_page_tag_connection = graphene.Field(
    #     BlogPageTagConnection,
    #     blog_page_tag_id=graphene.ID(required=True),
    # )
    blog_page_tag_connections = graphene.List(
        BlogPageTagConnection,
        tag=graphene.String(),
    )

    # def resolve_blog_page_tag(self, info, blog_page_tag_id=None):
    #     return BlogPageTag.objects.get(pk=blog_page_tag_id)

    def resolve_blog_page_tag_connections(self, info, tag=None):
        if tag is not None:
            return BlogPageTag.objects.filter(tag__name=tag)
        return BlogPageTag.objects.all()


