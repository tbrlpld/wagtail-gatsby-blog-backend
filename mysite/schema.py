import graphene

from grapple import schema as gs


GrappleQuery = gs.schema._query
GrappleSubscription = gs.schema._subscription
GrappleMutation = gs.schema._mutation


class Query(GrappleQuery):
    pass


# class Mutation(GrappleMutation):
#     pass


class Subscription(GrappleSubscription):
    pass


schema = graphene.Schema(
    query=Query,
    subscription=GrappleSubscription,
)
