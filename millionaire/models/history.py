from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class History(BaseModel):
    id: UUID
    created_at: datetime
    ended_at: datetime
    users: list[UUID]
