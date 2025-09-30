from fastapi import APIRouter, Depends, Response, Request, HTTPException
from app.core.cookies_config import CookiesConfig
from app.core.environment_config import AppConfig
from app.core.exceptions import ExternalServiceError, GenerationToken
from app.core.exceptions_handlers import build_success_response
from app.core.settings_config import load_config
from buddybet_logmon_common.logger import get_logger
from app.schemas.signup_schema_response import SignupResponse
from app.schemas.signupsubmit_schema_request import SignupSubmitRequest
from app.service.impl.signup_init_service_impl import SignupInitServiceImpl
from app.service.impl.signup_submit_service_impl import SignupSubmitServiceImpl
from buddybet_transactionmanager.http.transaction_http import HttpResponseSchema

router = APIRouter()
logger = get_logger()



@router.get("/signup/init",
            response_model_exclude_none=True,
            summary="Esta API permite generar JWT",
            response_model=HttpResponseSchema[SignupResponse],
            responses={200: {"description": "Success", },
                       404: {"description": "Not Found.", }, }, )
async def signup_init(response: Response, config: AppConfig = Depends(load_config)):
    logger.info("Execute Request - signup_init")
    signupInit_Service = SignupInitServiceImpl(config)
    signupInitDTO = signupInit_Service.orchestrate_signup_init()
    CookiesConfig.set_csrf_cookie(response, csrf_token=signupInitDTO.jwt_csrf)
    return build_success_response(e=GenerationToken, data=signupInitDTO)


@router.post("/signup/submit",
             response_model_exclude_none=True,
             response_model=HttpResponseSchema,
             summary="Valida Token JWT",
             responses={200: {"description": "Success", },
                        404: {"description": "Not Found.", }, }, )
async def signup_submit(signup_request: SignupSubmitRequest,
                        response: Response,
                        request: Request,
                        config: AppConfig = Depends(load_config)):
    logger.info("Execute Request - signup_submit")
    signupService = SignupSubmitServiceImpl(config)
    return signupService.orchestrate_signup_submit(signup_request, request.cookies)