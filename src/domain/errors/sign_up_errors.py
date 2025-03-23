class SignUpError(Exception):
    """Base class for registration errors."""
    def __init__(self, message="Registration failed", status_code=400):
        super().__init__(message)
        self.status_code = status_code
        self.message = message


class UserAlreadyExistsError(SignUpError):
    """Exception for trying to register a user that already exists."""
    def __init__(self, message="User already exists"):
        super().__init__(message, status_code=409)


class InvalidUserAttributesError(SignUpError):
    """Exception for invalid user attributes provided during registration."""
    def __init__(self, message="Invalid user attributes"):
        super().__init__(message, status_code=400)

