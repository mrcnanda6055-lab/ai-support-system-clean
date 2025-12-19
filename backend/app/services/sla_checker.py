import time
import asyncio

from app.db.session import SessionLocal
from app.db.models.ticket import Ticket
from app.services.audit_log_service import AuditLogService
from app.services.ws_broadcast import notify_admin


SLA_SECONDS = 3600  # 1 hour SLA


def run_sla_check():
    """
    This function:
    1. Finds old OPEN tickets
    2. Escalates them
    3. Writes audit log
    4. Sends WebSocket alert to ADMIN
    """

    db = SessionLocal()
    try:
        now = int(time.time())

        tickets = db.query(Ticket).filter(
            Ticket.status == "open"
        ).all()

        for ticket in tickets:
            age = now - ticket.created_at

            if age >= SLA_SECONDS:
                # 🔥 ESCALATE TICKET
                ticket.status = "escalated"
                ticket.assigned_to = "HUMAN"
                ticket.updated_at = now
                db.commit()

                # 🔥 AUDIT LOG
                AuditLogService.log_event(
                    event_type="SLA_ESCALATION",
                    entity_id=ticket.ticket_id,
                    actor="SYSTEM",
                    event_data={
                        "reason": "SLA breach",
                        "age_seconds": age
                    }
                )

                # 🔥 WEBSOCKET MESSAGE (THIS IS STEP 9.4)
                asyncio.create_task(
                    notify_admin(
                        f"SLA_ESCALATION 🔥 Ticket {ticket.ticket_id}"
                    )
                )

    finally:
        db.close()
