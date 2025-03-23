class SignInError(Exception):
    """Excepción general para errores de inicio de sesión."""
    def __init__(self, message="Failed to sign in", status_code=400):
        super().__init__(message)
        self.status_code = status_code
        self.message = message


class UserNotFoundError(SignInError):
    """Usuario no encontrado."""
    def __init__(self, message="User not found"):
        super().__init__(message, status_code=404)


class IncorrectPasswordError(SignInError):
    """Contraseña incorrecta proporcionada."""
    def __init__(self, message="Incorrect email or password"):
        super().__init__(message, status_code=401)


class PasswordResetRequiredError(SignInError):
    """Se requiere restablecimiento de contraseña."""
    def __init__(self, message="Password reset required"):
        super().__init__(message, status_code=403)
