# FastAPI WebSockets Demo

import asyncio
import random
from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

app = FastAPI()


class WsMessage(BaseModel):
    message: str
    code: int
    user_id: int


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    def __enter__(self):
        self.__init__()
        return self

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_str_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_json_message(self, data: dict, websocket: WebSocket):
        await websocket.send_json(data)

    async def send(self, websocket: WebSocket, message: WsMessage):
        await websocket.send_json(message.model_dump())

    async def broadcast_str(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def broadcast_json(self, data: dict):
        for connection in self.active_connections:
            await connection.send_json(data)

    async def broadcast(self, message: WsMessage):
        for connection in self.active_connections:
            await connection.send_json(message.model_dump())

    def __exit__(self, exc_type, exc_value, traceback):
        for connection in self.active_connections:
            try:
                asyncio.create_task(connection.close())
            except Exception as e:
                print(f"Error closing connection: {e}")


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data.lower() == "bye~~":
                await manager.send_str_message("bye~~", websocket)
                manager.disconnect(websocket)
                break
            print(f"[Server] Received from Client #{client_id}: {data}")
            await manager.send_str_message(f"You wrote: {data}", websocket)
            await manager.send_json_message(
                {"message": f"You wrote: {data}"}, websocket
            )
            await manager.send(
                websocket,
                WsMessage(
                    message=f"Hello Client #{client_id}, you sent: {data}",
                    code=200,
                    user_id=client_id,
                ),
            )
            await manager.send(
                websocket,
                WsMessage(
                    message=f"seed : {random.randint(1000,9999)}",
                    code=200,
                    user_id=client_id,
                ),
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(
            WsMessage(
                message=f"Client #{client_id} disconnected",
                code=1001,
                user_id=client_id,
            )
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )
