from fastapi import HTTPException
from src.domain.errors.token_refresh_errors import TokenRefreshError
from src.domain.interfaces.gateways.auth_gateway_interface import AuthGatewayInterface


class RefreshTokenUseCase:
    def __init__(self, auth_gateway: AuthGatewayInterface):
        self.auth_gateway = auth_gateway

    def execute(self, refresh_token: str, access_token: str):
        try:
            return self.auth_gateway.refresh_token(refresh_token=refresh_token, access_token=access_token)
        except TokenRefreshError as e:
            raise HTTPException(status_code=e.status_code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Server error")
