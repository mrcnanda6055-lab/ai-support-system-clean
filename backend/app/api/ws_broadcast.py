from app.api.ws_admin import admin_connections

async def notify_admin(message: str):
    for ws in admin_connections:
        await ws.send_text(message)
