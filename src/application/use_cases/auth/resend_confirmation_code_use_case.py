from src.domain.interfaces.gateways.auth_gateway_interface import AuthGatewayInterface


class ResendConfirmationCodeUseCase:
    def __init__(self, auth_gateway: AuthGatewayInterface):
        self.auth_gateway = auth_gateway

    def execute(self, email: str):
        return self.auth_gateway.resend_confirmation_code(email=email)
