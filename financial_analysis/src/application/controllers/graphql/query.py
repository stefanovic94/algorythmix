import strawberry


@strawberry.type
class Query:
    hello: str = strawberry.field(resolver=lambda: "World")
