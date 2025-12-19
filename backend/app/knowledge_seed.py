from app.services.knowledge_service import load_knowledge

docs = [
    "Payments may fail due to bank downtime. Auto-reversal usually completes within 24 hours.",
    "Password resets require email verification. Links expire in 15 minutes.",
    "Duplicate charges are flagged automatically and refunded within 3–5 business days.",
    "For high-risk issues, escalate immediately to a human operator."
]

def seed():
    load_knowledge(docs)
