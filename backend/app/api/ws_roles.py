from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

# =========================
# CONNECTION REGISTRY
# =========================
admin_connections: list[WebSocket] = []
agent_connections: dict[str, list[WebSocket]] = {}


# =========================
# ADMIN WEBSOCKET
# =========================
@router.websocket("/ws/admin")
async def admin_ws(websocket: WebSocket):
    await websocket.accept()
    admin_connections.append(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        admin_connections.remove(websocket)


# =========================
# AGENT WEBSOCKET
# =========================
@router.websocket("/ws/agent/{agent_id}")
async def agent_ws(websocket: WebSocket, agent_id: str):
    await websocket.accept()

    if agent_id not in agent_connections:
        agent_connections[agent_id] = []

    agent_connections[agent_id].append(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        agent_connections[agent_id].remove(websocket)
