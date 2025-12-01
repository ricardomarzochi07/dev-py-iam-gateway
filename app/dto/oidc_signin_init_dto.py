from pydantic import BaseModel


class OidcSigninInitDTO(BaseModel):
    authorize_url: str
    prelogin_id: str
