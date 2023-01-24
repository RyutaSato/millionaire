from fastapi import Cookie, Depends, FastAPI, Header, Query, Response, Request
from starlette import status
from starlette.exceptions import WebSocketException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, FileResponse, RedirectResponse, JSONResponse
from starlette.websockets import WebSocket
import logging

from millionaire.ws.client import WebSocketClient

logging.basicConfig(level=logging.INFO)
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
    response.set_cookie("token", "01835c3a-fb3d-b4e2-a43e-1682dc0be131", )  # TODO: replace set_cookie with token
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

app.add_api_websocket_route("/ws", WebSocketClient)
