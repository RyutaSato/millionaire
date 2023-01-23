from fastapi import Cookie, Depends, FastAPI, Header, Query, Response, Request
from starlette import status
from starlette.exceptions import WebSocketException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, FileResponse, RedirectResponse, JSONResponse
from starlette.websockets import WebSocket
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
    "http://127.0.0.1"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", )
async def get(request: Request):
    logger.info(f"accessed: ip: {request.client.host}, port:{request.client.port}")
    response = FileResponse(path="millionaire/static/index.html",
                        headers={"token": "01835c3a-fb3d-b4e2-a43e-1682dc0be131",
                                 "Access-Control-Allow-Origin": "http://127.0.0.1:8000"})
    return response


@app.get("/get_token")
def get_token(request: Request, session: str = Header(default=None)):
    print(request.cookies)
    response = JSONResponse({"token": "01835c3a-fb3d-b4e2-a43e-1682dc0be131"})
    response.set_cookie("key2", "value2", )  # TODO: replace set_cookie with token
    return response

# example of dependency
async def get_cookie_or_token(
        websocket: WebSocket,
        session: str | None = Cookie(default=None),
        token: str | None = Query(default=None),
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@app.websocket("/ws")
async def websocket_endpoint(
        websocket: WebSocket,
        # cookie_or_token: str = Depends(get_cookie_or_token),
        ):
    """
    Notes:
        type: websocket
        asgi: {'version': '3.0', 'spec_version': '2.3'}
        http_version: 1.1
        scheme: ws
        server: ('127.0.0.1', 8000)
        client: ('127.0.0.1', 56726)
        root_path:
        path: /items/foo/ws
        raw_path: b'/items/foo/ws'
        query_string: b'token=some-key-token'
        headers: [(b'host', b'localhost:8000'), (b'connection', b'Upgrade'), (b'pragma', b'no-cache'), (b'cache-control', b'no-cache'), (b'user-agent', b'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'), (b'upgrade', b'websocket'), (b'origin', b'http://127.0.0.1:8000'), (b'sec-websocket-version', b'13'), (b'accept-encoding', b'gzip, deflate, br'), (b'accept-language', b'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7'), (b'sec-websocket-key', b'ykXbV8Qyjon5w9/L0SD8ng=='), (b'sec-websocket-extensions', b'permessage-deflate; client_max_window_bits')]
        subprotocols: []
        app: <fastapi.applications.FastAPI object at 0x00000200183D2D90>
        fastapi_astack: <contextlib.AsyncExitStack object at 0x0000020018EA8C50>
        router: <fastapi.routing.APIRouter object at 0x00000200183D2C10>
        endpoint: <function websocket_endpoint at 0x0000020018E900E0>
        path_params: {'item_id': 'foo'}
        route: APIWebSocketRoute(path='/items/{item_id}/ws', name='websocket_endpoint')
    Args:
        websocket:
        item_id:
        q:
        cookie_or_token:

    Returns:

    """
    # TODO: websocket.cookies authentication
    await websocket.accept()
    await websocket.send_text("connection succeed")
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
