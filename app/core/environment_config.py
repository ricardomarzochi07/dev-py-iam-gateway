from pydantic import BaseModel
from typing import Optional


class AppConfigEnvironment(BaseModel):
    key_recaptcha_secret: str
    authcode_clientid_idp: str
    bff_service_domain: str
    idp_service_url: str
    key_recaptcha_int_secret: str
    oidc_service_url: str
    public_key: Optional[bytes] = None
    recaptcha_google_service_url: str
    callback_idp_service: str


class AppConfig(BaseModel):
    signup_gateway_env: AppConfigEnvironment
