from abc import ABC, abstractmethod

from app.schemas.signin_schemas.signin_init_response_schema import SigninInitResponseSchema
from app.schemas.signup_schemas.signup_schema_response import SignupResponse


class SigninService(ABC):

    @abstractmethod
    def orchestrate_signin_init(self) -> SigninInitResponseSchema:
        pass


