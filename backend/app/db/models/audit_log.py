from sqlalchemy import Column, Integer, String, JSON
from app.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    actor = Column(String, nullable=False)
    event_data = Column(JSON)
    timestamp = Column(Integer, nullable=False)
