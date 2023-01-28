from millionaire.libs.room.baseroom import BaseRoom, RoomType
from millionaire.schemas.message import Message, RoomMessage
import logging

from millionaire.schemas.msg_types import StatusTypes

logger = logging.getLogger(__name__)

class WaitingRoom(BaseRoom):
    """クライアントがwebsocket接続し，認証後はまずこのクラスに格納されます．
    """

    def __init__(self):
        super().__init__(RoomType.waiting)

    def msg_analyser(self, msg: Message):
        if not isinstance(msg.msg, RoomMessage):
            logger.error(f"msg is invalid type {type(msg.msg)}")
            return
        if msg.msg.status == StatusTypes.matching:
            player = self._roommates.get(msg.uid)
            if player is None:
                logger.critical(f"can't find uid {msg.uid} in waiting room "
                                f"msg {msg.json()}")
                return
            player.status = msg.msg.status




