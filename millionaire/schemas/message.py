from typing import Literal
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

from millionaire.schemas.msg_types import MsgTypes, StatusTypes


class NoneMessage(BaseModel):
    msg_type: MsgTypes = Literal['none']


class InPlayMessage(BaseModel):
    msg_type: MsgTypes = Literal['in_play']


class OutPlayMessage(BaseModel):
    msg_type: MsgTypes = Literal['out_play']


class RoomMessage(BaseModel):
    msg_type: MsgTypes = Literal['room']
    status: StatusTypes


class Message(BaseModel):
    """
    Attributes:
        uid (UUID):
        created_by (str):
        created_at (str):
        msg:
    """
    uid: UUID
    created_by: str  # class名
    created_at: datetime = Field(default_factory=datetime.utcnow)
    msg_type: MsgTypes = MsgTypes.none
    msg: InPlayMessage | OutPlayMessage | RoomMessage = Field(discriminator="msg_type")

    class Config:
        use_enum_values = True
