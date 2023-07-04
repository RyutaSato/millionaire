import asyncio
import websockets
from websockets.legacy.client import WebSocketClientProtocol
import logging

logger = logging.getLogger("test_ws")
uri = "ws://127.0.0.1:8000/ws?token="


async def test_provider():
    receive_que = asyncio.Queue()
    send_que = asyncio.Queue()
    async with websockets.connect(uri) as ws:
        await asyncio.gather(receive(ws, receive_que), send(ws, send_que),
                             test_message_controller(receive_que, send_que))


async def receive(ws: WebSocketClientProtocol, que: asyncio.Queue):
    while True:
        msg = await ws.recv()
        logger.info(f"recieved: {msg}")
        await asyncio.sleep(2.0)
        await que.put(msg)


async def send(ws: WebSocketClientProtocol, que: asyncio.Queue):
    while True:
        msg = await que.get()
        await asyncio.sleep(2.0)
        await ws.send(msg)


async def test_message_controller(receive_que, send_que):
    msg = await receive_que.get()
    assert msg == "connection success"
    await send_que.put("")


if __name__ == '__main__':
    asyncio.run(test_provider())
