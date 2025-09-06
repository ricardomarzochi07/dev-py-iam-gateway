from pydantic import BaseModel


class AppConfigEnvironment(BaseModel):
    key_jwt_secret: str
    key_recaptcha_secret: str
    key_recaptcha_int_secret: str


class AppConfig(BaseModel):
    iam_gateway_env: AppConfigEnvironment
