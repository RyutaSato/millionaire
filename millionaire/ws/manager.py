from starlette.websockets import WebSocket
from asyncio import CancelledError, Task, Future, Event, create_task

from websockets.exceptions import ConnectionClosed
from logging import getLogger
logger = getLogger(__name__)

def conn_watcher(func):
    async def _conn_watcher(*args, **kwargs):
        try:
            await func(*args, **kwargs)
        except ConnectionClosed:
            logger.debug("Connection was closed.")
        except CancelledError:
            logger.debug("task was cancelled.")

    return _conn_watcher

class ClientManager:
    def __init__(self, _ws: WebSocket):
        self.__ws = _ws
        self.tasks = {create_task(self.receive()), create_task(self.send())}

    @conn_watcher
    async def receive(self):
        pass

    @conn_watcher
    async def send(self):
        pass


