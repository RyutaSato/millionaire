from uuid import UUID
from datetime import datetime
from ulid import ULID

from millionaire.libs.match.cards import Cards
from millionaire.libs.match.player import Player
from millionaire.libs.match.settings import Settings
from millionaire.models.history import History


class Play:
    def __init__(self, players: list[Player], settings: Settings):
        self.cards = Cards()
        self.play_id: UUID = ULID().to_uuid()
        self.created_at: datetime = datetime.now()
        self.players = players
        self.settings = settings

    def to_models(self):
        return History(
            id=self.play_id,
            created_at=self.created_at,
            users=[player.uid for player in self.players]
        )


if __name__ == '__main__':
    pass
