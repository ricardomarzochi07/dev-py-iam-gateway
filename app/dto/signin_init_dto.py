from pydantic import BaseModel

class SigninInitDTO(BaseModel):
    authorize_url: str
    csrf_token: str
