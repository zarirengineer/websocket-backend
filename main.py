from fastapi import FastAPI, WebSocket
from typing import List

app = FastAPI()

active_connections: List[WebSocket] = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received: {data}")
            # Broadcast data to all clients
            for conn in active_connections:
                await conn.send_text(f"Message: {data}")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        active_connections.remove(websocket)
