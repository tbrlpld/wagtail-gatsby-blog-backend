import graphene
from grapple. schema import schema as gs

from blog.schema import TagQuery

GrappleQuery = gs._query
GrappleSubscription = gs._subscription
GrappleMutation = gs._mutation


class Query(GrappleQuery, TagQuery):
    pass


class Subscription(GrappleSubscription):
    pass


schema = graphene.Schema(
    query=Query,
    subscription=GrappleSubscription,
)
