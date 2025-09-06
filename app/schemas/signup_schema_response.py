from pydantic import BaseModel


class SignupResponse(BaseModel):
    jwt_nonce: str
    jwt_csrf: str
    captcha_token: str

