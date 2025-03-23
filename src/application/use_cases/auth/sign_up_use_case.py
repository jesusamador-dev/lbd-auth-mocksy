from fastapi import HTTPException

from src.domain.errors.sign_up_errors import SignUpError
from src.domain.interfaces.gateways.auth_gateway_interface import AuthGatewayInterface


class SignUpUseCase:
    def __init__(self, auth_gateway: AuthGatewayInterface):
        self.auth_gateway = auth_gateway

    def execute(self, email: str, password: str) -> object:
        try:
            return self.auth_gateway.sign_up(email=email, password=password)
        except SignUpError as e:
            raise HTTPException(status_code=e.status_code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Server error")

