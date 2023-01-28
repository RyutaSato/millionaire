from enum import StrEnum, auto


class MsgTypes(StrEnum):
    none = auto()  # for test or debug
    room = auto()
    in_play = auto()
    out_play = auto()

class StatusTypes(StrEnum):
    waiting = auto()
    matching = auto()
    playing = auto()

class RoomCmdTypes(StrEnum):
    ch_room = auto()
    mk_room = auto()

