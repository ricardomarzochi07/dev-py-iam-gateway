from abc import ABC, abstractmethod

from app.schemas.signup_schema_response import SignupResponse
from app.schemas.signupsubmit_schema_request import SignupSubmitRequest


class SignupService(ABC):

    @abstractmethod
    def generate_token_nonce(self) -> str:
        pass

    @abstractmethod
    def generate_csrf_token(self) -> str:
        pass

    @abstractmethod
    def validate_signup(self, req: SignupSubmitRequest, cookies: dict) -> bool:
        pass

    @abstractmethod
    def orchestrate_signup_init(self) -> SignupResponse:
        pass
