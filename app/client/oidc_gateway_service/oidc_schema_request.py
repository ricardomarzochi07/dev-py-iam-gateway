from pydantic import BaseModel


class OidcRequestSchema(BaseModel):
    jwt_nonce: str
    token_type: str
    expires_in: int
