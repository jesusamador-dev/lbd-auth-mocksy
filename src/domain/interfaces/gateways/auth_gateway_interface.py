from abc import ABC, abstractmethod


class AuthGatewayInterface(ABC):
    @abstractmethod
    def sign_up(self, email: str, password: str):
        pass

    @abstractmethod
    def sign_in(self, email: str, password: str):
        pass

    @abstractmethod
    def refresh_token(self, refresh_token: str, access_token: str):
        pass

    @abstractmethod
    def authorizer(self, access_token: str):
        pass
