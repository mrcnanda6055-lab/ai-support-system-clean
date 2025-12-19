from fastapi import APIRouter, Query
from typing import Optional, List

from app.db.session import SessionLocal
from app.db.models.ticket import Ticket

router = APIRouter()


@router.get("/dashboard/tickets")
def list_tickets(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    assigned_to: Optional[str] = Query(None)
):
    """
    PHASE 6.1
    Dashboard Tickets API (READ ONLY)
    """

    db = SessionLocal()
    try:
        query = db.query(Ticket)

        if status:
            query = query.filter(Ticket.status == status)

        if priority:
            query = query.filter(Ticket.priority == priority)

        if assigned_to:
            query = query.filter(Ticket.assigned_to == assigned_to)

        tickets = query.order_by(Ticket.created_at.desc()).all()

        return {
            "count": len(tickets),
            "tickets": [
                {
                    "ticket_id": t.ticket_id,
                    "user_id": t.user_id,
                    "channel": t.channel,
                    "intent": t.intent,
                    "sentiment": t.sentiment,
                    "priority": t.priority,
                    "status": t.status,
                    "assigned_to": t.assigned_to,
                    "created_at": t.created_at,
                    "updated_at": t.updated_at,
                }
                for t in tickets
            ]
        }
    finally:
        db.close()
