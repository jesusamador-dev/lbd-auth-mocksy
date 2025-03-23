from src.domain.errors.confirmation_code_errors import ConfirmationCodeError
from src.domain.interfaces.gateways.auth_gateway_interface import AuthGatewayInterface
from fastapi import HTTPException


class ConfirmUserUseCase:
    def __init__(self, auth_gateway: AuthGatewayInterface):
        self.auth_gateway = auth_gateway

    def execute(self, email: str, confirmation_code: str):
        try:
            return self.auth_gateway.confirm_user(email=email, confirmation_code=confirmation_code)
        except ConfirmationCodeError as e:
            raise HTTPException(status_code=e.status_code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Server error")
