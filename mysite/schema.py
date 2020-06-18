import graphene
from grapple. schema import schema as gs

from tagging.schema import TaggingQueries

GrappleQuery = gs._query
GrappleSubscription = gs._subscription
GrappleMutation = gs._mutation


class Query(GrappleQuery, TaggingQueries):
    pass


class Subscription(GrappleSubscription):
    pass


schema = graphene.Schema(
    query=Query,
    subscription=GrappleSubscription,
)
