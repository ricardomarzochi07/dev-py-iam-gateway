from pydantic import BaseModel, Field
from datetime import datetime, timezone
from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field


class SessionModel(BaseModel):
    sub: str
    username: str
    roles: List[str] = Field(default_factory=list)
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
