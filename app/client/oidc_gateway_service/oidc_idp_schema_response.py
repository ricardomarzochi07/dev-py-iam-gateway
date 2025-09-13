from pydantic import BaseModel


class OidcIdpResponseSchema(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
