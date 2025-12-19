import asyncio
from typing import Set
from fastapi import WebSocket

admin_connections: Set[WebSocket] = set()


async def register_admin(ws: WebSocket):
    await ws.accept()
    admin_connections.add(ws)


async def unregister_admin(ws: WebSocket):
    admin_connections.discard(ws)


async def notify_admin(message: str):
    dead = []
    for ws in admin_connections:
        try:
            await ws.send_text(message)
        except:
            dead.append(ws)

    for ws in dead:
        admin_connections.discard(ws)


def notify_admin_sync(message: str):
    """
    SAFE function for background threads
    """
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(notify_admin(message))
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(notify_admin(message))
