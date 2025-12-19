from fastapi import APIRouter
from pydantic import BaseModel

from app.services.admin_action_service import AdminActionService

router = APIRouter(prefix="/api/admin", tags=["Admin Actions"])


class ReassignRequest(BaseModel):
    ticket_id: str
    new_assigned_to: str
    actor: str


class PriorityRequest(BaseModel):
    ticket_id: str
    new_priority: str
    actor: str


class ForceCloseRequest(BaseModel):
    ticket_id: str
    actor: str


@router.post("/reassign")
def reassign_ticket(payload: ReassignRequest):
    return AdminActionService.reassign_ticket(
        payload.ticket_id,
        payload.new_assigned_to,
        payload.actor
    )


@router.post("/change-priority")
def change_priority(payload: PriorityRequest):
    return AdminActionService.change_priority(
        payload.ticket_id,
        payload.new_priority,
        payload.actor
    )


@router.post("/force-close")
def force_close(payload: ForceCloseRequest):
    return AdminActionService.force_close(
        payload.ticket_id,
        payload.actor
    )
