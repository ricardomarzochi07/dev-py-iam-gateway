from pydantic import BaseModel, Field
from datetime import datetime, timezone, timedelta


class SigninPreLoginModel(BaseModel):
    state: str
    nonce: str
    code_verifier: str
    code_challenge: str
    csrf_token: str
    redirect_uri: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def is_expired(self, ttl_seconds: int = 180) -> bool:
        return datetime.now(timezone.utc) - self.created_at > timedelta(seconds=ttl_seconds)