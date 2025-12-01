from buddybet_transactionmanager.http.exceptions import HttpClientError
from app.client.oidc_gateway_service.oidc_service_client import OidcGatewayServiceClient
from app.component.session_context import SessionContext
from app.core.iam_constants import IAMConstants
from app.schemas.signup_schemas.signup_schema_response import SignupResponse
from app.schemas.signup_schemas.signupsubmit_schema_request import SignupSubmitRequest
import jwt
import requests
from app.core.exceptions import InvalidToken, InvalidCaptcha, InvalidGenerationToken, ExternalServiceError
from buddybet_logmon_common.logger import get_logger
from app.core.environment_config import AppConfig
from jose import jwt, JWTError
from buddybet_transactionmanager.http.transaction_http import HttpResponseSchema
from app.services.iam.signup_services.signup_service import SignupService


class SignupServiceImpl(SignupService):
    logger = get_logger()

    def __init__(self, config: AppConfig):
        self.env_var = config.signup_gateway_env


    def orchestrate_signup_init(self) -> SignupResponse:
        self.logger.info("Execute Request - orchestrate_signup_init")
        try:
            session_obj = SessionContext(self.env_var)
            session_dto = session_obj.session_code_auth_init()
            signupResp = SignupResponse(
                jwt_nonce=session_dto.jwt_nonce,
                jwt_csrf=session_dto.jwt_csrf,
                captcha_token=session_dto.captcha_token)
            return signupResp
        except InvalidGenerationToken:
            self.logger.error("Error generate internal token ")
            raise
        except HttpClientError:
            self.logger.error("Error Execute Request - orchestrate_signup_init")
            raise ExternalServiceError()

    def orchestrate_signup_submit(self, data: SignupSubmitRequest, cookies: dict) -> HttpResponseSchema:
        self.logger.info("Execute Request - orchestrate_signup_submit")
        oidc_service = OidcGatewayServiceClient(self.env_var)

        # (1) Validate methods
        self._validate_jwt_nonce(data.jwt_nonce)
        self._validate_csrf_token(data.jwt_csrf, cookies)
        #self._validate_captcha(data.captcha_token)

        # (2) Call - Get OIDC to Register User in IDP
        response = oidc_service.post_register_user(body=data)
        return response


    def _validate_jwt_nonce(self, token: str) -> None:
        try:
            jwt.decode(token, self.env_var.public_key,
                       algorithms=IAMConstants.ALGORITHM,
                       audience=IAMConstants.AUDIENCE)
        except JWTError:
            self.logger.error("Token JWT inválido", exc_info=True)
            raise InvalidToken()

    def _validate_csrf_token(self, jwt_csrf: str, cookies: dict) -> None:
        csrf_cookie = str(cookies.get("csrf_token"))
        if jwt_csrf != csrf_cookie:
            self.logger.error("Token CSRF inválido", exc_info=True)
            raise InvalidToken()

    def _validate_captcha(self, captcha_token: str) -> None:
        r = requests.post(
            self.env_var.recaptcha_google_service_url,
            data={
                "secret": self.env_var.key_recaptcha_int_secret,
                "response": captcha_token
            }
        )
        r.raise_for_status()
        result = r.json()
        if not result.get("success", False):
            self.logger.warning(f"Captcha inválido: {result}")
            raise InvalidCaptcha()


