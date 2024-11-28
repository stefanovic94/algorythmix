class EventBrokerError(Exception):
    pass


class EventProcessingError(Exception):
    pass


class EventCouldNotBeDecoded(Exception):
    pass


class EventNotSupported(Exception):
    pass


class EventValidationError(Exception):
    pass
