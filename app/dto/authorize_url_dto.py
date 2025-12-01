from pydantic import BaseModel
from urllib.parse import urlencode


class AuthorizeUrlDto(BaseModel):
    issuer_authorize: str
    response_type: str
    client_id: str
    redirect_uri: str
    scope: str
    state: str
    nonce: str
    code_challenge: str
    code_challenge_method: str

    def build(self) -> str:
        # Construir los parámetros de la URL
        query_params = {
            "response_type": self.response_type,
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
            "state": self.state,
            "nonce": self.nonce,
            "code_challenge": self.code_challenge,
            "code_challenge_method": self.code_challenge_method
        }

        # Codificar los parámetros como query string
        query_string = urlencode(query_params)

        # Retornar la URL final
        return f"{self.issuer_authorize}?{query_string}"
