from src.domain.errors.sign_in_errors import SignInError
from src.domain.interfaces.gateways.auth_gateway_interface import AuthGatewayInterface
from fastapi import HTTPException


class SignInUseCase:
    def __init__(self, auth_gateway: AuthGatewayInterface):
        self.auth_gateway = auth_gateway

    def execute(self, email: str, password: str) -> object:
        try:
            return self.auth_gateway.sign_in(email=email, password=password)
        except SignInError as e:
            raise HTTPException(status_code=e.status_code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Server error")
