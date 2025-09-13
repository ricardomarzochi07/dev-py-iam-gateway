from pydantic import BaseModel


class OidcInternalResponseSchema(BaseModel):
    jwt_nonce: str
    token_type: str
    expires_in: int
