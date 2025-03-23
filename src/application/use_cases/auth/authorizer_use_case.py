from src.domain.interfaces.gateways.auth_gateway_interface import AuthGatewayInterface
from fastapi import HTTPException


class AuthorizerUseCase:
    def __init__(self, auth_gateway: AuthGatewayInterface):
        self.auth_gateway = auth_gateway

    def execute(self, token: str):
        try:
            return self.auth_gateway.authorizer(access_token=token)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Server error")
