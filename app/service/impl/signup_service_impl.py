import secrets

from app.core.iam_constants import IAMConstants
from app.core.jwt_config import JwtConfig
from app.dto.signup_dto import SignupInitDTO
from app.schemas.signup_schema_response import SignupResponse
from app.service.signup_service import SignupService
from app.core.environment_config import AppConfig
from buddybet_logmon_common.logger import get_logger
import jwt
import requests
from jose import jwt, JWTError
import os


class SignupServiceImpl(SignupService):
    logger = get_logger()

    def __init__(self, config: AppConfig):
        self.env_var = config.iam_gateway_env


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
            jwt_payload = JwtConfig.create_jwt()
            jwt_payload_nonce = jwt.encode(jwt_payload, self.env_var.key_jwt_secret, algorithm=IAMConstants.ALGORITHM)
            return jwt_payload_nonce
        except Exception as e:
            self.logger.error("Error Execute Request - generate_token_nonce", e)

    def generate_csrf_token(self) -> str:
        self.logger.info("Execute Request - generate_csrf_token")
        try:
            jwt_csrf = secrets.token_urlsafe(32)
            return jwt_csrf
        except Exception as e:
            self.logger.error("Error Execute Request - generate_csrf_token", e)

    def validate_signup(self, req, cookies) -> bool:
        self.logger.info("Execute Request - validate_signup")
        try:
            # (1) Validar JWT nonce
            payload = jwt.decode(
                req.jwt_nonce,
                self.env_var.key_jwt_secret,
                IAMConstants.ALGORITHM,
                audience="signup"
            )
        except Exception as e:
            self.logger.info("Error Token No Valid")
            return False

        # (2) Validar CSRF
        csrf_cookie = cookies.get("csrf_token")
        if req.jwt_csrf != csrf_cookie:  # O compara con cookie en request.headers
            return False

        # (3) Validar CAPTCHA
        captcha_google_secret = self.env_var.key_recaptcha_int_secret
        try:
            r = requests.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data={"secret": captcha_google_secret, "response": req.captcha_token}
            )
            result = r.json()
        except Exception as e:
            self.logger.error(f"Error al validar captcha: {e}")
            return False

        if not result.get("success", False):
            return False

        return True




