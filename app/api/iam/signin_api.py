from fastapi import APIRouter, Request, Response, Depends
from app.core.cookies_config import CookiesConfig
from app.core.environment_config import AppConfig
from app.core.exceptions import ExternalServiceError, InvalidUserDataError
from app.core.exceptions_handlers import build_success_response
from app.core.settings_config import load_config
from buddybet_logmon_common.logger import get_logger
from app.schemas.signin_schemas.signin_init_response_schema import SigninInitResponseSchema
from buddybet_transactionmanager.http.transaction_http import HttpResponseSchema
from app.core.cache.base import Cache
from app.core.cache.factory_cache import get_cache
from app.services.iam.signin_services.signin_callback_service_impl import CallbackServiceImpl
from app.services.iam.signin_services.signin_prelogin_service_impl import SigninPreLoginServiceImpl

router = APIRouter()
logger = get_logger()


def get_login_pre_service(
        config: AppConfig = Depends(load_config),  # FastAPI injeta AppConfig
        cache: Cache = Depends(get_cache),  # FastAPI injeta Cache (que já recebeu AppConfig)
) -> SigninPreLoginServiceImpl:
    return SigninPreLoginServiceImpl(config=config, cache=cache)


def get_login_callback_service(
        config: AppConfig = Depends(load_config),  # FastAPI injeta AppConfig
        cache: Cache = Depends(get_cache),  # FastAPI injeta Cache (que já recebeu AppConfig)
) -> CallbackServiceImpl:
    return CallbackServiceImpl(config=config, cache=cache)


@router.post("/auth/prelogin",
             response_model_exclude_none=True,
             summary="API Authorization ",
             response_model=HttpResponseSchema[SigninInitResponseSchema],
             responses={200: {"description": "Success", },
                        404: {"description": "Not Found.", }, }, )
async def auth_prelogin(response: Response,
                        signin_service: SigninPreLoginServiceImpl = Depends(get_login_pre_service)):
    logger.info("Execute Request - prelogin")
    prelogin_dto = await signin_service.orchestrate_signin_init()
    # Store SetCookie - CSRF
    CookiesConfig.set_csrf_cookie(response, csrf_token=prelogin_dto.csrf_token)

    signin_response = SigninInitResponseSchema(
        authorize_url=prelogin_dto.authorize_url,
        csrf_token=prelogin_dto.csrf_token
    )
    return build_success_response(message_key="register_user_success", data=signin_response)


@router.get(
    "/auth/callback",
    response_model=HttpResponseSchema,
    response_model_exclude_none=True,
    summary="Valida Token JWT",
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad Request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Not Found"},
        502: {"description": "Upstream IdP/Proxy error"},
    },
)
async def auth_callback(
        code: str | None = None,
        state: str | None = None,
        error: str | None = None,
        error_description: str | None = None,
        request: Request = None,
        response: Response = None,
        signin_call_service: CallbackServiceImpl = Depends(get_login_callback_service), ):
    logger.info("Execute Request - auth_callback")

    # 1) Errores IdP en /authorize (no hay 'code')
    if error:
        raise ExternalServiceError(message_key="oidc_authorize_error")

    # 2) Validación de parámetros requeridos
    if not code or not state:
        raise InvalidUserDataError(message_key="missing_code_or_state")  # 400

    # 3) Verificación/decodificación de 'state' y CSRF
    try:
        session_id = await signin_call_service.callback_idp_orq(code=code, state=state)
        cookie_dto = CookiesConfig.set_session_cookie(session_id=session_id)
        response.set_cookie(**cookie_dto.model_dump())

    except Exception:
        raise InvalidUserDataError(message_key="state_invalid")  # 400

    return build_success_response("login_user_success", data={"ok": "ok"})
