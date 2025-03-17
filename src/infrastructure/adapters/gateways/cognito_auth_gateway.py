import base64
import hashlib
import hmac
from abc import ABC

import boto3
import os
from src.domain.interfaces.gateways.auth_gateway_interface import AuthGatewayInterface


class CognitoAuthGateway(AuthGatewayInterface, ABC):
    def __init__(self):
        self.client = boto3.client("cognito-idp", region_name=os.getenv("AWS_REGION"))
        self.user_pool_id = os.getenv("COGNITO_USER_POOL_ID")
        self.client_id = os.getenv("COGNITO_CLIENT_ID")
        self.cognito_client_secret = os.getenv("COGNITO_CLIENT_SECRET")

    def sign_up(self, email: str, password: str) -> object:
        try:
            secret_hash = self._generate_secret_hash(email)
            self.client.sign_up(
                ClientId=self.client_id,
                SecretHash=secret_hash,
                Username=email,
                Password=password,
                UserAttributes=[{"Name": "email", "Value": email}],
            )
            return {"message": "Usuario registrado. Confirma el email."}
        except Exception as e:
            return {"error": str(e)}

    def sign_in(self, email: str, password: str) -> object:
        try:
            auth_response = self.client.initiate_auth(
                AuthFlow="USER_PASSWORD_AUTH",
                ClientId=self.client_id,
                AuthParameters={"USERNAME": email, "PASSWORD": password},
            )
            return {
                "access_token": auth_response["AuthenticationResult"]["IdToken"],
                "refresh_token": auth_response["AuthenticationResult"]["RefreshToken"]
            }
        except Exception as e:
            return {"error": str(e)}

    def refresh_token(self, refresh_token: str):
        try:
            auth_response = self.client.initiate_auth(
                AuthFlow="REFRESH_TOKEN_AUTH",
                ClientId=self.client_id,
                AuthParameters={"REFRESH_TOKEN": refresh_token},
            )
            return {
                "access_token": auth_response["AuthenticationResult"]["IdToken"]
            }
        except Exception as e:
            return {"error": str(e)}

    def authorizer(self, access_token: str):
        return "OK"

    def _generate_secret_hash(self, username: str) -> str:
        """Calcula el SECRET_HASH usando Client Secret, Client ID y el nombre de usuario"""
        message = f"{username}{self.client_id}".encode("utf-8")
        key = self.cognito_client_secret.encode("utf-8")
        secret_hash = base64.b64encode(hmac.new(key, message, digestmod=hashlib.sha256).digest()).decode("utf-8")
        return secret_hash
