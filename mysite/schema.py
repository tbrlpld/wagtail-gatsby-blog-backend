import graphene
from grapple.schema import schema as gs

from tagging.schema import Query as TaggingQuery
from documents_extension.schema import Query as ExtendedDocumentsQuery

GrappleQuery = gs.Query
GrappleSubscription = gs.Subscription


class Query(
    GrappleQuery,
    TaggingQuery,
    ExtendedDocumentsQuery,
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
