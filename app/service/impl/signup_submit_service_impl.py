from app.client.oidc_gateway_service.oidc_schema_request import OidcRequestSchema
from app.client.oidc_gateway_service.oidc_service_client import OidcGatewayServiceClient
from app.client.signup_core_service.signup_core_request_schema import SignupCoreRequestSchema
from app.client.signup_core_service.signup_core_service_client import SignupCoreServiceClient
from app.core.iam_constants import IAMConstants
from app.schemas.signup_schema_response import SignupResponse
from app.schemas.signupsubmit_schema_request import SignupSubmitRequest
from app.service.signup_submit_service import SignupSubmitService
import requests
import jwt
from buddybet_logmon_common.logger import get_logger
from app.core.environment_config import AppConfig
from fastapi import HTTPException
from jose import jwt, JWTError


class SignupSubmitServiceImpl(SignupSubmitService):
    logger = get_logger()

    def __init__(self, config: AppConfig):
        self.env_var = config.signup_gateway_env
        self.oidc_service = OidcGatewayServiceClient(config)
        self.signup_core_service = SignupCoreServiceClient(config)

    def orchestrate_signup_submit(self, data: SignupSubmitRequest, cookies: dict) -> SignupResponse:
        self.logger.info("Execute Request - orchestrate_signup_submit")
        try:
            # (1) Validate tokens
            if self.validate_signup(data.jwt_nonce, data.jwt_csrf, data.captcha_token, cookies):
                # (2) Call - Get Token in OIDC_Gateway_Service > WSO2
                print("========== VALIDACION OK =============")
                oidcRequest = OidcRequestSchema(
                    jwt_nonce=data.jwt_nonce,
                    token_type=IAMConstants.TOKEN_TYPE,
                    expires_in=120
                )
                print("========== BODY  OK =============", oidcRequest.jwt_nonce)

                oidcResponse = self.oidc_service.get_token_oidc_idp(oidcRequest)
                if oidcResponse is not None:
                    # (3) Call - Register User in Signup_Core_Service
                    print(" oidcResponse.access_token ", oidcResponse.access_token)

                    self.register_user_signup_core_service(data, oidcResponse.access_token)
        except Exception as e:
            self.logger.error(f"Error Execute Request - orchestrate_signup_submit:", exc_info=True)
            return False

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

    def register_user_signup_core_service(self, data: SignupSubmitRequest, access_token: str):
        self.logger.info("Execute Request - validate_signup")
        try:
            # Crear instancia de SignupCoreServiceSchema solo con atributos comunes
            signup_core_schema = SignupCoreRequestSchema(
                **data.dict(
                    include=SignupCoreRequestSchema.model_fields.keys()  # incluye solo campos comunes
                )
            )
            print(" signup_core_schema ", signup_core_schema    )

            return self.signup_core_service.post_register_user(signup_core_schema, access_token)
        except Exception as e:
            self.logger.error(f"Error OIDC_Service: {e}")
        return None
