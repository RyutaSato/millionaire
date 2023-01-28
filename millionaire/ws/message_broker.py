import asyncio
from uuid import UUID

from fastapi import Depends
from logging import getLogger

from starlette.websockets import WebSocket

from millionaire.libs.room.baseroom import Room
from millionaire.libs.room.user import UserManager
from millionaire.libs.room.waiting_room import WaitingRoom
from millionaire.schemas.message import Message
from millionaire.schemas.msg_types import StatusTypes
from millionaire.ws.message_provider import MessageProvider

logger = getLogger(__name__)


class MessageBroker:
    """このクラスはサーバーに接続される全ての接続を保持し管理します．
    Fastapiのwebサーバー１つにつき１つのみ生成されます．
    """

    def __init__(self):
        self.__online: dict[UUID, MessageProvider] = dict()
        self.__users: dict[UUID, UserManager] = dict()
        self.__user_to_room: dict[UUID, UUID] = dict()
        self.__rooms: dict[UUID, Room] = dict()
        waiting_room = WaitingRoom()
        self.__rooms[waiting_room.room_id] = waiting_room
        self.__waiting_room_uid = waiting_room.room_id
        self.__in_que = asyncio.Queue()
        self.__out_que = asyncio.Queue()
        self.__msg_task = asyncio.create_task(self.__msg_switcher(), name="Message Switcher")

    async def __call__(self, websocket: WebSocket):
        """ '/ws'のendpointです．

        Args:
            websocket:

        Returns:

        """
        conn = MessageProvider(websocket, self.__in_que)
        self.__add_client(conn)
        await conn
        self.__remove_client(conn)

    def __add_client(self, client: MessageProvider):
        logger.info(f"connections: added: {client.uid}")
        self.__online[client.uid] = client
        self.__users[client.uid] = UserManager(uid=client.uid, status=StatusTypes.waiting)
        self.__rooms[self.__waiting_room_uid].add(client)
        self.__user_to_room[client.uid] = self.__waiting_room_uid
        logger.info(f"connections: total: {len(self.__online)}")

    def __remove_client(self, client: MessageProvider):
        logger.info(f"connections: remove: {client.uid}")
        del self.__online[client.uid]
        del self.__users[client.uid]
        self.__rooms[self.__waiting_room_uid].remove(client)
        del self.__user_to_room[client.uid]
        logger.info(f"connections: total: {len(self.__online)}")

    async def __msg_switcher(self):
        try:
            async with asyncio.TaskGroup() as tg:
                task_in = tg.create_task(self.__in(), name="self.__in()")
                task_out = tg.create_task(self.__out(), name="self.__out()")
        except* Exception as exc:
            logger.error(exc.args)
        finally:
            logger.info(f"in: cancelled? {task_in.cancelled()} out: cancelled? {task_out.cancelled()}")
            if not task_in.done():
                task_in.cancel()
            if not task_out.done():
                task_out.cancel()

    async def __in(self):
        while True:
            request: Message = await self.__in_que.get()
            logger.info(f"in: {request.json()}")
            room_id = self.__user_to_room.get(request.uid)
            if room_id is not None:
                await self.__rooms[room_id].msg_in_que.put(request)
            else:
                logger.error(f"Invalid uid: {request.uid}")
                logger.error(f"content: {request.json()}")

    async def __out(self):
        while True:
            request: Message = await self.__out_que.get()
            logger.info(f"out: {request.json()}")
            conn: MessageProvider = self.__online.get(request.uid)
            if conn is not None:
                await conn.send(request.msg)
            else:
                logger.error(f"Invalid uid: {request.uid}")
                logger.error(f"content: {request.json()}")
