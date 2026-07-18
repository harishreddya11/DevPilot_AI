class DevPilotException(Exception):
    """Base application exception."""


class AuthenticationError(DevPilotException):
    """Raised when authentication fails."""


class AuthorizationError(DevPilotException):
    """Raised when authorization fails."""


class NotFoundError(DevPilotException):
    """Raised when a resource is not found."""


class ConflictError(DevPilotException):
    """Raised when a resource already exists."""