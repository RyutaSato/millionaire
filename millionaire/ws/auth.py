from starlette.websockets import WebSocket


def authenticator(websocket: WebSocket):
    token = websocket.cookies.get("token")
    # CRITICAL ERROR: websocket通信では一般のhttpおよびhttps通信でやり取りされるCookieを同一オリジンであっても取得できません．
    # したがってこの認証方法は使用できません．別の方法を考える必要があります．
    # TODO:データベースと認証
    return True