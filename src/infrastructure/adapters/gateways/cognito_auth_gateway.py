import base64
import hashlib
import hmac
from abc import ABC
import jwt
from botocore.exceptions import ClientError
import boto3
import os

from src.domain.errors.confirmation_code_errors import ResendConfirmationCodeError, InvalidConfirmationCodeError, \
    UserAlreadyConfirmedError
from src.domain.errors.sign_in_errors import IncorrectPasswordError, PasswordResetRequiredError
from src.domain.errors.sign_up_errors import UserAlreadyExistsError, InvalidUserAttributesError
from src.domain.errors.token_refresh_errors import InvalidRefreshTokenError, TokenRefreshError
from src.domain.interfaces.gateways.auth_gateway_interface import AuthGatewayInterface
from requests import get
from jwt.algorithms import RSAAlgorithm


class CognitoAuthGateway(AuthGatewayInterface, ABC):
    def __init__(self):
        self.client = boto3.client("cognito-idp", region_name=os.getenv("AWS_REGION"))
        self.user_pool_id = os.getenv("COGNITO_USER_POOL_ID")
        self.client_id = os.getenv("COGNITO_CLIENT_ID")
        self.cognito_client_secret = os.getenv("COGNITO_CLIENT_SECRET")
        self.aws_region = os.getenv("AWS_REGION")
        self.jwks_url = f"https://cognito-idp.{self.aws_region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json"

    def _fetch_jwks_keys(self):
        response = get(self.jwks_url)
        return response.json()["keys"]

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
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == "UsernameExistsException":
                raise UserAlreadyExistsError("A user with the given email already exists.")
            elif error_code in ["InvalidParameterException", "InvalidPasswordException"]:
                raise InvalidUserAttributesError("Provided user attributes are invalid.")

    def sign_in(self, email: str, password: str) -> object:
        auth_params = {
            "USERNAME": email,
            "PASSWORD": password,
            "SECRET_HASH": self._generate_secret_hash(email),
        }
        try:
            auth_response = self.client.initiate_auth(
                AuthFlow="USER_PASSWORD_AUTH",
                ClientId=self.client_id,
                AuthParameters=auth_params,
            )
            return {
                "access_token": auth_response["AuthenticationResult"]["IdToken"],
                "refresh_token": auth_response["AuthenticationResult"]["RefreshToken"]
            }
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == "NotAuthorizedException":
                raise IncorrectPasswordError()
            elif error_code == "PasswordResetRequiredException":
                raise PasswordResetRequiredError()

    def refresh_token(self, refresh_token: str, access_token: str):
        sub = self._extract_from_expired_token(access_token=access_token, key="sub")
        secret_hash = self._generate_secret_hash(sub)
        auth_params = {
            "REFRESH_TOKEN": refresh_token,
            "SECRET_HASH": secret_hash
        }
        try:
            auth_response = self.client.initiate_auth(
                AuthFlow="REFRESH_TOKEN_AUTH",
                ClientId=self.client_id,
                AuthParameters=auth_params,
            )
            return {
                "access_token": auth_response["AuthenticationResult"]["IdToken"]
            }
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == "NotAuthorizedException":
                raise InvalidRefreshTokenError()
            else:
                raise TokenRefreshError("An unexpected error occurred during token refresh")

    def _jwk_to_public_key(self, jwk_key):
        public_key = RSAAlgorithm.from_jwk(jwk_key)
        return public_key

    def authorizer(self, access_token: str):
        jwks_keys = self._fetch_jwks_keys()
        header = jwt.get_unverified_header(access_token)
        rsa_key = jwks_keys.get(header['kid'])
        if not rsa_key:
            raise ValueError("Key ID not found in JWKS keys")

        public_key = self._jwk_to_public_key(jwk_key=rsa_key)

        # Decodificar y verificar el token
        decoded = jwt.decode(
            access_token,
            public_key,
            algorithms=["RS256"],
            audience=self.client_id,
            issuer=f"https://cognito-idp.{self.aws_region}.amazonaws.com/{self.user_pool_id}"
        )
        return {"message": "Ok", "decode": decoded}

    def _generate_secret_hash(self, username: str) -> str:
        """Calcula el SECRET_HASH usando Client Secret, Client ID y el nombre de usuario"""
        message = f"{username}{self.client_id}".encode("utf-8")
        key = self.cognito_client_secret.encode("utf-8")
        secret_hash = base64.b64encode(hmac.new(key, message, digestmod=hashlib.sha256).digest()).decode("utf-8")
        return secret_hash

    def _extract_from_expired_token(self, access_token: str, key: str) -> str:
        payload = jwt.decode(access_token, options={"verify_signature": False})
        return payload.get(key)

    def confirm_user(self, email: str, confirmation_code: str):
        try:
            response = self.client.confirm_sign_up(
                ClientId=self.client_id,
                Username=email,
                ConfirmationCode=confirmation_code,
                SecretHash=self._generate_secret_hash(email)
            )
            return response
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            if error_code == "CodeMismatchException":
                raise InvalidConfirmationCodeError(f"Error confirming user: {error_message}")
            elif error_code == "NotAuthorizedException" or error_code == "LimitExceededException":
                raise UserAlreadyConfirmedError(f"Error confirming user: {error_message}")

    def resend_confirmation_code(self, email: str):
        try:
            response = self.client.resend_confirmation_code(
                ClientId=self.client_id,
                Username=email,
                SecretHash=self._generate_secret_hash(email)
            )
            return {"message": "Código reenviado."}
        except ClientError as e:
            error_message = e.response['Error']['Message']
            raise ResendConfirmationCodeError(f"Error resending confirmation code: {error_message}")
