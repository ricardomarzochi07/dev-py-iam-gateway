from fastapi import APIRouter, Body, Depends, Response

from app.core.cookies_config import CookiesConfig
from app.core.environment_config import AppConfig
from app.core.settings_config import load_config
from buddybet_logmon_common.logger import get_logger
from datetime import datetime, timedelta
import jwt
import secrets

from app.schemas.signup_schema_response import SignupResponse
from app.service.impl.signup_service_impl import SignupServiceImpl

router = APIRouter()
logger = get_logger()


@router.get("/api/signup/init",
            response_model_exclude_none=True,
            summary="Esta API permite generar JWT",
            response_model=SignupResponse,
            responses={200: {"description": "Success", },
                       404: {"description": "Not Found.", }, }, )
async def signup_init(response: Response, config: AppConfig = Depends(load_config)):
    logger.info("Execute Request - signup_init")
    try:
        signupService = SignupServiceImpl(config)
        signupInitDTO = signupService.orchestrate_signup_init()
        CookiesConfig.set_csrf_cookie(response, csrf_token=signupInitDTO.jwt_csrf)

        return SignupResponse(
            nonce=signupInitDTO.jwt_nonce,
            captchaSiteKey=signupInitDTO.captcha_key
        )
    except Exception as e:
        logger.error("Error Execute Request - signup_init" ,e)

