import graphene

from grapple import schema as gs

from blog.models import TagQuery

GrappleQuery = gs.schema._query
GrappleSubscription = gs.schema._subscription
GrappleMutation = gs.schema._mutation


class Query(
    GrappleQuery,
    TagQuery,
):
    pass


# class Mutation(GrappleMutation):
#     pass


class Subscription(GrappleSubscription):
    pass


schema = graphene.Schema(
    query=Query,
    subscription=GrappleSubscription,
)
