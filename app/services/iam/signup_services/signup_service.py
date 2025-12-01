from abc import ABC, abstractmethod

from buddybet_transactionmanager.http.transaction_http import HttpResponseSchema

from app.schemas.signup_schemas.signup_schema_response import SignupResponse
from app.schemas.signup_schemas.signupsubmit_schema_request import SignupSubmitRequest


class SignupService(ABC):

    @abstractmethod
    def orchestrate_signup_init(self) -> SignupResponse:
        pass

    @abstractmethod
    def orchestrate_signup_submit(self, data: SignupSubmitRequest, cookies: dict) -> HttpResponseSchema:
        pass



