import graphene

from grapple import schema as gs

from blog.schema import TagQuery

GrappleQuery = gs.schema._query
GrappleSubscription = gs.schema._subscription
GrappleMutation = gs.schema._mutation


class Query(
    GrappleQuery,
    TagQuery,
):
    pass


class Subscription(GrappleSubscription):
    pass


schema = graphene.Schema(
    query=Query,
    subscription=GrappleSubscription,
)
