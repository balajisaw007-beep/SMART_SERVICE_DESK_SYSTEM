class DuplicateRequestIdError(Exception):
    """Raised when a request ID already exists."""


class RequestNotFoundError(Exception):
    """Raised when a request ID cannot be found."""


class InvalidPriorityError(Exception):
    """Raised when the priority is outside the allowed values."""


class InvalidRequestDataError(Exception):
    """Raised when required request data is blank or invalid."""


class RequestResolutionUnauthorizedError(Exception):
    """Raised when someone other than the creator tries to resolve a request."""
