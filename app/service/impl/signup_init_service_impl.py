import secrets

from app.client.oidc_gateway_service.oidc_service_client import OidcGatewayServiceClient
from app.schemas.signup_schema_response import SignupResponse
from app.service.signup_init_service import SignupInitService
from app.core.environment_config import AppConfig
from buddybet_logmon_common.logger import get_logger
from fastapi import HTTPException


class SignupInitServiceImpl(SignupInitService):
    logger = get_logger()

    def __init__(self, config: AppConfig):
        self.env_var = config.signup_gateway_env

    def orchestrate_signup_init(self) -> SignupResponse:
        self.logger.info("Execute Request - orchestrate_signup_init")
        try:
            jwt_nonce_code = self.generate_token_nonce()
            jwt_csrf_code = self.generate_csrf_token()
            signupResp = SignupResponse(
                jwt_nonce=jwt_nonce_code,
                jwt_csrf=jwt_csrf_code,
                captcha_token=self.env_var.key_recaptcha_secret
            )
            return signupResp

        except Exception as e:
            self.logger.error("Error Execute Request - orchestrate_signup_init", e)



    def generate_token_nonce(self) -> str:
        self.logger.info("Execute Request - generate_token_nonce")
        try:
            oidc_client = OidcGatewayServiceClient()
            oidc_response = oidc_client.get_oidc_token_internal(self.env_var.oidc_service_url)
            return oidc_response.jwt_nonce
        except Exception as e:
            self.logger.error("Error Execute Request - generate_token_nonce", exc_info=True)
            raise HTTPException(status_code=500, detail="Error internal")

    def generate_csrf_token(self) -> str:
        self.logger.info("Execute Request - generate_csrf_token")
        try:
            jwt_csrf = secrets.token_urlsafe(32)
            return jwt_csrf
        except Exception as e:
            self.logger.error("Error Execute Request - generate_csrf_token", e)





