from src.domain.interfaces.gateways.auth_gateway_interface import AuthGatewayInterface


class ConfirmUserUseCase:
    def __init__(self, auth_gateway: AuthGatewayInterface):
        self.auth_gateway = auth_gateway

    def execute(self, email: str, confirmation_code: str):
        return self.auth_gateway.confirm_user(email=email, confirmation_code=confirmation_code)
