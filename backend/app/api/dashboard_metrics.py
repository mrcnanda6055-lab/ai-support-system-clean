from fastapi import APIRouter
from sqlalchemy import func

from app.db.session import SessionLocal
from app.db.models.ticket import Ticket

router = APIRouter()


@router.get("/dashboard/metrics")
def get_dashboard_metrics():
    db = SessionLocal()
    try:
        total = db.query(func.count(Ticket.ticket_id)).scalar()

        open_count = db.query(func.count()).filter(Ticket.status == "open").scalar()
        in_progress = db.query(func.count()).filter(Ticket.status == "in_progress").scalar()
        resolved = db.query(func.count()).filter(Ticket.status == "resolved").scalar()
        escalated = db.query(func.count()).filter(Ticket.status == "escalated").scalar()

        ai_handled = db.query(func.count()).filter(Ticket.assigned_to == "AI").scalar()
        human_handled = db.query(func.count()).filter(Ticket.assigned_to == "HUMAN").scalar()

        ai_percent = round((ai_handled / total) * 100, 2) if total else 0
        human_percent = round((human_handled / total) * 100, 2) if total else 0

        # Avg resolution time (only resolved tickets)
        avg_resolution = (
            db.query(func.avg(Ticket.updated_at - Ticket.created_at))
            .filter(Ticket.status == "resolved")
            .scalar()
        )

        return {
            "total_tickets": total,
            "open": open_count,
            "in_progress": in_progress,
            "resolved": resolved,
            "escalated": escalated,
            "ai_handled_percent": ai_percent,
            "human_handled_percent": human_percent,
            "avg_resolution_seconds": int(avg_resolution) if avg_resolution else 0
        }

    finally:
        db.close()
