from abc import ABC, abstractmethod

from app.schemas.signup_schema_response import SignupResponse


class SignupInitService(ABC):

    @abstractmethod
    def generate_token_nonce(self) -> str:
        pass

    @abstractmethod
    def generate_csrf_token(self) -> str:
        pass

    @abstractmethod
    def orchestrate_signup_init(self) -> SignupResponse:
        pass
