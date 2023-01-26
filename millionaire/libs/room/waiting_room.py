from millionaire.libs.room.baseroom import BaseRoom, RoomType


class WaitingRoom(BaseRoom):
    """クライアントがwebsocket接続し，認証後はまずこのクラスに格納されます．
    """
    def __init__(self):
        super().__init__(RoomType.waiting)
