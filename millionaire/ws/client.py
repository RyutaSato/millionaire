import asyncio
import typing

from fastapi import Depends, HTTPException
from starlette import status
from starlette.websockets import WebSocket, WebSocketDisconnect
from logging import getLogger

from millionaire.ws.auth import authenticator

logger = getLogger(__name__)


class WebSocketClient:
    def __init__(self, ws: WebSocket, is_authed: bool = Depends(authenticator)):
        logger.info(f"access: {ws.client.port} token: {is_authed}")
        if not is_authed:
            logger.info(f"cookie: {ws.cookies}")
            raise HTTPException(status_code=status.WS_1008_POLICY_VIOLATION)
        self.__ws = ws
        self.__in_msg_que = asyncio.Queue()
        self.__out_msg_que = asyncio.Queue()

    def __await__(self) -> typing.Generator:
        return self.dispatch().__await__()

    async def dispatch(self) -> None:
        # Websocket lifecycle
        await self.__on_connect()

        close_code: int = status.WS_1000_NORMAL_CLOSURE
        try:
            async with asyncio.TaskGroups() as tg:
                task_in_que: asyncio.Task = tg.create_task(self.__in())
                task_out_que: asyncio.Task = tg.create_task(self.__out())
                tasks = [task_out_que, task_in_que]
        except* WebSocketDisconnect:
            pass
            # Handle client normal disconnect here

        except* Exception as exc:
            # Handle other types of errors here
            close_code = status.WS_1011_INTERNAL_ERROR
            raise exc from None
        finally:
            await self.__on_disconnect(close_code)
            for task in tasks:
                if task.done() is False:
                    task.cancel()
        # try:
        #     while True:
        #         data = await self.__ws.receive_text()
        #         await self._on_receive(data)

    async def __on_connect(self):
        # Handle your new connection here
        await self.__ws.accept()
        logger.info(f"connect: client: {self.__ws.client.port}")
        await self.__ws.send_text("connection success")

    async def __on_disconnect(self, close_code: int):
        # Handle client disconnect here
        logger.info(f"disconnect: client: {self.__ws.client.port}")

    async def _on_receive(self, msg: str):
        logger.info(f"receive: {self.__ws.client.port}: {msg}")
        await self.__ws.send_text(f"received: {msg}")

    async def send(self, msg):
        await self.__out_msg_que.put(msg)

    async def __out(self):
        while True:
            msg = await self.__out_msg_que.get()
            await self.__ws.send_text(msg)

    async def __in(self):
        while True:
            msg = await self.__ws.receive_text()
            logger.info(f"receive: {self.__ws.client.port}: {msg}")
            await self.__in_msg_que.put(msg)
            # for debug
            await self.__out_msg_que.put(msg)
