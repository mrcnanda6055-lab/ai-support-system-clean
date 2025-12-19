import time
from typing import Dict

from app.db.session import SessionLocal
from app.db.models.ticket import Ticket
from app.services.audit_log_service import AuditLogService


class AdminActionService:

    @staticmethod
    def reassign_ticket(ticket_id: str, new_assigned_to: str, actor: str) -> Dict:
        db = SessionLocal()
        try:
            ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
            if not ticket:
                raise ValueError("Ticket not found")

            old = ticket.assigned_to
            ticket.assigned_to = new_assigned_to
            ticket.updated_at = int(time.time())
            db.commit()

            AuditLogService.log_event(
                event_type="TICKET_REASSIGNED",
                entity_id=ticket_id,
                actor=actor,
                event_data={"from": old, "to": new_assigned_to}
            )

            return {"ticket_id": ticket_id, "assigned_to": new_assigned_to}
        finally:
            db.close()

    @staticmethod
    def change_priority(ticket_id: str, new_priority: str, actor: str) -> Dict:
        db = SessionLocal()
        try:
            ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
            if not ticket:
                raise ValueError("Ticket not found")

            old = ticket.priority
            ticket.priority = new_priority
            ticket.updated_at = int(time.time())
            db.commit()

            AuditLogService.log_event(
                event_type="PRIORITY_CHANGED",
                entity_id=ticket_id,
                actor=actor,
                event_data={"from": old, "to": new_priority}
            )

            return {"ticket_id": ticket_id, "priority": new_priority}
        finally:
            db.close()

    @staticmethod
    def force_close(ticket_id: str, actor: str) -> Dict:
        db = SessionLocal()
        try:
            ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
            if not ticket:
                raise ValueError("Ticket not found")

            old = ticket.status
            ticket.status = "closed"
            ticket.updated_at = int(time.time())
            db.commit()

            AuditLogService.log_event(
                event_type="TICKET_FORCE_CLOSED",
                entity_id=ticket_id,
                actor=actor,
                event_data={"from": old, "to": "closed"}
            )

            return {"ticket_id": ticket_id, "status": "closed"}
        finally:
            db.close()
