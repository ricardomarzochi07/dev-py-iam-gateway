from fastapi import Response

from app.core.iam_constants import IAMConstants
from app.dto.cookie_dto import CookieDto


class CookiesConfig:

    @staticmethod
    def set_cookie(response: Response, cookie: CookieDto):
        response.set_cookie(
            key=cookie.key,
            value=cookie.value,
            httponly=cookie.httponly,
            samesite=cookie.samesite,
            secure=cookie.secure,
            max_age=cookie.max_age,
            path=cookie.path,
        )

    @staticmethod
    def set_csrf_cookie(response: Response, csrf_token: str):
        csrf_cookie = CookieDto(
            key="csrf_session",
            value=csrf_token,
            httponly=False,
            samesite="Strict",
            secure=False,
            max_age=300,
            path="/")
        CookiesConfig.set_cookie(response, csrf_cookie)

    @staticmethod
    def set_session_cookie(session_id: str) -> CookieDto:
        return CookieDto(
            key=IAMConstants.SESSION_COOKIE_NAME,
            value=session_id,
            httponly=True,
            samesite="lax",
            secure=True,
            path="/",
            max_age=IAMConstants.SESSION_TTL_SECONDS
        )
