from pydantic import BaseModel
from typing import Optional


class AppConfigEnvironment(BaseModel):
    key_recaptcha_secret: str
    key_recaptcha_int_secret: str
    oidc_idp_token_service_url: str
    oidc_internal_token_service_url: str
    signup_register_service_url: str
    public_key: Optional[bytes] = None
    recaptcha_google_service_url: str


class AppConfig(BaseModel):
    signup_gateway_env: AppConfigEnvironment
