from uuid import UUID

from pydantic import BaseModel

from millionaire.schemas.msg_types import RoomCmdTypes


class RoomCmd(BaseModel):
    uid: UUID
    room_cmd: RoomCmdTypes
    room_from: UUID
    room_to: UUID
