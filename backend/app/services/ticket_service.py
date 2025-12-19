import time
import uuid
from typing import Dict, Literal

from app.db.session import SessionLocal
from app.db.models.ticket import Ticket
from app.services.decision_log_service import DecisionLogService
from app.services.audit_log_service import AuditLogService


TicketStatus = Literal[
    "open",
    "in_progress",
    "escalated",
    "resolved",
    "closed"
]

TicketPriority = Literal[
    "low",
    "medium",
    "high",
    "critical"
]


class TicketService:
    """
    PHASE 4
    4.2.x Ticket + Decision Logs
    4.3   Resolve / Close + Audit Logs
    """

    # =========================
    # CREATE FROM AI
    # =========================
    def create_ticket_from_ai(
        self,
        user_id: str,
        channel: Literal["web", "whatsapp", "email"],
        ai_output: Dict
    ) -> Dict:

        intent = ai_output.get("intent", "unknown")
        sentiment = ai_output.get("sentiment", "calm")
        confidence = float(ai_output.get("confidence", 0))

        priority = self._decide_priority(intent, sentiment)
        assigned_to = self._decide_assignee(priority, confidence)
        status = self._initial_status(assigned_to)

        now = int(time.time())

        ticket_data = {
            "ticket_id": self._generate_ticket_id(),
            "user_id": user_id,
            "channel": channel,
            "intent": intent,
            "sentiment": sentiment,
            "ai_confidence": int(confidence * 100),
            "priority": priority,
            "status": status,
            "assigned_to": assigned_to,
            "created_at": now,
            "updated_at": now
        }

        # Save ticket
        self._save_ticket_to_db(ticket_data)

        # Decision log
        DecisionLogService.log_decision(
            ticket_id=ticket_data["ticket_id"],
            final_priority=priority,
            final_assignment=assigned_to,
            reasons={
                "intent": intent,
                "sentiment": sentiment,
                "ai_confidence": confidence,
                "rules_applied": [
                    "payment/refund → high",
                    "angry → critical",
                    "confidence < 0.75 → human"
                ]
            }
        )

        return ticket_data

    # =========================
    # UPDATE STATUS (RESOLVE / CLOSE)
    # =========================
    def update_status(
        self,
        ticket_id: str,
        new_status: TicketStatus,
        actor: str
    ) -> Dict:

        db = SessionLocal()
        try:
            ticket = (
                db.query(Ticket)
                .filter(Ticket.ticket_id == ticket_id)
                .first()
            )

            if not ticket:
                raise ValueError("Ticket not found")

            old_status = ticket.status
            ticket.status = new_status
            ticket.updated_at = int(time.time())

            db.commit()  # ✅ STATUS UPDATE COMMIT

            # ✅ AUDIT LOG (THIS WAS MISSING / NOT FIRING EARLIER)
            AuditLogService.log_event(
                event_type="TICKET_STATUS_UPDATED",
                entity_id=ticket_id,
                actor=actor,
                event_data={
                    "from": old_status,
                    "to": new_status
                }
            )

            return {
                "ticket_id": ticket_id,
                "old_status": old_status,
                "new_status": new_status
            }

        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    # =========================
    # DB SAVE
    # =========================
    def _save_ticket_to_db(self, ticket_data: Dict) -> None:
        db = SessionLocal()
        try:
            db.add(Ticket(**ticket_data))
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    # =========================
    # RULES
    # =========================
    def _decide_priority(self, intent: str, sentiment: str) -> TicketPriority:
        intent = intent.lower()
        sentiment = sentiment.lower()

        if "payment" in intent or "refund" in intent:
            return "high"
        if sentiment == "angry":
            return "critical"
        if "login" in intent or "password" in intent:
            return "medium"
        return "low"

    def _decide_assignee(
        self,
        priority: TicketPriority,
        confidence: float
    ) -> Literal["AI", "HUMAN"]:
        if priority == "critical" or confidence < 0.75:
            return "HUMAN"
        return "AI"

    def _initial_status(
        self,
        assigned_to: Literal["AI", "HUMAN"]
    ) -> TicketStatus:
        return "in_progress" if assigned_to == "AI" else "escalated"

    def _generate_ticket_id(self) -> str:
        return f"TKT-{uuid.uuid4().hex[:10].upper()}"
