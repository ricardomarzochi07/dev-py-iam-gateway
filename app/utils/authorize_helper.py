from enum import Enum


class AuthorizeHelper(Enum):
    RESPONSE_TYPE = "code"
    SCOPE = "openid profile email"
    AUTH_ISSUER = "/oauth2/authorize"
    CODE_CHALLENGE_METHOD = "S256"
    REDIRECT_URI = "/auth/callback"
