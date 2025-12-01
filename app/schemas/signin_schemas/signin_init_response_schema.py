from pydantic import BaseModel


class SigninInitResponseSchema(BaseModel):
    authorize_url: str
    csrf_token: str
