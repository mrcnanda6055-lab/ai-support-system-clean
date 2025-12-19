from sqlalchemy import Column, String, Integer
from app.db.base import Base


class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    channel = Column(String)
    intent = Column(String)
    sentiment = Column(String)
    ai_confidence = Column(Integer)
    priority = Column(String)
    status = Column(String)
    assigned_to = Column(String)
    created_at = Column(Integer)
    updated_at = Column(Integer)
