import time
from typing import Dict
from app.db.session import SessionLocal
from app.db.models.audit_log import AuditLog


class AuditLogService:

    @staticmethod
    def log_event(
        event_type: str,
        entity_id: str,
        actor: str,
        event_data: Dict
    ) -> None:
        db = SessionLocal()
        try:
            log = AuditLog(
                event_type=event_type,
                entity_id=entity_id,
                actor=actor,
                event_data=event_data,
                timestamp=int(time.time())
            )
            db.add(log)
            db.commit()
        except Exception as e:
            db.rollback()
            print("AUDIT LOG ERROR:", e)
            raise
        finally:
            db.close()
