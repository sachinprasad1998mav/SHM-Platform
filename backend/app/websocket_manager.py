from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self):
        # Store all active websocket connections
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        # Send the message to every connected client
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()
