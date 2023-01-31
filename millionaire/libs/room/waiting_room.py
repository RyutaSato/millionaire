from uuid import UUID

from millionaire.libs.room.baseroom import BaseRoom, RoomType
from millionaire.schemas.message import Message, RoomMessage
import logging

from millionaire.schemas.msg_types import StatusTypes

logger = logging.getLogger(__name__)
MIN_PLAYER_NUM = 4


class WaitingRoom(BaseRoom):
    """このクラスの役割は，userの状態管理です．
    クライアントがwebsocket接続し，認証後はまずこのクラスに格納されます．
    """

    def __init__(self, room_manager):
        super().__init__(RoomType.waiting, room_manager)
        self.__matching_list: list[UUID] = []

    def msg_analyser(self, msg: Message):
        if not isinstance(msg.msg, RoomMessage):
            logger.error(f"msg is invalid type {type(msg.msg)}")
            return
        if msg.msg.status == StatusTypes.matching:
            user = self._roommates.get(msg.uid)
            if user is None:
                logger.critical(f"can't find uid {msg.uid} in waiting room "
                                f"msg {msg.json()}")
                return
            user.status = msg.msg.status

    def add_matching(self, uid: UUID):
        user = self.__roommates.get(uid)
        user.status = StatusTypes.matching
        self.__matching_list.append(uid)
        logger.info(f"uid: {uid} is in matching que... Now waiting people: {len(self.__matching_list)}")
        if len(self.__matching_list) >= MIN_PLAYER_NUM:
            self.__manager.create_room([self.__matching_list.pop() for _ in range(MIN_PLAYER_NUM)])
