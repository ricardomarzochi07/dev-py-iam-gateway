from app.dto.jwt_dto import JwtTokenDTO
from datetime import datetime, timedelta, timezone
import jwt
import secrets
from app.core.iam_constants import IAMConstants


class JwtConfig:

    @staticmethod
    def create_jwt() -> dict:
        jwtToken = JwtTokenDTO(
            aud="signup",
            iat=int(datetime.now(timezone.utc).timestamp()),
            exp=int((datetime.now(timezone.utc) + timedelta(minutes=IAMConstants.DEFAULT_EXP_MINUTES)).timestamp()),
            jti=secrets.token_hex(32)
        )
        return jwtToken.dict()
