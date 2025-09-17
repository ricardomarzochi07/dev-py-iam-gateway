from fastapi import APIRouter, Body, Depends, Response, Request, HTTPException
from app.core.cookies_config import CookiesConfig
from app.core.environment_config import AppConfig
from app.core.settings_config import load_config
from buddybet_logmon_common.logger import get_logger
from app.schemas.signup_schema_response import SignupResponse
from app.schemas.signupsubmit_schema_request import SignupSubmitRequest
from app.service.impl.signup_init_service_impl import SignupInitServiceImpl
from app.service.impl.signup_submit_service_impl import SignupSubmitServiceImpl
from buddybet_transactionmanager.http.transaction_http import HttpResponseSchema

router = APIRouter()
logger = get_logger()



@router.get("/signup/teste")
async def teste():
    logger.info("Execute Request - signup_init")
    try:
        return "ok"
    except Exception as e:
        logger.error(f"Error Execute Request - signup_init: {e}")



@router.get("/signup/init",
            response_model_exclude_none=True,
            summary="Esta API permite generar JWT",
            response_model=SignupResponse,
            responses={200: {"description": "Success", },
                       404: {"description": "Not Found.", }, }, )
async def signup_init(response: Response, config: AppConfig = Depends(load_config)):
    logger.info("Execute Request - signup_init")
    try:
        signupInit_Service = SignupInitServiceImpl(config)
        signupInitDTO = signupInit_Service.orchestrate_signup_init()
        CookiesConfig.set_csrf_cookie(response, csrf_token=signupInitDTO.jwt_csrf)
        return signupInitDTO
    except Exception as e:
        logger.error(f"Error Execute Request - signup_init: {e}")
        raise HTTPException(status_code=500, detail="Error interno en signup_init")


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
    try:
        signupService = SignupSubmitServiceImpl(config)
        response = signupService.orchestrate_signup_submit(signup_request, request.cookies)
        return response
    except Exception as e:
        logger.error(f"Error Execute Request - internal_token:", exc_info=True)
        return HttpResponseSchema(
            status_response=False,
            status_code=500,
            data=None,
            message=f"Unhandled exception: {str(e)}"
        )

