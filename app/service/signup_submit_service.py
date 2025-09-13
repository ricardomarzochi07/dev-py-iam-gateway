from abc import ABC, abstractmethod

from app.client.signup_core_service.signup_core_request_schema import SignupCoreRequestSchema
from app.schemas.signup_schema_response import SignupResponse
from app.schemas.signupsubmit_schema_request import SignupSubmitRequest


class SignupSubmitService(ABC):


    @abstractmethod
    def orchestrate_signup_submit(self, req: SignupSubmitRequest, cookies: dict) -> SignupResponse:
        pass

    @abstractmethod
    def validate_signup(self, jwt_nonce: str , jwt_csrf: str, captcha_token: str, cookies: dict) -> bool:
        pass


    @abstractmethod
    def register_user_signup_core_service(self, data: SignupSubmitRequest, access_token: str):
        pass
