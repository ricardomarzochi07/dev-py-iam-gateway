# exceptions_handlers.py
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from http import HTTPStatus
from typing import TypeVar

from buddybet_transactionmanager.http.transaction_http import HttpResponseSchema
from app.core.exceptions import OperationStatus
from app.core.i18n_instance import i18n

T = TypeVar('T')


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(OperationStatus)
    async def operation_status_handler(request: Request, exc: OperationStatus):
        message = i18n.gettext(exc.message_key)
        schema = HttpResponseSchema(
            status_response=False,
            status_code=exc.status_code,
            message=message,
            # Recomendado: agrega error_code en tu schema
            # error_code=exc.message_key,
            data=None,
        )
        content = schema.dict() if hasattr(schema, "dict") else schema.model_dump()
        return JSONResponse(status_code=exc.status_code, content=content)

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        schema = HttpResponseSchema(
            status_response=False,
            status_code=exc.status_code,
            message=str(exc.detail),
            data=None,
        )
        content = schema.dict() if hasattr(schema, "dict") else schema.model_dump()
        return JSONResponse(status_code=exc.status_code, content=content)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        schema = HttpResponseSchema(
            status_response=False,
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY.value,  # 422
            message=i18n.gettext("validation_error"),
            data=exc.errors(),  # útil para el front
        )
        content = schema.dict() if hasattr(schema, "dict") else schema.model_dump()
        return JSONResponse(status_code=HTTPStatus.UNPROCESSABLE_ENTITY.value, content=content)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        # Loguea exc con stacktrace aquí
        schema = HttpResponseSchema(
            status_response=False,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            message=i18n.gettext("internal_server_error"),
            data=None,
        )
        content = schema.dict() if hasattr(schema, "dict") else schema.model_dump()
        return JSONResponse(status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value, content=content)


def build_success_response(message_key: str, data: T) -> HttpResponseSchema:
    """Utilidad para respuestas 200 OK con i18n."""
    message = i18n.gettext(message_key)
    return HttpResponseSchema(
        status_response=True,
        data=data,
        status_code=HTTPStatus.OK.value,
        message=message
    )
