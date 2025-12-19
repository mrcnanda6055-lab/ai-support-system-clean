# backend/core/prompt_firewall.py

from typing import Dict, List


class PromptFirewall:
    """
    STEP 3.3
    Prompt Firewall

    - Prevents same-answer bug
    - Prevents unsafe replies
    - Controls what AI can see
    """

    BLOCKED_PHRASES = [
        "as an ai language model",
        "i am not sure",
        "i cannot help with that"
    ]

    def build_safe_prompt(
        self,
        user_message: str,
        conversation_history: List[str],
        system_context: Dict
    ) -> Dict:
        """
        Builds a CONTROLLED prompt for AI
        """

        # Trim history (last 3 only)
        recent_history = conversation_history[-3:]

        prompt = {
            "role": "system",
            "content": (
                "You are an AI advisor for a customer support system.\n"
                "You MUST NOT reply directly to the user.\n"
                "You MUST ONLY return structured analysis.\n"
                "Do NOT repeat previous answers.\n"
                "Do NOT make final decisions.\n"
            )
        }

        user_payload = {
            "role": "user",
            "content": f"""
Context:
- Product: {system_context.get("product", "Unknown")}
- Domain: {system_context.get("domain", "general support")}

Recent Conversation:
{recent_history}

Current User Message:
{user_message}

Your task:
Return ONLY a JSON object with:
intent, sentiment, confidence, suggestedReply
"""
        }

        return {
            "system_prompt": prompt,
            "user_prompt": user_payload
        }

    def validate_ai_output(self, ai_output: Dict) -> Dict:
        """
        Final safety check on AI output
        """

        reply = ai_output.get("suggestedReply", "").lower()

        for phrase in self.BLOCKED_PHRASES:
            if phrase in reply:
                ai_output["suggestedReply"] = (
                    "Your issue is being reviewed by our support team."
                )
                ai_output["confidence"] = 0.0

        return ai_output
