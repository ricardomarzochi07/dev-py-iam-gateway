import uuid
from app.core.cache.base import Cache
from buddybet_transactionmanager.http.exceptions import HttpClientError
from app.component.session_context import SessionContext
from app.core.exceptions import ExternalServiceError
from app.dto.authorize_url_dto import AuthorizeUrlDto
from app.core.environment_config import AppConfig
from buddybet_logmon_common.logger import get_logger
from datetime import datetime, timezone

from app.dto.signin_init_dto import SigninInitDTO
from app.model.prelogin_model import SigninPreLoginModel
from app.services.iam.signin_services.signin_service import SigninService
import json

from app.utils.authorize_helper import AuthorizeHelper


class SigninPreLoginServiceImpl(SigninService):
    logger = get_logger()

    def __init__(self, config: AppConfig, cache: Cache):
        self.cache = cache
        self.env_var = config.signup_gateway_env

    async def orchestrate_signin_init(self) -> SigninInitDTO:
        self.logger.info("Execute Request - orchestrate_signup_init")
        try:
            # (1) - Generate Codes PKCE
            session_obj = SessionContext(self.env_var)
            login_session_dto = session_obj.session_code_auth_init()
            preLoginModel = SigninPreLoginModel(
                state=login_session_dto.state,
                nonce=login_session_dto.nonce,
                code_verifier=login_session_dto.code_verifier,
                code_challenge=login_session_dto.code_challenge,
                redirect_uri=self.env_var.bff_service_domain + AuthorizeHelper.REDIRECT_URI,
                created_at=datetime.now(timezone.utc)
            )

            # 2) Store pré-login (uso único, TTL curto)
            prelogin_id = f"pl_{uuid.uuid4().hex}"
            store_prelogin = await self._save_prelogin(prelogin_id=prelogin_id,
                                           state=preLoginModel.state,
                                           data=preLoginModel.dict())

            # 3) Construir URL de autorização IdP - # ---- Montar authorize_url (WSO2) ----
            idp_uri_auth = self.env_var.idp_service_url+AuthorizeHelper.AUTH_ISSUER
            auth_idp_dto = AuthorizeUrlDto(
                issuer_authorize=idp_uri_auth,
                response_type=AuthorizeHelper.RESPONSE_TYPE,
                client_id=self.env_var.authcode_clientid_idp,
                redirect_uri=self.env_var.bff_service_domain + AuthorizeHelper.REDIRECT_URI,
                scope=AuthorizeHelper.SCOPE,
                state=preLoginModel.state,
                nonce=preLoginModel.nonce,
                code_challenge=preLoginModel.code_challenge,
                code_challenge_method=AuthorizeHelper.CODE_CHALLENGE_METHOD)

            auth_dto = auth_idp_dto.build()

            # 4) Construir Return Objecto para layer API
            response = SigninInitDTO(
                authorize_url=auth_dto,
                csrf_token=login_session_dto.csrf_token
            )
            return response

        except HttpClientError:
            self.logger.error("Error Execute Request - orchestrate_signup_init")
            raise ExternalServiceError()

    async def _save_prelogin(self, prelogin_id: str, state: str, data: dict):
        payload = json.dumps(data, separators=(",", ":"))
        # 1) Guarda el payload completo por prelogin_id
        await self.cache.set(prelogin_id, payload, ttl=180)
        # 2) Guarda un índice "pre:{state}" → prelogin_id
        await self.cache.set(f"pre:{state}", prelogin_id, ttl=180)
        ok = await self.cache.set(prelogin_id, payload, ttl=180)
        return bool(ok)

