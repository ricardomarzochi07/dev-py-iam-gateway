from buddybet_logmon_common.logger import get_logger
from app.client.oidc_gateway_service.oidc_token_internal_schema import OidcTokenInternalResponse
from app.client.oidc_gateway_service.oidc_paths import OidcPaths
from buddybet_transactionmanager.http.transaction_http import HttpClient
from buddybet_transactionmanager.schemas.http_response_schema import HttpResponseSchema
from app.schemas.signupsubmit_schema_request import SignupSubmitRequest


class OidcGatewayServiceClient:
    logger = get_logger()

    def post_register_user(self, url: str, body: SignupSubmitRequest) -> HttpResponseSchema:
        self.logger.info("Execute Request - post_register_user")
        headers = {"Content-Type": f"application/json"}
        try:
            client = HttpClient(url, cert=None, verify=None)
            return client.post(path=OidcPaths.CREATE_USER,
                               json_data=body.dict(),
                               headers=headers)
        except Exception as e:
            self.logger.error("Unexpected error while preparing or sending request", exc_info=True)
            return HttpResponseSchema(
                status_response=False,
                status_code=500,
                data=None,
                message=f"Unhandled exception: {str(e)}"
            )

    def get_oidc_token_internal(self, url: str) -> OidcTokenInternalResponse:
        self.logger.info("Execute Request - get_oidc_token_internal")
        headers = {"Accept": f"application/json"}
        try:
            client = HttpClient(url, cert=None, verify=None)
            response = client.get(path=OidcPaths.TOKEN_INT,
                                  params=None,
                                  headers=headers)
            return OidcTokenInternalResponse(**response.data)
        except Exception as e:
            self.logger.error("Execute Request - get_oidc_token_internal", exc_info=True)
