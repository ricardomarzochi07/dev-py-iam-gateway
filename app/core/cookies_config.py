from fastapi import Response
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
            max_age=cookie.max_age
        )

    @staticmethod
    def set_csrf_cookie(response: Response, csrf_token: str):
        csrf_cookie = CookieDto(
            key="csrf_token",
            value=csrf_token,
            httponly=True,
            samesite="strict",
            secure=False,
            max_age=120)
        CookiesConfig.set_cookie(response, csrf_cookie)

    @staticmethod
    def set_session_cookie(self, csrf_token: str) -> CookieDto:
        session_cookie = CookieDto(
            key="csrf_session",
            value=csrf_token,
            httponly=True,
            samesite="None",
            secure=True,
            max_age=120)
        return session_cookie
