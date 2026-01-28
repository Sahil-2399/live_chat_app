from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from sockets import chat_socket
import os

app = FastAPI(title="Live Chat App")

@app.websocket("/ws/chat")
async def websocket_endpoint(ws: WebSocket):
    await chat_socket(ws)

@app.get("/")
def home():
    return {"status": "Chat backend running"}

@app.get("/chat", response_class=HTMLResponse)
def chat_ui():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "frontend", "index.html")

    if not os.path.exists(file_path):
        return HTMLResponse(f"Frontend file not found at {file_path}", status_code=500)

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
