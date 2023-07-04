from datetime import datetime
from uuid import UUID

from millionaire.libs.match.player import Player


class History:
    def __init__(self, *args, **kwargs):
        play_id: UUID = kwargs["play_id"]
        created_at: datetime = kwargs["created_at"]
        users: list[Player] = kwargs["users"]
