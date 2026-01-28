from fastapi import WebSocket, WebSocketDisconnect
from typing import List
from models import ChatMessage
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active_connections.remove(ws)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

async def chat_socket(ws: WebSocket):
    await manager.connect(ws)

    try:
        while True:
            data = await ws.receive_text()
            msg = ChatMessage(**json.loads(data))   # Pydantic validation
            await manager.broadcast(msg.json())

    except WebSocketDisconnect:
        manager.disconnect(ws)
