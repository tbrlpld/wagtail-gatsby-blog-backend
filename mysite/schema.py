import graphene
from grapple. schema import schema as gs

from tagging.schema import Query as TaggingQuery
# from blog.schema import Query as BlogQuery

GrappleQuery = gs._query
GrappleSubscription = gs._subscription
GrappleMutation = gs._mutation


class Query(
    GrappleQuery,
    TaggingQuery,
    # BlogQuery,
):
    pass


class Subscription(GrappleSubscription):
    pass


schema = graphene.Schema(
    query=Query,
    subscription=GrappleSubscription,
)
