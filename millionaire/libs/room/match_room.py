import asyncio
from uuid import UUID

from millionaire.libs.match.play import Play
from millionaire.libs.room.baseroom import BaseRoom, RoomType
from millionaire.schemas.message import Message
import logging

logger = logging.getLogger(__name__)


class MatchRoom(BaseRoom):
    def __init__(self, room_manager, uids: list[UUID]):
        logger.info(f"match initialize...")
        super().__init__(RoomType.match, room_manager)
        for uid in uids:
            self.__manager.move_user(uid, self.room_id)
        self.__play = Play.from_user_manager(users=list(self.__roommates.values()))
        self.play_task = asyncio.create_task(self.init_play())
        # TODO: 試合終了後のコールバックを書く

    def msg_analyser(self, msg: Message):
        if not msg.msg_type != msg.msg_type.in_play:
            logger.critical(f"msg_analyser got invalid type message {msg.msg_type}")
            return


    async def init_play(self):
        # TODO: match ライブラリと連携する
        pass
