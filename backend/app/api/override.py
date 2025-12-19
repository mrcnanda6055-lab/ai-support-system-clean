from fastapi import APIRouter
from pydantic import BaseModel

from app.services.override_service import OverrideService

router = APIRouter(prefix="/api/override", tags=["Override"])


class OverrideRequest(BaseModel):
    ticket_id: str
    new_priority: str
    new_assigned_to: str
    reason: str
    actor: str


@router.post("")
def override_ticket(payload: OverrideRequest):
    return OverrideService.override_ticket(
        ticket_id=payload.ticket_id,
        new_priority=payload.new_priority,
        new_assigned_to=payload.new_assigned_to,
        reason=payload.reason,
        actor=payload.actor
    )
