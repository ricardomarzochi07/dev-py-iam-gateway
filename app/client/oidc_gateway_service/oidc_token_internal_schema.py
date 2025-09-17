from pydantic import BaseModel


class OidcTokenInternalResponse(BaseModel):
    jwt_nonce: str
    token_type: str
    expires_in: int
