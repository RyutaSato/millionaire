import asyncio
from uuid import UUID

from millionaire.libs.room.baseroom import Room
from millionaire.libs.room.user import UserManager
from millionaire.libs.room.waiting_room import WaitingRoom
from millionaire.schemas.room_cmd import RoomCmd
import logging

logger = logging.getLogger(__name__)


class RoomManager:
    """このクラスの役割は，RoomのCRUD管理をすることです．
    Roomのインスタンスを動的に生成，削除，変更を行います．
    なお，clientとのメッセージのやり取りは，各Roomインスタンスが行うものとし，RoomManagerは一切関与しません．

    """
    def __init__(self, room_cmd_que: asyncio.Queue, user_to_room: dict[UUID, UUID], room: dict[UUID, Room]):
        self.__room = room
        self.__user_to_room = user_to_room

        self.room_que = room_cmd_que
        waiting_room = WaitingRoom()
        self.__room[waiting_room.room_id] = waiting_room
        self.__waiting_room_id = waiting_room.room_id
        self.__que_task = asyncio.create_task(self.__que_task_func())
        pass

    def __await__(self):
        return

    async def __que_task_func(self):
        while True:
            msg: RoomCmd = await self.room_que.get()
            logger.info(f"que received msg: {msg.json()}")
            room_from = self.__room.get(msg.room_from)
            room_to = self.__room.get(msg.room_to)
            if room_from is None or room_to is None:
                logger.critical(f"can't find room_id room_from: {room_from}"
                                f" or room_to: {room_to} in rooms")
            logger.info(f"transport uid: {msg.uid} from {room_from.room_id} to {room_to.room_id}")
            user = room_from.pop(msg.uid)
            room_to.add(user)

    def add_user(self, user: UserManager):
        self.__room[self.__waiting_room_id].add(user)
        self.__user_to_room[user.uid] = self.__waiting_room_id

    def remove_user(self, user: UserManager):
        room_id = self.__user_to_room[user.uid]
        self.__room[room_id].remove(user)

    def pop_user(self, uid: UUID):
        room_id = self.__user_to_room[uid]
        self.__room[room_id].pop(uid)
