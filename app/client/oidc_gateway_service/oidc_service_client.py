from buddybet_logmon_common.logger import get_logger
from buddybet_transactionmanager.schemas.http_response_schema import HttpResponseSchema

from app.client.oidc_gateway_service.schemas.authorization_code_response_schema import AuthorizationCodeResponse
from app.client.oidc_gateway_service.schemas.oidc_token_internal_schema import OidcTokenInternalResponse
from app.client.oidc_gateway_service.oidc_paths import OidcPaths
from buddybet_transactionmanager.http.transaction_http import HttpClient
from app.core.exceptions import (InvalidGenerationToken, ExternalServiceError, InvalidUserDataError,
                                 ResourceNotFoundError, UserAlreadyExistsError)
from app.schemas.signup_schemas.signupsubmit_schema_request import SignupSubmitRequest
from app.core.i18n_instance import i18n
from app.core.environment_config import AppConfigEnvironment


class OidcGatewayServiceClient:
    logger = get_logger()

    def __init__(self, config: AppConfigEnvironment):
        self.env_var = config

    def post_register_user(self, body: SignupSubmitRequest) -> HttpResponseSchema:
        self.logger.info("Execute Request - post_register_user")
        headers = {"Content-Type": f"application/json",
                   "Accept-Language": i18n.get_language()}
        url = self.env_var.oidc_service_url
        try:
            client = HttpClient(url, cert=None, verify=None)
            response = client.post(path=OidcPaths.CREATE_USER,
                                   json_data=body.dict(),
                                   headers=headers)

            if response.status_response:
                return response
            elif not response.status_response:
                if response.status_code == 400:
                    raise InvalidUserDataError()
                elif response.status_code == 404:
                    raise ResourceNotFoundError()
                elif response.status_code == 409:
                    raise UserAlreadyExistsError()
                else:
                    raise ExternalServiceError()

        except UserAlreadyExistsError:
            self.logger.warning("The user is already registered in the system..")
            raise
        except Exception as e:
            self.logger.error("Error de red al comunicar con Alta de Clientes", exc_info=True)
            raise ExternalServiceError() from e

    def get_oidc_token_internal(self) -> OidcTokenInternalResponse:
        self.logger.info("Execute Request - get_oidc_token_internal")
        headers = {"Accept": f"application/json",
                   "Accept-Language": i18n.get_language()}
        url = self.env_var.oidc_service_url
        try:
            client = HttpClient(url, cert=None, verify=None)
            response = client.get(path=OidcPaths.TOKEN_INT,
                                  params=None,
                                  headers=headers)
            if response.status_response:
                return OidcTokenInternalResponse(**response.data['data'])
            else:
                raise InvalidGenerationToken

        except Exception as e:
            self.logger.error("Error de red al comunicar con Alta de Clientes", exc_info=True)
            raise ExternalServiceError() from e

    def post_signin_init(self, body: SignupSubmitRequest) -> HttpResponseSchema:
        self.logger.info("Execute Request - post_signin_init")
        headers = {"Content-Type": f"application/json",
                   "Accept-Language": i18n.get_language()}
        url = self.env_var.oidc_service_url
        try:
            client = HttpClient(url, cert=None, verify=None)
            response = client.post(path=OidcPaths.AUTH_INIT,
                                   json_data=body.dict(),
                                   headers=headers)

            if response.status_response:
                return response
            elif not response.status_response:
                if response.status_code == 400:
                    raise InvalidUserDataError()
                elif response.status_code == 404:
                    raise ResourceNotFoundError()
                elif response.status_code == 409:
                    raise UserAlreadyExistsError()
                else:
                    raise ExternalServiceError()

        except UserAlreadyExistsError:
            self.logger.warning("Error SignIN..")
            raise
        except Exception as e:
            self.logger.error("Error de red al comunicar con Alta de Clientes", exc_info=True)
            raise ExternalServiceError() from e


    def get_oidc_exchange_code_for_tokens(self, params: dict) -> AuthorizationCodeResponse:
        self.logger.info("Execute Request - get_oidc_token_internal")
        headers = {"Accept": f"application/json",
                   "Accept-Language": i18n.get_language()}
        url = self.env_var.oidc_service_url
        try:
            client = HttpClient(url, cert=None, verify=None)
            response = client.get(path=OidcPaths.EXCHANGE_CODE,
                                  params=params,
                                  headers=headers)
            if response.status_response:
                return AuthorizationCodeResponse(**response.data['data'])
            else:
                raise InvalidGenerationToken

        except Exception as e:
            self.logger.error("Error de red al comunicar con Alta de Clientes", exc_info=True)
            raise ExternalServiceError() from e