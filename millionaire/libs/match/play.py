from uuid import UUID
from datetime import datetime
from ulid import ULID

from millionaire.libs.match.cards import Cards
from millionaire.libs.match.player import Player
from millionaire.libs.match.settings import Settings
from millionaire.libs.room.user import UserManager
from millionaire.models.history import History
from millionaire.schemas.message import OutPlayMessage
from millionaire.schemas.msg_types import PlayMsgTypes


class Play:
    """このクラスは，ゲーム進行のメインプログラムです．
    このクラスでは，ゲーム進行に必要なメソッドを全て持ちますが，実行タイミングは，MatchRoomに一任されています．
    """
    def __init__(self, players: list[Player], settings: Settings):
        self.cards = Cards()
        self.play_id: UUID = ULID().to_uuid()
        self.created_at: datetime = datetime.now()
        self.players: dict[UUID, Player] = {player.uid: player for player in players}
        self.settings = settings

    def to_models(self):
        return History(
            id=self.play_id,
            created_at=self.created_at,
            users=[player.uid for player in self.players.values()]
        )

    @classmethod
    def from_user_manager(cls, users: list[UserManager]):
        players = [Player(uid=user.uid, name=user.name) for user in users]
        settings = Settings()
        return cls(players, settings)

    def distribute_cards(self):
        cards_set: tuple = Cards.create_cards(player_num=len(self.players))
        uids = list(self.players.keys())
        for i, cards in enumerate(cards_set):
            for card in cards:
                self.players[uids[i]].cards += card

    def snapshot_my_cards(self, uid: UUID) -> OutPlayMessage:
        return OutPlayMessage(
            msg_type='out_play',
            play_type=PlayMsgTypes.my_cards,
            cards=self.players[uid].cards.to_list_str()
        )


if __name__ == '__main__':
    uids = [ULID().to_uuid() for _ in range(4)]
    play = Play(
        players=[Player(uid=uids[i], name=f'player{i}') for i in range(4)],
        settings=Settings()
    )
    play.distribute_cards()
    print(play.snapshot_my_cards(uid=uids[1]).json())
