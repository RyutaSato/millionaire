import asyncio
from datetime import datetime
from enum import Enum
from typing import TypeVar
from uuid import UUID

from ulid import ULID

from millionaire.libs.room.rooms_manager import RoomManager
from millionaire.libs.room.user import UserManager
from millionaire.schemas.message import Message


class RoomType(Enum):
    waiting = "waiting"
    matching = "matching"
    match = "match"


class BaseRoom:
    """このクラスはRoomクラスの親クラスであり, Messageインスタンスの適切な受け渡し(Broker)を担います，

    """

    def __init__(self, room_type: RoomType, room_manager: RoomManager):
        self.__manager = room_manager
        self.__room_id: UUID = ULID().to_uuid()
        self.__created_at: datetime = datetime.now()
        self.room_type = room_type  # enumで定義
        self.__roommates: dict[UUID, UserManager] = dict()
        self.msg_in_que = asyncio.Queue()
        self._msg_in_task = asyncio.create_task(self.msg_parser())

    @property
    def room_id(self):
        return self.__room_id

    def add(self, user: UserManager):
        self.__roommates[user.uid] = user

    def remove(self, user: UserManager):
        del self.__roommates[user.uid]

    def pop(self, uid: UUID):
        return self.__roommates.pop(uid)

    async def msg_parser(self):
        while True:
            msg = await self.msg_in_que.get()  # from message_broker
            self.msg_analyser(msg)
            # TODO: 構文解析

    def msg_analyser(self, msg: Message):
        raise NotImplementedError

    async def send(self, msg):
        await self.__manager.send(msg)

Room = TypeVar("Room", bound=BaseRoom)
