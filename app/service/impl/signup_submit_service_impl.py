from app.client.oidc_gateway_service.oidc_service_client import OidcGatewayServiceClient
from app.core.iam_constants import IAMConstants
from app.schemas.signupsubmit_schema_request import SignupSubmitRequest
from app.service.signup_submit_service import SignupSubmitService
import jwt
from buddybet_logmon_common.logger import get_logger
from app.core.environment_config import AppConfig
from fastapi import HTTPException
from jose import jwt, JWTError
from buddybet_transactionmanager.http.transaction_http import HttpResponseSchema



class SignupSubmitServiceImpl(SignupSubmitService):
    logger = get_logger()

    def __init__(self, config: AppConfig):
        self.env_var = config.signup_gateway_env

    def orchestrate_signup_submit(self, data: SignupSubmitRequest, cookies: dict) -> HttpResponseSchema:
        self.logger.info("Execute Request - orchestrate_signup_submit")
        oidc_service = OidcGatewayServiceClient()
        try:
            # (1) Validate tokens
            if self.validate_signup(data.jwt_nonce, data.jwt_csrf, data.captcha_token, cookies):
                # (2) Call - Get OIDC to Register User in IDP
                response = oidc_service.post_register_user(url=self.env_var.oidc_service_url,body=data)
                return response
        except Exception as e:
            self.logger.error(f"Error register_user_idp: {e}")
            return HttpResponseSchema(
                status_response=False,
                status_code=500,
                data=None,
                message=f"Unhandled exception: {str(e)}"
            )

    def validate_signup(self, internal_token: str, jwt_csrf: str, captcha_token: str, cookies: dict) -> bool:
        self.logger.info("Execute Request - validate_signup")
        try:
            # (1) Validar JWT nonce
            jwt.decode(internal_token, self.env_var.public_key,
                       algorithms=IAMConstants.ALGORITHM,
                       audience=IAMConstants.AUDIENCE)
        except JWTError as e:
            self.logger.error("Token inválido", exc_info=True)
            raise HTTPException(status_code=401, detail="Invalid token")

        # (2) Validar CSRF
        csrf_cookie = str(cookies.get("csrf_token"))
        print(" csrf_cookie csrf_cookie ", csrf_cookie)
        if jwt_csrf != csrf_cookie:  # O compara con cookie en request.headers
            self.logger.error("csrf_cookie inválido", exc_info=True)
            return False

        # (3) Validar CAPTCHA
        """ 
        captcha_google_secret = self.env_var.key_recaptcha_int_secret
        try:
            r = requests.post(
                self.env_var.recaptcha_google_service_url,
                data={"secret": captcha_google_secret, "response": captcha_token}
            )
            result = r.json()
        except Exception as e:
            self.logger.error(f"Error al validar captcha: {e}")
            return False
        if not result.get("success", False):
            return False
        
        """
        return True

