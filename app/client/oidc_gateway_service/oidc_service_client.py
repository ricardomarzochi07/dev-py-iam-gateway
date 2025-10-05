from buddybet_logmon_common.logger import get_logger
from buddybet_transactionmanager.schemas.http_response_schema import HttpResponseSchema
from app.client.oidc_gateway_service.oidc_token_internal_schema import OidcTokenInternalResponse
from app.client.oidc_gateway_service.oidc_paths import OidcPaths
from buddybet_transactionmanager.http.transaction_http import HttpClient
from app.core.exceptions import (InvalidGenerationToken, ExternalServiceError, InvalidUserDataError,
                                 ResourceNotFoundError, UserAlreadyExistsError)
from app.schemas.signupsubmit_schema_request import SignupSubmitRequest
from app.core.i18n_instance import i18n


class OidcGatewayServiceClient:
    logger = get_logger()

    def post_register_user(self, url: str, body: SignupSubmitRequest) -> HttpResponseSchema:
        self.logger.info("Execute Request - post_register_user")
        headers = {"Content-Type": f"application/json",
                   "Accept-Language": i18n.get_language()}
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


    def get_oidc_token_internal(self, url: str) -> OidcTokenInternalResponse:
        self.logger.info("Execute Request - get_oidc_token_internal")
        headers = {"Accept": f"application/json",
                   "Accept-Language": i18n.get_language()}
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
