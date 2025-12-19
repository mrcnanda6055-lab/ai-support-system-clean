from app.db.session import engine
from app.db.base import Base

from app.db.models.ticket import Ticket
from app.db.models.decision_log import DecisionLog
from app.db.models.audit_log import AuditLog

Base.metadata.create_all(bind=engine)
print("✅ Tables created")
