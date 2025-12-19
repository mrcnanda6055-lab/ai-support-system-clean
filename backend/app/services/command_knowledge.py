RULES = [
    {
        "keywords": ["payment", "debited", "failed"],
        "response": (
            "STATUS: IDENTIFIED\n"
            "ISSUE TYPE: PAYMENT FAILURE\n"
            "ACTION: AUTO-REVERSAL IN PROGRESS\n"
            "ETA: WITHIN 24 HOURS\n"
            "NOTE: NO MANUAL ACTION REQUIRED"
        ),
        "confidence": 0.9,
        "escalate": False
    },
    {
        "keywords": ["password", "login", "reset"],
        "response": (
            "STATUS: IDENTIFIED\n"
            "ISSUE TYPE: AUTHENTICATION\n"
            "ACTION: PASSWORD RESET REQUIRED\n"
            "NOTE: RESET LINK SENT TO REGISTERED EMAIL"
        ),
        "confidence": 0.85,
        "escalate": False
    },
    {
        "keywords": ["agent", "human", "call", "support"],
        "response": (
            "STATUS: ESCALATED\n"
            "RISK LEVEL: HIGH\n"
            "ACTION: HUMAN OPERATOR ASSIGNED"
        ),
        "confidence": 0.4,
        "escalate": True
    }
]

def match_command_knowledge(message: str):
    msg = message.lower()
    for rule in RULES:
        if any(k in msg for k in rule["keywords"]):
            return rule
    return None
