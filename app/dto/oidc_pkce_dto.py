from pydantic import BaseModel


class OidcPkceDTO(BaseModel):
    state = str
    nonce = str
    csrf_token = str
    code_verifier = str
    code_challenge = str
