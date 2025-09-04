from abc import ABC, abstractmethod

from app.dto.signup_dto import SignupInitDTO


class SignupService(ABC):

    @abstractmethod
    def generate_token_nonce(self) -> str:
        pass

    @abstractmethod
    def generate_csrf_token(self) -> str:
        pass

    @abstractmethod
    def orchestrate_signup_init(self) -> SignupInitDTO:
        pass
