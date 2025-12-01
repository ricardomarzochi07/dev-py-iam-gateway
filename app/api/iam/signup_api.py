from fastapi import APIRouter, Depends, Response, Request
from app.core.cookies_config import CookiesConfig
from app.core.environment_config import AppConfig
from app.core.exceptions_handlers import build_success_response
from app.core.settings_config import load_config
from buddybet_logmon_common.logger import get_logger
from app.schemas.signup_schemas.signup_schema_response import SignupResponse
from app.schemas.signup_schemas.signupsubmit_schema_request import SignupSubmitRequest
from buddybet_transactionmanager.http.transaction_http import HttpResponseSchema
from app.service.iam.signin_services import SignupServiceImpl

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
    signupInit_Service = SignupServiceImpl(config)
    signupInitDTO = signupInit_Service.orchestrate_signup_init()
    CookiesConfig.set_csrf_cookie(response, csrf_token=signupInitDTO.jwt_csrf)
    return build_success_response(message_key="generation_token", data=signupInitDTO)


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
    signupService = SignupServiceImpl(config)
    response = signupService.orchestrate_signup_submit(signup_request, request.cookies)
    print("RESPONSE ", response)
    return response
