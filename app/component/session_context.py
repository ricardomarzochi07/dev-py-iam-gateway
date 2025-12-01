from buddybet_transactionmanager.http.exceptions import HttpClientError
from app.client.oidc_gateway_service.oidc_service_client import OidcGatewayServiceClient
from app.core.environment_config import AppConfigEnvironment
from app.core.exceptions import InvalidGenerationToken, ExternalServiceError
import secrets
from buddybet_logmon_common.logger import get_logger

from app.dto.oidc_pkce_dto import OidcPkceDTO
from app.dto.session_dto import SessionDTO
from app.utils.generate_codes_helper import generate_codes_signin


class SessionContext:
    logger = get_logger()

    def __init__(self, config: AppConfigEnvironment):
        self.env_var = config

    def session_code_auth_init(self) -> OidcPkceDTO:
        self.logger.info("Execute Request - orchestrate_auth_init")
        try:
            code_pkce_dto = generate_codes_signin()
            return code_pkce_dto
        except HttpClientError:
            self.logger.error("Error Execute Request - orchestrate_auth_init")
            raise ExternalServiceError()

    def generate_token_nonce(self) -> str:
        self.logger.info("Execute Request - generate_token_nonce")
        try:
            oidc_client = OidcGatewayServiceClient(self.env_var)
            oidc_response = oidc_client.get_oidc_token_internal()
            return oidc_response.jwt_nonce

        except InvalidGenerationToken:
            self.logger.error("Error No Generate Token", exc_info=True)
            raise
        except HttpClientError:
            self.logger.error("Error Execute Request - generate_token_nonce", exc_info=True)
            raise


    def generate_csrf_token(self) -> str:
        self.logger.info("Execute Request - generate_csrf_token")
        try:
            jwt_csrf = secrets.token_urlsafe(32)
            return jwt_csrf
        except Exception:
            self.logger.error("Failed to generate CSRF token", exc_info=True)
            raise
