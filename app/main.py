from fastapi import FastAPI, Body
from starlette.websockets import WebSocket
import syslog

app = FastAPI()

# websocketで接続中のクライアントを識別するためのIDを格納
clients = {}

@app.get("/")
def read():
    return {"Result": "ok"}

@app.post("/")
async def post(body=Body(...)):

    # 緊急地震速報がなりすぎると緊急性が失われるので震度3以上の地震のみ通知をするようにする
    if body["type"] == "eew" and body["report"] == "1" and int(body["intensity"]) >= 3:
        for client in clients.values():
            await client.send_text("{}".format(body))
        syslog.syslog(syslog.LOG_INFO, 'SentAlert:{}'.format(body))

    # 緊急地震速報以外はキャンセル扱いのだが送信をしてクライアント側で処理する
    elif body["type"] == "pga_alert_cancel":
        for client in clients.values():
            await client.send_text("{}".format(body))
        syslog.syslog(syslog.LOG_DEBUG, 'SentCancelAlert:{}'.format(body))
    else:
        syslog.syslog(syslog.LOG_DEBUG, 'NotSentAlert:{}'.format(body))

    return {"Result": "ok", "Body": body}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    # クライアントを識別するためのIDを取得
    key = ws.headers.get('sec-websocket-key')
    clients[key] = ws

    # TODO debuglog
    syslog.syslog(syslog.LOG_DEBUG, 'ConnectedClientList:{}'.format(clients))

    try:
        while True:
            data = await ws.receive_text()
    except Exception as e:
        syslog.syslog(syslog.LOG_DEBUG, '{}:{}'.format(type(e),e))
        # TODO close状態で下記のコネクションクローズするとさらにRuntimeError出るのでコメントアウト中
        #await ws.close()
        del clients[key]

