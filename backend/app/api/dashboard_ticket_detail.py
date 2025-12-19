from fastapi import APIRouter, HTTPException
from app.db.session import SessionLocal
from app.db.models.ticket import Ticket
from app.db.models.decision_log import DecisionLog
from app.db.models.audit_log import AuditLog

router = APIRouter()


@router.get("/dashboard/tickets/{ticket_id}")
def get_ticket_detail(ticket_id: str):
    db = SessionLocal()
    try:
        ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        decision_logs = (
            db.query(DecisionLog)
            .filter(DecisionLog.ticket_id == ticket_id)
            .order_by(DecisionLog.created_at.asc())
            .all()
        )

        audit_logs = (
            db.query(AuditLog)
            .filter(AuditLog.entity_id == ticket_id)
            .order_by(AuditLog.timestamp.asc())
            .all()
        )

        return {
            "ticket": {
                "ticket_id": ticket.ticket_id,
                "user_id": ticket.user_id,
                "channel": ticket.channel,
                "intent": ticket.intent,
                "sentiment": ticket.sentiment,
                "priority": ticket.priority,
                "status": ticket.status,
                "assigned_to": ticket.assigned_to,
                "created_at": ticket.created_at,
                "updated_at": ticket.updated_at,
            },
            "decision_logs": [
                {
                    "final_priority": d.final_priority,
                    "final_assignment": d.final_assignment,
                    "decision_reasons": d.decision_reasons,
                    "created_at": d.created_at,
                }
                for d in decision_logs
            ],
            "audit_logs": [
                {
                    "event_type": a.event_type,
                    "actor": a.actor,
                    "event_data": a.event_data,
                    "timestamp": a.timestamp,
                }
                for a in audit_logs
            ],
        }
    finally:
        db.close()
