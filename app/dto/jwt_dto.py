from pydantic import BaseModel


class JwtTokenDTO(BaseModel):
    aud: str
    iat: int
    exp: int
    jti: str