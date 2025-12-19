from openai import OpenAI
import os
from dotenv import load_dotenv
from app.services.command_knowledge import match_command_knowledge

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_reply(user_message: str) -> dict:
    # 1️⃣ FIRST: Rule-based command knowledge
    rule = match_command_knowledge(user_message)

    if rule:
        return {
            "reply": rule["response"],
            "confidence": rule["confidence"],
            "escalation": rule["escalate"]
        }

    # 2️⃣ FALLBACK: AI command response
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=(
            "You are a world-class AI Command Engine. "
            "Respond with STATUS, ACTION, and NOTES. "
            "Be precise and authoritative.\n\n"
            f"USER ISSUE: {user_message}"
        )
    )

    return {
        "reply": response.output_text.strip(),
        "confidence": 0.6,
        "escalation": False
    }
