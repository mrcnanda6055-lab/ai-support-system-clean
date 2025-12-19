from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Core Decision Engine")

class Query(BaseModel):
    message: str

@app.post("/decide")
def decide(query: Query):
    msg = query.message.lower()

    # PAYMENT ISSUE (robust match)
    if (
        "payment" in msg
        or "amount" in msg
        or "debited" in msg
        or "failed" in msg
    ):
        return {
            "status": "IDENTIFIED",
            "issue": "PAYMENT FAILURE",
            "action": "AUTO REVERSAL IN 24 HOURS"
        }

    # HUMAN / AGENT REQUEST
    if "human" in msg or "agent" in msg:
        return {
            "status": "ESCALATED",
            "action": "HUMAN OPERATOR ASSIGNED"
        }

    # DEFAULT
    return {
        "status": "UNKNOWN",
        "action": "MANUAL REVIEW REQUIRED"
    }

