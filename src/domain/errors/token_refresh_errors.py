class TokenRefreshError(Exception):
    """Excepción general para errores de actualización de token."""
    def __init__(self, message="Failed to refresh token", status_code=400):
        super().__init__(message)
        self.status_code = status_code
        self.message = message


class InvalidRefreshTokenError(TokenRefreshError):
    """Token de actualización inválido o expirado."""
    def __init__(self, message="Invalid or expired refresh token"):
        super().__init__(message, status_code=401)
