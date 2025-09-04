from pydantic import BaseModel


class SignupResponse(BaseModel):
    nonce: str
    captchaSiteKey: str
