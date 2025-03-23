class ServerError(Exception):
    """Excepción general para errores del servidor."""
    def __init__(self, message="An unexpected error occurred"):
        self.message = message
        super().__init__(self.message)
