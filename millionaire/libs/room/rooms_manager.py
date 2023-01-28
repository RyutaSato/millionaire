import asyncio
from uuid import UUID

from millionaire.libs.room.baseroom import BaseRoom
from millionaire.schemas.room_cmd import RoomCmd
import logging

logger = logging.getLogger(__name__)


class RoomsManager:
    def __init__(self):
        self.__rooms: dict[UUID, BaseRoom] = dict()
        self.rooms_que = asyncio.Queue()
        self.__que_task = asyncio.create_task(self.__que_task_func())
        pass

    def __await__(self):
        return

    async def __que_task_func(self):
        while True:
            msg: RoomCmd = await self.rooms_que.get()
            logger.info(f"que received msg: {msg.json()}")
            room_from = self.__rooms.get(msg.room_from)
            room_to = self.__rooms.get(msg.room_to)
            if room_from is None or room_to is None:
                logger.critical(f"can't find room_id room_from: {room_from}"
                                f" or room_to: {room_to} in rooms")
            logger.info(f"transport uid: {msg.uid} from {room_from.room_id} to {room_to.room_id}")
            user = room_from.pop(msg.uid)
            room_to.add(user)
