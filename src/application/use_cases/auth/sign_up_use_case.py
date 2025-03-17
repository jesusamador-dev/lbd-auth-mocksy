from src.domain.interfaces.gateways.auth_gateway_interface import AuthGatewayInterface


class SignUpUseCase:
    def __init__(self, auth_gateway: AuthGatewayInterface):
        self.auth_gateway = auth_gateway

    def execute(self, email: str, password: str) -> object:
        return self.auth_gateway.sign_up(email, password)
