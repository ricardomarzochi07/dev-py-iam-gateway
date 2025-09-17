from abc import ABC, abstractmethod

from buddybet_transactionmanager.http.transaction_http import HttpResponseSchema
from app.schemas.signupsubmit_schema_request import SignupSubmitRequest


class SignupSubmitService(ABC):


    @abstractmethod
    def orchestrate_signup_submit(self, req: SignupSubmitRequest, cookies: dict) -> HttpResponseSchema:
        pass

    @abstractmethod
    def validate_signup(self, jwt_nonce: str , jwt_csrf: str, captcha_token: str, cookies: dict) -> bool:
        pass

