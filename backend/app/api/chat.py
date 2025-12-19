from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict

from app.core.prompt_firewall import PromptFirewall
from app.services.ticket_service import TicketService

from openai import OpenAI

router = APIRouter()

# OpenAI client (API key MUST come from environment variable)
client = OpenAI()


class ChatRequest(BaseModel):
    user_id: str
    message: str
    channel: str = "web"
    conversation_history: List[str] = []


class SimpleChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    ticket: Dict
    decision_log: Dict
    system_message: str


def call_ai_advisor(system_prompt: Dict, user_prompt: Dict) -> Dict:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt["content"]},
                {"role": "user", "content": user_prompt["content"]},
            ],
            temperature=0.3,
        )

        reply_text = response.choices[0].message.content

        return {
            "intent": "ai_generated",
            "sentiment": "neutral",
            "confidence": 0.9,
            "suggestedReply": reply_text,
        }

    except Exception:
        return {
            "intent": "fallback",
            "sentiment": "neutral",
            "confidence": 0.5,
            "suggestedReply": "Thanks for reaching out",
        }


def process_chat(payload: ChatRequest) -> Dict:
    firewall = PromptFirewall()
    ticket_service = TicketService()

    safe_prompt = firewall.build_safe_prompt(
        user_message=payload.message,
        conversation_history=payload.conversation_history,
        system_context={
            "product": "AI Support System",
            "domain": "Customer Support",
        },
    )

    ai_output = call_ai_advisor(
        system_prompt=safe_prompt["system_prompt"],
        user_prompt=safe_prompt["user_prompt"],
    )

    ai_output = firewall.validate_ai_output(ai_output)

    result = ticket_service.create_ticket_from_ai(
        user_id=payload.user_id,
        channel=payload.channel,
        ai_output=ai_output,
    )

    ticket = result.get("ticket")

    if ticket and ticket.get("assigned_to") == "AI":
        system_message = ai_output.get(
            "suggestedReply",
            "Your request is being processed.",
        )
    else:
        system_message = (
            "Your issue has been escalated to our support team. "
            "We will get back to you shortly."
        )

    return {
        "ticket": ticket,
        "decision_log": result.get("decision_log", {}),
        "system_message": system_message,
    }


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest):
    try:
        return process_chat(payload)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chat processing failed: {str(e)}",
        )


@router.post("/chat/simple")
def simple_chat(payload: SimpleChatRequest):
    try:
        enriched_payload = ChatRequest(
            user_id="demo_user",
            message=payload.message,
            channel="web",
            conversation_history=[],
        )

        result = process_chat(enriched_payload)

        return {"reply": result.get("system_message", "Thanks for reaching out")}

    except Exception:
        return {"reply": "Thanks for reaching out"}
