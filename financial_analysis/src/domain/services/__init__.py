"""
Package containing all the domain services.

A domain service is used only for operations where more than one domain entity
is involved.

Example
-------
    Calculating the average profit of all historically used strategies.

    The service could be something like `StrategyMetricsCalculatorService`.
    The `Strategy` entity could have a method for calculating the profit it has
    made -> e.g. `.profit(): Decimal` which would likely be a computed_field (pydantic).

    The service could then have a method which accepts a list of strategy objects, and
    calls the .profit() method on each of them, returning the sum.
"""
