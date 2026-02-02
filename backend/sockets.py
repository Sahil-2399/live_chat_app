from fastapi import WebSocket, WebSocketDisconnect
from typing import List
from models import ChatMessage, SystemNotification
from datetime import datetime
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.active_connections:
            self.active_connections.remove(ws)

    async def broadcast(self, payload: dict):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(payload))

manager = ConnectionManager()

async def chat_socket(ws: WebSocket):
    await manager.connect(ws)

    username = None

    try:
        while True:
            data = json.loads(await ws.receive_text())

            # First message is treated as join event
            if data.get("type") == "join":
                username = data["user"]
                notification = SystemNotification(
                    event="join",
                    user=username,
                    timestamp=datetime.now().strftime("%H:%M:%S")
                )
                await manager.broadcast({
                    "type": "notification",
                    **notification.dict()
                })
                continue

            # Chat message
            msg = ChatMessage(
                user=data["user"],
                message=data["message"],
                timestamp=datetime.now().strftime("%H:%M:%S")
            )

            await manager.broadcast({
                "type": "message",
                **msg.dict()
            })

    except WebSocketDisconnect:
        manager.disconnect(ws)

        if username:
            notification = SystemNotification(
                event="leave",
                user=username,
                timestamp=datetime.now().strftime("%H:%M:%S")
            )
            await manager.broadcast({
                "type": "notification",
                **notification.dict()
            })
