from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.ws_broadcast import register_admin, unregister_admin

router = APIRouter()

@router.websocket("/ws/admin")
async def admin_ws(websocket: WebSocket):
    await register_admin(websocket)
    print("ADMIN WS CONNECTED")

    try:
        while True:
            await websocket.receive_text()  # keep alive
    except WebSocketDisconnect:
        await unregister_admin(websocket)
        print("ADMIN WS DISCONNECTED")
