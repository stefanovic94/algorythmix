"""
Package containing all the potential mappings.

Example
-------
    A mapping could be using some enum in the HTTP router like specifying time ranges:

        e.g. '7d', '3mo', '5y'

    Which might be incompatible with the DB when making a query. Here a mapping can be used for
    converting into the supported format of the infrastructure service.
"""
