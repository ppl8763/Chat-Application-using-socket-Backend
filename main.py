import socketio
from fastapi import FastAPI

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://z1vmgmts-5173.inc1.devtunnels.ms" ,
        "https://chat-application-using-socket-frontend.onrender.com"
    ]
)


app = FastAPI()
socket_app = socketio.ASGIApp(
    sio,
    other_asgi_app=app,
    socketio_path="socket.io"
)

users = {}

@sio.event
async def connect(sid, environ):
    print("✅ Connected:", sid)

@sio.event
async def join(sid, username):
    users[sid] = username
    await sio.emit("users", list(users.values()))

@sio.event
async def chat_message(sid, msg):
    await sio.emit(
        "chat_message",
        {
            "user": users.get(sid),
            "message": msg
        }
    )

@sio.event
async def disconnect(sid):
    users.pop(sid, None)
    await sio.emit("users", list(users.values()))
    print("❌ Disconnected:", sid)

@app.get("/health")
async def root():
    return {"status": "ok"}
