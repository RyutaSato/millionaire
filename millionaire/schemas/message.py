from typing import Literal
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

from millionaire.schemas.msg_types import MsgTypes, PlayMsgTypes, StatusTypes


class NoneMessage(BaseModel):
    msg_type: Literal['none']
    body: str


class InPlayMessage(BaseModel):
    msg_type: Literal['in_play']
    play_type: PlayMsgTypes
    cards: list[str] = []


class OutPlayMessage(BaseModel):
    msg_type: Literal['out_play']
    play_type: PlayMsgTypes
    cards: list[str] = []



class RoomMessage(BaseModel):
    msg_type: Literal['room']
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
    msg_type: MsgTypes = Literal['none']
    msg: InPlayMessage | OutPlayMessage | RoomMessage = Field(discriminator="msg_type")

    class Config:
        use_enum_values = True
