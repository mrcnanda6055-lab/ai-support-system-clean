import time
from typing import Dict

from app.db.session import SessionLocal
from app.db.models.ticket import Ticket
from app.services.audit_log_service import AuditLogService
from app.services.ws_broadcast import notify_admin_sync


class SLAService:
    """
    PHASE 6.2 – SLA Auto Escalation
    """

    SLA_RULES: Dict[str, int] = {
        "low": 24 * 60 * 60,
        "medium": 12 * 60 * 60,
        "high": 60 * 60,
        "critical": 15 * 60,
    }

    @classmethod
    def run_sla_check(cls) -> None:
        db = SessionLocal()
        try:
            now = int(time.time())

            tickets = (
                db.query(Ticket)
                .filter(Ticket.status.in_(["open", "in_progress"]))
                .all()
            )

            for ticket in tickets:
                limit = cls.SLA_RULES.get(ticket.priority)
                if not limit:
                    continue

                if now - ticket.created_at > limit:
                    cls._escalate_ticket(db, ticket, now)

            db.commit()
        except:
            db.rollback()
            raise
        finally:
            db.close()

    @classmethod
    def _escalate_ticket(cls, db, ticket: Ticket, now: int):
        old_priority = ticket.priority

        ticket.priority = cls._next_priority(old_priority)
        ticket.status = "escalated"
        ticket.assigned_to = "HUMAN"
        ticket.updated_at = now

        AuditLogService.log_event(
            event_type="SLA_ESCALATION",
            entity_id=ticket.ticket_id,
            actor="SYSTEM",
            event_data={"reason": "SLA_BREACHED"},
        )

        # 🔔 THIS IS THE KEY LINE
        notify_admin_sync(
            f"SLA_ESCALATION 🔔 Ticket {ticket.ticket_id}"
        )

    @staticmethod
    def _next_priority(priority: str) -> str:
        order = ["low", "medium", "high", "critical"]
        return order[min(order.index(priority) + 1, 3)]
