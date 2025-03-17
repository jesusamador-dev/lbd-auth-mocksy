from src.domain.interfaces.gateways.auth_gateway_interface import AuthGatewayInterface


class RefreshTokenUseCase:
    def __init__(self, auth_gateway: AuthGatewayInterface):
        self.auth_gateway = auth_gateway

    def execute(self, refresh_token: str, access_token: str):
        return self.auth_gateway.refresh_token(refresh_token, access_token)
