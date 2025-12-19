from fastapi import APIRouter, HTTPException
from app.services.ticket_service import TicketService

router = APIRouter()
ticket_service = TicketService()


@router.post("/tickets/{ticket_id}/resolve")
def resolve_ticket(ticket_id: str):
    try:
        return ticket_service.update_status(
            ticket_id=ticket_id,
            new_status="resolved",
            actor="agent"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tickets/{ticket_id}/close")
def close_ticket(ticket_id: str):
    try:
        return ticket_service.update_status(
            ticket_id=ticket_id,
            new_status="closed",
            actor="agent"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
