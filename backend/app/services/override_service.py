import time
from typing import Dict

from app.db.session import SessionLocal
from app.db.models.ticket import Ticket
from app.services.decision_log_service import DecisionLogService
from app.services.audit_log_service import AuditLogService


class OverrideService:

    @staticmethod
    def override_ticket(
        ticket_id: str,
        new_priority: str,
        new_assigned_to: str,
        reason: str,
        actor: str
    ) -> Dict:

        db = SessionLocal()
        try:
            ticket = db.query(Ticket).filter(
                Ticket.ticket_id == ticket_id
            ).first()

            if not ticket:
                raise ValueError("Ticket not found")

            old_state = {
                "priority": ticket.priority,
                "assigned_to": ticket.assigned_to,
                "status": ticket.status
            }

            # Apply override
            ticket.priority = new_priority
            ticket.assigned_to = new_assigned_to
            ticket.status = "escalated"
            ticket.updated_at = int(time.time())

            db.commit()

            # Decision log
            DecisionLogService.log_decision(
                ticket_id=ticket_id,
                final_priority=new_priority,
                final_assignment=new_assigned_to,
                reasons={
                    "override": True,
                    "reason": reason
                }
            )

            # Audit log
            AuditLogService.log_event(
                event_type="TICKET_OVERRIDE",
                entity_id=ticket_id,
                actor=actor,
                event_data={
                    "from": old_state,
                    "to": {
                        "priority": new_priority,
                        "assigned_to": new_assigned_to,
                        "status": "escalated"
                    },
                    "reason": reason
                }
            )

            return {
                "ticket_id": ticket_id,
                "status": "overridden"
            }

        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
