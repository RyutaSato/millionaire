from uuid import UUID

from millionaire.schemas.msg_types import StatusTypes


class UserManager:
    def __init__(self, uid, status):
        self.uid: UUID = uid
        self._status: StatusTypes = status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
