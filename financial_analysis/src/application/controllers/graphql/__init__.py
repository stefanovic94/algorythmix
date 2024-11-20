import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.subscriptions import GRAPHQL_TRANSPORT_WS_PROTOCOL, GRAPHQL_WS_PROTOCOL

from .query import Query


schema = strawberry.federation.Schema(
    query=Query,
    types=[],
    enable_federation_2=True,
)
graphql_app = GraphQLRouter(
    schema,
    subscription_protocols=[
        GRAPHQL_TRANSPORT_WS_PROTOCOL,
        GRAPHQL_WS_PROTOCOL,
    ],
    graphql_ide="apollo-sandbox",
)
