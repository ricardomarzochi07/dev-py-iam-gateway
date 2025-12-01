from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field


class AuthorizationCodeResponse(BaseModel):
    access_token: str
    sub: str
    roles: List[str] = Field(default_factory=list)
    username: str
    token_type: str
    expires_in: str
    scope: str
    id_token: str
    refresh_token: str
