from sqlalchemy import Column, String, Integer, JSON
from app.db.base import Base


class DecisionLog(Base):
    __tablename__ = "decision_logs"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, index=True)
    final_priority = Column(String)
    final_assignment = Column(String)
    decision_reasons = Column(JSON)
    created_at = Column(Integer)
