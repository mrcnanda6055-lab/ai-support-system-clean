import time
from typing import Dict

from app.db.session import SessionLocal
from app.db.models.decision_log import DecisionLog


class DecisionLogService:
    """
    STEP 4.2.2
    Stores FINAL CORE decisions for audit & compliance
    """

    @staticmethod
    def log_decision(
        ticket_id: str,
        final_priority: str,
        final_assignment: str,
        reasons: Dict
    ) -> None:

        db = SessionLocal()
        try:
            log = DecisionLog(
                ticket_id=ticket_id,
                final_priority=final_priority,
                final_assignment=final_assignment,
                decision_reasons=reasons,
                created_at=int(time.time())
            )
            db.add(log)
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
