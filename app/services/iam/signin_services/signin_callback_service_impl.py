from app.client.oidc_gateway_service.oidc_service_client import OidcGatewayServiceClient
from app.client.oidc_gateway_service.schemas.authorization_code_response_schema import AuthorizationCodeResponse
from app.core.cache.base import Cache
from app.core.exceptions import InvalidToken, InvalidPreLogin, CodeExchangeError
from app.core.environment_config import AppConfig
from buddybet_logmon_common.logger import get_logger
from app.model.prelogin_model import SigninPreLoginModel
import json
from secrets import token_urlsafe
from app.model.session_model import SessionModel
from app.utils.authorize_helper import AuthorizeHelper
from buddybet_idpsecure.authorization.transaction_auth import TransactionAuthorization
from datetime import datetime, timedelta, timezone


class CallbackServiceImpl:
    logger = get_logger()

    def __init__(self, config: AppConfig, cache: Cache):
        self.cache = cache
        self.env_var = config.signup_gateway_env

    async def callback_idp_orq(self, code: str, state: str) -> str:
        self.logger.info("Execute Request - callback_idp_orq")

        # 1) Cargar pre-login por state
        prelogin_model = await self._load_cache(state)
        if not prelogin_model:
            raise InvalidPreLogin()

        # 2) Intercambiar code por tokens (PKCE)
        try:
            authorization_code_resp = await self._call_oidc_exchange_code(preLogin=prelogin_model)
        except Exception as ex:
            raise CodeExchangeError()

        # 3) Validar token (firma + claims)
        id_token = authorization_code_resp.id_token
        access_token = authorization_code_resp.access_token
        if not id_token and access_token:
            raise InvalidToken()
        claims = self._validate_token(id_token=id_token, access_token=access_token, nonce=prelogin_model.nonce)

        # 4) Crear sesión del BFF
        session_id = await self._store_session(authToken=authorization_code_resp)
        return

    async def _store_session(self, authToken: AuthorizationCodeResponse) -> str:
        self.logger.info("Execute Request - _store_session")

        session_id = token_urlsafe(32)
        now = datetime.now(timezone.utc)

        # Creamos el objeto SessionModel
        session = SessionModel(
            sub=authToken.sub,
            username=authToken.username,
            roles=authToken.roles,
            access_token=authToken.access_token,
            refresh_token=authToken.refresh_token,
            expires_at=now + timedelta(seconds=authToken.expires_in),
            created_at=now,
        )
        try:
            await self.cache.set(key=session_id, value=session, ttl=320)
            return session_id
        except Exception as ex:
            print("Errror - Cache ", ex)

    async def _load_cache(self, state: str) -> SigninPreLoginModel:
        self.logger.info("Execute Request - _load_cache")

        # Recuperar el prelogin_id asociado a ese state
        prelogin_id = await self.cache.get(f"pre:{state}")
        if not prelogin_id:
            raise InvalidPreLogin()

        # Recuperar el payload completo del prelogin
        payload_json = await self.cache.get(prelogin_id)
        if not payload_json:
            raise InvalidPreLogin()

        # Convertir de JSON a dict
        payload_dict = json.loads(payload_json)
        prelogin_model = SigninPreLoginModel(**payload_dict)
        return prelogin_model

    async def _call_oidc_exchange_code(self, preLogin: SigninPreLoginModel) -> AuthorizationCodeResponse:
        self.logger.info("Execute Request - _call_oidc_exchange_code")
        u  = OidcGatewayServiceClient(self.env_var)
        # (2) Call - Get OIDC service to Exchange Code for IdToken
        data = {
            "code": AuthorizeHelper.RESPONSE_TYPE,
            "code_verifier": preLogin.code_verifier,
            "redirect_uri": preLogin.redirect_uri}
        response = oidc_service.get_oidc_exchange_code_for_tokens(params=data)
        return response

    async def _validate_token(self, id_token: str, access_token: str, nonce: str):
        self.logger.info("Execute Request - _validate_id_token")
        idp_validation = TransactionAuthorization(id_token=id_token, access_token=access_token, nonce=nonce)
        claims = await idp_validation.transaction_valid()
        return claims
