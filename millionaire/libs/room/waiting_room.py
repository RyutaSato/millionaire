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
        if msg.uid not in self.__roommates:
            logger.critical(f"can't find uid {msg.uid} in waiting room "
                            f"msg {msg.json()}")
            return
        match msg.msg.status:
            case StatusTypes.matching:
                self.add_matching(msg.uid)
            case StatusTypes.waiting:
                self.remove_matching(msg.uid)
            case _:
                logger.critical(f"this status type: {msg.msg.status} doesn't follow ")


    def add_matching(self, uid: UUID):
        user = self.__roommates.get(uid)
        user.status = StatusTypes.matching
        self.__matching_list.append(uid)
        logger.info(f"uid: {uid} is in matching que... Now waiting people: {len(self.__matching_list)}")
        if len(self.__matching_list) >= MIN_PLAYER_NUM:
            self.__manager.create_room([self.__matching_list.pop() for _ in range(MIN_PLAYER_NUM)])

    def remove_matching(self, uid: UUID):
        user = self.__roommates.get(uid)
        user.status = StatusTypes.waiting
        if user.uid in self.__matching_list:
            self.__matching_list.remove(uid)
            logger.info(f"uid: {uid} out of matching que.. Now waiting people: {len(self.__matching_list)}")
        else:
            logger.error(f"couldn't remove uid: {uid} due not to find in matching que..")
