import asyncio
from datetime import datetime
from enum import Enum
from typing import TypeVar
from uuid import UUID

from ulid import ULID

from millionaire.libs.room.user import UserManager
from millionaire.schemas.message import Message

class RoomType(Enum):
    waiting = "waiting"
    matching = "matching"
    match = "match"

class BaseRoom:
    """このクラスはRoomクラスの親クラスであり, Messageインスタンスの適切な受け渡し(Broker)を担います，

    """
    def __init__(self, room_type: RoomType):
        self._uid: UUID = ULID().to_uuid()
        self.created_at: datetime = datetime.now()
        self.room_type = room_type  # enumで定義
        self._roommate: dict[UUID, UserManager] = dict()
        self.msg_in_que = asyncio.Queue()
        self._msg_in_task = asyncio.create_task(self.msg_parser())
    @property
    def uid(self):
        return self._uid

    def add(self, user: UserManager):
        self._roommate[user.uid] = user

    def remove(self, user: UserManager):
        del self._roommate[user.uid]

    async def msg_parser(self):
        while True:
            msg = await self.msg_in_que.get()
            # TODO: 構文解析


Room = TypeVar("Room", bound=BaseRoom)
