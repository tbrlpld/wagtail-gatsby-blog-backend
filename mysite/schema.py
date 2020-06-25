import graphene
from grapple.schema import schema as gs

from tagging.schema import Query as TaggingQuery

GrappleQuery = gs.Query
GrappleSubscription = gs.Subscription


class Query(
    GrappleQuery,
    TaggingQuery,
):
    pass


class Subscription(
    GrappleSubscription,
):
    pass


types = gs.types + []

schema = graphene.Schema(
    query=Query,
    subscription=Subscription,
    types=types,
)
