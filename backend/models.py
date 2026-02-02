from pydantic import BaseModel
from datetime import datetime

class ChatMessage(BaseModel):
    user: str
    message: str
    timestamp: str

class SystemNotification(BaseModel):
    event: str      # join / leave
    user: str
    timestamp: str
