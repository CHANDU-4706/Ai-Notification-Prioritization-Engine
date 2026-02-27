import os
import json
from groq import Groq
from dotenv import load_dotenv
from app.models import NotificationEvent, DecisionResult

load_dotenv()

class ClassifierService:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"

    async def classify(self, event: NotificationEvent) -> DecisionResult:
        prompt = f"""
        You are an AI-Native Notification Prioritization Engine.
        Classify the following notification event into one of: NOW, LATER, NEVER.
        
        Rules:
        - NOW: Urgent, time-sensitive, critical alerts (security, OTP, immediate action needed).
        - LATER: Informational, non-urgent updates, reminders that can be seen later.
        - NEVER: Spam, promotional noise, or irrelevant system chatter.

        Event Details:
        - Type: {event.event_type}
        - Message: {event.message}
        - Source: {event.source}
        - Priority Hint: {event.priority_hint}
        
        Respond ONLY in JSON format with the following fields:
        {{
          "decision": "NOW | LATER | NEVER",
          "reason": "Clear explanation of why this decision was made",
          "score": 0.0 to 1.0 (urgency score),
          "confidence": 0.0 to 1.0
        }}
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                response_format={"type": "json_object"},
                timeout=2.0 # Strict latency requirement
            )
            
            response_data = json.loads(chat_completion.choices[0].message.content)
            
            return DecisionResult(
                event_id=event.id,
                user_id=event.user_id,
                decision=response_data.get("decision", "LATER"),
                reason=response_data.get("reason", "AI Classification"),
                engine_used="GROQ_LLAMA",
                score=response_data.get("score", 0.5),
                confidence=response_data.get("confidence", 0.0)
            )
        except Exception as e:
            # Fallback to a safe rule-based decision if AI is unavailable or slow
            return DecisionResult(
                event_id=event.id,
                user_id=event.user_id,
                decision="NOW" if event.priority_hint == "critical" else "LATER",
                reason=f"Fallback due to AI error: {str(e)}",
                engine_used="FALLBACK",
                confidence=1.0
            )
