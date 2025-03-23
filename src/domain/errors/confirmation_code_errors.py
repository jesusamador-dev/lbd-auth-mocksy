class ConfirmationCodeError(Exception):
    """Excepción base para errores relacionados con el código de confirmación."""
    def __init__(self, message="Error with confirmation code", status_code=400):
        super().__init__(message)
        self.status_code = status_code
        self.message = message


class ResendConfirmationCodeError(ConfirmationCodeError):
    """Excepción específica para errores al reenviar códigos de confirmación."""
    def __init__(self, message="Failed to resend confirmation code"):
        super().__init__(message, status_code=400)


class InvalidConfirmationCodeError(ConfirmationCodeError):
    """Código de confirmación inválido o expirado."""
    def __init__(self, message="Invalid or expired confirmation code"):
        super().__init__(message, status_code=400)


class UserAlreadyConfirmedError(ConfirmationCodeError):
    """Usuario ya confirmado."""
    def __init__(self, message="User is already confirmed"):
        super().__init__(message, status_code=400)
